from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('./02.배경&프랍/4.맵/PNG/Maptile_1.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        # 배경을 타일링해서 그리기
        for x in range(0, self.canvas_width, self.w):
            for y in range(0, self.canvas_height, self.h):
                self.image.draw(x + self.w // 2, y + self.h // 2)

    def update(self):
        pass

