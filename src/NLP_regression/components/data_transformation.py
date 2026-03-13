import re

from pydantic import BaseModel
from pathlib import Path
from NLP_regression.entity.config_entity import DataTransformationConfig
from NLP_regression import logger
import json
from openai import OpenAI
from NLP_regression.constants import SYSTEM_PROMPT
import time

class FinalRecord(BaseModel):
    summary: str
    weight: float|None=None
    price: float

class DataTransformation:
    def __init__(self,
                 model_name: str = "gpt-oss:20b",
                 base_url: str = "http://localhost:11434/v1",
                 api_key: str = "ollama_api_key"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model_name = model_name
    def curate_data(self,text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            temperature=0.01,   
        )
        try:
            content = response.choices[0].message.content
            content = content.strip().removeprefix("```json").removesuffix("```").strip()
        
            return content
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise ValueError("Failed to parse structured data from the model response.")
    
    @staticmethod
    def _load_split_data(file_split_path: Path) -> dict:
        with  file_split_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    @staticmethod
    def _save_split_data(data: list[dict], output_path: Path):
        with output_path.open("w", encoding="utf-8") as f:
            for row in data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def initiate_data_transformation(self,config: DataTransformationConfig)-> None:
        raw_data_path = config.raw_data_dir
        output_dir=config.root_dir
        if not raw_data_path.exists():
            logger.error(f"Raw data directory does not exist: {raw_data_path}")
            raise FileNotFoundError(f"Raw data directory not found: {raw_data_path}")
        
        splits=["train", "test", "validation"]
        for split in splits:
            file_split_path = raw_data_path / f"{split}.json"
            if not file_split_path.exists():
                logger.error(f"Data split file does not exist: {file_split_path}")
                raise FileNotFoundError(f"Data split file not found: {file_split_path}")
            
            data = self._load_split_data(file_split_path)
            curated_data = []
            start_time = time.time()
            for item in data:
                try:
                    structured_item = self.curate_data(item["full"])
                    final_record=FinalRecord(
                        summary=structured_item,
                        price=item.get("price", 0.0),
                        weight=item.get("weight", None)
                    )
                    curated_data.append(final_record.model_dump())
                except Exception as e:
                    logger.error(f"Error curating item: {e}")

            end_time = time.time()
            logger.info(f"Time taken for {split} split: {end_time - start_time} seconds")
            
            output_path = output_dir / f"{split}_transformed.jsonl"
            self._save_split_data(curated_data, output_path)
            logger.info(f"Transformed data saved to: {output_path}")