from PIL import Image, ImageDraw
import pathlib
from find_figure.fund_line.find import FindLongLineX
from find_figure.algorithms.alg import algorithm_1


def extract_figure(fact_color, draw, coordinates):
    if algorithm_1(fact_color):
        draw.point(coordinates, fill=fact_color)
        return True


def go_to_pixel(img: Image, new_img: Image):
    draw = ImageDraw.Draw(new_img)
    find_long_line_x = FindLongLineX()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            color = img.getpixel((x, y))
            if color != (255, 255, 255, 255) and extract_figure(color, draw, (x, y)):
                find_long_line_x.accumulate((x, y))
            else:
                find_long_line_x.comparison()
    return find_long_line_x.coordinates_long_line


def del_one_pixel_x(img: Image):
    draw = ImageDraw.Draw(img)
    pattern = "-*-"
    for y in range(img.size[1]):
        fact = "---"
        for x in range(img.size[0]):
            color = img.getpixel((x, y))
            if color == (255, 255, 255, 255):
                fact += "-"
            else:
                fact += "*"
            fact = fact[1:]
            if fact == pattern:
                draw.point((x - 1, y), fill=(255, 255, 255, 255))


def del_one_pixel_y(img: Image):
    draw = ImageDraw.Draw(img)
    pattern = "-*-"
    for x in range(img.size[0]):
        fact = "---"
        for y in range(img.size[1]):
            color = img.getpixel((x, y))
            if color == (255, 255, 255, 255):
                fact += "-"
            else:
                fact += "*"
            fact = fact[1:]
            if fact == pattern:
                draw.point((x, y - 1), fill=(255, 255, 255, 255))

#
# root = pathlib.Path("exp")
# for directory in root.iterdir():
#     file_name = directory / pathlib.Path("template_capcha.png")
#     file_name_result = directory / pathlib.Path("extracted_figure.png")
#     file_name_del_line = directory / pathlib.Path("extracted_figure(del_line).png")
#     file_name_long_line = directory / pathlib.Path("extracted_figure(long_line).png")
#
#     _img = Image.open(file_name)
#     box = (764, 423, 1139, 680)
#     region = _img.crop(box)
#     cut_image = Image.new("RGBA", size=_img.size, color=(255, 255, 255, 255))
#     cut_image.paste(region, box)
#     cut_image.save(file_name_result)
#
#     _img = Image.open(file_name_result)
#     new_image = Image.new("RGBA", size=_img.size, color=(255, 255, 255, 255))
#     coord = go_to_pixel(_img, new_image)
#     print("coordinates long line: {}".format(coord[0]))
#
#     # for _ in range(3):
#     #     del_one_pixel_x(new_image)
#     #     del_one_pixel_y(new_image)
#
#     new_image.save(file_name_result)
#     draw = ImageDraw.Draw(new_image)
#     for _x, _y in coord:
#         draw.point((_x, _y), fill=(255, 0, 0, 255))
#         draw.point((_x, _y + 1), fill=(255, 0, 0, 255))
#     new_image.save(file_name_long_line)
#     print(directory, "done")


