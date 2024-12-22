import subprocess
import os
from arcadia.modules.logger.factory import Factory

from supabase import create_client, Client
from arcadia.modules.login import load_credentials

class ArcadiaClient:
    """
    This module provides the client functionality for Arcadia.
    """
    def __init__(self):
        """
        Initialize the ArcadiaClient class with API key validation.
        """
        credentials = load_credentials()
        self.username = credentials['username']
        self.api_key = credentials['api_key']

        self.logger = Factory.get_logger()
        
        # Initialize Supabase client (add these as environment variables in production)
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(supabase_url, supabase_key)

    def predict(self, model_name=None, description=None, hardware="cpu", **model_kwargs):
        """
        Decorator to run model predictions with configurable settings.

        Args:
            model_name (str, optional): Name of the model to use for prediction
            description (str, optional): Description of what this model does
            hardware (str, optional): Hardware requirements (e.g. "cpu", "gpu"). Defaults to "cpu"
            **model_kwargs: Additional model configuration parameters

        Returns:
            function: The wrapped prediction function
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.logger.info(f"Preparing to run prediction with model '{model_name or 'default'}'...")
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

    def deploy(self):
        """
        Deploy the project using arcadia deploy command.
        """
        try:
            self.logger.info("Initializing Cog project...")
            subprocess.run(["cog", "init"], check=True)

            # Create new model entry in Supabase
            try:
                model_data = {
                    'name': 'test',  # TODO: Make configurable
                    'description': 'Test model deployment', 
                    'gpu': True,
                }
                
                response = self.supabase.table('models').insert(model_data).execute()
                self.logger.info(f"Created model entry in database: {response.data}")
            except Exception as e:
                self.logger.error(f"Failed to create model entry: {e}")
                raise
            self.logger.info("Pushing model to Arcadia...")
            subprocess.run(
                ["cog", "push", "r8.im/timothy102/test"], check=True
            )
            self.logger.info("Deployment successful.")
        except subprocess.CalledProcessError as e:
            self.logger.info(f"An error occurred during deployment: {e}")


if __name__ == "__main__":
    c = ArcadiaClient(api_key="timcibimci")
    
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        c.deploy()
