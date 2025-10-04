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
    """Apply heuristic repairs to common JSON problems and try to parse.
    This is intentionally conservative: it attempts fixes in several passes.
    """
    t = text.strip()

    # 1) Try direct json.loads
    try:
        return json.loads(t)
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
    t2 = re.sub(r"'([^"]*?)'", r'"\1"', t2)

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
                return json.loads(re.sub(r"'([^"]*?)'", r'"\1"', block))
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
        # Use seq2seq text2text-generation model (flan-t5 small is CPU-friendly)
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            device_map = 0 if (self.device == 'cuda') else -1
            self._pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                device=device_map,
                truncation=True,
                max_length=self.max_length,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize local LLM pipeline: {e}")

    def _llm_extract_json(self, text: str) -> dict:
        """Use a local seq2seq model to extract structured JSON from free text.
        The model chosen should be small for CPU usage (flan-t5-small by default).
        """
        self._init_pipeline()

        prompt = (
            "Extract a JSON object with ONLY the following fields (no extra keys):\n"
            "{\n"
            '  "action": "string",\n'
            '  "target_units": ["string"],\n'
            '  "coordinates": {"x": float, "y": float},\n'
            '  "timeframe": "string",\n'
            '  "priority": "HIGH|MEDIUM|LOW"\n'
            "}\n\n"
            "Output: ONLY valid JSON (no explanation).\n\n"
            "Text: \n" + text + "\n\nJSON:\n"
        )

        out = self._pipe(prompt, max_length=self.max_length)
        generated = out[0]["generated_text"]

        # Extract JSON substring
        candidate = extract_first_balanced_braces(generated)
        if candidate is None:
            # As a fallback, try to find any {...} in the response
            match = re.search(r"\{.*\}", generated, flags=re.DOTALL)
            candidate = match.group(0) if match else generated

        # Try to parse and repair if necessary
        parsed = heuristic_repair_json(candidate)
        if not parsed:
            raise ValueError("LLM returned no parsable JSON")

        # Validate via Pydantic
        validated = MilitaryPacket(**parsed)
        return validated.dict()

    def process_text(self, text: str) -> Dict[str, Any]:
        """Main entry point: try to parse/repair JSON locally first; otherwise use LLM fallback."""
        # If it looks like JSON, try repair/parse first
        if is_probably_json(text):
            parsed = heuristic_repair_json(text)
            if parsed is not None:
                try:
                    validated = MilitaryPacket(**parsed)
                    return validated.dict()
                except ValidationError as e:
                    # If validation fails, we may still attempt LLM extraction
                    pass

        # If we reach here, use the LLM fallback
        try:
            return self._llm_extract_json(text)
        except Exception as e:
            return {"error": f"LLM extraction failed: {e}"}

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

    messy_text = """
    Alpha team needs 2 move quickly!! coordinates are (123.45, 678.90)
    time: 0600Z tmrw... Bravo & Charlie providing backup
    THIS IS URGENT/HIGH PRIORITY!!!
    """

    results = encoder.process_and_save_all(messy_text, ReportType.EOINCREP)
    if results.get('status') == 'success':
        print("Processing completed successfully!")
        print(f"Saved JSON to: {results['json_path']}")
        print(f"Saved report to: {results['report_path']}")
        print("Report content:\n", results['report_content'])
    else:
        print("Error:", results.get('error'))
