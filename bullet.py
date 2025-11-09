from pico2d import *
import game_framework
import game_world
import math

class Bullet:
    def __init__(self, x, y, angle, speed=300, damage=10):
        self.x, self.y = x, y
        self.angle = angle
        self.speed = speed
        self.damage = damage  # 데미지 추가
        self.width, self.height = 5, 5

        # 각도를 라디안으로 변환하여 방향 계산
        rad = math.radians(angle + 90)
        self.dir_x = math.cos(rad)
        self.dir_y = math.sin(rad)

    def update(self):
        self.x += self.dir_x * self.speed * game_framework.frame_time
        self.y += self.dir_y * self.speed * game_framework.frame_time

        # 화면 밖으로 나가면 삭제
        if self.x < 0 or self.x > get_canvas_width() or self.y < 0 or self.y > get_canvas_height():
            game_world.remove_object(self)

    def draw(self):
        # 노란색 작은 원으로 표시
        draw_rectangle(self.x - 2, self.y - 2, self.x + 2, self.y + 2)

    def get_bb(self):
        return self.x - 2, self.y - 2, self.x + 2, self.y + 2

    def handle_collision(self, group, other):
        if group == 'bullet:enemy':
            game_world.remove_object(self)
