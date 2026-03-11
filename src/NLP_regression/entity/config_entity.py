from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    raw_data_dir: Path
    
