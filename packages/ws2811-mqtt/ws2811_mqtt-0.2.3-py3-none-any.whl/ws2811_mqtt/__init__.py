import os

import time
from dotenv import load_dotenv

load_dotenv(os.getenv("WS2811_ENV_PATH", ".env"))

from .args import init_args
init_args()

from .logger import init_logger
init_logger()

from .mqtt import init_mqtt
init_mqtt()

def main():
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()