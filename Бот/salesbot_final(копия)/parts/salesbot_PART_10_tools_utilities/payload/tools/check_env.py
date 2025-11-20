
import os

REQUIRED_ENV = [
    "DEEPSEEK_API_KEY",
    "ASSEMBLYAI_API_KEY",
    "CRM_API_BASE",
    "CRM_API_TOKEN"
]

def run():
    missing = []
    for k in REQUIRED_ENV:
        if not os.getenv(k):
            missing.append(k)
    return {
        "ok": len(missing)==0,
        "missing": missing
    }

if __name__ == "__main__":
    print(run())
