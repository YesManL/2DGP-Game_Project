from pico2d import *
import game_framework
import game_world
import math

class Bullet:
    images = None

    def __init__(self, x, y, angle, speed=300, damage=10):
        self.x, self.y = x, y
        self.angle = angle
        self.speed = speed
        self.damage = damage  # 데미지 추가
        self.width, self.height = 40, 40  # 크기를 40x40으로 증가

        # 이미지 로드 (클래스 변수로 한 번만 로드)
        if Bullet.images is None:
            Bullet.images = []
            for i in range(1, 8):  # 7프레임
                frame_file = f'05.VFX/VFX_Bullet/VFX_Bullet_1/VFX_Bullet_1_{i:04d}.png'
                Bullet.images.append(load_image(frame_file))

        # 애니메이션 관련
        self.frame = 0
        self.frame_count = 7  # VFX_Bullet_1은 7프레임
        self.frame_time = 0
        self.frame_per_action = 0.05  # 프레임당 시간

        # 각도를 라디안으로 변환하여 방향 계산
        rad = math.radians(angle + 90)
        self.dir_x = math.cos(rad)
        self.dir_y = math.sin(rad)

    def update(self):
        # 위치 업데이트
        self.x += self.dir_x * self.speed * game_framework.frame_time
        self.y += self.dir_y * self.speed * game_framework.frame_time

        # 애니메이션 프레임 업데이트
        self.frame_time += game_framework.frame_time
        if self.frame_time >= self.frame_per_action:
            self.frame = (self.frame + 1) % self.frame_count
            self.frame_time = 0

        # 화면 밖으로 나가면 삭제
        if self.x < 0 or self.x > get_canvas_width() or self.y < 0 or self.y > get_canvas_height():
            game_world.remove_object(self)

    def draw(self):
        # VFX_Bullet_1 애니메이션 이미지로 그리기
        # 총알의 각도만큼 회전하여 그리기
        Bullet.images[self.frame].rotate_draw(math.radians(self.angle), self.x, self.y, self.width, self.height)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'bullet:enemy':
            game_world.remove_object(self)
