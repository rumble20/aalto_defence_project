from pathlib import Path
import json
import re
from datetime import datetime
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize LLM pipeline
llm_model_name = "google/flan-t5-small"
llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
llm_model = AutoModelForSeq2SeqLM.from_pretrained(llm_model_name)
llm_pipeline = pipeline("text2text-generation", model=llm_model, tokenizer=llm_tokenizer)

# Optional JSON repair (soft dependency)
try:
    import json_repair
    _HAS_JSON_REPAIR = True
except Exception:
    _HAS_JSON_REPAIR = False


# -------------------------
# Schema
# -------------------------
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
    radio_call_sign: Optional[str] = None
    extras: Optional[dict] = {}
    transmission_time: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    received_time: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class ReportType(str, Enum):
    EOINCREP = "EOINCREP"
    CASEVAC = "CASEVAC"

class MilitaryReportFormatter:
    def format_and_save_report(self, data: dict, report_type: ReportType = ReportType.EOINCREP) -> tuple[str, str]:
        content = f"Report type: {report_type}\n{json.dumps(data, indent=2)}"
        out_path = Path("processed_data")
        out_path.mkdir(exist_ok=True)
        p = out_path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        p.write_text(content, encoding="utf-8")
        return content, str(p)


# -------------------------
# Helpers: validation/repair utilities
# -------------------------
def is_probably_json(text: str) -> bool:
    s = (text or "").strip()
    if not s:
        return False
    if s.startswith("{") or s.startswith("["):
        return True
    # looks like key: value pairs somewhere
    if re.search(r"\"?\w+\"?\s*:\s*", s) and (":" in s):
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
                return s[start:i+1]
    return None

def heuristic_repair_json(text: str) -> Optional[dict]:
    """Best-effort attempts to turn messy JSON-like text into a dict."""
    if not isinstance(text, str):
        return None
    t = text.strip()
    # 1) try direct parse
    try:
        parsed = json.loads(t)
        if isinstance(parsed, dict):
            return parsed
        return {"data": parsed}
    except Exception:
        pass
    # 2) json_repair if available
    if _HAS_JSON_REPAIR:
        try:
            return json_repair.loads(t)
        except Exception:
            pass
    # 3) basic textual repairs
    t2 = t
    # replace single quotes with double quotes around words (naive but useful)
    t2 = re.sub(r"(?<!\w)'([^']+)'", r'"\1"', t2)
    # ensure unquoted keys get quoted when followed by colon
    t2 = re.sub(r'(?<=\{|\s|,)([A-Za-z_][A-Za-z0-9_\-]*)\s*:', r'"\1":', t2)
    # remove trailing commas
    t2 = re.sub(r',\s*(\}|])', r'\1', t2)
    # python None/True/False -> json equivalents
    t2 = re.sub(r'\bNone\b', 'null', t2)
    t2 = re.sub(r'\bTrue\b', 'true', t2)
    t2 = re.sub(r'\bFalse\b', 'false', t2)
    # try parse repaired string
    try:
        parsed = json.loads(t2)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    # 4) try to extract first JSON block
    block = extract_first_balanced_braces(t)
    if block:
        try:
            return json.loads(block)
        except Exception:
            try:
                # quick fix single quotes in block
                return json.loads(re.sub(r"(?<!\w)'([^']+)'", r'"\1"', block))
            except Exception:
                pass
    return None


# -------------------------
# Extraction functions (robust)
# -------------------------
_UNIT_TYPES = ["Squad", "Team", "Platoon", "Company", "Unit", "Section", "Battery"]
_UNIT_TYPES_RE = r'(?:' + '|'.join(_UNIT_TYPES) + r')\b'

_STOPWORDS = { "ID", "HIGH", "LOW", "MEDIUM", "CALL", "SIGN", "MISSIONID", "OBJECTIVE",
               "ASAP", "TOMORROW", "ZULU", "EXECUTE", "MAINTAIN", "NEED", "HOLD" }

_ACTION_VERBS = [
    "advance", "attack", "evacuate", "hold", "defend", "secure", "move",
    "withdraw", "retreat", "support", "occupy", "protect"
]

def extract_units(text: str) -> list[str]:
    """Return list of unit phrases, prefer matches that include a unit type."""
    t = text or ""
    # 1) find explicit unit phrases like "Alpha Squad", "Bravo Team"
    pattern_with_type = rf'\b([A-Z][a-z0-9]+(?:\s+(?:{ "|".join(_UNIT_TYPES) }))?)'
    # Use a safer approach:
    explicit = []
    for ut in _UNIT_TYPES:
        for m in re.finditer(rf'\b([A-Z][a-z0-9]+)\s+{ut}\b', t):
            explicit.append(f"{m.group(1)} {ut}")
    if explicit:
        # deduplicate preserving order
        seen = set()
        out = []
        for u in explicit:
            if u not in seen:
                out.append(u)
                seen.add(u)
        return out

    # 2) fallback: find capitalized words (but filter stopwords and words that are all-caps or contain digits)
    candidates = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', t)
    out = []
    for c in candidates:
        cw = c.upper()
        if cw in _STOPWORDS:
            continue
        if re.search(r'\d', c):  # skip names with digits (likely IDs)
            continue
        if len(c) <= 2:
            continue
        if c not in out:
            out.append(c)
    return out or ["Unknown"]

def extract_coordinates(text: str) -> dict:
    t = text or ""
    # Try explicit 'coords' or 'at coords' style first
    m = re.search(r'(?:coords?|coordinates?|position|pos|at)\s*[:\-]?\s*([-\+]?\d{1,3}\.\d+)[,;\s]+([-\+]?\d{1,3}\.\d+)', t, re.IGNORECASE)
    if m:
        try:
            return {"x": float(m.group(1)), "y": float(m.group(2))}
        except Exception:
            pass
    # fallback: any two floats separated by comma (first occurrence)
    m2 = re.search(r'([-\+]?\d{1,3}\.\d+)[,;\s]+([-\+]?\d{1,3}\.\d+)', t)
    if m2:
        try:
            return {"x": float(m2.group(1)), "y": float(m2.group(2))}
        except Exception:
            pass
    return {"x": 0.0, "y": 0.0}

def extract_action(text: str) -> str:
    # first, look for constructs like "need to hold" or "must hold" -> prioritize the verb after 'to' or modal
    m = re.search(r'\b(?:need to|must|should|will|shall|ordered to)\s+([a-z]+)\b', text, re.IGNORECASE)
    if m and m.group(1).lower() in _ACTION_VERBS:
        return m.group(1).lower()
    # then direct verb matches
    m2 = re.search(r'\b(' + '|'.join(_ACTION_VERBS) + r')\b', text, re.IGNORECASE)
    if m2:
        return m2.group(1).lower()
    return "move"

def extract_priority(text: str) -> str:
    t = text or ""
    if re.search(r'\b(urgent|critical|high)\b', t, re.IGNORECASE):
        return Priority.HIGH.value
    if re.search(r'\b(low|routine)\b', t, re.IGNORECASE):
        return Priority.LOW.value
    return Priority.MEDIUM.value

def extract_timeframe(text: str) -> str:
    t = text or ""
    # HHMMZ or HMMZ etc. e.g. 0800Z
    m = re.search(r'\b(\d{3,4})\s*Z\b', t, re.IGNORECASE)
    if m:
        tf = f"{m.group(1)}Z"
        if re.search(r'\btomorrow\b', t, re.IGNORECASE):
            tf = tf + " (tomorrow)"
        return tf
    # common words: immediate/asap/tomorrow
    if re.search(r'\b(asap|immediately|immediate)\b', t, re.IGNORECASE):
        return "immediate"
    if re.search(r'\btomorrow\b', t, re.IGNORECASE):
        return "tomorrow"
    return "immediate"

def extract_soldier_id(text: str) -> str:
    m = re.search(r'\b(?:ID|Soldier)[:=]?\s*([A-Z0-9\-]+)\b', text, re.IGNORECASE)
    if m:
        return m.group(1)
    return "UNKNOWN"

def extract_radio_call_sign(text: str) -> Optional[str]:
    m = re.search(r'\bCall[- ]?Sign[:=]?\s*([A-Z0-9\-]+)\b', text, re.IGNORECASE)
    if m:
        return m.group(1)
    # also accept "Callsign: X" variants
    m2 = re.search(r'\bCallsign[:=]?\s*([A-Z0-9\-]+)\b', text, re.IGNORECASE)
    if m2:
        return m2.group(1)
    return None

def extract_mission_id(text: str) -> dict:
    m = re.search(r'\bMissionID[:=]?\s*([A-Z0-9\-]+)\b', text, re.IGNORECASE)
    if m:
        return {"mission_id": m.group(1)}
    return {}


# -------------------------
# Main encoder
# -------------------------
class MilitaryTextEncoder:
    def __init__(self, model_name: str = "google/flan-t5-small", max_length: int = 512, device: Optional[str] = None):
        self.model_name = model_name
        self.max_length = max_length
        self.device = device
        self.output_dir = Path("./processed_data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._pipe = None

    def _init_pipeline(self):
        """Initialize HuggingFace LLM pipeline if needed."""
        if self._pipe is not None:
            return
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        device_map = 0 if self.device == "cuda" else -1
        self._pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device_map,
            max_length=self.max_length
        )

    def _create_json_template(self, text: str) -> dict:
        """Rule-based regex extraction."""
        text = text.replace("\n", " ").strip()
        return {
            "action": extract_action(text),
            "target_units": extract_units(text),
            "coordinates": extract_coordinates(text),
            "timeframe": extract_timeframe(text),
            "priority": extract_priority(text),
            "soldier_id": extract_soldier_id(text),
            "radio_call_sign": extract_radio_call_sign(text),
            "extras": extract_mission_id(text),
            "transmission_time": datetime.now().isoformat(),
            "received_time": datetime.now().isoformat()
        }

    def _llm_parse(self, text: str) -> Optional[dict]:
        """Fallback: Use local LLM to parse free text into structured JSON."""
        try:
            self._init_pipeline()
            prompt = (
                "Extract military structured data as JSON with fields: "
                "action, target_units, coordinates(x,y), timeframe, priority, "
                "soldier_id, radio_call_sign, extras.\n\n"
                f"Message: {text}"
            )
            output = self._pipe(prompt, num_return_sequences=1)[0]["generated_text"]

            # Attempt to parse JSON
            if _HAS_JSON_REPAIR:
                parsed = json_repair.loads(output)
            else:
                parsed = json.loads(output)

            # Validate & normalize
            validated = MilitaryPacket(**parsed)
            return validated.model_dump()
        except Exception as e:
            print(f"[LLM Fallback Failed] {e}")
            return None

    def process_text(self, text: str) -> dict:
        # 1. Regex / heuristic path
        template = self._create_json_template(text)
        try:
            validated = MilitaryPacket(**template)
            return validated.model_dump()
        except Exception:
            pass  # If regex template fails, continue to LLM

        # 2. LLM fallback path
        try:
            self._init_pipeline()
            prompt = (
                "Convert this military message into JSON with fields: "
                "action, target_units, coordinates{x,y}, timeframe, priority, "
                "soldier_id, radio_call_sign, extras.\n\nMessage:\n"
                f"{text}"
            )
            llm_out = self._pipe(prompt)[0]["generated_text"]

            # Try to extract valid JSON from model output
            try:
                parsed = json.loads(llm_out)
            except Exception:
                if "{" in llm_out and "}" in llm_out:
                    # Try to grab substring between { ... }
                    start, end = llm_out.find("{"), llm_out.rfind("}") + 1
                    snippet = llm_out[start:end]
                    parsed = json.loads(snippet)
                else:
                    raise ValueError("LLM did not return JSON")

            # Normalize with schema
            validated = MilitaryPacket(**parsed)
            print("[LLM Path Succeeded ✅] Structured JSON generated via model")
            return validated.model_dump()

        except Exception as e:
            print(f"[LLM Fallback Failed] {e}")
            # As a last resort, return regex template
            return template

    def process_and_save_all(self, text: str, report_type: ReportType = ReportType.EOINCREP) -> dict:
        """Full pipeline: process text, save JSON + formatted report."""
        data = self.process_text(text)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save structured JSON
        json_path = self.output_dir / f"structured_data_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        # Save formatted report
        formatter = MilitaryReportFormatter()
        report_content, report_path = formatter.format_and_save_report(data, report_type)

        return {
            "json_path": str(json_path),
            "report_path": report_path,
            "report_content": report_content,
            "structured": data
        }
   