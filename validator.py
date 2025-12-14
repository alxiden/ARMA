import re
from typing import Tuple, List


def validate_rule_name(value: str) -> Tuple[bool, str]:
    if not value:
        return False, "Rule name is required."
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        return False, "Rule name must start with a letter/underscore and contain only letters, digits, and underscores."
    return True, ""


def validate_tags(value: str) -> Tuple[bool, str]:
    if not value:
        return True, ""
    tags = value.replace(",", " ").split()
    for t in tags:
        if not re.fullmatch(r"[A-Za-z0-9_+-]+", t):
            return False, f"Invalid tag: {t}"
    return True, ""


def validate_strings(strings: list) -> Tuple[bool, str]:
    if not strings:
        return False, "At least one string is required."

    for idx, s in enumerate(strings, start=1):
        sid = s.get("id", "").strip()
        stype = s.get("type", "").strip()
        sval = s.get("value", "").strip()

        if not sid:
            return False, f"String {idx}: Identifier is required."
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", sid):
            return False, f"String {idx}: Identifier must be letters, digits, underscores and not start with a digit."
        if stype not in {"text", "regex", "hex"}:
            return False, f"String {idx}: Type must be text, regex, or hex."
        if not sval:
            return False, f"String {idx}: Value is required."

        if stype == "hex":
            if not re.fullmatch(r"[0-9A-Fa-f\s]+", sval):
                return False, f"String {idx}: Hex value may only contain 0-9 A-F and spaces."

    return True, ""


def validate_condition(value: str, strings: list) -> Tuple[bool, str]:
    if not value:
        return False, "Condition is required (e.g., any of them)."

    # Simple sanity check: ensure referenced identifiers exist when they look like $id
    ids = {s.get("id") for s in strings}
    referenced = set(re.findall(r"\$([A-Za-z_][A-Za-z0-9_]*)", value))
    missing = referenced - ids
    if missing:
        return False, f"Condition references undefined strings: {', '.join(sorted(missing))}"

    return True, ""


def validate_all(vals: dict) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    ok, msg = validate_rule_name(vals.get("rule_name", ""))
    if not ok:
        errors.append(msg)

    ok, msg = validate_tags(vals.get("tags", ""))
    if not ok:
        errors.append(msg)

    strings = vals.get("strings", [])
    ok, msg = validate_strings(strings)
    if not ok:
        errors.append(msg)

    ok, msg = validate_condition(vals.get("condition", ""), strings)
    if not ok:
        errors.append(msg)

    return (len(errors) == 0), errors
