
import datetime

def log(msg):
    ts = datetime.datetime.utcnow().isoformat()
    print(f"[salesbot][{ts}] {msg}")
