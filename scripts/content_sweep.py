#!/usr/bin/env python3
"""Second-pass Magnence content alignment — agency copy, location, team, pricing."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS: list[tuple[str, str]] = [
    # Hero headline
    ("UNLOCK", "BUILD"),
    ("YOUR TARGET", "DIGITAL PRODUCTS"),
    # Hero subcopy
    ("MEMORABLE &amp; CAPTIVATING DIGITAL", "SOFTWARE, MARKETING, DESIGN"),
    ("MEMORABLE & CAPTIVATING DIGITAL", "SOFTWARE, MARKETING, DESIGN"),
    ("EXPERIENCES THAT GROW YOUR BRAND", "SERVICES THAT GROW YOUR BRAND"),
    ("EXPERIENCES.", "SERVICES."),
    ("PARTNERING WITH VISIONARIES PEOPLE &amp; TRAILBLAZERS", "PARTNERING WITH FOUNDERS &amp; OPERATORS"),
    ("PARTNERING WITH VISIONARIES PEOPLE & TRAILBLAZERS", "PARTNERING WITH FOUNDERS & OPERATORS"),
    ("WITh visionaries PEOPLe who need software, marketing, design &amp; editing TO innovate.", "WITH founders &amp; operators who need software, marketing, design &amp; editing to grow."),
    # Location
    ("BASED IN LA, CALIFORINA", "BASED IN GURUGRAM, HARYANA"),
    ("BASED IN LA, CALIFORNIA", "BASED IN GURUGRAM, HARYANA"),
    ("Los Angeles, California", "Gurugram, Haryana, India"),
    ("Los Angeles", "Gurugram"),
    # About section
    ("WE ARE MAGNENCE", "WE ARE MAGNENCE"),
    ("Design Studio.", "Creative Agency."),
  # Team — lead with CEO on home preview
    ("William Coork", "Anurag Singh"),
    ("Creative Director", "CEO &amp; Founder"),
    # Pricing / CTA
    ("Premium plan", "Website Package"),
    ("Premium plus plan", "Full-Service Package"),
    ("SUBSCRIBE NOW", "GET STARTED"),
    ("/Month", "/Project"),
    ("/YEAR", "/Year"),
    ("10 Days Delivery", "2–3 Weeks Delivery"),
    ("07 Days Delivery", "1–2 Weeks Delivery"),
    ("8 Revisions", "3 Revisions"),
    ("UNLIMITED Revisions", "Unlimited Revisions"),
    ("1750+ Subscribers", "50+ Projects Delivered"),
    ("1,450+ People Rated", "50+ Happy Clients"),
    ("Web-Meet CLIENT PROJECT", "Discovery Call Included"),
    ("REAL-Meet CLIENT PROJECT", "Dedicated Project Manager"),
    ("LIFETIME ACCESS", "Priority Support"),
    ("Limited ACCESS", "Standard Support"),
    ("16 HOURS OF Tutorial CONTENT", "Design &amp; Development Included"),
    ("32 HOURS OF Tutorial CONTENT", "Marketing &amp; Editing Included"),
    ("ACCESS TO 24/7 Support SERVER", "24/7 Support Channel"),
    ("ACCESS TO Latest assets Library", "Asset Handoff Included"),
    ("COMMUNITY SUPPORT", "Ongoing Maintenance"),
    # Awards strip — de-template
    ("3x Framer Award", "3x Design Award"),
    ("Red dot Award", "Brand Award"),
    ("Link One Awards", "Marketing Award"),
    ("Marketing Systems SOTD", "Campaign of the Year"),
    # Remaining AI-led phrasing
    ("AI-Led Technology Services Company", "Software, Marketing, Design & Editing Agency"),
    ("AI-led technology services company", "full-service software, marketing, design & editing agency"),
    ("AI-led technology", "software, marketing, design & editing"),
    ("AI-Led Technology", "Software & Creative"),
    ("AI-Led Services", "Agency Services"),
    ("AI-led services", "agency services"),
    ("AI-Led Delivery", "Software & Design"),
    ("AI-led delivery", "software & design"),
    ("AI-Led Execution", "Creative Execution"),
    ("AI-led execution", "creative execution"),
    ("AI-Led", "Full-Service"),
    ("AI-led", "full-service"),
    # Process section

    # Voice section
    ("VOICE OF CE-yO.", "FROM THE CEO."),
    # Misc template
    ("BIG OR SMALL?", "STARTUP OR ENTERPRISE?"),
    ("IN OUR Class MAGNENCE.", "WITH MAGNENCE."),
    ("TEam &amp; Talent", "Team &amp; Talent"),
    ("&amp; TALENT", "&amp; EXPERTS"),
    ("RECogNITION", "RECOGNITION"),
    ("EVOLUTIONARily", "DELIBERATELY"),
    ("Wired to sleek", "Built to deliver"),
    ("Fundamentally", "Fundamentally"),
    ("tuned to Sharp", "focused on quality"),
    ("Cre-ation.", "creation."),
    ("wo—nder", "wonder"),
    # Contact meta leftovers
    ("9001 Beverly Blvd", "Gurugram"),
    ("49th St", "Sector"),
    ("+1 (310)", "+91"),
    ("California 90048", "Haryana, India"),
    ("United States", "India"),
    # Ticker remnants
    ("STRATEGIZE AUTOMATE SCALE", "DESIGN DEVELOP MARKET EDIT"),
    ("BUILT FOR MODERN BUSINESSES", "BUILT FOR GROWING BRANDS"),
    ("AI-LED TECHNOLOGY SERVICES", "FULL-SERVICE AGENCY"),
]


def sweep_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for pattern in ("*.html", "*.mjs", "*.js"):
        for path in ROOT.rglob(pattern):
            if "node_modules" in path.parts:
                continue
            if sweep_file(path):
                updated.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(updated)} files")
    for p in sorted(updated)[:30]:
        print(f"  - {p}")
    if len(updated) > 30:
        print(f"  ... and {len(updated) - 30} more")


if __name__ == "__main__":
    main()
