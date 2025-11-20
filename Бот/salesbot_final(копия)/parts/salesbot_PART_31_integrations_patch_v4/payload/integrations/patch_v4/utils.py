
import time, random

def retry(fn, attempts=3, delay=0.3):
    for i in range(attempts):
        try:
            return fn()
        except Exception:
            time.sleep(delay)
    raise Exception("Retry failed")

def integration_result(ok: bool, data=None, error=None):
    return {
        "ok": ok,
        "data": data,
        "error": error
    }
