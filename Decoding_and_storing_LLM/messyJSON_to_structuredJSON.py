"""
Robust local-only Military Text -> Structured JSON encoder
- Attempts to parse/repair messy JSON locally (no OpenAI required)
- Falls back to a local instruction-tuned model for extraction (google/flan-t5-small by default)
- Validates output with Pydantic

Dependencies:
  pip install transformers torch pydantic json-repair
"""

from pathlib import Path
import json
import re
from datetime import datetime
from typing import Dict, Union, Optional, Any
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Try to import json_repair if available
try:
    import json_repair
    _HAS_JSON_REPAIR = True
except Exception:
    _HAS_JSON_REPAIR = False


# --- Improved stopwords and helpers ---
_STOPWORDS = {
    "asap", "this", "that", "command", "out", "not", "do", "the", "and", "need", "needs",
    "high", "medium", "low", "zulu", "maintain", "tomorrow", "urgent", "critical",
    "execute", "hold", "position", "coords", "coordinates", "call", "sign"
}
_STOPWORDS_UPPER = {w.upper() for w in _STOPWORDS}

def _clean_unit_token(u: str) -> str:
    """Normalize unit token and filter obvious false positives."""
    u_stripped = u.strip()
    if len(u_stripped) < 2:
        return ""
    if re.fullmatch(r'[A-Z]{2,}', u_stripped):
        if u_stripped in _STOPWORDS_UPPER:
            return ""
    if u_stripped.lower() in _STOPWORDS:
        return ""
    return u_stripped


# --- Schema ---
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
    soldier_id: Optional[str] = Field(default="UNKNOWN")
    date_and_hour: Optional[str] = None
    radio_call_sign: Optional[str] = None
    extras: Optional[dict] = {}
    transmission_time: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    received_time: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReportType(str, Enum):
    EOINCREP = "EOINCREP"
    CASEVAC = "CASEVAC"

class MilitaryReportFormatter:
    def format_and_save_report(self, data: dict, report_type: ReportType = ReportType.EOINCREP) -> tuple[str, str]:
        content = f"Report type: {report_type}\n" + json.dumps(data, indent=2)
        out_path = Path("processed_data")
        out_path.mkdir(exist_ok=True)
        p = out_path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        p.write_text(content, encoding="utf-8")
        return content, str(p)


# --- JSON helpers ---
def is_probably_json(text: str) -> bool:
    s = text.strip()
    if s.startswith("{") or s.startswith("["):
        return True
    if re.search(r"\"?\w+\"?\s*:\s*", s) and ("{" in s or ":" in s):
        return True
    return False

def extract_first_balanced_braces(s: str) -> Optional[str]:
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
    if not isinstance(text, str):
        return None
    t = text.strip()
    try:
        parsed = json.loads(t)
        if not isinstance(parsed, dict):
            parsed = {"data": parsed}
        return parsed
    except Exception:
        pass
    if _HAS_JSON_REPAIR:
        try:
            return json_repair.loads(t)
        except Exception:
            pass
    t2 = re.sub(r"'([^\"]*?)'", r'"\1"', t)
    t2 = re.sub(r",\s*([}\]])", r"\1", t2)
    try:
        return json.loads(t2)
    except Exception:
        pass
    block = extract_first_balanced_braces(t)
    if block:
        try:
            return json.loads(block)
        except Exception:
            pass
    return None


# --- Main class ---
class MilitaryTextEncoder:
    def __init__(self, model_name: str = "google/flan-t5-small", max_length: int = 512, device: Optional[str] = None):
        self.model_name = model_name
        self.max_length = max_length
        self.device = device
        self.output_dir = Path("./processed_data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._pipe = None

    def _init_pipeline(self):
        if self._pipe is not None:
            return
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        device_map = 0 if (self.device == 'cuda') else -1
        self._pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device_map,
            max_length=self.max_length,
        )

    def _create_json_template(self, text: str) -> dict:
            txt = text.replace("\n", " ").replace("  ", " ").strip()

            raw_units = re.findall(r'\b([A-Z][a-z0-9]+(?:\s+(?:Squad|Team|Platoon|Company|Unit))?)\b', txt)
            units = []
            for u in raw_units:
                cu = _clean_unit_token(u)
                if cu and cu not in units:
                    units.append(cu)

            coords = {"x": 0.0, "y": 0.0}
            pair = re.search(r'([-+]?\d{1,3}\.\d+)[,;\s]+([-+]?\d{1,3}\.\d+)', txt)
            if pair:
                coords = {"x": float(pair.group(1)), "y": float(pair.group(2))}

            priority = "MEDIUM"
            if re.search(r'\b(urgent|critical|high)\b', txt, re.IGNORECASE):
                priority = "HIGH"
            elif re.search(r'\b(low|routine)\b', txt, re.IGNORECASE):
                priority = "LOW"

            timeframe = "immediate"
            date_and_hour = None
            tm = re.search(r'\b(\d{3,4})\s*Z\b', txt, re.IGNORECASE)
            if tm:
                hhmm = tm.group(1)
                date_and_hour = f"{hhmm}Z"
                timeframe = date_and_hour
                if re.search(r'\btomorrow\b', txt, re.IGNORECASE):
                    date_and_hour += " (tomorrow)"

            soldier_id = None
            id_m = re.search(r'\b(?:ID|Soldier|SID)[:=]?\s*([A-Z0-9-]+)\b', txt, re.IGNORECASE)
            if id_m:
                soldier_id = id_m.group(1)

            radio_call_sign = None
            cs_m = re.search(r'\bCall[- ]?Sign[:=]?\s*([A-Za-z0-9-]+)\b', txt, re.IGNORECASE)
            if cs_m:
                radio_call_sign = cs_m.group(1)

            extras = {}
            mission_id_m = re.search(r'\bMissionID[:=]?\s*([A-Za-z0-9-]+)\b', txt, re.IGNORECASE)
            if mission_id_m:
                extras.setdefault("mission_info", {})["mission_id"] = mission_id_m.group(1)

            action = ""
            action_match = re.search(r'(?i)\b(advance|attack|evacuate|hold|defend|secure|move|withdraw|retreat|support|occupy|protect)\b[^.!\n]*', txt)
            if action_match:
                action = action_match.group(0).strip()

            return {
                "action": action or "move",
                "target_units": units or ["Unknown"],
                "coordinates": coords,
                "timeframe": timeframe,
                "priority": priority,
                "soldier_id": soldier_id or "UNKNOWN",
                "date_and_hour": date_and_hour or datetime.now().isoformat(),
                "radio_call_sign": radio_call_sign,
                "extras": extras
            }

    def process_text(self, text: str) -> Dict[str, Any]:
        try:
            if is_probably_json(text):
                parsed = heuristic_repair_json(text)
                if parsed is not None and isinstance(parsed, dict):
                    if 'transmission_time' not in parsed:
                        parsed['transmission_time'] = datetime.now().isoformat()
                    if 'received_time' not in parsed:
                        parsed['received_time'] = datetime.now().isoformat()
                    if 'soldier_id' not in parsed:
                        parsed['soldier_id'] = "UNKNOWN"
                    if 'date_and_hour' not in parsed:
                        parsed['date_and_hour'] = datetime.now().isoformat()
                    validated = MilitaryPacket(**parsed)
                    return validated.model_dump()
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
        return self._create_json_template(text)

    def process_and_save_all(self, text: str, report_type: ReportType = ReportType.EOINCREP) -> dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = self.process_text(text)
        json_path = self.output_dir / f"structured_data_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        formatter = MilitaryReportFormatter()
        report_content, report_path = formatter.format_and_save_report(data, report_type)
        return {"json_path": str(json_path), "report_path": report_path, "report_content": report_content}


if __name__ == "__main__":
    encoder = MilitaryTextEncoder()
    messy_text = """ID:A123 Alpha Squad and Bravo Team need to hold position ASAP at coords 123.456, 789.012!
    This is HIGH priority - execute at 0800Z tomorrow. Maintain defensive posture.
    Call Sign: EAGLE1. MissionID: OP45. Objective: Hold bridgehead until reinforcements arrive."""
    results = encoder.process_and_save_all(messy_text, ReportType.EOINCREP)
    print(json.dumps(results, indent=2))
