from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum
import os
from datetime import datetime
from pathlib import Path

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Coordinates(BaseModel):
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")

class MilitaryPacket(BaseModel):
    action: str = Field(..., description="Military action to be taken")
    target_units: List[str] = Field(default_factory=list, description="Units involved in the action")
    coordinates: Coordinates
    timeframe: str = Field(..., description="Timeframe for the action")
    priority: Priority = Field(..., description="Priority level of the action")

class ReportType(str, Enum):
    EOINCREP = "EOINCREP"
    CASEVAC = "CASEVAC"

class MilitaryReportFormatter:
    def __init__(self, model_name="microsoft/phi-1_5", output_dir="./reports"):
        """
        Initialize the formatter with a specified model.
        Recommended freely accessible models:
        - "microsoft/phi-1_5" (default, 1.3B parameters)
        - "TinyLlama/TinyLlama-1.1B-Chat-v1.0" (1.1B parameters)
        - "facebook/opt-350m" (350M parameters, very light)
        """
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                torch_dtype=torch.float32,  # Use full precision for better compatibility
                device_map="auto" if torch.cuda.is_available() else None,
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_name}. Error: {str(e)}")

    def format_eoincrep(self, packet: MilitaryPacket) -> str:
        """
        Format a validated MilitaryPacket into EOINCREP standard report.
        Used for enemy contact reports, threat sightings, and other operational updates.
        """
        return (
            f"EOINCREP REPORT\n"
            f"Action: {packet.action}\n"
            f"Units Involved: {', '.join(packet.target_units) if packet.target_units else 'N/A'}\n"
            f"Coordinates: X={packet.coordinates.x}, Y={packet.coordinates.y}\n"
            f"Timeframe: {packet.timeframe}\n"
            f"Priority: {packet.priority}\n"
        )

    def format_casevac(self, packet: MilitaryPacket) -> str:
        """
        Format a validated MilitaryPacket into CASEVAC standard report.
        Used for casualty evacuation requests.
        """
        return (
            f"CASEVAC REPORT\n"
            f"Evacuation Action: {packet.action}\n"
            f"Units to Evacuate: {', '.join(packet.target_units) if packet.target_units else 'N/A'}\n"
            f"Evacuation Coordinates: X={packet.coordinates.x}, Y={packet.coordinates.y}\n"
            f"Required Timeframe: {packet.timeframe}\n"
            f"Evacuation Priority: {packet.priority}\n"
        )

    def format_report(self, packet_dict: dict, report_type: ReportType = ReportType.EOINCREP) -> str:
        """
        Format packet into EOINCREP report type with validation.
        """
        try:
            packet = MilitaryPacket(**packet_dict)
            if report_type == ReportType.EOINCREP:
                return self.format_eoincrep(packet)
            elif report_type == ReportType.CASEVAC:
                return self.format_casevac(packet)
        except Exception as e:
            return f"Error processing report: {str(e)}"

    def save_report_to_file(self, report: str, report_type: ReportType) -> str:
        """
        Save the formatted report to a text file with timestamp.
        Returns the path to the saved file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type}_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(filepath)

    def format_and_save_report(self, packet_dict: dict, report_type: ReportType = ReportType.EOINCREP) -> tuple[str, str]:
        """
        Format the report, save it to a file, and return both the report content and file path.
        """
        report_content = self.format_report(packet_dict, report_type)
        if not report_content.startswith("Error"):
            filepath = self.save_report_to_file(report_content, report_type)
            return report_content, filepath
        return report_content, ""


# Example usage:
# formatter = MilitaryReportFormatter()
# packet_dict = {
#     "action": "Advance",
#     "target_units": ["Alpha", "Bravo"],
#     "coordinates": {"x": 123.0, "y": 456.0},
#     "timeframe": "0600Z",
#     "priority": "HIGH"
# }
# print(formatter.format_report(packet_dict, ReportType.EOINCREP))
# print(formatter.format_report(packet_dict, ReportType.CASEVAC))