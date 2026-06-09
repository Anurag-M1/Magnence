#!/usr/bin/env python3
"""Update Magnence homepage hero headline and subcopy."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS: list[tuple[str, str]] = [
    # Main headline (two-line hero)
    ('children:"BUILD"', 'children:"CRAFT"'),
    (">BUILD</h1>", ">CRAFT</h1>"),
    ('children:"DIGITAL PRODUCTS"', 'children:"BRANDS THAT WIN"'),
    (">DIGITAL PRODUCTS</h1>", ">BRANDS THAT WIN</h1>"),
    ('children:"YOUR start"', 'children:"YOUR EDGE"'),
    (">YOUR start</h1>", ">YOUR EDGE</h1>"),
    # Single-line hero variants
    (
        "SOFTWARE, MARKETING, DESIGN \\u2014 SERVICES.",
        "SOFTWARE · MARKETING · DESIGN · EDITING \\u2014 ONE STUDIO.",
    ),
    (
        "SOFTWARE, MARKETING, DESIGN — SERVICES.",
        "SOFTWARE · MARKETING · DESIGN · EDITING — ONE STUDIO.",
    ),
    (
        "SOFTWARE, MARKETING, DESIGN \\u2014 EXPERIENCES THAT GROW YOUR BRAND. Partnering WHO NEED SOFTWARE, MARKETING, DESIGN & EDITING TO SCALE.",
        "ONE TEAM FOR SOFTWARE, MARKETING, DESIGN & EDITING \\u2014 PARTNERING WITH FOUNDERS SINCE 2000.",
    ),
    (
        "SOFTWARE, MARKETING, DESIGN PEOPLE & things CREATE Variant in field DISRUPTORS.",
        "SOFTWARE · MARKETING · DESIGN · EDITING \\u2014 BUILT FOR BRANDS THAT LEAD.",
    ),
    # Animated subcopy (home.mjs array children)
    ("SOFTWARE, MARKETING, DESIGN & ", "SOFTWARE · MARKETING · DESIGN · "),
    ("EDITING SERVICES ", "EDITING — "),
    ("\\u2014 EXPERIENCES", "ONE STUDIO FOR "),
    ("THAT GROW YOUR BRAND. ", "BRANDS BUILT TO LEAD. "),
    (', "Partnering"]', "]"),
    ('}),"Partnering"]', "})]"),
    ("WITh ", "WITH "),
    ("visionaries PEOPLe ", "founders & operators "),
    ("& trailblazers ", "since 2000 "),
    ("TO innovate.", "TO build what lasts."),
    # SSR hero paragraph fragments
    ("MEMORABLE &amp; ", "ONE TEAM · "),
    ("MEMORABLE & ", "ONE TEAM · "),
    ("BUILD </span>DIGITAL PRODUCTS", "four disciplines </span>one studio"),
    ("that grow your brand. ", "built to lead. "),
    ("PARTNERING WITH FOUNDERS &amp; OPERATORS.", "PARTNERING WITH FOUNDERS SINCE 2000."),
    ("PARTNERING WITH FOUNDERS & OPERATORS.", "PARTNERING WITH FOUNDERS SINCE 2000."),
    (
        "SOFTWARE, MARKETING, DESIGN — EXPERIENCES that grow your brand. Partnering WITH founders &amp; operators who need software, marketing, design &amp; editing to grow.",
        "SOFTWARE · MARKETING · DESIGN · EDITING — one studio for brands built to lead. Partnering with founders since 2000.",
    ),
    (
        "SOFTWARE, MARKETING, DESIGN PEOPLE &amp; things CREATE Variant in field DISRUPTORS.",
        "SOFTWARE · MARKETING · DESIGN · EDITING — built for brands that lead.",
    ),
    ("WITh </span>visionaries PEOPLe ", "WITH </span>founders &amp; operators "),
    ("who need software, marketing, design &amp; editing TO innovate.", "since 2000 TO build what lasts."),
]


def main() -> None:
    targets = [ROOT / "index.html", ROOT / "assets" / "js" / "pages" / "home.mjs"]
    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
