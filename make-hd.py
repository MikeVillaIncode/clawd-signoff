# Builds clawd-hd.gif from clawd.gif: the native 145x125 mascot, untouched,
# placed left and vertically centred on a 3x transparent canvas (435x377).
#
# Why: Conductor's chat renders every image into a fixed box (~150x130 CSS px,
# object-fit: cover) and ignores width/height attributes and inline style. A
# small GIF gets upscaled to fill the box (blurry, ~150px mascot); a padded
# canvas of the box's aspect ratio is scaled to fit instead, so the mascot's
# share of the canvas (1/3) is its on-screen size (~50px) and the 3x pixel
# density keeps it crisp on retina. Vertical centring keeps it clear of the
# box's crop whichever way the aspect drifts.
from PIL import Image, ImageSequence
src = Image.open('clawd.gif')
W, H = 435, 377
mw, mh = src.size
pos = (24, (H - mh) // 2)
frames, durs = [], []
for fr in ImageSequence.Iterator(src):
    rgba = fr.convert('RGBA')
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cv.paste(rgba, pos, rgba)
    frames.append(cv)
    durs.append(fr.info.get('duration', 80))
out = []
for f in frames:
    q = f.quantize(colors=255, method=Image.FASTOCTREE)
    q.paste(255, mask=f.getchannel('A').point(lambda a: 255 if a < 128 else 0))
    out.append(q)
out[0].save('clawd-hd.gif', save_all=True, append_images=out[1:], loop=0,
            duration=durs, transparency=255, disposal=2, optimize=False)
