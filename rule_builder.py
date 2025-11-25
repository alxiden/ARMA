from xml.sax.saxutils import escape


def build_wazuh_rule(vals: dict) -> str:
    esc = lambda s: escape(str(s))

    rule_id = esc(vals.get('id') or '100001')
    level = esc(vals.get('level') or '3')
    description = esc(vals.get('description') or '')
    program = esc(vals.get('program_name') or '')
    mitre = esc(vals.get('mitre') or '')

    parts = []
    parts.append('<group name="custom_rules">')
    parts.append(f'  <rule id="{rule_id}" level="{level}">')

    if description:
        parts.append(f'    <description>{description}</description>')
    if mitre:
        parts.append(f'    <mitre>{mitre}</mitre>')
    if program:
        parts.append(f'    <field name="program_name">{program}</field>')

    # Emit <match> for every non-meta UI field. This simplifies Wazuh compatibility.
    meta_keys = {'id', 'level', 'description', 'mitre', 'program_name'}

    for key, val in vals.items():
        if key in meta_keys:
            continue
        if val is None:
            continue
        if isinstance(val, str) and not val.strip():
            continue

        parts.append(f'    <!-- {key} -->')
        parts.append(f'    <match>{esc(val)}</match>')

    parts.append('  </rule>')
    parts.append('</group>')

    return "\n".join(parts)

