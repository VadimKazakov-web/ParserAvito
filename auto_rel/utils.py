from PIL import Image, ImageDraw


def new_icon(tag, path, new_path):
    length_tag = len(tag)
    if length_tag == 7:
        offset = 4
    elif length_tag == 6:
        offset = 25
    elif length_tag == 5:
        offset = 45
    else:
        offset = 0

    im = Image.open(path)
    frame = Image.new(mode="RGBA", size=(im.size[0], 90), color=(255, 255, 255, 200))
    draw = ImageDraw.Draw(frame)
    draw.text((offset, 0), tag, (0, 0, 139), font_size=75)
    im.paste(frame, (0, 0), frame)
    im.save(new_path)
