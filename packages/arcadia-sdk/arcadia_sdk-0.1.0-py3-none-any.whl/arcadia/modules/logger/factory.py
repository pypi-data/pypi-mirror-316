import os
import sys

from dotenv import load_dotenv

load_dotenv()
import json

from logtail import LogtailHandler
from loguru import logger


class Factory:
    @staticmethod
    def get_logger(log_level="INFO"):
        load_dotenv()  # Ensure this is called before accessing env variables

        environment = os.getenv("ENVIRONMENT", "staging")
        log_level_env = os.getenv("LOGGING_LEVEL", log_level)

        def serialize(record):
            def default_serializer(obj):
                if hasattr(obj, "__dict__"):
                    return str(obj)
                raise TypeError(
                    f"Object of type {type(obj)} is not JSON serializable"
                )

            log_record = {
                "timestamp": record["time"].timestamp(),
                "level": record["level"].name,
                "service": record["name"],
                "message": record["message"],
                "context": {
                    k: v
                    for k, v in record["extra"].items()
                    if k not in ["job_id", "serialized"]
                },
                "file": record["file"].name,
                "function": record["function"],
                "line": record["line"],
                "module": record["module"],
                "elapsed": str(record["elapsed"]),
            }
            return json.dumps(log_record, default=default_serializer)

        def json_formatter(record):
            record["extra"]["serialized"] = serialize(record)
            return "{extra[serialized]}\n"

        # Remove default logger
        logger.remove()

        if environment in ["production", "staging"]:
            logtail_token = os.getenv("LOGTAIL_TOKEN")
            logtail_handler = LogtailHandler(source_token=logtail_token)

            logger.add(
                logtail_handler,
                format=json_formatter,
                level=log_level_env,
                serialize=True,
            )

            # Add minimal console logging for production and staging
            logger.add(
                sys.stdout,
                format=json_formatter,
                level="DEBUG" if log_level_env == "DEBUG" else "INFO",
                backtrace=(environment == "staging"),
                diagnose=(environment == "staging"),
            )
        else:
            logger.add(
                f"logs/arcadia.log",
                format=json_formatter,
                level=log_level_env,
                retention="10 days",
                rotation="500 MB",
                mode="a",
            )

        return logger

    @staticmethod
    def bind_logger_to_job(logger, job_id):
        return logger.bind(job_id=job_id)

    @staticmethod
    def set_log_level(logger, level):
        for handler in logger._core.handlers.values():
            handler._level = logger.level(level).no
