from xml.sax.saxutils import escape


def _quote(val: str) -> str:
    # YARA needs backslashes and quotes escaped inside string literals.
    return escape(val.replace("\\", "\\\\").replace('"', '\\"'))


def _format_string(identifier: str, stype: str, value: str) -> str:
    if stype == "text":
        return f"    ${identifier} = \"{_quote(value)}\""
    if stype == "regex":
        return f"    ${identifier} = /{value}/"
    # hex
    normalized = " ".join(value.upper().split())
    return f"    ${identifier} = {{ {normalized} }}"


def build_yara_rule(vals: dict) -> str:
    name = vals.get("rule_name", "rule_name").strip()
    tags_raw = vals.get("tags", "") or ""
    tags = " ".join(t for t in tags_raw.replace(",", " ").split() if t)

    meta = []
    if vals.get("author"):
        meta.append(f"    author = \"{_quote(vals['author'])}\"")
    if vals.get("description"):
        meta.append(f"    description = \"{_quote(vals['description'])}\"")
    if vals.get("reference"):
        meta.append(f"    reference = \"{_quote(vals['reference'])}\"")

    strings_section = []
    for s in vals.get("strings", []):
        strings_section.append(_format_string(s["id"], s["type"], s["value"]))

    condition = vals.get("condition") or "any of them"

    lines = []
    if tags:
        lines.append(f"rule {name} : {tags} {{")
    else:
        lines.append(f"rule {name} {{")

    if meta:
        lines.append("  meta:")
        lines.extend(meta)

    lines.append("  strings:")
    lines.extend(strings_section)

    lines.append("  condition:")
    lines.append(f"    {condition}")
    lines.append("}")

    return "\n".join(lines)

