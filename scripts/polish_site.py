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
#process [data-framer-name="Icon"] .magnence-step-symbol-svg {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 30px !important;
  height: 30px !important;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));
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
  var SVGS = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" style="display:block;width:100%;height:100%;fill:currentColor;color:rgb(20,20,20);"><path d="M63.81,192.19c-47.89-79.81,16-159.62,151.64-151.64C223.43,176.23,143.62,240.08,63.81,192.19Z" opacity="0.2"/><path d="M223.45,40.07a8,8,0,0,0-7.52-7.52C139.8,28.08,78.82,51,52.82,94a87.09,87.09,0,0,0-12.76,49c.57,15.92,5.21,32,13.79,47.85l-19.51,19.5a8,8,0,0,0,11.32,11.32l19.5-19.51C81,210.73,97.09,215.37,113,215.94q1.67.06,3.33.06A86.93,86.93,0,0,0,162,203.18C205,177.18,227.93,116.21,223.45,40.07ZM153.75,189.5c-22.75,13.78-49.68,14-76.71.77l88.63-88.62a8,8,0,0,0-11.32-11.32L65.73,179c-13.19-27-13-54,.77-76.71,22.09-36.47,74.6-56.44,141.31-54.06C210.2,114.89,190.22,167.41,153.75,189.5Z"/></svg>',
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" style="display:block;width:100%;height:100%;fill:currentColor;color:rgb(20,20,20);"><path d="M176,232H80l10.27-71.89,17.63-30,58.46,34.41Z" opacity="0.2"/><path d="M224,224H182.94l-6.3-44.12,3.24,1.91a16,16,0,0,0,21.91-5.67l12-20.34a16,16,0,0,0-5.67-21.91l-35-20.61,40.69-69.13a16,16,0,0,0-5.67-21.91l-20.34-12a16,16,0,0,0-21.91,5.67l-20.61,35L76.12,10.22a16,16,0,0,0-21.91,5.67l-12,20.33a16,16,0,0,0,5.67,21.92l35,20.61L42.21,147.88a16,16,0,0,0,5.67,21.91l20.34,12a15.57,15.57,0,0,0,10.58,2L73.06,224H32a8,8,0,0,0,0,16H224a8,8,0,0,0,0-16Zm-24-76.34L188,168l-69.13-40.69,12-20.35ZM179.66,24,200,36l-40.69,69.14L139,93.17ZM56,44.35,68,24,137.14,64.7l-12,20.35ZM76.34,168,56,156,96.69,86.86l20.36,12Zm12.88,56L98,162.8l12.77-21.7L159,169.5l7.79,54.5Z"/></svg>',
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" style="display:block;width:100%;height:100%;fill:currentColor;color:rgb(20,20,20);"><path d="M216,128a88,88,0,1,1-88-88A88,88,0,0,1,216,128Z" opacity="0.2"/><path d="M245.11,60.68c-7.65-13.19-27.84-16.16-58.5-8.66A95.93,95.93,0,0,0,32,128a98,98,0,0,0,.78,12.31C5.09,169,5.49,186,10.9,195.32,16,204.16,26.64,208,40.64,208a124.11,124.11,0,0,0,28.79-4A95.93,95.93,0,0,0,224,128a97.08,97.08,0,0,0-.77-12.25c12.5-13,20.82-25.35,23.65-35.92C248.83,72.51,248.24,66.07,245.11,60.68ZM128,48a80.11,80.11,0,0,1,78,62.2c-17.06,16.06-40.15,32.53-62.07,45.13C116.38,171.14,92.48,181,73.42,186.4A79.94,79.94,0,0,1,128,48ZM24.74,187.29c-1.46-2.51-.65-7.24,2.22-13a79.05,79.05,0,0,1,10.29-15.05,96,96,0,0,0,18,31.32C38,193.46,27.24,191.61,24.74,187.29ZM128,208a79.45,79.45,0,0,1-38.56-9.94,370,370,0,0,0,62.43-28.86c21.58-12.39,40.68-25.82,56.07-39.08A80.07,80.07,0,0,1,128,208ZM231.42,75.69c-1.7,6.31-6.19,13.53-12.63,21.13a95.69,95.69,0,0,0-18-31.35c14.21-2.35,27.37-2.17,30.5,3.24C232.19,70.28,232.24,72.63,231.42,75.69Z"/></svg>'
  ];
  function inject() {
    var section = document.getElementById("process");
    if (!section) return;
    var containers = section.querySelectorAll('[data-framer-name="Icon"] .framer-8vporc-container, [data-framer-name="Icon"] [class*="8vporc-container"]');
    containers.forEach(function (el, i) {
      if (el.querySelector(".magnence-step-symbol-svg")) return;
      var sym = document.createElement("div");
      sym.className = "magnence-step-symbol-svg";
      sym.setAttribute("aria-hidden", "true");
      sym.style.width = "30px";
      sym.style.height = "30px";
      sym.style.display = "flex";
      sym.style.alignItems = "center";
      sym.style.justifyContent = "center";
      sym.innerHTML = SVGS[i % SVGS.length];
      el.innerHTML = "";
      el.appendChild(sym);
    });
  }
  inject();
  new MutationObserver(inject).observe(document.documentElement, { childList: true, subtree: true });
})();
"""

REPLACEMENTS: list[tuple[str, str]] = [
    # Process section titles - HTML
    ('class="framer-text">Production</h6>', 'class="framer-text">PRODUCTION</h6>'),
    ('class="framer-text">Post</h6>', 'class="framer-text">POST</h6>'),
    ('style="--framer-text-alignment:center">Discovery</p>', 'style="--framer-text-alignment:center">AI CREATION</p>'),
    ('style="--framer-text-alignment:center"> Design Sprint</p>', 'style="--framer-text-alignment:center">UX MOODBOARD</p>'),
    ('style="--framer-text-alignment:center">Design Sprint</p>', 'style="--framer-text-alignment:center">UX MOODBOARD</p>'),
    ('style="--framer-text-alignment:center">Content Marketing</p>', 'style="--framer-text-alignment:center">CONTENT STRATEGY</p>'),
    ('style="--framer-text-alignment:center">Development</p>', 'style="--framer-text-alignment:center">FRONT-END</p>'),
    ('style="--framer-text-alignment:center">AI Integration</p>', 'style="--framer-text-alignment:center">AI IMPLEMENT</p>'),
    ('style="--framer-text-alignment:center">Video Editing</p>', 'style="--framer-text-alignment:center">MOTION DESIGN</p>'),
    ('style="--framer-text-alignment:center">deployment</p>', 'style="--framer-text-alignment:center">DEPLOYMENT</p>'),
    ('style="--framer-text-alignment:center">Deployment</p>', 'style="--framer-text-alignment:center">DEPLOYMENT</p>'),
    ('style="--framer-text-alignment:center">Optimization</p>', 'style="--framer-text-alignment:center">AUTO ENHANCING</p>'),
    ('style="--framer-text-alignment:center">Product Marketing</p>', 'style="--framer-text-alignment:center">PRODUCT MARKETING</p>'),

    # Process section titles - JS attributes / variables
    ('wdewp3Cqj:"Production"', 'wdewp3Cqj:"PRODUCTION"'),
    ('wdewp3Cqj:"Post"', 'wdewp3Cqj:"POST"'),
    ('zK4dx5gI0:"Discovery"', 'zK4dx5gI0:"AI CREATION"'),
    ('rPVLqvqQi:" Design Sprint"', 'rPVLqvqQi:"UX MOODBOARD"'),
    ('rPVLqvqQi:"Design Sprint"', 'rPVLqvqQi:"UX MOODBOARD"'),
    ('uyJTFZ8Ot:"Content Marketing"', 'uyJTFZ8Ot:"CONTENT STRATEGY"'),
    ('zK4dx5gI0:"Development"', 'zK4dx5gI0:"FRONT-END"'),
    ('rPVLqvqQi:"AI Integration"', 'rPVLqvqQi:"AI IMPLEMENT"'),
    ('uyJTFZ8Ot:"Video Editing"', 'uyJTFZ8Ot:"MOTION DESIGN"'),
    ('zK4dx5gI0:"deployment"', 'zK4dx5gI0:"DEPLOYMENT"'),
    ('rPVLqvqQi:"Optimization"', 'rPVLqvqQi:"AUTO ENHANCING"'),
    ('uyJTFZ8Ot:"Product Marketing"', 'uyJTFZ8Ot:"PRODUCT MARKETING"'),

    # Process section default values (in React components definition)
    ('defaultValue:"Discovery"', 'defaultValue:"AI CREATION"'),
    ('defaultValue:" Design Sprint"', 'defaultValue:"UX MOODBOARD"'),
    ('defaultValue:"Design Sprint"', 'defaultValue:"UX MOODBOARD"'),
    ('defaultValue:"Content Marketing"', 'defaultValue:"CONTENT STRATEGY"'),

    # Header restoration
    ('HOW WE WORK</h5>', 'WELCOME TO THE WORK PROCESS</h5>'),
    ('children:"HOW WE WORK"', 'children:"WELCOME TO THE WORK PROCESS"'),

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
