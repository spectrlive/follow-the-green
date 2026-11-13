# Recolore les personnages de la planche en verts Keep Hush, les pixelise et ajoute une ombre.
# Usage : python3 tools/process_characters.py <dossier des originaux> <hauteur en pixels>
import sys, colorsys, glob, os
import numpy as np
from PIL import Image
src, target_h = sys.argv[1], int(sys.argv[2])
G = np.array([38, 253, 117]); MINT = np.array([186, 255, 212])
def recolor(im, keep_top=0.0):
    a = np.array(im.convert('RGBA')).astype(float); rgb = a[..., :3] / 255
    out = a.copy()
    h, w = rgb.shape[:2]
    for y in range(h):
        for x in range(w):
            if a[y, x, 3] < 10: continue
            r, g, b = rgb[y, x]; hh, s, v = colorsys.rgb_to_hsv(r, g, b); deg = hh * 360
            if 250 <= deg <= 350 and ((s > .30 and v > .30) or (s > .42 and v > .08 and y > keep_top * h)):          # violet et rose
                if v < .5:                              # violet sombre -> vert profond
                    nr, ng, nb = colorsys.hsv_to_rgb(148 / 360, .72, min(1, v * 1.25))
                    out[y, x, :3] = np.array([nr, ng, nb]) * 255
                else:                                   # rose vif -> vert Keep Hush
                    out[y, x, :3] = G * min(1, v * 1.05)
            elif s > .45 and 40 <= deg <= 72:           # jaune -> menthe claire
                out[y, x, :3] = MINT * min(1, v * 1.02)
    return Image.fromarray(out.astype(np.uint8))
def pixelate(im, th):
    w = max(1, round(im.width * th / im.height))
    a = np.array(im).astype(float); a[..., :3] *= a[..., 3:4] / 255      # alpha prémultiplié
    small = Image.fromarray(a.astype(np.uint8)).resize((w, th), Image.BOX)
    s = np.array(small).astype(float); al = s[..., 3:4]
    s[..., :3] = np.where(al > 0, s[..., :3] * 255 / np.maximum(al, 1), 0)
    s[..., 3] = np.where(s[..., 3] > 110, 255, 0)
    res = Image.fromarray(np.clip(s, 0, 255).astype(np.uint8))
    rgb = res.convert('RGB').quantize(colors=28, method=Image.Quantize.MEDIANCUT).convert('RGB')
    res = Image.merge('RGBA', (*rgb.split(), res.split()[3]))
    return res.crop(res.getbbox())
done = {}
for f in sorted(glob.glob(os.path.join(src, '*.png'))):
    name = os.path.basename(f)
    done[name] = pixelate(recolor(Image.open(f), 0 if name.startswith('mystery') else .36), target_h)
groups = {}
for name, p in done.items():
    groups.setdefault(name.rsplit('-', 1)[0], []).append(p)
size = {k: (max(p.width for p in v) + 6, max(p.height for p in v) + 3) for k, v in groups.items()}
for f, p in done.items():
    f = os.path.join(src, f)
    cw, chh = size[os.path.basename(f).rsplit('-', 1)[0]]
    canvas = Image.new('RGBA', (cw, chh), (0, 0, 0, 0))
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); px = sh.load()
    cx, cy, rx = canvas.width / 2, canvas.height - 2, p.width * .42
    for y in range(canvas.height - 4, canvas.height):
        for x in range(canvas.width):
            if ((x - cx) / rx) ** 2 + ((y - cy) / 1.6) ** 2 <= 1: px[x, y] = (0, 0, 0, 120)
    canvas.alpha_composite(sh); canvas.alpha_composite(p, ((cw - p.width) // 2, chh - 3 - p.height))
    canvas.save(os.path.join('assets/sprites', os.path.basename(f)))
    print(os.path.basename(f), canvas.size)
