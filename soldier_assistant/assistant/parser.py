from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

def parser_text(parser, text, action_map,min_confidence=0.6):
    intent = None
    for i in parser.determine_intent(text):
        confidence = i.get("confidence", 1.0)
        print(f"[INTENT] Parsed: {i} (confidence: {confidence:.2f})")
        if confidence >= min_confidence:
            intent = i

    if intent is None:
        return None

    action_text = intent["Action"].lower()
    return action_map.get(action_text)


def build_parser():
    engine = IntentDeterminationEngine()

    # Intent: Turn on light
    action_intent = IntentBuilder("ActionIntent") \
        .require("Action") \
        .build()

    engine.register_intent_parser(action_intent)
    ACTION_MAP = {
        "opord": "OPORD",
        "operation order": "OPORD",
        "operation orders": "OPORD",
        "frago": "FRAGO",
        "fragmentary order": "FRAGO",
        "fragmentary orders": "FRAGO"
    }

    # Registrazione delle entità
    for keyword in ACTION_MAP.keys():
        engine.register_entity(keyword, "Action")

    # Restituisci motore e mappatura
    return engine, ACTION_MAP