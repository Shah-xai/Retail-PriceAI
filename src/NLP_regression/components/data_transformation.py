import os
import re

from pydantic import BaseModel
from pathlib import Path
from NLP_regression.entity.config_entity import DataTransformationConfig
from NLP_regression import logger
import json
from groq import Groq
from NLP_regression.constants import SYSTEM_PROMPT
from dotenv import load_dotenv
import time

MODEL_NAME:str='openai/gpt-oss-20b'

class FinalRecord(BaseModel):
    summary: str
    weight: float|None=None
    price: float

class DataTransformation:
     def __init__(self,model_name:str=MODEL_NAME,
                    ):
        load_dotenv()
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name
     @staticmethod
     def _load_split_data(file_path: Path) -> list[dict]:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
     @staticmethod
     def _save_split_data(data: list[dict], output_path: Path) -> None:
        with output_path.open("w", encoding="utf-8") as f:
            for record in data:
                f.write(json.dumps(record) + "\n")

     @staticmethod
     def _make_batch_data(data: list[dict], output_path: Path, model_name: str  ) -> None:
        with output_path.open("w", encoding="utf-8") as f:
            for idx,item in enumerate(data):
                full_text = item.get("full")
                if not full_text:
                    logger.warning(f"Record at index {idx} is missing 'full' key. Skipping.")
                    continue
                request = {
                    "custom_id":str(idx),
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": full_text}
                        ],"temperature": 0.01,
                          "max_completion_tokens": 400, 
                          "seed":42
                    }
                }
                f.write(json.dumps(request, ensure_ascii=False) + "\n")
     def batch_submition(self, batch_file_path: Path) -> dict:
         batch_file =self.client.files.create(
             file=open(batch_file_path, "rb"),
             purpose="batch"
         )
         batch_response = self.client.batches.create(
             input_file_id=batch_file.id,
             endpoint="/v1/chat/completions",
             completion_window="24h"
         )
         logger.info(f"Created batch with ID: {batch_response.id}")
         return batch_response 
     def check_batch_status(self, batch_id: str,poll_interval:int=30) -> dict:
            while True:
                batch_status = self.client.batches.retrieve(batch_id)
                logger.info(f"Batch {batch_id} status: {batch_status.status}")
                if batch_status.status in ["completed", "failed", "canceled"]:
                    return batch_status
                time.sleep(poll_interval)
     def download_batch_results(self, file_id: str, output_path: Path) -> None:
         response=self.client.files.content(file_id)
         response.write_to_file(output_path)
     
     @staticmethod
     def process_batch_results(original_data: list[dict], batch_results_path: Path) -> list[dict]:
         with batch_results_path.open("r", encoding="utf-8") as f:
             batch_results = [json.loads(line) for line in f]
         processed_data = []
         for idx, (original, result) in enumerate(zip(original_data, batch_results)):
             
             try:
                 content = result["response"]["body"]["choices"][0]["message"]["content"].strip()
                 processed_record=FinalRecord(summary=content, 
                                              price=original.get("price"), 
                                              weight=original.get("weight"))
                 processed_data.append(processed_record.model_dump())
             except json.JSONDecodeError as e:
                 logger.error(f"JSON decoding error for index {idx}: {e}. Skipping.")
         return processed_data
     def initiate_data_transformation(self, config: DataTransformationConfig):
         raw_data_path=config.raw_data_dir
         output_data_path=config.root_dir
         batch_dir= output_data_path / "batch_data"
         batch_dir.mkdir(parents=True, exist_ok=True)
         splits = ["train", "test", "validation"]
         for split in splits:
             file_split_path = raw_data_path / f"{split}.json"
             if not file_split_path.exists():
                 logger.error(f"File {file_split_path} does not exist. Skipping {split} split.")
                 continue
             logger.info(f"Processing {split} split.")
             data = self._load_split_data(file_split_path)
             batch_input_path = batch_dir / f"{split}_batch.jsonl"
             batch_output_path = batch_dir / f"{split}_batch_results.jsonl"
             final_output_path = output_data_path / f"{split}_processed.jsonl"
             self._make_batch_data(data, batch_input_path, self.model_name)
             logger.info(f"Submitting batch for {split} split.")
             batch_response = self.batch_submition(batch_input_path)
             completed_batch = self.check_batch_status(batch_response.id)
             if completed_batch.status != "completed":
                 logger.error(f"Batch {batch_response.id} did not complete successfully. Status: {completed_batch.status}. Skipping {split} split.")
                 continue
             self.download_batch_results(completed_batch.output_file_id, batch_output_path)
             logger.info(f"Batch results for {split} split downloaded to {batch_output_path}.")
             transformed_data = self.process_batch_results(data, batch_output_path)
             self._save_split_data(transformed_data, final_output_path)
             logger.info(f"Data transformation for {split} split completed. Processed data saved to {final_output_path}.")
        

        
    

        
   
