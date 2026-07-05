import logging
import pathlib
import time
import autopy
import pyautogui
from PIL import Image
from find_figure.find_fig import FindFigure


class AutoGuiCapcha:

    def __init__(self):
        self.root = pathlib.Path("auto_gui") / pathlib.Path("templates")
        self.target = self.root / pathlib.Path("blue_arrow.png")
        self.title = self.root / pathlib.Path("main_anchor.png")
        self.target_img = Image.open(self.target)
        self.title_img = Image.open(self.title)
        self.screenshot = self.root / pathlib.Path("screenshot.png")
        self.center = self.target_img.width / 2, self.target_img.height / 2
        self.left_edge_x = 28
        self.box = None

    def _create_screenshot(self):
        autopy.bitmap.capture_screen().save(str(self.screenshot))

    def _find_image(self, file, target):
        needle = autopy.bitmap.Bitmap.open(str(target))
        haystack = autopy.bitmap.Bitmap.open(str(file))
        _pos = haystack.find_bitmap(needle)
        return _pos

    def _move_center(self, coordinates):
        center = (coordinates[0] + self.center[0], coordinates[1] + self.center[1])
        pyautogui.moveTo(center, duration=1)
        return center

    def _dragging(self, x):
        pyautogui.dragRel(x - self.center[0] + self.left_edge_x, button="left", duration=1.5)

    def start(self):
        # autopy.alert.alert("Приготовьтесь")
        # time.sleep(4)
        self._create_screenshot()

        coord = self._find_image(self.screenshot, self.target)
        if not coord:
            logging.warning("изображение {} не найдено".format(self.target))
            return False

        pos_title = self._find_image(self.screenshot, self.title)
        if not pos_title:
            logging.warning("изображение {} не найдено".format(self.title))
            return False

        self.box = (int(pos_title[0]), pos_title[1] + self.title_img.height,
                    coord[0] + self.title_img.width, coord[1] - 15)
        self.box = list(map(int, self.box))
        _fing_fig = FindFigure(self.screenshot, self.box)
        coordinates_long_line = _fing_fig.start()
        self.center = self._move_center(coord)
        time.sleep(1)
        self._dragging(coordinates_long_line[0])
        # autopy.alert.alert("Готово")
