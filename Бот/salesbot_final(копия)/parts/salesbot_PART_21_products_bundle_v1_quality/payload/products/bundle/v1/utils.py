
def deal_title(bundle)->str:
    title = bundle.name or "Bundle"
    parts = [i.get("type","") for i in (bundle.items or [])]
    if parts:
        title += " (" + ", ".join(parts) + ")"
    return title
