#!/usr/bin/env python3
"""Lit la date et la position GPS EXIF d'une ou plusieurs photos.

But : placer une photo du voyage sur la BONNE escale sans avoir à demander à
Hugo. La date EXIF → la fenêtre de dates de l'escale (parcours.csv) ; le GPS →
le lieu exact (ouvrir le lien Google Maps pour vérifier la ville/l'île).

Usage :
    python3 scripts/photo-exif.py <fichier.jpg> [<fichier2.jpg> ...]

Note : si une photo a été transférée via WhatsApp/Telegram, l'EXIF est souvent
supprimé (« pas de GPS ») — dans ce cas, se rabattre sur le contexte ou demander.
"""
import sys
import subprocess

try:
    from PIL import Image
except ImportError:
    # Container éphémère : on installe Pillow à la volée (rapide, sans bruit).
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "Pillow"], check=False)
    from PIL import Image

GPS_IFD = 34853


def to_deg(value):
    try:
        d, m, s = value
        return round(float(d) + float(m) / 60 + float(s) / 3600, 5)
    except Exception:
        return None


def read(path):
    try:
        exif = Image.open(path).getexif()
    except Exception as e:
        return f"{path}\n  ⚠️ EXIF illisible ({e})"
    date = exif.get(36867) or exif.get(306) or "?"  # DateTimeOriginal, sinon DateTime
    gps = exif.get_ifd(GPS_IFD)
    lat, lon = to_deg(gps.get(2)), to_deg(gps.get(4))
    if lat is not None and gps.get(1) == "S":
        lat = -lat
    if lon is not None and gps.get(3) == "W":
        lon = -lon
    if lat is not None and lon is not None:
        return f"{path}\n  date : {date} | GPS : {lat}, {lon} | https://maps.google.com/?q={lat},{lon}"
    return f"{path}\n  date : {date} | GPS : (absent — photo probablement transférée)"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for f in sys.argv[1:]:
        print(read(f))
