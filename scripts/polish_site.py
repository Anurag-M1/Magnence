#!/usr/bin/env python3
"""Magnence polish: tagline, process icons, pricing, footer, font credit removal."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TAGLINE = "✦ STRATEGIZE · CREATE · ENGINEER · AMPLIFY · MAGNENCE"
TAGLINE_TICKER = (
    "✦ STRATEGIZE · 🎨 CREATE · 💻 ENGINEER · 📣 AMPLIFY · ✨ MAGNENCE"
)

FONT_CREDIT_OLD = (
    "Fjalla One and Inter Display are used under the terms of free license "
    "for commercial use."
)
FONT_CREDIT_OLD_EMOJI = (
    "Fjalla One and Inter Display are used under the terms of free license "
    "for commercial use  \\u{1F49B}  Fjalla One and Inter Display are used "
    "under the terms of free license for commercial use  \\u{1F308}"
)
FONT_CREDIT_NEW = (
    "Magnence — software, marketing, design & editing from Gurugram, India."
)
FONT_CREDIT_NEW_EMOJI = (
    "Magnence — software, marketing, design & editing from Gurugram, India. "
    "\\u{1F49B}  Magnence — software, marketing, design & editing from Gurugram, India. "
    "\\u{1F308}"
)

GOOGLE_FONTS_COPY = "Copyright \\xA9 Google Fonts\\xAE Foundry"
MAGNENCE_COPY = "© Magnence 2026 · Gurugram, Haryana, India"

PROCESS_CSS = """
/* === Process step symbols === */
#process [data-framer-name="Icon"] .framer-8vporc-container,
#process [data-framer-name="Icon"] [class*="8vporc-container"] {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 100% !important;
  position: absolute !important;
  inset: 0 !important;
  z-index: 2 !important;
  pointer-events: none !important;
}
#process [data-framer-name="Icon"] .magnence-step-symbol {
  font-size: 52px !important;
  line-height: 1 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 100% !important;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.25));
}
#process [data-framer-name="Detailing Image"] {
  min-height: 280px !important;
}

/* === Pricing: prevent truncated revision text === */
[data-framer-name="pricing"] h6,
[data-framer-name="pricing"] .framer-text,
.framer-6KK3U h6,
.framer-6KK3U .framer-text {
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: unset !important;
  word-break: normal !important;
}
"""

PROCESS_JS = """
(function () {
  var ICONS = ["\\u{1F33F}", "\\u{1F300}", "\\u{1FA90}"]; /* leaf, windmill, planet */
  function inject() {
    var section = document.getElementById("process");
    if (!section) return;
    var containers = section.querySelectorAll('[data-framer-name="Icon"] .framer-8vporc-container, [data-framer-name="Icon"] [class*="8vporc-container"]');
    containers.forEach(function (el, i) {
      if (el.querySelector(".magnence-step-symbol")) return;
      var sym = document.createElement("span");
      sym.className = "magnence-step-symbol";
      sym.setAttribute("aria-hidden", "true");
      sym.textContent = ICONS[i % ICONS.length];
      el.innerHTML = "";
      el.appendChild(sym);
    });
  }
  inject();
  new MutationObserver(inject).observe(document.documentElement, { childList: true, subtree: true });
})();
"""

REPLACEMENTS: list[tuple[str, str]] = [
    # Taglines
    (
        "⚡ DESIGN  ·  💻 DEVELOP  ·  📣 MARKET  ·  ✂️ EDIT  ·  🚀 DELIVER  ·  MAGNENCE",
        TAGLINE_TICKER,
    ),
    (
        "⚡ DESIGN · 💻 DEVELOP · 📣 MARKET · ✂️ EDIT · 🚀 DELIVER · MAGNENCE",
        TAGLINE_TICKER.replace("  ", " "),
    ),
    (
        "⚡ DESIGN  ·  💻 DEVELOP  ·  📣 MARKET  ·  ✂️ EDIT  ·  MAGNENCE",
        TAGLINE_TICKER.replace(" · 🚀 DELIVER", "").replace(" · ✨", " · ✨"),
    ),
    (
        "⚡ DESIGN · 💻 DEVELOP · 📣 MARKET · ✂️ EDIT · MAGNENCE",
        "✦ STRATEGIZE · 🎨 CREATE · 💻 ENGINEER · 📣 AMPLIFY · ✨ MAGNENCE",
    ),
    (
        "FULL-SERVICE AGENCY 💛 DESIGN DEVELOP MARKET EDIT 🌈 BUILT FOR GROWING BRANDS ⚡",
        TAGLINE_TICKER,
    ),
    (
        "DESIGN DEVELOP MARKET EDIT",
        "STRATEGIZE · CREATE · ENGINEER · AMPLIFY",
    ),
    (
        "BUILT FOR GROWING BRANDS",
        "CRAFTED IN GURUGRAM",
    ),
    (
        "MAGNENCE AGENCY  \\u{1F49B}  STRATEGIZE · CREATE · ENGINEER · AMPLIFY  \\u{1F308}  CRAFTED IN GURUGRAM  \\u{26A1}",
        "✦ STRATEGIZE · 🎨 CREATE · 💻 ENGINEER · 📣 AMPLIFY · ✨ MAGNENCE",
    ),
    # Footer / font credits (HTML escaped)
    ("Get a Remix link", "Launch With Magnence →"),
    ("Get a Remix Link", "Launch With Magnence →"),
    (FONT_CREDIT_OLD, FONT_CREDIT_NEW),
    ("Copyright © Google Fonts® Foundry", "© Magnence 2026 · Gurugram, Haryana, India"),
    ("Copyright © Google Fonts&reg; Foundry", "© Magnence 2026 · Gurugram, Haryana, India"),
    ("© Magnence Studio 2026", "© Magnence 2026"),
    ("Magnence Studio 2026", "Magnence 2026"),
    ("./work/remix-supply", "./contact"),
    ('href="./work/remix-supply"', 'href="./contact"'),
    ('mAx9fAYnn:"/work/remix-supply"', 'mAx9fAYnn:"/contact"'),
    ('mAx9fAYnn:"./work/remix-supply"', 'mAx9fAYnn:"/contact"'),
    # Revisions fix (avoid double-s when already plural)
    ("Unlimited Revisionss", "Unlimited Revisions"),
    (
        "Unlimited Revision",
        "Unlimited Revisions",
    ),
    # Pricing — website package
    (
        "Platinum 10 Pages Ecommerce, Booking, 🌈 SEO Optimized, Custom Design, 4 Breakpoints, Responsive Website.",
        "Up to 10 pages · Custom UI/UX design · Mobile-responsive · SEO-ready · CMS setup · 3 revision rounds · 2–3 week delivery.",
    ),
    (
        "Platinum 10 Pages Ecommerce, Booking, \\u{1F308} SEO Optimized, Custom Design, 4 Breakpoints, Responsive Website.",
        "Up to 10 pages · Custom UI/UX · Mobile-responsive · SEO-ready · CMS setup · 3 revision rounds · 2–3 week delivery.",
    ),
    (
        "Platinum+ 20 Pages Ecommerce, Booking, 🐝 Unique CRM, Custom Design, 4 Breakpoints, Marketing & More.",
        "Up to 20 pages · Web apps & dashboards · Marketing campaigns · Video editing · CRM & automation · Unlimited revisions · Dedicated PM.",
    ),
    (
        "Platinum+ 20 Pages Ecommerce, Booking, \\u{1F30D} Unique CRM, Custom Design, 4 Breakpoints, Marketing & More.",
        "Up to 20 pages · Web apps & dashboards · Marketing campaigns · Video editing · CRM & automation · Unlimited revisions · Dedicated PM.",
    ),
    (
        "Platinum+ 20 Pages Ecommerce, Booking, \\u{1F41D} Unique CRM, Custom Design, 4 Breakpoints, Marketing & More.",
        "Up to 20 pages · Web apps & dashboards · Marketing campaigns · Video editing · CRM & automation · Unlimited revisions · Dedicated PM.",
    ),
    # Pricing feature bullets
    ("Discovery Call Included", "Free strategy & discovery call"),
    ("Design & Development Included", "Full design + development"),
    ("Design &amp; Development Included", "Full design + development"),
    ("Marketing & Editing Included", "Marketing + video editing"),
    ("Marketing &amp; Editing Included", "Marketing + video editing"),
    ("Dedicated Project Manager", "Dedicated project manager"),
    ("Asset Handoff Included", "Complete asset handoff"),
    ("24/7 Support Channel", "Priority support channel"),
    ("Ongoing Maintenance", "Monthly maintenance option"),
    ("Standard Support", "Email & chat support"),
    ("Priority Support", "Priority phone & chat support"),
    ("50+ Happy Clients", "50+ happy clients"),
    ("50+ Projects Delivered", "50+ projects delivered"),
    ("16 HOURS OF Tutorial CONTENT", "Full design + development"),
    ("16 HOURS OF Tutorial&nbsp;CONTENT", "Full design + development"),
    (
        "Business websites, landing pages, and brand surfaces built to attract and convert.",
        "Up to 10 pages · Custom UI/UX · Mobile-responsive · SEO-ready · CMS setup · 3 revision rounds · 2–3 week delivery.",
    ),
    (
        "Websites, web apps, marketing campaigns, design systems, video edits, and ongoing support.",
        "Up to 20 pages · Web apps & dashboards · Marketing campaigns · Video editing · CRM & automation · Unlimited revisions · Dedicated PM.",
    ),
]


def sweep_text(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # Fix revision label without doubling the trailing s
    text = text.replace("Unlimited Revisionss", "Unlimited Revisions")
    text = re.sub(r"Unlimited Revision(?!s)", "Unlimited Revisions", text)
    # JS bundle font credit (escaped)
    text = text.replace(FONT_CREDIT_OLD_EMOJI, FONT_CREDIT_NEW_EMOJI)
    text = text.replace(GOOGLE_FONTS_COPY, MAGNENCE_COPY)
    text = text.replace('GPoIl1uBW:"Get a Remix link"', 'GPoIl1uBW:"Launch With Magnence →"')
    return text


def patch_magnence_overrides(html: str) -> str:
    if "magnence-process-icons" in html:
        return html

    if "magnence-overrides" in html and "Process step symbols" not in html:
        html = html.replace(
            "</style>\n</head>",
            PROCESS_CSS + "\n</style>\n</head>",
            1,
        ) if "</style>\n</head>" in html and 'id="magnence-overrides"' in html else html
        # append before closing magnence-overrides style tag
        marker = '<style id="magnence-overrides">'
        if marker in html and "Process step symbols" not in html:
            html = html.replace(
                marker,
                marker + PROCESS_CSS,
                1,
            )

    script = f'<script id="magnence-process-icons">{PROCESS_JS}</script>'
    if "magnence-process-icons" not in html:
        html = html.replace("</body>", script + "\n</body>", 1)
    return html


def main() -> None:
    updated: list[str] = []

    targets = list(ROOT.rglob("*.html"))
    targets += list((ROOT / "assets" / "js").rglob("*.mjs"))

    for path in targets:
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        text = sweep_text(text)
        if path.suffix == ".html":
            text = patch_magnence_overrides(text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            updated.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(updated)} files")
    for p in sorted(updated):
        print(f"  - {p}")


if __name__ == "__main__":
    main()
