from pico2d import *
import random
from resource_path import resource_path

class Background:
    def __init__(self):
        # 메인 배경 타일
        self.image = load_image(resource_path('./02.배경&프랍/4.맵/PNG/Maptile_1.png'))
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

        # 프랍(장애물) 이미지들 로드
        self.props = []
        try:
            prop_images = [
                load_image(resource_path('./02.배경&프랍/4.맵/PNG/Prop_Container_1.png')),
                load_image(resource_path('./02.배경&프랍/4.맵/PNG/Prop_Container_2.png')),
                load_image(resource_path('./02.배경&프랍/4.맵/PNG/Prop_Wreck_S_1.png')),
                load_image(resource_path('./02.배경&프랍/4.맵/PNG/Prop_Wreck_S_2.png')),
            ]

            # 랜덤하게 프랍 배치 (10~15개)
            num_props = random.randint(10, 15)
            for _ in range(num_props):
                prop_img = random.choice(prop_images)
                x = random.randint(50, self.canvas_width - 50)
                y = random.randint(50, self.canvas_height - 50)
                size = random.uniform(0.8, 1.5)  # 크기 변화
                self.props.append({
                    'image': prop_img,
                    'x': x,
                    'y': y,
                    'size': size,
                    'rotation': random.uniform(0, 360)  # 랜덤 회전
                })
        except:
            pass

    def draw(self):
        # 배경을 타일링해서 그리기
        for x in range(0, self.canvas_width, self.w):
            for y in range(0, self.canvas_height, self.h):
                self.image.draw(x + self.w // 2, y + self.h // 2)

        # 프랍들 그리기
        for prop in self.props:
            img = prop['image']
            width = int(img.w * prop['size'])
            height = int(img.h * prop['size'])
            img.rotate_draw(prop['rotation'] * 3.14159 / 180, prop['x'], prop['y'], width, height)

    def update(self):
        pass

