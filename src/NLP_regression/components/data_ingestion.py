from NLP_regression import logger
from NLP_regression.entity.config_entity import DataIngestionConfig
from pydantic import BaseModel
import json
from typing import Optional, Self
from datasets import load_dataset
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self)->None:
        logger.info(f"Downloading data from {self.config.source_URL} to {self.config.root_dir}")
        train, val, test = DataItem.pull_from_hub(self.config.source_URL)

        # Save the data to local file
        data_splits = {
            'train': train,
            'validation': val,
            'test': test
        }
        for split_name, data in data_splits.items():
            split_file = Path(self.config.root_dir) / f"{split_name}.json"
            with split_file.open('w', encoding='utf-8') as f:
                json.dump([item.model_dump() for item in data], f,ensure_ascii=False, indent=2)
            logger.info(f"Saved {split_name} data to {split_file}")




class DataItem(BaseModel):
    title: str
    category: str
    price: float
    full: Optional[str] = None
    weight: Optional[float] = None
    summary: Optional[str] = None
    prompt: Optional[str] = None
    id: Optional[int] = None

    @classmethod
    def pull_from_hub(cls,dataset_name: str) -> tuple[list[Self], list[Self], list[Self]]:
        data=load_dataset(dataset_name)
        train_data = [cls.model_validate(item) for item in data['train']]
        test_data = [cls.model_validate(item) for item in data['test']]
        validation_data = [cls.model_validate(item) for item in data['validation']]
        return train_data, validation_data, test_data

    
