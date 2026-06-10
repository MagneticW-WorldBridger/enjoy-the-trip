#!/usr/bin/env python
"""QR del catálogo SVM con el logo al centro. ECC_H (corrige ~30%),
logo en badge blanco redondeado (~22% del area) -> sigue escaneando."""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
import os

URL = "https://magneticw-worldbridger.github.io/enjoy-the-trip/"
LOGO = "svm-logo.jpg"
OUT = os.path.expanduser("~/Downloads/qr-svm-logo.png")

# QR negro sobre blanco, alta correccion de error
qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=3)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="#1b1815", back_color="white").convert("RGBA")
W, H = img.size

# badge blanco redondeado
badge = int(W * 0.24)
pad = int(badge * 0.10)
b = Image.new("RGBA", (badge, badge), (0, 0, 0, 0))
d = ImageDraw.Draw(b)
r = int(badge * 0.22)
d.rounded_rectangle([0, 0, badge - 1, badge - 1], radius=r, fill="white")
# borde dorado sutil
d.rounded_rectangle([0, 0, badge - 1, badge - 1], radius=r, outline=(155, 119, 44, 255), width=max(2, badge // 90))

# logo dentro del badge (recortado a la marca, sin su fondo gris)
logo = Image.open(LOGO).convert("RGBA")
# recorta el margen gris claro del jpg quedandose con el centro util
lw, lh = logo.size
logo = logo.crop((int(lw*0.04), int(lh*0.02), int(lw*0.96), int(lh*0.98)))
target = badge - 2 * pad
logo.thumbnail((target, target), Image.LANCZOS)
lx = (badge - logo.width) // 2
ly = (badge - logo.height) // 2
b.alpha_composite(logo, (lx, ly))

# pega el badge al centro del QR
img.alpha_composite(b, ((W - badge) // 2, (H - badge) // 2))
img.convert("RGB").save(OUT, quality=95)
print(f"guardado: {OUT}  ({W}x{H}, badge {badge}px)")
