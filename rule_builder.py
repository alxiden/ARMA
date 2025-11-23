from xml.sax.saxutils import escape


def build_wazuh_rule(vals: dict) -> str:
    """Build a simple Wazuh-style XML rule from a values dict.

    This mirrors the previous logic embedded in `main.py`.
    """
    esc = lambda s: escape(str(s))

    rule_id = esc(vals.get('id') or '100000')
    level = esc(vals.get('level') or '3')
    description = esc(vals.get('description') or '')
    program = esc(vals.get('program_name') or '')
    mitre = esc(vals.get('mitre') or '')

    parts = []
    parts.append(f'<group name="custom_rules">')
    parts.append(f'  <rule id="{rule_id}" level="{level}">')
    if description:
        parts.append(f'    <description>{description}</description>')
    if program:
        parts.append(f'    <field name="program_name">{program}</field>')
    if mitre:
        parts.append(f'    <mitre>{mitre}</mitre>')

    # Networking conditions
    proto = vals.get('protocol')
    src = vals.get('src_ip')
    dst = vals.get('dst_ip')
    port = vals.get('port')
    if proto or src or dst or port:
        parts.append('    <!-- Networking conditions -->')
        if proto:
            parts.append(f'    <protocol>{esc(proto)}</protocol>')
        if src:
            parts.append(f'    <src_ip>{esc(src)}</src_ip>')
        if dst:
            parts.append(f'    <dst_ip>{esc(dst)}</dst_ip>')
        if port:
            parts.append(f'    <port>{esc(port)}</port>')

    # Hash conditions
    htype = vals.get('hash_type')
    hval = vals.get('hash_value')
    fpath = vals.get('file_path')
    if htype or hval or fpath:
        parts.append('    <!-- Hash conditions -->')
        if htype:
            parts.append(f'    <hash_type>{esc(htype)}</hash_type>')
        if hval:
            parts.append(f'    <hash_value>{esc(hval)}</hash_value>')
        if fpath:
            parts.append(f'    <file_path>{esc(fpath)}</file_path>')

    # Behaviour
    btype = vals.get('behavior_type')
    proc = vals.get('process_name')
    cmd = vals.get('command_line')
    persistence = vals.get('persistence')
    if btype or proc or cmd or persistence:
        parts.append('    <!-- Behaviour conditions -->')
        if btype:
            parts.append(f'    <behavior_type>{esc(btype)}</behavior_type>')
        if proc:
            parts.append(f'    <process_name>{esc(proc)}</process_name>')
        if cmd:
            parts.append(f'    <command_line>{esc(cmd)}</command_line>')
        parts.append(f'    <persistence>{esc(persistence)}</persistence>')

    parts.append('  </rule>')
    parts.append('</group>')

    return '\n'.join(parts)


def build_elastic_rule(vals: dict) -> str:
    """Build a minimal Elastic detection rule (JSON string).

    This is a minimal approximate format suitable for copy/paste or further editing.
    """
    import json

    rule = {
        'name': vals.get('description') or vals.get('program_name') or f"rule-{vals.get('id','')}",
        'description': vals.get('description',''),
        'risk_score': int(vals.get('level') or 50),
        'severity': 'medium',
        'index': ['logs-*'],
        'query': '',
    }

    # Build a simple query from available fields
    clauses = []
    if vals.get('program_name'):
        clauses.append(f"process.name: {vals.get('program_name')}")
    if vals.get('src_ip'):
        clauses.append(f"source.ip: {vals.get('src_ip')}")
    if vals.get('dst_ip'):
        clauses.append(f"destination.ip: {vals.get('dst_ip')}")
    if vals.get('hash_value'):
        clauses.append(f"file.hash.md5: {vals.get('hash_value')}")

    if clauses:
        rule['query'] = ' AND '.join(clauses)
    else:
        rule['query'] = 'true'

    return json.dumps(rule, indent=2)


def build_splunk_rule(vals: dict) -> str:
    """Build a simple Splunk savedsearch definition (SPL string) to be adapted by the user."""
    parts = []
    base_index = 'index=*'
    parts.append(base_index)
    if vals.get('program_name'):
        parts.append(f'process={vals.get("program_name")}')
    if vals.get('src_ip'):
        parts.append(f'src_ip={vals.get("src_ip")}')
    if vals.get('dst_ip'):
        parts.append(f'dst_ip={vals.get("dst_ip")}')
    if vals.get('hash_value'):
        parts.append(f'file_hash={vals.get("hash_value")}')

    spl = ' | search ' + ' '.join(parts[1:]) if len(parts) > 1 else ' | stats count by host'
    header = f"-- Splunk saved search: {vals.get('description') or vals.get('program_name') or 'rule'}\n"
    return header + spl


def build_rules_for_selected(vals: dict) -> dict:
    """Return a dict of {tool_name: rule_string} for selected tools in vals.

    Expects boolean flags in vals: `siem_wazuh`, `siem_elastic`, `siem_splunk`.
    """
    outputs = {}
    if vals.get('siem_wazuh'):
        outputs['Wazuh'] = build_wazuh_rule(vals)
    if vals.get('siem_elastic'):
        outputs['Elastic'] = build_elastic_rule(vals)
    if vals.get('siem_splunk'):
        outputs['Splunk'] = build_splunk_rule(vals)
    return outputs
