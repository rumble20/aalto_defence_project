from assistant.sst import clean_command, listen_once
from assistant.parser import build_parser, parser_text
from assistant.mqtt_client import publish_command
from assistant.wake import wait_for_wake_word, cleanup
import json

def handle_command(text, parser, action_map=None):
    print(f"[COMMAND] Raw: {text}")
    cleaned = clean_command(text)
    print(f"[COMMAND] Cleaned: {cleaned}")
    action= parser_text(parser, cleaned, action_map)
    if action:
        payload = {
            "action": action,
            "text": text  
        }
    else:
        payload = {
            "action": "UNKNOWN",
            "text": text  
        }
    json_payload = json.dumps(payload)
    publish_command(json_payload)   
    print(f"[COMMAND] Published payload: {json_payload}")      


def main():
    parser, ACTION_MAP = build_parser()
    try:
        while True:
            wait_for_wake_word()
            text = listen_once()
            handle_command(text, parser, ACTION_MAP)
    except KeyboardInterrupt:
        print("[SYSTEM] Interrupted by user.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()