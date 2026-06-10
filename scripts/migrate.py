#!/usr/bin/env python3
"""Magnence migration: content, cleanup, rename, restructure."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

META_TITLE = "Magnence | Software, Marketing, Design & Editing Agency"
META_DESC = (
    "Magnence is a full-service agency for software development, digital marketing, "
    "UI/UX design, video editing, and content production — delivering websites, apps, "
    "campaigns, and creative assets for growing businesses."
)

TAGLINE = (
    "⚡ DESIGN  ·  💻 DEVELOP  ·  📣 MARKET  ·  ✂️ EDIT  ·  🚀 DELIVER  ·  MAGNENCE"
)
TAGLINE_SHORT = "⚡ DESIGN  ·  💻 DEVELOP  ·  📣 MARKET  ·  ✂️ EDIT  ·  MAGNENCE"

# Route/page bundles -> readable names
JS_RENAMES = {
    "script_main.MQLY5MZV.mjs": "app.mjs",
    "x6tipuAozajKXY4nU3bGLMaMtyZR68f0Tmr6NmUm1Y0.ZVF57H4K.mjs": "pages/home.mjs",
    "Z213P4Uu2IISc-NVcCY64buYvwqqS3U1W1Ur85wh6Xk.MULTWS2D.mjs": "pages/team.mjs",
    "oa_XZz1st08iS-eYxwRIvVyQZf8Auab1iRQs8NWxaCI.ADVYF7MG.mjs": "pages/services.mjs",
    "6ihs9JZk6ab6pxOZEmYXjz5RS3Q-c06RxO4pwGXKm14.KOHNG5C3.mjs": "pages/work.mjs",
    "D7LhShWt7ZIl34mAElrb3rVP7EBptxV9Nf_FbYAs80c.VMMPIYLP.mjs": "pages/contact.mjs",
    "x8eYI_Tf2HQQPrfBM9pA-bgmYjtSCSHdOrRBI1JJo8o.FCYNWKZB.mjs": "pages/blog.mjs",
    "f-zuToQL353Fm1qpthacMorW1___g3Fq2Fj13mh1ebE.2YCQ7I4U.mjs": "pages/work-detail.mjs",
    "Jgjx2G1v5-wlDRkGMZUAxDyJJz5PtNy2uQ5QNG7or0o.FVPNM5IX.mjs": "pages/blog-detail.mjs",
    "LTkd40jjTDSg-eiN0x0QwhowrZY2cHUEDwRPnZiPNi4.OICXOZPB.mjs": "pages/not-found.mjs",
    "9AT1tsnUrvnt80-C1c5NzHzXTFXdnRujVMdDd4HlRxY.4KNUDZY6.mjs": "data/work-collection.mjs",
    "Oem55xZhb-fbrtYstl5VqV6YmDkzJzH-KS9bn4VqSds.NKR4XBX7.mjs": "data/blog-collection.mjs",
    "F4pZnMMIi-2-ALFC73O5.mjs": "data/blog-data.mjs",
    "DJy8vEuY5-2-W7A55K7S.mjs": "data/work-data.mjs",
    "offline-runtime.js": "runtime/offline.js",
}

IMAGE_RENAMES = {
    "magnence-icon.png": "brand/icon.png",
    "LKTsmRFX5xCNyOOYdnG0nBJZenk.svg": "brand/logo.svg",
    "MTN7lwa706KrVikQhsFchPwMQzY.png": "brand/social-share.png",
    "rR6HYXBrMmX4cRpXfXUOvpvpB0.png": "ui/noise-texture.png",
}

CONTENT_REPLACEMENTS = [
    ("Magnence | AI-Led Technology Services Company", META_TITLE),
    (
        "Magnence is an AI-led technology services company building intelligent websites, automation workflows, web apps, digital products, and growth systems for modern businesses.",
        META_DESC,
    ),
    (
        "STRATEGIZE  ·  AUTOMATE  ·  SCALE  ·  AI-LED TECHNOLOGY DELIVERY  ·  MAGNENCE",
        TAGLINE,
    ),
    ("STRATEGIZE  ·  AUTOMATE  ·  SCALE  ·  MAGNENCE", TAGLINE_SHORT),
    (
        "AI-LED TECHNOLOGY SERVICES  💛  STRATEGIZE AUTOMATE SCALE  🌈  BUILT FOR MODERN BUSINESSES  ⚡️",
        TAGLINE,
    ),
    (
        "AI-LED TECHNOLOGY SERVICES  💛  STRATEGIZE AUTOMATE SCALE  🌈.",
        TAGLINE_SHORT,
    ),
    ("BUILD YOUR </span>NEXT AI PLATFORM", "BUILD </span>DIGITAL PRODUCTS"),
    ("who expect disciplined AI-led execution ", "who need software, marketing, design &amp; editing "),
    ("for modern businesses. ", "that grow your brand. "),
    ("AI-led technology", "software, marketing, design &amp; editing"),
    ("AI-Led Technology", "Software &amp; Creative"),
    ("AI-led services designed to keep work moving", "Services designed to design, build, market, and edit"),
    ("AI-Led Delivery", "Software &amp; Design"),
    ("Automation Systems", "Marketing Systems"),
    ("Product Engineering", "Video Editing"),
    ("Magnence combines strategy, automation, product engineering, and dependable execution", "Magnence combines software development, marketing, design, editing, and dependable delivery"),
    ("Our work reflects disciplined AI-led delivery and clean execution.", "Our work reflects clean software builds, sharp design, and marketing that converts."),
    ("What AI-led technology services does Magnence offer?", "What software, marketing, design, and editing services does Magnence offer?"),
    ("Games Development", "Software Development"),
    ("Creative STUDIO.", "Design Studio."),
    ("CREATIVE TECHnology", "SOFTWARE &amp; CREATIVE"),
    ("CONTENT STRATEGY", "Content Marketing"),
    ("PRODUCT marketing", "Product Marketing"),
    ("Custom 3d Designs", "UI/UX Design"),
    ("Custom Game Design", "Custom Software"),
    ("Custom Development", "Web Development"),
    ("Motion Design", "Video Editing"),
    ("ai implement", "AI Integration"),
    ("Innovative Design Strategies", "Marketing &amp; Design Strategy"),
    ("Interactive Design", "Interface Design"),
    ("User-Centered Design", "User-Centered UX"),
    ("Product Designing in UX", "Product UI/UX Design"),
    ("Iterative Development", "Agile Development"),
    ("WE ARE MAGNENCE", "WE ARE MAGNENCE"),
    ("SelfGPT Studio Agency", "Software Agency"),
    ("Startup Agency", "Growth Agency"),
    ("— wide range of creative", "— software, marketing, design, editing"),
    ("Magnence is a", "Magnence is a software, marketing, design &amp; editing agency —"),
    ("Led by CEO Anurag Singh, Magnence combines strategy, AI workflows, product engineering, and dependable execution.", "Led by CEO Anurag Singh, Magnence delivers software, marketing campaigns, design systems, and polished edits under one roof."),
    ("Full-stack web apps, AI workflows, automation systems, and ongoing technical delivery.", "Websites, web apps, marketing campaigns, design systems, video edits, and ongoing support."),
    ("AI-led business websites, landing pages, and digital brand surfaces built for trust and enquiries.", "Business websites, landing pages, and brand surfaces built to attract and convert."),
    ("StayVise", "Brand Platform"),
    ("SelfGPT Studio", "SaaS Dashboard"),
    ("SelfGPT", "Web Application"),
    ("Atlas Ops", "Marketing Suite"),
    ("Pulse Commerce", "E-Commerce Build"),
    ("Harbor Stay", "Content Campaign"),
    ("3,500+/Project", "From $3,500"),
    ("4,750+/Project", "From $4,750"),
    ("5,000+/Project", "From $5,000"),
    ("TEam &amp; Talent", "Team &amp; Talent"),
    ("IN OUR Class MAGNENCE.", "WITH MAGNENCE."),
    ("design technology services company", "software, marketing, design &amp; editing agency"),
    ("technology services company", "software, marketing, design &amp; editing agency"),
    ("Magnence Home", "Magnence — Home"),
    ("displayName=\"Magnence Home\"", "displayName=\"Magnence Home\""),
]

MAGNENCE_STYLE = """<style id="magnence-overrides">
#__framer-badge-container,#__framer-badge-container-removed,.__framer-badge,
.framer-TLVk2,[class*="TLVk2"],.framer-TE6Xr,[class*="TE6Xr"],
div[class*="framer-TLVk2"],a[href*="framer.com"],a[href*="utm_campaign=freeplanbadge"],
a[title*="Framer"],[data-exported-badge]{display:none!important;visibility:hidden!important;
opacity:0!important;pointer-events:none!important;position:absolute!important;width:0!important;
height:0!important;overflow:hidden!important}
[data-framer-name="Nav Menu"],.framer-AgH81,header.framer-AgH81,.framer-xtqlxw-container,
.framer-1inyamc-container,.framer-1eixyol-container{position:sticky!important;top:0!important;z-index:2000!important}
.framer-r984el{width:150px!important;height:52px!important;aspect-ratio:2.885!important;min-width:150px!important}
.framer-r984el img{object-fit:contain!important;object-position:left center!important}
</style>"""

BADGE_SCRIPT = """<script id="magnence-badge-remover">(function(){var s=["#__framer-badge-container","#__framer-badge-container-removed",".__framer-badge","[class*='TLVk2']","[class*='TE6Xr']","a[href*='framer.com']","[data-exported-badge]"];function r(){s.forEach(function(e){document.querySelectorAll(e).forEach(function(n){n.remove()})})}r();new MutationObserver(r).observe(document.documentElement,{childList:!0,subtree:!0})})();</script>"""


def apply_content(text: str) -> str:
    for old, new in CONTENT_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def collect_referenced_assets() -> set[str]:
    refs: set[str] = set()
    pattern = re.compile(r"/assets/(?:js|images|fonts|videos)/([^\"'\\s?)]+)")
    for path in ROOT.rglob("*"):
        if path.suffix in {".html", ".mjs", ".js", ".css"} and path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            refs.update(pattern.findall(text))
            for m in re.finditer(r'from"\./([^"]+\.mjs)"', text):
                refs.add(m.group(1))
            for m in re.finditer(r'import\("\./([^"]+\.mjs)"\)', text):
                refs.add(m.group(1))
    return refs


def delete_unreferenced_assets(refs: set[str]) -> list[str]:
    removed: list[str] = []
    all_text = ""
    for p in (ROOT / "assets" / "js").rglob("*"):
        if p.is_file():
            all_text += p.read_text(encoding="utf-8", errors="ignore")
    for p in ROOT.glob("*.html"):
        all_text += p.read_text(encoding="utf-8", errors="ignore")

    for img in (ROOT / "assets" / "images").glob("*"):
        if not img.is_file():
            continue
        name = img.name
        subpath = name
        for new, old in [(v, k) for k, v in IMAGE_RENAMES.items()]:
            if name == old.split("/")[-1]:
                subpath = name
        if name not in all_text and name not in refs:
            img.unlink()
            removed.append(str(img.relative_to(ROOT)))

    dead_js = ROOT / "assets" / "js" / "PX9hIOIVM-6ZNBMRCF.mjs"
    if dead_js.exists() and dead_js.name not in all_text:
        dead_js.unlink()
        removed.append(str(dead_js.relative_to(ROOT)))

    return removed


def rename_assets() -> dict[str, str]:
    """Return old->new path mapping relative to assets/."""
    mapping: dict[str, str] = {}

    js_dir = ROOT / "assets" / "js"
    (js_dir / "pages").mkdir(parents=True, exist_ok=True)
    (js_dir / "data").mkdir(parents=True, exist_ok=True)
    (js_dir / "runtime").mkdir(parents=True, exist_ok=True)

    for old_name, new_rel in JS_RENAMES.items():
        src = js_dir / old_name
        if not src.exists():
            continue
        dst = js_dir / new_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            dst.unlink()
        shutil.move(str(src), str(dst))
        mapping[f"js/{old_name}"] = f"js/{new_rel}"
        mapping[old_name] = new_rel

    img_root = ROOT / "assets" / "images"
    (img_root / "brand").mkdir(parents=True, exist_ok=True)
    (img_root / "ui").mkdir(parents=True, exist_ok=True)

    for old_name, new_rel in IMAGE_RENAMES.items():
        src = img_root / old_name
        if not src.exists():
            continue
        dst = img_root / new_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            dst.unlink()
        shutil.move(str(src), str(dst))
        mapping[f"images/{old_name}"] = f"images/{new_rel}"
        mapping[old_name] = new_rel

    return mapping


def rewrite_paths(text: str, mapping: dict[str, str]) -> str:
    # longest keys first to avoid partial replacements
    items = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
    for old, new in items:
        text = text.replace(old, new)
    # fix imports after page moves: ./pages/foo.mjs from app.mjs stays same
    # chunks still at ./chunk-*.mjs from pages/*.mjs need ../
    text = re.sub(
        r'from"\./(chunk-[^"]+\.mjs)"',
        lambda m: f'from"../{m.group(1)}"' if "/pages/" in text[:200] else f'from"./{m.group(1)}"',
        text,
    )
    return text


def fix_page_imports():
    """Page modules live in assets/js/pages/ — point imports at ../chunk-*.mjs"""
    pages_dir = ROOT / "assets" / "js" / "pages"
    data_dir = ROOT / "assets" / "js" / "data"
    for directory in (pages_dir, data_dir):
        if not directory.exists():
            continue
        for path in directory.glob("*.mjs"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            updated = re.sub(r'from"\./(chunk-[^"]+)"', r'from"../\1"', text)
            updated = re.sub(r'import"\./(chunk-[^"]+)"', r'import"../\1"', updated)
            updated = re.sub(r'import\("\./(chunk-[^"]+)"\)', r'import("../\1")', updated)
            updated = re.sub(r'from"\./(data/[^"]+)"', r'from"../\1"', updated)
            updated = re.sub(r'import\("\./(data/[^"]+)"\)', r'import("../\1")', updated)
            if updated != text:
                path.write_text(updated, encoding="utf-8")


def fix_app_imports():
    app = ROOT / "assets" / "js" / "app.mjs"
    if not app.exists():
        return
    text = app.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r'import\("\./([^"]+\.mjs)"\)', r'import("./\1")', text)
    # page bundles now under pages/
    for name in [
        "pages/home.mjs",
        "pages/team.mjs",
        "pages/services.mjs",
        "pages/work.mjs",
        "pages/contact.mjs",
        "pages/blog.mjs",
        "pages/work-detail.mjs",
        "pages/blog-detail.mjs",
        "pages/not-found.mjs",
        "data/work-collection.mjs",
        "data/blog-collection.mjs",
    ]:
        old_hashes = [k for k, v in JS_RENAMES.items() if v == name]
        for h in old_hashes:
            text = text.replace(f'import("./{h}")', f'import("./{name}")')
            text = text.replace(f'import("./{h.split("/")[-1]}")', f'import("./{name}")')
    app.write_text(text, encoding="utf-8")


def patch_html_files(mapping: dict[str, str]):
    style_re = re.compile(r"<style id=\"magnence-overrides\">.*?</style>", re.DOTALL)
    old_style = re.compile(r"<style>\s*/\* === MAGNENCE:.*?</style>", re.DOTALL)

    for html in ROOT.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="ignore")
        text = apply_content(text)
        for old, new in mapping.items():
            text = text.replace(f"/assets/{old}", f"/assets/{new}")
            text = text.replace(old, new.split("/")[-1] if "/" in new else new)

        text = text.replace(
            "/assets/js/script_main.MQLY5MZV.mjs",
            "/assets/js/app.mjs",
        )
        text = text.replace(
            "assets/js/script_main.MQLY5MZV.mjs",
            "assets/js/app.mjs",
        )
        text = text.replace(
            "/assets/js/offline-runtime.js",
            "/assets/js/runtime/offline.js",
        )
        text = text.replace(
            "assets/js/offline-runtime.js",
            "assets/js/runtime/offline.js",
        )

        # depth fix for pages/* html
        if "/pages/" in str(html):
            text = text.replace("../../assets/js/", "/assets/js/")
            text = text.replace("../assets/js/", "/assets/js/")

        old_style.sub("", text)
        style_re.sub("", text)
        if 'id="magnence-overrides"' not in text:
            text = text.replace("</head>", MAGNENCE_STYLE + "\n</head>", 1)
        if 'id="magnence-badge-remover"' not in text:
            text = re.sub(r"(<body[^>]*>)", r"\1\n" + BADGE_SCRIPT, text, count=1)

        html.write_text(text, encoding="utf-8")


def patch_chunk_hq():
    path = ROOT / "assets" / "js" / "chunk-HQ4KIEB2.mjs"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = text.replace(
        'title:"Magnence | AI-Led Technology Services Company"',
        f'title:"{META_TITLE}"',
    )
    text = text.replace(
        "Magnence is an AI-led technology services company building intelligent websites, automation workflows, web apps, digital products, and growth systems for modern businesses.",
        META_DESC,
    )
    text = text.replace("magnence-icon.png", "brand/icon.png")
    text = text.replace("MTN7lwa706KrVikQhsFchPwMQzY.png", "brand/social-share.png")
    path.write_text(text, encoding="utf-8")


def patch_all_mjs(mapping: dict[str, str]):
    js_dir = ROOT / "assets" / "js"
    for path in js_dir.rglob("*.mjs"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = apply_content(text)
        for old, new in mapping.items():
            if old.startswith("images/"):
                text = text.replace(old.split("/")[-1], new.split("/")[-1])
                text = text.replace(f"/assets/{old}", f"/assets/{new}")
        text = re.sub(r"//\# sourceMappingURL=.*\n?", "", text)
        path.write_text(text, encoding="utf-8")


def write_manifest(mapping: dict[str, str]):
    manifest = {
        "meta_title": META_TITLE,
        "meta_description": META_DESC,
        "tagline": TAGLINE,
        "asset_map": mapping,
        "structure": {
            "assets/js/app.mjs": "Main application entry",
            "assets/js/pages/": "Route page bundles",
            "assets/js/data/": "CMS collection modules",
            "assets/js/runtime/": "Offline runtime helpers",
            "assets/js/chunk-*.mjs": "Shared vendor/runtime chunks",
            "assets/images/brand/": "Logo, icon, social images",
            "assets/images/ui/": "UI textures and decorations",
        },
    }
    (ROOT / "assets" / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def main():
    refs = collect_referenced_assets()
    removed = delete_unreferenced_assets(refs)
    mapping = rename_assets()
    fix_app_imports()
    fix_page_imports()
    patch_all_mjs(mapping)
    patch_chunk_hq()
    patch_html_files(mapping)

    # rewrite imports in app for pages paths - second pass
    app = ROOT / "assets" / "js" / "app.mjs"
    if app.exists():
        t = app.read_text(encoding="utf-8", errors="ignore")
        replacements = {
            "x6tipuAozajKXY4nU3bGLMaMtyZR68f0Tmr6NmUm1Y0.ZVF57H4K.mjs": "pages/home.mjs",
            "Z213P4Uu2IISc-NVcCY64buYvwqqS3U1W1Ur85wh6Xk.MULTWS2D.mjs": "pages/team.mjs",
            "oa_XZz1st08iS-eYxwRIvVyQZf8Auab1iRQs8NWxaCI.ADVYF7MG.mjs": "pages/services.mjs",
            "6ihs9JZk6ab6pxOZEmYXjz5RS3Q-c06RxO4pwGXKm14.KOHNG5C3.mjs": "pages/work.mjs",
            "D7LhShWt7ZIl34mAElrb3rVP7EBptxV9Nf_FbYAs80c.VMMPIYLP.mjs": "pages/contact.mjs",
            "x8eYI_Tf2HQQPrfBM9pA-bgmYjtSCSHdOrRBI1JJo8o.FCYNWKZB.mjs": "pages/blog.mjs",
            "f-zuToQL353Fm1qpthacMorW1___g3Fq2Fj13mh1ebE.2YCQ7I4U.mjs": "pages/work-detail.mjs",
            "Jgjx2G1v5-wlDRkGMZUAxDyJJz5PtNy2uQ5QNG7or0o.FVPNM5IX.mjs": "pages/blog-detail.mjs",
            "LTkd40jjTDSg-eiN0x0QwhowrZY2cHUEDwRPnZiPNi4.OICXOZPB.mjs": "pages/not-found.mjs",
            "9AT1tsnUrvnt80-C1c5NzHzXTFXdnRujVMdDd4HlRxY.4KNUDZY6.mjs": "data/work-collection.mjs",
            "Oem55xZhb-fbrtYstl5VqV6YmDkzJzH-KS9bn4VqSds.NKR4XBX7.mjs": "data/blog-collection.mjs",
        }
        for old, new in replacements.items():
            t = t.replace(f'import("./{old}")', f'import("./{new}")')
        app.write_text(t, encoding="utf-8")

    write_manifest(mapping)

    print(f"Removed {len(removed)} unused assets")
    for r in removed[:15]:
        print(f"  - {r}")
    print(f"Renamed {len(mapping)} asset paths")
    print("Wrote assets/manifest.json")


if __name__ == "__main__":
    main()
