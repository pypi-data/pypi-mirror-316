import importlib.metadata
from datetime import datetime

__version__ = importlib.metadata.version(__package__ or __name__)
__release_time__= datetime.strptime('2024-12-19T23:50:29','%Y-%m-%dT%H:%M:%S')
is_released_version=True
