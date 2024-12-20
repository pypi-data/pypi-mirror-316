import os
import time
import socket
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class LoggingSettings(BaseSettings):
    # AppAuth Settings
    application_name: str = ""
    application_version: str = ""
    # Logging Settings
    graylog_host: str = ""
    graylog_port: int = 0
    graylog_protocol: str = ""
    log_file_path: str = ""
    facility: str = ""
    hostname: str = socket.gethostname()
    ip_address: str = socket.gethostbyname(hostname)
    env_file: str = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_file)
    model_config = SettingsConfigDict(env_file=env_file)

def get_logging_settings() -> LoggingSettings:
    return LoggingSettings()

def init_logging(
        facility: str,
        application_name: str,
        application_version: str,
        graylog_host: str,
        graylog_port: int,
        graylog_protocol: str = "udp",
        log_file_path: str = "",
    ):

    env_file = os.path.join(os.path.dirname(__file__), ".env")
    with open(env_file, "w") as f:
        f.write(f'application_name="{application_name}"\n')
        f.write(f'application_version="{application_version}"\n')
        f.write(f'graylog_host="{graylog_host}"\n')
        f.write(f'graylog_port={graylog_port}\n')
        f.write(f'graylog_protocol="{graylog_protocol}"\n')
        f.write(f'log_file_path="{log_file_path}"\n')
        f.write(f'facility="{facility}"\n')

        time.sleep(5)
        # load the settings
        print("Logging settings: ", get_logging_settings().model_dump())


if __name__ == "__main__":
    init_logging(
        facility="test_facility",
        application_name="test_application",
        application_version="1.0.0",
        graylog_host="localhost",
        graylog_port=12201,
    )
