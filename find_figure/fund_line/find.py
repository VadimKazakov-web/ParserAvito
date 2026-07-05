from PIL import Image, ImageDraw
from find_figure.settings import MAX_WIDTH_FIGURE


class FindLongLineX:
    """
    Нахождение самой широкой фигуры на картинке
    """
    def __init__(self):
        self.long_line = 0
        self.coordinates_long_line = []
        self.counter = 0
        self.coordinates = []

    def accumulate(self, coordinates):
        self.counter += 1
        self.coordinates.append(coordinates)

    def comparison(self):
        if self.counter > self.long_line and self.counter < MAX_WIDTH_FIGURE:
            self.long_line = self.counter
            self.coordinates_long_line = self.coordinates
        self.counter = 0
        self.coordinates = []


def del_small_line_x(img: Image, width):
    """
    Удаление линий по x, которые меньше width
    """
    draw = ImageDraw.Draw(img)
    counter = 0
    coordinates = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            color = img.getpixel((x, y))
            if color != (255, 255, 255, 255):
                counter += 1
                coordinates.append((x, y))
            else:
                if counter < width:
                    for _x, _y in coordinates:
                        draw.point((_x, _y), fill=(255, 255, 255, 255))
                counter = 0
                coordinates = []
