# llm_processor.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re
import json

class MilitaryReportFormatter:
    def __init__(self, model_name="mosaicml/mpt-7b-instruct"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,  # Use half precision for efficiency
            device_map="auto"  # Automatically manage model placement
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
    def format_eoincrep(self, packet):
        """
        Format a JSON military packet into EOINCREP standard report. Used for threat reporting, 
        incident details, intelligence, and follow-up actions.
        """
        action = packet.get("action", "UNKNOWN")
        units = ", ".join(packet.get("target_units", [])) or "N/A"
        coords = packet.get("coordinates", {})
        x = coords.get("x", "N/A")
        y = coords.get("y", "N/A")
        timeframe = packet.get("timeframe", "N/A")
        priority = packet.get("priority", "N/A")

        report = (
            f"EOINCREP REPORT\n"
            f"Action: {action}\n"
            f"Units Involved: {units}\n"
            f"Coordinates: X={x}, Y={y}\n"
            f"Timeframe: {timeframe}\n"
            f"Priority: {priority}\n"
        )
        return report

    def format_casevac(self, packet):
        """
        Format a JSON military packet into CASEVAC standard report.
        Used for casualty evacuation details, including location, urgency, and resources needed.
        """
        action = packet.get("action", "UNKNOWN")
        units = ", ".join(packet.get("target_units", [])) or "N/A"
        coords = packet.get("coordinates", {})
        x = coords.get("x", "N/A")
        y = coords.get("y", "N/A")
        timeframe = packet.get("timeframe", "N/A")
        priority = packet.get("priority", "N/A")

        report = (
            f"CASEVAC REPORT\n"
            f"Evacuation Action: {action}\n"
            f"Units to Evacuate: {units}\n"
            f"Evacuation Coordinates: X={x}, Y={y}\n"
            f"Required Timeframe: {timeframe}\n"
            f"Evacuation Priority: {priority}\n"
        )
        return report

    def format_report(self, packet, report_type="EOINCREP"):
        """
        Format packet into the requested report type.
        """
        if report_type.upper() == "EOINCREP":
            return self.format_eoincrep(packet)
        elif report_type.upper() == "CASEVAC":
            return self.format_casevac(packet)
        else:
            return "Unknown report type."
            

# Example usage:
# formatter = MilitaryReportFormatter()
# packet = {
#     "action": "Advance",
#     "target_units": ["Alpha", "Bravo"],
#     "coordinates": {"x": 123, "y": 456},
#     "timeframe": "0600Z",
#     "priority": "HIGH"
# }
# print(formatter.format_report(packet, "EOINCREP"))
# print(formatter.format_report(packet, "CASEVAC"))