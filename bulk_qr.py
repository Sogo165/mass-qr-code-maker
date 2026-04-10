#!/usr/bin/env python3
"""
Generátor QR kódů z více URL.

Příklady:
  # z příkazové řádky (čárkami oddělené)
  python bulk_qr.py --urls "https://a.cz, https://b.cz, https://c.cz"

  # ze souboru (každý řádek nebo čárkami)
  python bulk_qr.py --input urls.txt

  # PNG, chyba H, větší měřítko, do složky out a se ZIPem
  python bulk_qr.py --input urls.txt --format png --ec H --scale 8 --out out --zip
"""

import argparse
import os
import re
import sys
import zipfile
from pathlib import Path
from typing import List

import segno

URL_SPLIT_REGEX = re.compile(r"[,\n\r]+")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Hromadné generování QR kódů z více URL.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--urls", help="Seznam URL oddělených čárkami (může obsahovat mezery).")
    g.add_argument("--input", help="Cesta k souboru s URL (každý řádek nebo čárkami oddělené).")

    p.add_argument("--format", choices=["png", "svg"], default="png", help="Výstupní formát (default: png).")
    p.add_argument("--ec", choices=["L", "M", "Q", "H"], default="M", help="Error correction level (default: M).")
    p.add_argument("--scale", type=int, default=6, help="Měřítko pixelů / velikost modulu (default: 6).")
    p.add_argument("--border", type=int, default=4, help="Okraj v modulech (default: 4).")
    p.add_argument("--prefix", default="qr_", help="Prefix názvů souborů (default: qr_).")
    p.add_argument("--out", default="qr_out", help="Cílová složka (default: qr_out).")
    p.add_argument("--zip", action="store_true", help="Zabalit výsledky do ZIP archivu.")
    p.add_argument("--delimiter", default=None, help="Vlastní oddělovač (pokud nechceš čárku/nový řádek).")
    return p.parse_args()

def read_urls_from_string(s: str, delimiter: str = None) -> List[str]:
    if delimiter:
        parts = [x.strip() for x in s.split(delimiter)]
    else:
        parts = [x.strip() for x in URL_SPLIT_REGEX.split(s)]
    return [x for x in parts if x]

def read_urls_from_file(path: str, delimiter: str = None) -> List[str]:
    text = Path(path).read_text(encoding="utf-8")
    return read_urls_from_string(text, delimiter=delimiter)

def looks_like_url(s: str) -> bool:
    return bool(re.match(r"^(https?://|www\.)\S+$", s, re.IGNORECASE))

def slugify_from_url(url: str) -> str:
    # zkuste získat smysluplné jméno ze URL
    try:
        clean = re.sub(r"^[a-z]+://", "", url, flags=re.IGNORECASE)  # bez schématu
        clean = clean.split("?")[0].split("#")[0]
        # poslední segment cesty nebo doména
        parts = [p for p in re.split(r"[\/]", clean) if p]
        base = parts[-1] if parts else clean
        # odstranit přípony typu .html atd.
        base = re.sub(r"\.[a-z0-9]{1,6}$", "", base, flags=re.IGNORECASE)
        # bezpečné pro souborový systém
        base = re.sub(r"[^a-z0-9\-_.]+", "-", base.lower())
        base = base.strip("-._")
        return base or "link"
    except Exception:
        return "link"

def unique_name(target_dir: Path, base: str, ext: str, existing: set) -> str:
    name = f"{base}.{ext}"
    i = 2
    while name in existing or (target_dir / name).exists():
        name = f"{base}-{i}.{ext}"
        i += 1
    existing.add(name)
    return name

def save_qr(url: str, out_dir: Path, fmt: str, ec: str, scale: int, border: int, prefix: str, existing: set) -> str:
    q = segno.make(url, error=ec)
    base = slugify_from_url(url)
    filename = unique_name(out_dir, f"{prefix}{base}", fmt, existing)
    out_path = out_dir / filename
    if fmt == "png":
        q.save(out_path, scale=scale, border=border)
    else:  # svg
        q.save(out_path, border=border, scale=scale)
    return str(out_path)

def main():
    args = parse_args()

    # načtení URL
    if args.urls:
        urls = read_urls_from_string(args.urls, delimiter=args.delimiter)
    else:
        urls = read_urls_from_file(args.input, delimiter=args.delimiter)

    # základní kontrola
    cleaned = []
    for u in urls:
        u = u.strip()
        if not u:
            continue
        # doplníme http, pokud chybí
        if not re.match(r"^[a-z]+://", u, re.IGNORECASE):
            if looks_like_url(u):
                u = "https://" + u
        cleaned.append(u)

    if not cleaned:
        print("Nenalezeny žádné URL. Zkontroluj vstup.", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing = set()
    saved_files = []
    errors = []

    for idx, url in enumerate(cleaned, start=1):
        try:
            path = save_qr(
                url=url,
                out_dir=out_dir,
                fmt=args.format,
                ec=args.ec,
                scale=max(1, args.scale),
                border=max(0, args.border),
                prefix=args.prefix,
                existing=existing,
            )
            print(f"[OK] {url} -> {path}")
            saved_files.append(path)
        except Exception as e:
            print(f"[ERR] {url} -> {e}", file=sys.stderr)
            errors.append((url, str(e)))

    # ZIP archiv
    if args.zip and saved_files:
        zip_path = Path(out_dir) / "qr_codes.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in saved_files:
                zf.write(f, arcname=os.path.basename(f))
        print(f"\nArchiv vytvořen: {zip_path}")

    # Shrnutí
    print(f"\nHotovo. Úspěšně: {len(saved_files)} | Chyby: {len(errors)}")
    if errors:
        print("Problémové položky:")
        for u, e in errors:
            print(f"  - {u} -> {e}")

if __name__ == "__main__":
    main()
