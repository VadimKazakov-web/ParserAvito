from PIL import Image, ImageDraw


def new_icon(tag, path):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    draw.rectangle((59, 10, 195, 50), fill='white')
    draw.text((56, 5), tag, (50, 205, 50), font_size=40)
    new_img = img.resize((256, 256))
    new_img.save('icon.png')
    new_img.show()