from datetime import timedelta
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

GIGAPIXEL_EXECUTABLE_PATH = Path(env.str("GIGAPIXEL_EXECUTABLE_PATH"))
OUTPUT_PATH = Path(env.str("OUTPUT_PATH"))
OUTPUT_SUFFIX = env.str("OUTPUT_SUFFIX")
IMAGE_DELETION_TIMEOUT = timedelta(hours=1)
