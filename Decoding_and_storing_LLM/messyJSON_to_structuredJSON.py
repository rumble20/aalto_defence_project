"""
Robust local-only Military Text -> Structured JSON encoder
- Attempts to parse/repair messy JSON locally (no OpenAI required)
- Falls back to a local instruction-tuned model for extraction (google/flan-t5-small by default)
- Validates output with Pydantic

Dependencies:
  pip install transformers torch pydantic json-repair
  (json-repair is optional but recommended)

Usage: run this script or import MilitaryTextEncoder class in your project.
"""

from pathlib import Path
import json
import re
from datetime import datetime
from typing import Dict, Union, Optional, Any

# Pydantic for validation
from pydantic import BaseModel, Field, ValidationError
from enum import Enum

# Transformer pipeline for local LLM fallback (text2text)
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Try to import json_repair if available
try:
    import json_repair
    _HAS_JSON_REPAIR = True
except Exception:
    _HAS_JSON_REPAIR = False


# --- Schema: either import from user's module or define local fallback ---
try:
    # If you already have these models in json_to_text_DECODING we will prefer them
    from json_to_text_DECODING import (
        MilitaryPacket as ImportedMilitaryPacket,
        Priority as ImportedPriority,
        Coordinates as ImportedCoordinates,
        ReportType as ImportedReportType,
        MilitaryReportFormatter as ImportedMilitaryReportFormatter,
    )
    MilitaryPacket = ImportedMilitaryPacket
    Priority = ImportedPriority
    Coordinates = ImportedCoordinates
    ReportType = ImportedReportType
    MilitaryReportFormatter = ImportedMilitaryReportFormatter
except Exception:
    class Priority(str, Enum):
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"

    class Coordinates(BaseModel):
        x: float
        y: float

    class MilitaryPacket(BaseModel):
        action: str
        target_units: list[str]
        coordinates: Coordinates
        timeframe: str
        priority: Priority

    class ReportType(str, Enum):
        EOINCREP = "EOINCREP"

    class MilitaryReportFormatter:
        def format_and_save_report(self, data: dict, report_type: ReportType = ReportType.EOINCREP) -> tuple[str, str]:
            # Minimal example implementation — user can replace with their own formatter
            content = f"Report type: {report_type}\n" + json.dumps(data, indent=2)
            out_path = Path("processed_data")
            out_path.mkdir(exist_ok=True)
            p = out_path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            p.write_text(content, encoding="utf-8")
            return content, str(p)


# --- Utility functions ---

def is_probably_json(text: str) -> bool:
    """Quick heuristic to decide if input looks like JSON or JSON-ish."""
    s = text.strip()
    # obvious JSON or JSON-lines
    if s.startswith("{") or s.startswith("["):
        return True
    # contains key: value pairs typical of JSON
    if re.search(r"\"?\w+\"?\s*:\s*", s) and ("{" in s or ":" in s):
        return True
    return False


def extract_first_balanced_braces(s: str) -> Optional[str]:
    """Return the first substring that contains balanced braces { ... }.
    Useful to pull out JSON the model embedded in stray text.
    """
    start = None
    depth = 0
    for i, ch in enumerate(s):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}' and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                return s[start:i + 1]
    return None


def heuristic_repair_json(text: str) -> Optional[dict]:
    """Apply heuristic repairs to common JSON problems and try to parse."""
    if not isinstance(text, str):
        return None
        
    t = text.strip()

    # 1) Try direct json.loads
    try:
        parsed = json.loads(t)
        if not isinstance(parsed, dict):
            parsed = {"data": parsed}
        return parsed
    except Exception:
        pass

    # 2) Use json_repair if available (best effort)
    if _HAS_JSON_REPAIR:
        try:
            return json_repair.loads(t)
        except Exception:
            pass

    # 3) Basic textual fixes
    # - Replace single quotes with double quotes (naive, but common)
    t2 = t.replace("\"'\"", '"')  # no-op protective
    t2 = re.sub(r"'([^\"]*?)'", r'"\1"', t2)

    # - Remove trailing commas before } or ]
    t2 = re.sub(r",\s*([}\]])", r"\1", t2)

    # - Add quotes around unquoted keys (only when safe: at start of line, or after { or ,)
    def quote_keys(match: re.Match) -> str:
        key = match.group(1)
        return f'"{key}":'

    t2 = re.sub(r'(?<=\{|,|\[)\s*([A-Za-z_][A-Za-z0-9_\-]*)\s*:', quote_keys, t2)

    # - Replace Python booleans/None
    t2 = re.sub(r"\bNone\b", "null", t2)
    t2 = re.sub(r"\bTrue\b", "true", t2)
    t2 = re.sub(r"\bFalse\b", "false", t2)

    # Try parse
    try:
        return json.loads(t2)
    except Exception:
        pass

    # 4) Try to find a JSON-like block and parse that
    block = extract_first_balanced_braces(t)
    if block:
        try:
            return json.loads(block)
        except Exception:
            # try repairs on block
            try:
                return json.loads(re.sub(r"'([^']*?)'", r'"\1"', block))
            except Exception:
                pass

    return None


# --- Main class ---
class MilitaryTextEncoder:
    def __init__(self, model_name: str = "google/flan-t5-small", max_length: int = 512, device: Optional[str] = None):
        """
        model_name: local seq2seq model to use as fallback (defaults to flan-t5-small).
        max_length: token length for generation.
        device: None (auto CPU) or 'cuda' if you have GPU and want to use it.
        """
        self.model_name = model_name
        self.max_length = max_length
        self.device = device

        # Prepare output folder
        self.output_dir = Path("./processed_data")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize LLM pipeline lazily (only if we need it) to keep startup light
        self._pipe = None

    def _init_pipeline(self):
        if self._pipe is not None:
            return
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            device_map = 0 if (self.device == 'cuda') else -1
            self._pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                device=device_map,
                dtype="auto",  # Add dtype parameter
                truncation=True,
                max_length=self.max_length,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize local LLM pipeline: {e}")

    def _preprocess_text(self, text: str) -> str:
        """Clean and standardize input text for better LLM processing."""
        # Convert parentheses coordinates to standard format
        text = re.sub(r'\((\d+\.?\d*),\s*(\d+\.?\d*)\)', r'{"x": \1, "y": \2}', text)
        
        # Convert common time formats
        text = re.sub(r'\b(\d{4})Z\b', r'\1 Zulu', text)
        
        # Normalize priority indicators
        text = re.sub(r'\b(?:urgent|critical)\b', 'HIGH', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(?:normal|standard)\b', 'MEDIUM', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(?:low|routine)\b', 'LOW', text, flags=re.IGNORECASE)
        
        return text

    def _create_json_template(self, text: str) -> dict:
        """Create a structured JSON template from the input text."""
        # Extract potential units (words starting with capital letters)
        units = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+team)?\b', text)
        
        # Extract potential coordinates
        coords_match = re.search(r'(?:coordinates?|loc|position).*?(?:(?:[-+]?\d*\.?\d+),\s*(?:[-+]?\d*\.?\d+)|\{.*?\})', text, re.IGNORECASE)
        coords = {"x": 0.0, "y": 0.0}
        if coords_match:
            try:
                coords_text = coords_match.group(0)
                if '{' in coords_text:
                    coords = json.loads(re.search(r'\{.*?\}', coords_text).group(0))
                else:
                    x, y = map(float, re.findall(r'[-+]?\d*\.?\d+', coords_text)[:2])
                    coords = {"x": x, "y": y}
            except Exception:
                pass

        # Extract priority
        priority = "MEDIUM"
        if re.search(r'\b(?:urgent|critical|high)\b', text, re.IGNORECASE):
            priority = "HIGH"
        elif re.search(r'\b(?:low|routine)\b', text, re.IGNORECASE):
            priority = "LOW"

        return {
            "action": "move",  # default action
            "target_units": units or ["Unknown"],
            "coordinates": coords,
            "timeframe": "immediate",  # default timeframe
            "priority": priority
        }

    def _llm_extract_json(self, text: str) -> dict:
        """Use a local seq2seq model to extract structured JSON from free text."""
        self._init_pipeline()
        
        # Preprocess text and create initial template
        cleaned_text = self._preprocess_text(text)
        template = self._create_json_template(cleaned_text)
        
        prompt = (
            f"Convert this military message into JSON. Use this template and fix any wrong values:\n"
            f"{json.dumps(template, indent=2)}\n\n"
            f"Message:\n{cleaned_text}\n"
            f"Fixed JSON (output only valid JSON):"
        )

        best_result = None
        for _ in range(3):
            try:
                out = self._pipe(prompt, max_length=self.max_length)
                generated = out[0]["generated_text"].strip()
                
                # Try to find JSON in the response
                json_match = extract_first_balanced_braces(generated)
                if json_match:
                    parsed = json.loads(json_match)
                    if isinstance(parsed, dict):
                        # Validate fields
                        validated = MilitaryPacket(**parsed)
                        return validated.model_dump()  # Changed from dict()
                
                # If we got here, try to merge with template
                merged = template.copy()
                try:
                    if json_match:
                        parsed = json.loads(json_match)
                        if isinstance(parsed, dict):
                            merged.update(parsed)
                            validated = MilitaryPacket(**merged)
                            return validated.model_dump()  # Changed from dict()
                except Exception:
                    continue
                    
            except Exception:
                continue
        
        # If all attempts failed, try to use the template directly
        try:
            return MilitaryPacket(**template).model_dump()  # Changed from dict()
        except Exception:
            raise ValueError("Failed to generate valid JSON")

    def process_text(self, text: str) -> Dict[str, Any]:
        """Main entry point: try to parse/repair JSON locally first; otherwise use LLM fallback."""
        try:
            # If it looks like JSON, try repair/parse first
            if is_probably_json(text):
                parsed = heuristic_repair_json(text)
                if parsed is not None and isinstance(parsed, dict):
                    try:
                        validated = MilitaryPacket(**parsed)
                        return validated.model_dump()  # Changed from dict()
                    except ValidationError as e:
                        # If validation fails, we may still attempt LLM extraction
                        pass

            # If we reach here, use the LLM fallback
            return self._llm_extract_json(text)
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}

    def process_and_format(self, text: str, report_type: ReportType = ReportType.EOINCREP) -> tuple[str, str]:
        data = self.process_text(text)
        if isinstance(data, dict) and "error" in data:
            return f"Error: {data['error']}", ""

        formatter = MilitaryReportFormatter()
        return formatter.format_and_save_report(data, report_type)

    def save_output(self, data: dict, output_path: Optional[Path] = None) -> str:
        if output_path is None:
            output_path = Path.cwd() / f"military_data_{abs(hash(json.dumps(data, sort_keys=True)))}.json"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return str(output_path)
        except Exception as e:
            return f"Error saving output: {e}"

    def process_and_save_all(self, text: str, report_type: ReportType = ReportType.EOINCREP) -> dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {"status": "success"}

        data = self.process_text(text)
        if isinstance(data, dict) and "error" in data:
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


# --- If run as script: example usage ---
if __name__ == "__main__":
    encoder = MilitaryTextEncoder()

    messy_text = """ Alpha Squad and Bravo Team need to hold position ASAP at coords 123.456, 789.012! 
    This is HIGH priority - execute at 0800Z tomorrow. Maintain defensive posture
    and await further orders. DO NOT let anyone through! Command out.
    """

    
    #"""
    #Alpha team needs 2 move quickly!! coordinates are (123.45, 678.90)
    #time: 0600Z tmrw... Bravo & Charlie providing backup
    #THIS IS URGENT/HIGH PRIORITY!!!
    #"""

    results = encoder.process_and_save_all(messy_text, ReportType.EOINCREP)
    if results.get('status') == 'success':
        print("Processing completed successfully!")
        print(f"Saved JSON to: {results['json_path']}")
        print(f"Saved report to: {results['report_path']}")
        print("Report content:\n", results['report_content'])
    else:
        print("Error:", results.get('error'))
