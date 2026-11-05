#!/usr/bin/env python3
"""Generate src/components/IgorArchitecture.astro — the interactive Igor diagram.

Run from the repo root:   python3 scripts/gen-igor-diagram.py
Then commit both this script and the generated component.

Everything that is tuned lives in the CONFIG section. Facts come from the
verified source review of 5 Nov 2026 (shared-context/handoffs/2026-11-05-igor-failure-facts.md).
Layout "A" puts external services in their own column; "B" keeps them inside
the bands with an EXTERNAL tag. The site uses A.
"""
import os
import sys
from html import escape

# ---------------------------------------------------------------- CONFIG ----

LAYOUT = "A"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "src", "components", "IgorArchitecture.astro")

FLOWS = {
    # key: (button label, description)
    "req": ("request", "messages & API calls"),
    "data": ("data", "storage & budget"),
    "mon": ("monitoring", "scheduled work & heartbeat"),
    "run": ("runtime", "service supervision"),
}

# Icons: 18x18 line drawings, no brand logos.
ICONS = {
    "phone": '<rect x="4" y="0" width="10" height="18" rx="2"/><line x1="8" y1="15" x2="10" y2="15"/>',
    "chat": '<path d="M2,3 h10 a1.5,1.5 0 0 1 1.5,1.5 v6 a1.5,1.5 0 0 1 -1.5,1.5 h-5 l-4,3 v-3 h-1 a1.5,1.5 0 0 1 -1.5,-1.5 v-6 a1.5,1.5 0 0 1 1.5,-1.5 z"/><path d="M15,7 h1.5 a1.5,1.5 0 0 1 1.5,1.5 v5 a1.5,1.5 0 0 1 -1.5,1.5 h-0.5 v2.5 l-3,-2.5 h-3"/>',
    "siri": '<line x1="2" y1="7.5" x2="2" y2="10.5"/><line x1="5.5" y1="5" x2="5.5" y2="13"/><line x1="9" y1="2" x2="9" y2="16"/><line x1="12.5" y1="5" x2="12.5" y2="13"/><line x1="16" y1="7.5" x2="16" y2="10.5"/>',
    "shield": '<path d="M9,1 L16,4 V9 C16,13 13,16 9,17.5 C5,16 2,13 2,9 V4 z"/><path d="M5.5,9.5 L8,12 L12.5,7"/>',
    "restart": '<path d="M15.5,7 A7,7 0 0 0 3,5"/><path d="M2.5,11 A7,7 0 0 0 15,13"/><path d="M3,1.5 V5.5 H7"/><path d="M15,16.5 V12.5 H11"/>',
    "robot": '<rect x="2" y="5" width="14" height="11" rx="3"/><line x1="9" y1="5" x2="9" y2="2"/><circle cx="9" cy="1.5" r="1"/><circle cx="6.5" cy="10" r="1.2"/><circle cx="11.5" cy="10" r="1.2"/><line x1="7" y1="13.3" x2="11" y2="13.3"/>',
    "sparkle": '<path d="M9,1 C9.6,6 12,8.4 17,9 C12,9.6 9.6,12 9,17 C8.4,12 6,9.6 1,9 C6,8.4 8.4,6 9,1 z"/>',
    "db": '<ellipse cx="9" cy="3" rx="8" ry="3"/><path d="M1,3 v12 a8,3 0 0 0 16,0 v-12"/><path d="M1,9 a8,3 0 0 0 16,0"/>',
    "wallet": '<path d="M2,5 H14 a2,2 0 0 1 2,2 V15 a2,2 0 0 1 -2,2 H4 a2,2 0 0 1 -2,-2 z"/><path d="M2,5 L12,1.5 L13.5,5"/><path d="M16,9 H12 a1.8,1.8 0 0 0 0,3.6 H16"/><circle cx="12.6" cy="10.8" r=".6"/>',
    "calendar": '<rect x="1.5" y="3" width="15" height="14" rx="2"/><line x1="1.5" y1="7" x2="16.5" y2="7"/><line x1="5.5" y1="1" x2="5.5" y2="4.5"/><line x1="12.5" y1="1" x2="12.5" y2="4.5"/><path d="M6,12 L8.2,14 L12,10"/>',
    "pulse": '<path d="M0,10 h4 l2,-6 l4,12 l2,-6 h6"/>',
}

# Node definitions. "flows" = which SOLO groups light this module.
NODES = [
    {"id": "me", "title": "Me, on my phone", "short": "Me · phone", "sub": "owner-only chat", "icon": "phone",
     "flow": "req", "flows": ["req"], "external": False, "zone": "Access",
     "info": "Only my own Telegram account can talk to Igor."},
    {"id": "tg", "title": "Telegram Bot API", "short": "Telegram API", "sub": "messages in and out", "msub": "messages in / out", "icon": "chat",
     "flow": "req", "flows": ["req"], "external": True, "zone": "Access",
     "info": "Telegram's Bot API carries my messages in and Igor's replies out."},
    {"id": "siri", "title": "Siri endpoint", "short": "Siri endpoint", "sub": "voice requests", "icon": "siri",
     "flow": "req", "flows": ["req"], "external": False, "zone": "Access",
     "info": "Voice requests by Siri. If Igor is slow, Siri gets an apology and the answer follows in Telegram."},
    {"id": "ts", "title": "Tailscale", "short": "Tailscale", "sub": "remote admin", "icon": "shield",
     "flow": "run", "flows": ["run"], "external": False, "zone": "Access",
     "info": "I administer the home server remotely over Tailscale, a private network."},
    {"id": "sysd", "title": "systemd", "short": "systemd", "sub": "runs the service", "icon": "restart",
     "flow": "run", "flows": ["run"], "external": False, "zone": "Runtime & Data",
     "info": "systemd runs Igor as a service. The checked-in unit restarts it 10 seconds after a crash; that is configuration, not a guarantee."},
    {"id": "igor", "title": "Igor service", "short": "Igor service", "sub": "Python · python-telegram-bot", "msub": "Python bot", "icon": "robot",
     "flow": "req", "flows": ["req", "data", "mon", "run"], "external": False, "zone": "Runtime & Data",
     "info": "The Igor service: Python with python-telegram-bot. Chat, memory, tasks and reminders."},
    {"id": "claude", "title": "Claude API", "short": "Claude API", "sub": "Anthropic SDK", "icon": "sparkle",
     "flow": "req", "flows": ["req", "data"], "external": True, "zone": "Runtime & Data",
     "info": "Igor calls the Claude API through the Anthropic SDK, with up to two automatic retries on retryable errors."},
    {"id": "db", "title": "SQLite", "short": "SQLite", "sub": "memory · tasks", "icon": "db",
     "flow": "data", "flows": ["data"], "external": False, "zone": "Runtime & Data",
     "info": "SQLite stores memory, tasks, reminders and status."},
    {"id": "cap", "title": "Spend cap", "short": "Spend cap", "sub": "monthly limit", "icon": "wallet",
     "flow": "data", "flows": ["data"], "external": False, "zone": "Runtime & Data",
     "info": "A monthly AI spend cap, checked when a conversation starts (not before every single call)."},
    {"id": "sched", "title": "Scheduler", "short": "Scheduler", "sub": "reminders · morning brief", "msub": "reminders · brief", "icon": "calendar",
     "flow": "mon", "flows": ["mon"], "external": False, "zone": "Monitoring",
     "info": "Runs reminders and the daily morning brief, and sends the heartbeat."},
    {"id": "hc", "title": "healthchecks.io", "short": "healthchecks", "sub": "outside monitor", "icon": "pulse",
     "flow": "mon", "flows": ["mon"], "external": True, "zone": "Monitoring",
     "info": "An outside monitor. If the heartbeat stops arriving, it notices."},
]

# Edges: (from, to, flow, label). Paths are hand-routed per layout below (90° only).
EDGES = [
    ("me", "tg", "req", "chat"),
    ("tg", "igor", "req", "messages"),
    ("siri", "igor", "req", "voice"),
    ("sysd", "igor", "run", "runs"),
    ("igor", "claude", "req", "requests"),
    ("igor", "db", "data", ""),
    ("cap", "claude", "data", "cap checked at chat start"),
    ("sched", "igor", "mon", "reminders · brief"),
    ("sched", "hc", "mon", "heartbeat"),
]

# Fault cards: (module id, title, body). Wording follows the verified facts file.
FAULTS = [
    ("sysd", "Igor crashes", "The checked-in systemd unit restarts it after 10 s. That is configuration, not a promise of recovery time."),
    ("claude", "Claude API error", "Up to two SDK retries, then a plain-language reply instead of a crash."),
    ("cap", "Monthly cap reached", "At conversation start Igor answers with a 'Budget cap reached' message instead of a reply. Not a per-call check."),
    ("hc", "Heartbeat fails", "Logged and shown as an error in /status. A missed heartbeat is what healthchecks.io watches for; alert delivery is not shown here."),
    ("siri", "Siri too slow", "Siri gets an apology now; the answer follows in Telegram."),
]

ONE_SENTENCE = ("Igor is a Telegram assistant I run on a home Linux server: owner-only access, remote admin over "
                "Tailscale, memory in SQLite, Claude API calls under a monthly spend cap, and a heartbeat to "
                "healthchecks.io so I know if it stops.")

# Desktop geometry per layout: box = (x, y, w, h). Bands = (label, x, y, w, h).
if LAYOUT == "A":
    VIEW_W, VIEW_H = 1000, 640
    BANDS = [
        ("ACCESS", 20, 30, 700, 140),
        ("RUNTIME & DATA · HOME LENOVO (XUBUNTU)", 20, 190, 700, 250),
        ("MONITORING", 20, 460, 700, 140),
        ("EXTERNAL SERVICES", 745, 30, 235, 570),
    ]
    BOX = {
        "ts": (45, 70, 190, 70),
        "siri": (255, 70, 210, 70),
        "me": (485, 70, 210, 70),
        "tg": (760, 70, 205, 70),
        "sysd": (40, 230, 190, 70),
        "igor": (280, 225, 300, 80),
        "claude": (760, 230, 205, 70),
        "db": (280, 345, 150, 70),
        "cap": (450, 345, 200, 70),
        "sched": (280, 500, 300, 70),
        "hc": (760, 500, 205, 70),
    }
    # path, label anchor (x, y of label centre)
    PATHS = {
        ("me", "tg"): ("M695,105 L760,105", (727, 92)),
        ("tg", "igor"): ("M862,140 L862,185 L530,185 L530,225", (700, 172)),
        ("siri", "igor"): ("M360,140 L360,225", (392, 182)),
        ("sysd", "igor"): ("M230,265 L280,265", (255, 252)),
        ("igor", "claude"): ("M580,265 L760,265", (670, 252)),
        ("igor", "db"): ("M355,305 L355,345", None),
        ("cap", "claude"): ("M650,380 L862,380 L862,300", (756, 367)),
        ("sched", "igor"): ("M280,535 L252,535 L252,290 L280,290", (252, 330)),
        ("sched", "hc"): ("M580,535 L760,535", (670, 522)),
    }
else:
    VIEW_W, VIEW_H = 1000, 640
    BANDS = [
        ("ACCESS", 20, 30, 960, 140),
        ("RUNTIME & DATA · HOME LENOVO (XUBUNTU)", 20, 190, 960, 250),
        ("MONITORING", 20, 460, 960, 140),
    ]
    BOX = {
        "me": (45, 70, 222, 70),
        "tg": (284, 70, 236, 70),
        "siri": (537, 70, 205, 70),
        "ts": (759, 70, 196, 70),
        "sysd": (45, 230, 210, 70),
        "igor": (335, 225, 300, 80),
        "claude": (750, 230, 205, 70),
        "db": (335, 345, 152, 70),
        "cap": (503, 345, 177, 70),
        "sched": (335, 500, 300, 70),
        "hc": (750, 500, 205, 70),
    }
    PATHS = {
        ("me", "tg"): ("M267,105 L284,105", None),
        ("tg", "igor"): ("M385,140 L385,182 L430,182 L430,225", (340, 182)),
        ("siri", "igor"): ("M620,140 L620,182 L580,182 L580,225", (650, 168)),
        ("sysd", "igor"): ("M255,265 L335,265", (294, 252)),
        ("igor", "claude"): ("M635,265 L750,265", (692, 252)),
        ("igor", "db"): ("M405,305 L405,345", None),
        ("cap", "claude"): ("M680,380 L852,380 L852,300", (766, 367)),
        ("sched", "igor"): ("M335,535 L300,535 L300,290 L335,290", (300, 330)),
        ("sched", "hc"): ("M635,535 L750,535", (692, 522)),
    }

# Mobile geometry: two columns, boxes 164x66, same for both layouts.
MOB_W = 380
MOB_BOX_W = 164
MOB_BOX_H = 66
MOB_COL_X = [20, 192]

# --------------------------------------------------------------- HELPERS ----

TITLE_PX = 17
SUB_PX = 13.5
LABEL_PX = 13
ICON_SIZE = 18
ICON_SCALE = 1.1111
ICON_GAP = 8


def text_width(text, px, bold=False):
    """Rough width of an Inter string. Good enough to centre icon + title."""
    factor = 0.58
    if bold:
        factor = 0.56
    return len(text) * px * factor


def node_by_id(node_id):
    for node in NODES:
        if node["id"] == node_id:
            return node
    raise KeyError(node_id)


def flow_classes(node):
    classes = ["mod", "m-" + node["flow"]]
    for f in node["flows"]:
        classes.append("in-" + f)
    if node["external"]:
        classes.append("ext")
    return " ".join(classes)


def module_svg(node, x, y, w, h, title_px, sub_px, icon_scale, title_key, mobile):
    """One mixer-desk module: panel, colour strip, outline, LED, icon + title, subtitle."""
    cx = x + w / 2
    title = node[title_key]
    sub_text = node["sub"]
    if mobile and "msub" in node:
        sub_text = node["msub"]
    title_w = text_width(title, title_px, bold=True)
    icon_w = ICON_SIZE * icon_scale
    line_w = icon_w + ICON_GAP + title_w
    icon_x = cx - line_w / 2
    if icon_x < x + 18:
        icon_x = x + 18
    title_x = icon_x + icon_w + ICON_GAP
    title_y = y + 34
    if mobile:
        title_y = y + 30
    sub_y = title_y + 20
    icon_y = title_y - 16
    led_x = x + w - 12
    led_y = y + 12
    tag = ""
    if node["external"] and LAYOUT == "B":
        tag = f'<text class="tag" x="{x + w - 22:.0f}" y="{y + 16:.0f}">EXTERNAL</text>'
    parts = [
        f'<g class="{flow_classes(node)}" tabindex="0" role="button" data-id="{node["id"]}" aria-label="{escape(title)}; {escape(node["sub"])}">',
        f'<rect class="panel" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>',
        f'<rect class="strip" x="{x + 7}" y="{y + 12}" width="3" height="{h - 24}" rx="1.5"/>',
        f'<rect class="po" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>',
        f'<circle class="led" cx="{led_x}" cy="{led_y}" r="3.5"/>',
        f'<text class="fault-badge" x="{led_x}" y="{led_y + 4}">!</text>',
        f'<g transform="translate({icon_x:.1f},{icon_y:.1f}) scale({icon_scale})">'
        f'<g class="ic" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[node["icon"]]}</g></g>',
        f'<text class="t" x="{title_x:.1f}" y="{title_y}" style="font-size:{title_px}px">{escape(title)}</text>',
        f'<text class="s" x="{cx:.1f}" y="{sub_y}" style="font-size:{sub_px}px">{escape(sub_text)}</text>',
        tag,
        '</g>',
    ]
    return "".join(parts)


def cable_svg(flow, path, label, anchor):
    parts = [f'<g class="cable k-{flow}">',
             f'<path class="cb" d="{path}" marker-end="url(#ah-{flow})"/>',
             f'<path class="pulse" d="{path}"/>']
    if label and anchor:
        lw = text_width(label, LABEL_PX) + 12
        lx, ly = anchor
        parts.append(f'<rect class="lbg" x="{lx - lw / 2:.1f}" y="{ly - 14}" width="{lw:.1f}" height="19" rx="3"/>')
        parts.append(f'<text class="lt" x="{lx}" y="{ly}">{escape(label)}</text>')
    parts.append('</g>')
    return "".join(parts)


def band_svg(label, x, y, w, h):
    parts = [f'<rect class="band" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>']
    for sx, sy in ((x + 10, y + 10), (x + 10, y + h - 10), (x + w - 10, y + 10), (x + w - 10, y + h - 10)):
        parts.append(f'<circle class="screw" cx="{sx}" cy="{sy}" r="3.5"/>')
    parts.append(f'<text class="bandl" x="{x + 24}" y="{y + 24}">{escape(label)}</text>')
    return "".join(parts)


def markers_svg():
    parts = ['<defs>']
    for flow in FLOWS:
        parts.append(f'<marker id="ah-{flow}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto">'
                     f'<path class="ah ah-{flow}" d="M0,0 L10,5 L0,10 z"/></marker>')
    parts.append('</defs>')
    return "".join(parts)


def desktop_svg():
    parts = [f'<svg class="sf" viewBox="0 0 {VIEW_W} {VIEW_H}" xmlns="http://www.w3.org/2000/svg" role="group" aria-label="Igor architecture as a signal-flow diagram">',
             markers_svg(),
             f'<rect class="bg" width="{VIEW_W}" height="{VIEW_H}"/>']
    for band in BANDS:
        parts.append(band_svg(*band))
    for src, dst, flow, label in EDGES:
        path, anchor = PATHS[(src, dst)]
        parts.append(cable_svg(flow, path, label, anchor))
    for node in NODES:
        x, y, w, h = BOX[node["id"]]
        parts.append(module_svg(node, x, y, w, h, TITLE_PX, SUB_PX, ICON_SCALE, "title", mobile=False))
    parts.append('</svg>')
    return "".join(parts)


def mobile_svg():
    """Boxes only, two per row, grouped by zone. Connections are listed below the diagram on mobile."""
    zones = ["Access", "Runtime & Data", "Monitoring"]
    y = 14
    parts = []
    body = []
    for zone in zones:
        zone_nodes = [n for n in NODES if n["zone"] == zone]
        rows = (len(zone_nodes) + 1) // 2
        band_h = 34 + rows * (MOB_BOX_H + 12)
        body.append(band_svg(zone.upper(), 8, y, MOB_W - 16, band_h))
        for i, node in enumerate(zone_nodes):
            bx = MOB_COL_X[i % 2]
            by = y + 34 + (i // 2) * (MOB_BOX_H + 12)
            body.append(module_svg(node, bx, by, MOB_BOX_W, MOB_BOX_H, 15, 12.5, 0.944, "short", mobile=True))
        y += band_h + 14
    total_h = y
    parts.append(f'<svg class="sf" viewBox="0 0 {MOB_W} {total_h}" xmlns="http://www.w3.org/2000/svg" role="group" aria-label="Igor architecture, mobile">')
    parts.append(markers_svg())
    parts.append(f'<rect class="bg" width="{MOB_W}" height="{total_h}"/>')
    parts.extend(body)
    parts.append('</svg>')
    return "".join(parts)


def routes_html():
    """Connection list for small screens, grouped by flow."""
    parts = ['<div class="routes" aria-label="Connections">']
    for flow, (name, desc) in FLOWS.items():
        flow_edges = [e for e in EDGES if e[2] == flow]
        if not flow_edges:
            continue
        parts.append(f'<section class="track k-{flow}"><h4>{escape(name)} <span>{escape(desc)}</span></h4>')
        for src, dst, _, label in flow_edges:
            a = node_by_id(src)
            b = node_by_id(dst)
            lab = label
            if not lab:
                lab = "stores"
            parts.append(f'<div class="route"><button class="ep" data-id="{a["id"]}">{escape(a["short"])}</button>'
                         f'<span class="arrow" aria-hidden="true">→</span>'
                         f'<button class="ep" data-id="{b["id"]}">{escape(b["short"])}</button>'
                         f'<span class="rl">{escape(lab)}</span></div>')
        parts.append('</section>')
    parts.append('</div>')
    return "".join(parts)


def faults_html():
    parts = ['<div class="faults-list">']
    for node_id, title, body in FAULTS:
        node = node_by_id(node_id)
        parts.append(f'<article class="fault" data-id="{node_id}"><button class="fault-pick" data-id="{node_id}">'
                     f'<span class="fault-mod">{escape(node["title"])}</span><b>{escape(title)}</b><p>{escape(body)}</p></button></article>')
    parts.append('<p class="failnote">Failure behaviour is taken from Igor\'s source code (checked 5 Nov 2026). It describes expected behaviour, not a live incident.</p></div>')
    return "".join(parts)


def solo_buttons_html():
    parts = []
    for flow, (name, _) in FLOWS.items():
        parts.append(f'<button class="solob" data-k="{flow}" style="--c:var(--c-{flow})" aria-pressed="false">SOLO · {escape(name)}</button>')
    return "".join(parts)


FAULT_IDS = [f[0] for f in FAULTS]

CSS = """
.igor-arch{--ia-el:var(--color-bg-elevated,#141414);--ia-tx:var(--color-text,#e5e5e5);--ia-mu:var(--color-text-secondary,#a3a3a3);--ia-bd:var(--color-border,#262626);--ia-ac:var(--color-accent,#3b82f6);
--d-bg:#16161a;--d-band:#1b1b21;--d-bandline:#2c2c35;--d-screw:#3a3a44;--d-panel:#22222a;--d-pline:#3a3a46;--d-fg:#f4f1ea;--d-dim:#9b98a6;--d-off:#33333d;
--c-req:#ff6b4a;--c-data:#ffd23f;--c-mon:#3ec1d3;--c-run:#b28dff;--red:#ff4d4d;margin:1.5rem 0}
[data-theme="light"] .igor-arch{--d-bg:#efe9dd;--d-band:#f7f2e8;--d-bandline:#d8cfbd;--d-screw:#bfb5a2;--d-panel:#fffdf8;--d-pline:#cfc5b2;--d-fg:#2a2622;--d-dim:#7a7064;--d-off:#e2dacb;
--c-req:#e2502f;--c-data:#d9a400;--c-mon:#1a9fb1;--c-run:#8a63e0;--red:#d92d2d}
.igor-arch button{font:inherit;cursor:pointer}
.igor-arch .bar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.igor-arch .tabs{display:flex;gap:8px;flex-wrap:wrap}
.igor-arch .tab{border:1px solid var(--ia-bd);background:none;color:var(--ia-mu);border-radius:999px;padding:7px 14px;font-size:15px;min-height:36px}
.igor-arch .tab[aria-selected=true]{border-color:var(--ia-ac);color:var(--ia-tx)}
.igor-arch .pauseb{border:1px solid var(--ia-bd);background:var(--ia-el);color:var(--ia-tx);border-radius:999px;padding:6px 12px;font-size:13px;min-height:36px}
.igor-arch .frame{border:1px solid var(--ia-bd);border-radius:10px;overflow:hidden}
.igor-arch .frame svg{display:block;width:100%;height:auto}
.igor-arch .mob,.igor-arch .routes{display:none}
@media (max-width:700px){.igor-arch .desk{display:none}.igor-arch .mob,.igor-arch .routes{display:block}}
.igor-arch .sf text{font-family:inherit}
.igor-arch .sf .bg{fill:var(--d-bg)}.igor-arch .sf .band{fill:var(--d-band);stroke:var(--d-bandline)}.igor-arch .sf .screw{fill:var(--d-screw)}
.igor-arch .sf .bandl{fill:var(--d-dim);font-weight:700;font-size:13px;letter-spacing:2px}
.igor-arch .sf .cable .cb{fill:none;stroke-width:3;stroke-linecap:butt;stroke-linejoin:miter}
.igor-arch .ah-req{fill:var(--c-req)}.igor-arch .ah-data{fill:var(--c-data)}.igor-arch .ah-mon{fill:var(--c-mon)}.igor-arch .ah-run{fill:var(--c-run)}
.igor-arch .sf .cable .pulse{fill:none;stroke:#fff;stroke-opacity:.85;stroke-width:3;stroke-linecap:butt;stroke-dasharray:3 60;animation:igor-flow 2.4s linear infinite}
@keyframes igor-flow{to{stroke-dashoffset:-62}}
@media (prefers-reduced-motion:reduce){.igor-arch .sf .cable .pulse{animation:none;display:none}}
.igor-arch.paused .sf .cable .pulse{animation:none;display:none}
.igor-arch .sf .lbg{fill:var(--d-bg)}.igor-arch .sf .lt{font-weight:500;font-size:13px;text-anchor:middle}
.igor-arch .k-req .cb{stroke:var(--c-req)}.igor-arch .k-req .lt{fill:var(--c-req)}
.igor-arch .k-data .cb{stroke:var(--c-data)}.igor-arch .k-data .lt{fill:var(--c-data)}
.igor-arch .k-mon .cb{stroke:var(--c-mon)}.igor-arch .k-mon .lt{fill:var(--c-mon)}
.igor-arch .k-run .cb{stroke:var(--c-run)}.igor-arch .k-run .lt{fill:var(--c-run)}
.igor-arch .sf .mod{cursor:pointer;outline:none;color:var(--d-fg)}
.igor-arch .sf .panel{fill:var(--d-panel)}.igor-arch .sf .po{fill:none;stroke:var(--d-pline);stroke-width:1.5;transition:stroke .15s}
.igor-arch .sf .ext .po{stroke-dasharray:5 3}
.igor-arch .sf .t{fill:var(--d-fg);font-weight:700;text-anchor:start}.igor-arch .sf .s{fill:var(--d-dim);text-anchor:middle}
.igor-arch .sf .tag{fill:var(--d-dim);font-weight:700;font-size:9px;letter-spacing:1.5px;text-anchor:end}
.igor-arch .sf .ic{stroke:var(--d-fg)}
.igor-arch .sf .led{fill:var(--d-off);transition:fill .15s}
.igor-arch .sf .fault-badge{display:none;fill:var(--d-bg);font-weight:800;font-size:9px;text-anchor:middle}
.igor-arch .m-req .strip{fill:var(--c-req)}.igor-arch .m-data .strip{fill:var(--c-data)}.igor-arch .m-mon .strip{fill:var(--c-mon)}.igor-arch .m-run .strip{fill:var(--c-run)}
.igor-arch .sf .mod:hover .po,.igor-arch .sf .mod:focus-visible .po,.igor-arch .sf .mod.sel .po{stroke-width:2.5}
.igor-arch .m-req:hover .po,.igor-arch .m-req.sel .po,.igor-arch .m-req:focus-visible .po{stroke:var(--c-req)}.igor-arch .m-req:hover .led,.igor-arch .m-req.sel .led{fill:var(--c-req)}
.igor-arch .m-data:hover .po,.igor-arch .m-data.sel .po,.igor-arch .m-data:focus-visible .po{stroke:var(--c-data)}.igor-arch .m-data:hover .led,.igor-arch .m-data.sel .led{fill:var(--c-data)}
.igor-arch .m-mon:hover .po,.igor-arch .m-mon.sel .po,.igor-arch .m-mon:focus-visible .po{stroke:var(--c-mon)}.igor-arch .m-mon:hover .led,.igor-arch .m-mon.sel .led{fill:var(--c-mon)}
.igor-arch .m-run:hover .po,.igor-arch .m-run.sel .po,.igor-arch .m-run:focus-visible .po{stroke:var(--c-run)}.igor-arch .m-run:hover .led,.igor-arch .m-run.sel .led{fill:var(--c-run)}
.igor-arch.solo-req .cable:not(.k-req),.igor-arch.solo-data .cable:not(.k-data),.igor-arch.solo-mon .cable:not(.k-mon),.igor-arch.solo-run .cable:not(.k-run){opacity:.12}
.igor-arch.solo-req .mod:not(.in-req),.igor-arch.solo-data .mod:not(.in-data),.igor-arch.solo-mon .mod:not(.in-mon),.igor-arch.solo-run .mod:not(.in-run){opacity:.28}
.igor-arch.solo-req .in-req .led{fill:var(--c-req)}.igor-arch.solo-data .in-data .led{fill:var(--c-data)}.igor-arch.solo-mon .in-mon .led{fill:var(--c-mon)}.igor-arch.solo-run .in-run .led{fill:var(--c-run)}
.igor-arch.failing .sf .pulse{display:none}
.igor-arch.failing .sf .mod.has-fault .led{fill:var(--red);r:6}
.igor-arch.failing .sf .mod.has-fault .fault-badge{display:inline}
.igor-arch.failing .sf .mod.has-fault .po{stroke:var(--red)}
.igor-arch.failing .sf .mod:not(.has-fault){opacity:.45}
.igor-arch .solos{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.igor-arch .solob{border:1.5px solid var(--c);background:transparent;color:var(--ia-tx);border-radius:6px;padding:8px 12px;font-size:14px;font-weight:700;letter-spacing:.5px;min-height:40px}
.igor-arch .solob[aria-pressed=true]{background:var(--c);color:#111}
.igor-arch.failing .solos{display:none}
.igor-arch .info{margin-top:10px;padding:10px 14px;border:1px solid var(--ia-bd);border-left:3px solid var(--ia-ac);border-radius:6px;background:var(--ia-el);font-size:16px;min-height:46px}
.igor-arch .info b{color:var(--ia-ac)}
.igor-arch .talk{margin-top:12px;font-size:16px;color:var(--ia-mu);line-height:1.6}.igor-arch .talk b{color:var(--ia-tx)}
.igor-arch .faults-list{display:none;margin-top:10px}.igor-arch.failing .faults-list{display:block}
.igor-arch .fault{margin:0 0 8px}.igor-arch .fault-pick{width:100%;text-align:left;border:1px solid var(--ia-bd);border-left:3px solid var(--red);background:var(--ia-el);color:var(--ia-tx);border-radius:6px;padding:10px 14px}
.igor-arch .fault-pick .fault-mod{display:block;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--ia-mu)}
.igor-arch .fault-pick b{display:block;color:var(--red);font-size:16px;margin:2px 0}.igor-arch .fault-pick p{margin:0;font-size:15px;color:var(--ia-mu);line-height:1.5}
.igor-arch .fault.sel .fault-pick{border-color:var(--red)}
.igor-arch .failnote{font-size:12px;color:var(--ia-mu);margin-top:8px}
.igor-arch .routes{margin-top:12px}.igor-arch .routes h4{margin:12px 0 6px;font-size:13px;letter-spacing:1.5px;text-transform:uppercase}
.igor-arch .routes h4 span{font-weight:400;letter-spacing:0;text-transform:none;color:var(--ia-mu);margin-left:6px}
.igor-arch .track.k-req h4{color:var(--c-req)}.igor-arch .track.k-data h4{color:var(--c-data)}.igor-arch .track.k-mon h4{color:var(--c-mon)}.igor-arch .track.k-run h4{color:var(--c-run)}
.igor-arch .route{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:6px;margin-bottom:6px}
.igor-arch .route .rl{grid-column:1/-1;font-size:12px;color:var(--ia-mu);text-align:center;margin-top:-2px}
.igor-arch .route .ep{border:1px solid var(--ia-bd);background:var(--ia-el);color:var(--ia-tx);border-radius:6px;padding:8px 6px;font-size:13px;min-height:40px}
.igor-arch .route .ep.sel{border-color:var(--ia-ac)}
.igor-arch .route .arrow{color:var(--ia-mu)}
"""

JS = """
const root = document.getElementById('igor-arch') as HTMLElement | null;
const info = document.getElementById('igor-arch-info') as HTMLElement | null;
const pauseButton = document.getElementById('igor-arch-pause') as HTMLButtonElement | null;
if (!root || !info || !pauseButton) {
  throw new Error('IgorArchitecture: expected #igor-arch, #igor-arch-info and #igor-arch-pause in the page');
}
const diagram: HTMLElement = root;
const infoBox: HTMLElement = info;
const pauseBtn: HTMLButtonElement = pauseButton;
const FAULT_IDS: string[] = %(fault_ids)s;

const infoById: Record<string, string> = {};
diagram.querySelectorAll<HTMLElement>('.desk .mod').forEach((m) => {
  const id = m.dataset.id;
  const text = m.getAttribute('data-info');
  if (id && text) {
    infoById[id] = text;
  }
});

function pick(id: string | undefined): void {
  if (!id || !infoById[id]) {
    return;
  }
  diagram.querySelectorAll('.sel').forEach((m) => m.classList.remove('sel'));
  diagram.querySelectorAll('[data-id="' + id + '"]').forEach((m) => m.classList.add('sel'));
  infoBox.textContent = infoById[id];
}

diagram.querySelectorAll<HTMLElement>('.mod').forEach((m) => {
  const id = m.dataset.id;
  if (id && FAULT_IDS.includes(id)) {
    m.classList.add('has-fault');
  }
  m.addEventListener('click', () => pick(id));
  m.addEventListener('focus', () => pick(id));
  m.addEventListener('mouseenter', () => {
    if (id && infoById[id]) {
      infoBox.textContent = infoById[id];
    }
  });
  m.addEventListener('keydown', (e: KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      pick(id);
    }
  });
});

diagram.querySelectorAll<HTMLElement>('.ep,.fault-pick').forEach((b) => {
  b.addEventListener('click', () => pick(b.dataset.id));
});

diagram.querySelectorAll<HTMLElement>('.solob').forEach((b) => {
  b.addEventListener('click', () => {
    const k = b.dataset.k;
    const turnOn = b.getAttribute('aria-pressed') !== 'true';
    diagram.querySelectorAll('.solob').forEach((x) => x.setAttribute('aria-pressed', 'false'));
    diagram.classList.remove('solo-req', 'solo-data', 'solo-mon', 'solo-run');
    if (turnOn && k) {
      b.setAttribute('aria-pressed', 'true');
      diagram.classList.add('solo-' + k);
    }
  });
});

diagram.querySelectorAll<HTMLElement>('.tab').forEach((t) => {
  t.addEventListener('click', () => {
    diagram.querySelectorAll('.tab').forEach((x) => x.setAttribute('aria-selected', 'false'));
    t.setAttribute('aria-selected', 'true');
    diagram.classList.toggle('failing', t.dataset.v === 'fail');
  });
});

pauseBtn.addEventListener('click', () => {
  const paused = diagram.classList.toggle('paused');
  pauseBtn.textContent = paused ? 'Play pulses' : 'Pause pulses';
  pauseBtn.setAttribute('aria-pressed', String(paused));
});

// Optional URL switches, used for screenshots: ?tab=fail&solo=mon&sel=igor&paused=1
const q = new URLSearchParams(location.search);
const soloParam = q.get('solo');
if (soloParam) {
  const b = diagram.querySelector<HTMLElement>('.solob[data-k="' + soloParam + '"]');
  if (b) {
    b.click();
  }
}
if (q.get('tab') === 'fail') {
  const failTab = diagram.querySelector<HTMLElement>('.tab[data-v=fail]');
  if (failTab) {
    failTab.click();
  }
}
const selParam = q.get('sel');
if (selParam) {
  pick(selParam);
}
if (q.get('paused')) {
  pauseBtn.click();
}
"""


def attach_info(svg_markup):
    """Add data-info attributes to module groups so the script can read them."""
    out = svg_markup
    for node in NODES:
        needle = f'data-id="{node["id"]}" aria-label='
        replacement = f'data-id="{node["id"]}" data-info="{escape(node["info"])}" aria-label='
        out = out.replace(needle, replacement)
    return out


def component_astro():
    desk = attach_info(desktop_svg())
    mob = attach_info(mobile_svg())
    js = JS % {"fault_ids": str(FAULT_IDS).replace("'", '"')}
    return f"""---
// GENERATED FILE — do not edit by hand. Run: python3 scripts/gen-igor-diagram.py
// Interactive architecture diagram for the Igor case study. No dependencies.
---
<div class="igor-arch" id="igor-arch">
<div class="bar"><div class="tabs" role="tablist" aria-label="Diagram view"><button class="tab" role="tab" data-v="ok" aria-selected="true">How it works</button><button class="tab" role="tab" data-v="fail" aria-selected="false">When something fails</button></div>
<button class="pauseb" id="igor-arch-pause" aria-pressed="false">Pause pulses</button></div>
<div class="frame"><div class="desk">{desk}</div><div class="mob">{mob}</div></div>
{routes_html()}
<div class="solos">{solo_buttons_html()}</div>
{faults_html()}
<div class="info"><b>Tap any box ·</b> <span id="igor-arch-info">Each module explains itself when you tap or hover it. LEDs and pulses are illustration, not live status.</span></div>
<p class="talk"><b>In one sentence:</b> {escape(ONE_SENTENCE)}</p>
<noscript><p class="failnote">The interactive controls need JavaScript; the diagram and the connection list above still show the full picture.</p></noscript>
</div>
<style is:global>{CSS}</style>
<script>{js}</script>
"""


with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(component_astro())
print("wrote", OUT_PATH)
