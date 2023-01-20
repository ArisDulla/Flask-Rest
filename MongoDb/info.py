import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from pathlib import Path

dotenv_path = Path('./keys/mongoInfo.env')
load_dotenv(dotenv_path=dotenv_path)


@dataclass(frozen=True)
class InfoData:
    mongoInfo: str = os.getenv('mongoInfo')

