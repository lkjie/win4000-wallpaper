from PIL import Image
import os

files = os.listdir('images')
for i, file in enumerate(files):
    if file.endswith('jpg'):
        im = Image.open("images/%s"%file,"r")
        width, height = im.size
        if height > width:
            im = im.rotate(90)
        im = im.convert("L")
        box = ((width - 1072)/2, (height - 1448)/2, (width + 1072)/2, (height + 1448)/2)
        im = im.crop(box)
        # im = im.resize((1072, 1448))
        im.save("kpwsuited/bg_ss%d.png"%i,"PNG",optimize=True,quality=70)