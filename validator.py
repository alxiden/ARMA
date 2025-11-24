import re
import ipaddress
from typing import Tuple, List


def _is_int_in_range(value: str, min_v: int, max_v: int) -> bool:
    try:
        iv = int(value)
        return min_v <= iv <= max_v
    except Exception:
        return False


def validate_id(value: str) -> Tuple[bool, str]:
    if not value:
        return False, "Rule ID is required."
    if not re.fullmatch(r"\d+", value):
        return False, "Rule ID must be a positive integer."
    return True, ""


def validate_level(value: str) -> Tuple[bool, str]:
    if not value:
        return False, "Level is required."
    if not _is_int_in_range(value, 0, 10):
        return False, "Level must be an integer between 0 and 10."
    return True, ""


def validate_ip(value: str) -> Tuple[bool, str]:
    if not value:
        return True, ""  # optional
    try:
        # Accept single IP or CIDR
        try:
            ipaddress.ip_address(value)
        except ValueError:
            ipaddress.ip_network(value, strict=False)
        return True, ""
    except Exception:
        return False, f"Invalid IP or network: {value}"


def validate_port(value: str) -> Tuple[bool, str]:
    if not value:
        return True, ""  # optional
    if not _is_int_in_range(value, 1, 65535):
        return False, "Port must be an integer between 1 and 65535."
    return True, ""


def validate_hash(hash_type: str, hash_value: str) -> Tuple[bool, str]:
    if not hash_value and not hash_type:
        return True, ""
    if hash_type and not hash_value:
        return False, "Hash value is required when a hash type is selected."
    if hash_value and not hash_type:
        return False, "Hash type is required when a hash value is provided."

    hv = hash_value.strip().lower()
    if hash_type == "MD5":
        ok = bool(re.fullmatch(r"[0-9a-f]{32}", hv))
        msg = "MD5 must be 32 hex characters."
    elif hash_type == "SHA1":
        ok = bool(re.fullmatch(r"[0-9a-f]{40}", hv))
        msg = "SHA1 must be 40 hex characters."
    elif hash_type == "SHA256":
        ok = bool(re.fullmatch(r"[0-9a-f]{64}", hv))
        msg = "SHA256 must be 64 hex characters."
    else:
        return False, f"Unknown hash type: {hash_type}"

    if not ok:
        return False, msg
    return True, ""


def validate_mitre(value: str) -> Tuple[bool, str]:
    if not value:
        return True, ""
    parts = [p.strip() for p in value.split(',') if p.strip()]
    for p in parts:
        if not re.fullmatch(r"T\d{4}(?:\.\d+)?", p):
            return False, f"MITRE ID '{p}' is not valid (expected T#### or T####.x)."
    return True, ""


def validate_domain(value: str) -> Tuple[bool, str]:
    if not value:
        return True, ""
    # simple domain regex (allows subdomains)
    if re.fullmatch(r"(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[A-Za-z]{2,}", value):
        return True, ""
    return False, f"Invalid domain: {value}"


def validate_http_method(value: str) -> Tuple[bool, str]:
    if not value:
        return True, ""
    allowed = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"}
    if value.upper() in allowed:
        return True, ""
    return False, f"HTTP method must be one of: {', '.join(sorted(allowed))}"


def validate_all(vals: dict) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    ok, msg = validate_id(vals.get('id', ''))
    if not ok:
        errors.append(msg)

    ok, msg = validate_level(vals.get('level', ''))
    if not ok:
        errors.append(msg)

    ok, msg = validate_ip(vals.get('src_ip', ''))
    if not ok:
        errors.append(f"Source IP: {msg}")

    ok, msg = validate_ip(vals.get('dst_ip', ''))
    if not ok:
        errors.append(f"Destination IP: {msg}")

    ok, msg = validate_port(vals.get('port', ''))
    if not ok:
        errors.append(msg)

    ok, msg = validate_hash(vals.get('hash_type', ''), vals.get('hash_value', ''))
    if not ok:
        errors.append(msg)

    ok, msg = validate_mitre(vals.get('mitre', ''))
    if not ok:
        errors.append(msg)

    # New networking-related validations
    ok, msg = validate_domain(vals.get('domain', ''))
    if not ok:
        errors.append(msg)

    ok, msg = validate_http_method(vals.get('http_method', ''))
    if not ok:
        errors.append(msg)

    return (len(errors) == 0), errors
