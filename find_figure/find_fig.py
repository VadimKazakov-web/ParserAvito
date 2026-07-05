from PIL import Image, ImageDraw
from find_figure.utils import go_to_pixel


class FindFigure:

    def __init__(self, screenshot, box):
        self.screenshot = screenshot
        self.box = box
        self.img = Image.open(self.screenshot)

    def _cut_place(self):
        region = self.img.crop(self.box)
        cut_image = Image.new("RGBA", size=self.img.size, color=(255, 255, 255, 255))
        cut_image.paste(region, self.box)
        return cut_image

    def _find_figure(self, img, new_image):
        coord = go_to_pixel(img, new_image)
        print("coordinates long line: {}".format(coord[0]))
        return coord

    def start(self):
        cut_place = self._cut_place()
        new_image = Image.new("RGBA", size=cut_place.size, color=(255, 255, 255, 255))
        coord = self._find_figure(cut_place, new_image)
        draw = ImageDraw.Draw(new_image)
        for _x, _y in coord:
            draw.point((_x, _y), fill=(255, 0, 0, 255))
            draw.point((_x, _y + 1), fill=(255, 0, 0, 255))
        return coord[0]


