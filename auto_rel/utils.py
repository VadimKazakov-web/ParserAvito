from PIL import Image, ImageDraw


def new_icon(tag, path, new_path):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    draw.rectangle((40, 5, 220, 60), fill='white')
    draw.ellipse((15, 5, 60, 60), fill="white")
    draw.ellipse((196, 5, 241, 60), fill="white")
    draw.text((40, 0), tag, (50, 205, 50), font_size=58)
    new_img = img.resize((256, 256))
    new_img.save(new_path)
