from PIL import Image, ImageDraw


def new_icon(tag, path, new_path):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    draw.rectangle((30, 5, 230, 60), fill='white')
    draw.text((30, 3), tag, (50, 205, 50), font_size=55)
    new_img = img.resize((256, 256))
    new_img.save(new_path)
