
import os

DEFAULT_KGS_USD = float(os.getenv("KGS_USD", "0.011"))  # пример
DEFAULT_KGS_UZS = float(os.getenv("KGS_UZS", "140.0"))  # пример
DEFAULT_VAT_RATE = float(os.getenv("VAT_RATE", "0.12"))

def convert(amount_kgs: float, currency: str)->float:
    c = (currency or "KGS").upper()
    if c == "KGS":
        return amount_kgs
    if c == "USD":
        return round(amount_kgs * DEFAULT_KGS_USD, 2)
    if c == "UZS":
        return round(amount_kgs * DEFAULT_KGS_UZS, 2)
    return amount_kgs

def apply_pricing(bundle, currency: str="KGS", coupon: float|None=None, promo: float|None=None, vat: bool=False):
    base = float(bundle.base_price or 0.0)
    # скидки
    if coupon:
        base = base * (1.0 - float(coupon)/100.0)
    if promo:
        base = max(0.0, base - float(promo))

    # НДС
    if vat:
        base = base * (1.0 + DEFAULT_VAT_RATE)

    # конвертация
    final = convert(base, currency)
    out = bundle.to_dict()
    out["pricing"] = {
        "currency": currency.upper(),
        "subtotal_kgs": round(bundle.base_price, 2),
        "total_kgs": round(base, 2),
        "total_converted": final,
        "vat_applied": bool(vat),
        "vat_rate": DEFAULT_VAT_RATE,
        "coupon_percent": float(coupon or 0),
        "promo_fixed": float(promo or 0),
    }
    return out
