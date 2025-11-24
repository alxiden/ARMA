from xml.sax.saxutils import escape


def build_wazuh_rule(vals: dict) -> str:
    esc = lambda s: escape(str(s))

    rule_id = esc(vals.get('id') or '100001')
    level = esc(vals.get('level') or '3')
    description = esc(vals.get('description') or '')
    program = esc(vals.get('program_name') or '')
    mitre = esc(vals.get('mitre') or '')

    wazuh_fields = ['user', 'srcip', 'dstip', 'srcport', 'dstport', 'protocol', 'url', 'http_method', 'user_agent', 'domain']

    parts = []
    parts.append('<group name="custom_rules">')
    parts.append(f'  <rule id="{rule_id}" level="{level}">')

    if description:
        parts.append(f'    <description>{description}</description>')
    if mitre:
        parts.append(f'    <mitre>{mitre}</mitre>')
    if program:
        parts.append(f'    <field name="program_name">{program}</field>')

    # Conditions: map UI keys to Wazuh field names when possible, otherwise emit <match>
    ui_to_wazuh = {
        'src_ip': 'srcip',
        'dst_ip': 'dstip',
        'hostname': 'domain',
        'port': 'dstport',
        'protocol': 'protocol',
        'http_path': 'url',
        'http_method': 'http_method',
        'user_agent': 'user_agent',
        'hash_type': 'hash_type',
        'hash_value': 'hash',
        'file_path': 'filepath',
        'behavior_type': 'behavior',
        'process_name': 'process',
        'command_line': 'command',
        'persistence': 'persistence',
    }

    keys = list(ui_to_wazuh.keys())

    for key in keys:
        val = vals.get(key)
        if val is None:
            continue
        if isinstance(val, str) and not val.strip():
            continue

        field_name = ui_to_wazuh.get(key)
        parts.append(f'    <!-- {key} -->')

        # If the mapped field name is a known Wazuh field, emit a <field name="..."> tag.
        if field_name and field_name in wazuh_fields:
            parts.append(f'    <field name="{field_name}">{esc(val)}</field>')
        else:
            # Fallback to a generic match clause
            parts.append(f'    <match>{esc(val)}</match>')

    parts.append('  </rule>')
    parts.append('</group>')

    return "\n".join(parts)

