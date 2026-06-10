#!/usr/bin/env python
"""Quita el fondo de las fotos de carros (BiRefNet SOTA) y las compone
sobre blanco con sombra suave de piso. Respalda originales en fotos_orig/
y guarda PNGs transparentes en fotos_transparent/ para reuso."""
import os, glob, time
from rembg import remove, new_session
from PIL import Image, ImageFilter

SRC, ORIG, TRANS = "fotos", "fotos_orig", "fotos_transparent"
os.makedirs(ORIG, exist_ok=True)
os.makedirs(TRANS, exist_ok=True)

session = new_session("birefnet-general")
files = sorted(glob.glob(f"{SRC}/*.jpg"))
print(f"{len(files)} fotos\n")

for f in files:
    t0 = time.time()
    name = os.path.basename(f)
    stem = os.path.splitext(name)[0]
    bak = os.path.join(ORIG, name)
    if not os.path.exists(bak):
        Image.open(f).convert("RGB").save(bak, quality=95)
    img = Image.open(bak).convert("RGB")          # siempre desde el original limpio
    cut = remove(img, session=session, post_process_mask=True)  # RGBA recortado
    cut.save(os.path.join(TRANS, stem + ".png"))

    W, H = cut.size
    pad = max(12, int(min(W, H) * 0.07))
    canvas = Image.new("RGBA", (W + 2 * pad, H + 2 * pad), (255, 255, 255, 255))
    alpha = cut.split()[3]
    # sombra: silueta desplazada hacia abajo, difuminada y atenuada
    sh = Image.new("L", canvas.size, 0)
    sh.paste(alpha, (pad, pad + int(pad * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(pad * 0.7)).point(lambda p: int(p * 0.40))
    shadow = Image.new("RGBA", canvas.size, (40, 34, 24, 0))
    shadow.putalpha(sh)
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.alpha_composite(cut, (pad, pad))
    canvas.convert("RGB").save(f, quality=92)
    print(f"  {name:24s} {W}x{H}  {time.time()-t0:.1f}s")

print("\nlisto")
