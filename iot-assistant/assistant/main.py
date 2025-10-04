from assistant.sst import clean_command, listen_once
from assistant.parser import build_parser, parser_text
from assistant.mqtt_client import publish_command
from assistant.wake import wait_for_wake_word, cleanup

def handle_command(text, parser):
    print(f"[COMMAND] Raw: {text}")
    cleaned = clean_command(text)
    print(f"[COMMAND] Cleaned: {cleaned}")
    intent = parser_text(parser, cleaned)
    if intent and 'Device' in intent:
        subject = intent['Device']
    else:
        subject = "unknown"
    publish_command(subject, text)
def main():
    parser = build_parser()
    try:
        while True:
            wait_for_wake_word()
            text = listen_once()
            handle_command(text, parser)
    except KeyboardInterrupt:
        print("[SYSTEM] Interrupted by user.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
