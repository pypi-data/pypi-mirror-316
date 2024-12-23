import subprocess

import replicate
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from supabase import Client, create_client

from arcadia.modules.logger.factory import LoggerFactory
from arcadia.modules.login import load_credentials
from arcadia.utils.settings import Settings


class ArcadiaClient:
    """
    This module provides the client functionality for Arcadia.
    """

    def __init__(self):
        """
        Initialize the ArcadiaClient class with API key validation.
        """
        credentials = load_credentials()
        self.username = credentials["username"]
        self.api_key = credentials["api_key"]

        self.logger = LoggerFactory.get_logger()
        self.settings = Settings()
        self.console = Console()
        self.supabase: Client = create_client(
            self.settings.supabase_url, self.settings.supabase_key
        )

    def predict(
        self, model_name=None, description=None, hardware="cpu", **model_kwargs
    ):
        """Decorator for model predictions"""

        def decorator(func):
            def wrapper(*args, **kwargs):
                self.logger.info(
                    f"Preparing to run prediction with model '{model_name or 'default'}'..."
                )
                self.logger.info(f"Hardware: {hardware}")
                if description:
                    self.logger.info(f"Model description: {description}")
                if model_kwargs:
                    self.logger.info(f"Additional model config: {model_kwargs}")

                result = func(*args, **kwargs)

                self.logger.info("Prediction complete.")
                return result

            return wrapper

        return decorator

    def deploy(self, model_name: str, description: str = None, gpu: bool = True):
        """
        Deploy a model to Arcadia.

        Args:
            model_name: Name of the model to deploy
            description: Optional description of the model
            gpu: Whether the model requires GPU (default: True)
        """
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                # Initialize Cog
                task = progress.add_task(
                    description="[cyan]Initializing Cog project...", total=None
                )
                subprocess.run(["cog", "init"], check=True)
                progress.remove_task(task)

                # Create model entry
                task = progress.add_task(
                    description="[cyan]Creating model entry...", total=None
                )
                try:
                    model_data = {
                        "name": model_name,
                        "description": description or f"Deployment of {model_name}",
                        "gpu": gpu,
                        "username": self.username,
                    }

                    response = (
                        self.supabase.table("models").insert(model_data).execute()
                    )
                    self.console.print(
                        "[green]✓[/green] Created model entry in database"
                    )
                except Exception as e:
                    self.console.print(
                        f"[red]✗ Failed to create model entry: {e}[/red]"
                    )
                    raise
                progress.remove_task(task)

                # Push to Arcadia
                task = progress.add_task(
                    description="[cyan]Pushing model to Arcadia...", total=None
                )
                model_path = f"r8.im/{self.username}/{model_name}"
                subprocess.run(["cog", "push", model_path], check=True)
                progress.remove_task(task)

            self.console.print("\n[green]✓ Deployment successful![/green]")
            self.console.print(
                Panel.fit(
                    f"[bold green]🚀 Model {model_name} Deployed Successfully![/bold green]\n\n"
                    "Your model is now live on Arcadia. Here are some things you can try:\n\n"
                    f"[cyan]• View your model:[/cyan] arcadia status {model_name}\n"
                    f"[cyan]• Monitor usage:[/cyan] arcadia logs {model_name}\n"
                    f"[cyan]• Update settings:[/cyan] arcadia config {model_name}\n\n"
                    "For more information, visit [link]https://docs.arcadia.ai[/link]",
                    title="Deployment Complete",
                    border_style="green",
                )
            )

        except subprocess.CalledProcessError as e:
            self.console.print(f"\n[red]✗ Deployment failed![/red]")
            self.console.print(f"[yellow]Error: {e}[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]✗ An error occurred during deployment[/red]")
            self.console.print(f"[yellow]Error: {e}[/yellow]")

    def run(self, model_name: str, prompt: str):
        """
        Run inference on a deployed model using Replicate and track usage in Supabase:

        1. It gets the model id
        2. It gets the user id
        3. it runs inference
        4. It increases count in the model_usage table in Supabase for that user and that model.

        Args:
            model_name: Name of the deployed model
            prompt: Input prompt for the model
        """
        try:
            # First get model_id from models table
            model_response = (
                self.supabase.table("models")
                .select("id")
                .eq("name", model_name)
                .execute()
            )

            if not model_response.data:
                raise ValueError(f"Model {model_name} not found")

            model_id = model_response.data[0]["id"]

            # Get user_id from users table using username
            user_response = (
                self.supabase.table("users")
                .select("id")
                .eq("username", self.username)
                .execute()
            )

            if not user_response.data:
                raise ValueError(f"User {self.username} not found")

            user_id = user_response.data[0]["id"]

            # Run the actual model inference
            model_string = f"{self.username}/{model_name}"

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task(
                    description=f"[cyan]Running {model_name}...", total=None
                )
                output = replicate.run(model_string, input={"prompt": prompt})
                progress.remove_task(task)

            # Record the usage in model_usage table
            try:
                # Check if entry exists
                usage_response = (
                    self.supabase.table("model_usage")
                    .select("*")
                    .eq("model_id", model_id)
                    .eq("user_id", user_id)
                    .execute()
                )

                if usage_response.data:
                    # Update existing entry
                    self.supabase.table("model_usage").update(
                        {"count": usage_response.data[0]["count"] + 1}
                    ).eq("model_id", model_id).eq("user_id", user_id).execute()
                else:
                    # Create new entry
                    self.supabase.table("model_usage").insert(
                        {"model_id": model_id, "user_id": user_id, "count": 1}
                    ).execute()

            except Exception as e:
                self.console.print(
                    f"\n[yellow]Warning: Failed to record usage stats: {e}[/yellow]"
                )
                # Continue execution even if usage tracking fails

            self.console.print(f"\n[green]✓ Model run completed successfully![/green]")
            return output

        except Exception as e:
            self.console.print(f"\n[red]✗ Error running model: {e}[/red]")
            raise
