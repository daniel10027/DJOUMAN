import hmac, hashlib, math

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return R * (2*math.atan2(math.sqrt(a), math.sqrt(1-a)))

def verify_hmac_signature(raw_body: bytes, header_signature: str | None, secret: str) -> bool:
    if not header_signature or not secret:
        return False
    mac = hmac.new(secret.encode("utf-8"), msg=raw_body, digestmod=hashlib.sha256).hexdigest()
    # header may be "sha256=..." or raw hex
    provided = header_signature.split("=", 1)[-1].lower()
    return hmac.compare_digest(mac, provided)
