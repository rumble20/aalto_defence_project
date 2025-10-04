from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json
from pathlib import Path
import re
from typing import Dict, Union, Optional
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from json_to_text_DECODING import MilitaryPacket, Priority, Coordinates, ReportType, MilitaryReportFormatter
from datetime import datetime

class MilitaryTextEncoder:
    def __init__(self, model_name: str = "microsoft/phi-1_5", max_length: int = 512):
        """Initializne with a small, accessible model for text processing."""
        self.model_name = model_name
        self.max_length = max_length
        
        try:
            # Initialize model and pipeline
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                dtype=torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=max_length
            )
        except Exception as e:
            raise RuntimeError(f"Model initialization failed: {str(e)}")

        self.output_dir = Path("./processed_data")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def clean_text(self, text: str) -> str:
        """Clean and standardize input text."""
        # Remove multiple spaces and normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,():-]', '', text)
        return text

    def process_text(self, text: str) -> Dict[str, Union[str, list, dict]]:
        """Process text input into structured military data."""
        cleaned_text = self.clean_text(text)
        prompt = f"""Convert this military message into precise JSON format with these exact fields:
        {{
            "action": "string",
            "target_units": ["string array"],
            "coordinates": {{"x": float, "y": float}},
            "timeframe": "string",
            "priority": "HIGH/MEDIUM/LOW"
        }}

        Text: {cleaned_text}

        JSON:"""

        try:
            response = self.pipe(prompt, max_new_tokens=256)[0]['generated_text']
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in response")
            
            data = json.loads(json_match.group())
            
            # Validate with Pydantic model
            validated_data = MilitaryPacket(**data)
            return validated_data.dict()

        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}

    def process_and_format(self, text: str, report_type: ReportType = ReportType.EOINCREP) -> tuple[str, str]:
        """Process text and format it into a military report."""
        data = self.process_text(text)
        if "error" not in data:
            formatter = MilitaryReportFormatter()
            return formatter.format_and_save_report(data, report_type)
        return f"Error: {data['error']}", ""

    def save_output(self, data: dict, output_path: Optional[Path] = None) -> str:
        """Save processed data to JSON file."""
        if output_path is None:
            output_path = Path.cwd() / f"military_data_{hash(str(data))}.json"
        
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            return str(output_path)
        except Exception as e:
            return f"Error saving output: {str(e)}"

    def process_and_save_all(self, text: str, report_type: ReportType = ReportType.EOINCREP) -> dict:
        """Process text and save both JSON and formatted report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {"status": "success"}

        # Process text to JSON
        data = self.process_text(text)
        if "error" in data:
            return {"status": "error", "error": data["error"]}

        # Save JSON
        json_path = self.output_dir / f"structured_data_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        results["json_path"] = str(json_path)

        # Generate and save report
        report_content, report_path = self.process_and_format(text, report_type)
        results["report_content"] = report_content
        results["report_path"] = report_path

        return results

if __name__ == "__main__":
    # Create encoder instance
    encoder = MilitaryTextEncoder()
    
    # Example messy text input
    messy_text = """
    Alpha team needs 2 move quickly!! coordinates are (123.45, 678.90)
    time: 0600Z tmrw... Bravo & Charlie providing backup
    THIS IS URGENT/HIGH PRIORITY!!!
    """
    
    try:
        # Process and save both JSON and reports
        results = encoder.process_and_save_all(messy_text, ReportType.EOINCREP)
        
        if results['status'] == 'success':
            print("\nProcessing completed successfully!")
            print(f"JSON file saved to: {results['json_path']}")
            print(f"Report file saved to: {results['report_path']}")
            print("\nReport Content:")
            print(results['report_content'])
        else:
            print(f"\nError occurred: {results['error']}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")