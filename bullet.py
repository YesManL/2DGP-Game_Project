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


# 적 전용 총알 클래스
class EnemyBullet:
    images = None

    def __init__(self, x, y, angle, speed=200, damage=5):
        self.x, self.y = x, y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.width, self.height = 30, 30  # 적 총알은 조금 작게

        # 적 총알용 이미지 로드 (동일한 VFX 사용하되 색상이 다르게 보이도록)
        if EnemyBullet.images is None:
            EnemyBullet.images = []
            for i in range(1, 8):  # 7프레임
                frame_file = f'05.VFX/VFX_Bullet/VFX_Bullet_1/VFX_Bullet_1_{i:04d}.png'
                EnemyBullet.images.append(load_image(frame_file))

        # 애니메이션 관련
        self.frame = 0
        self.frame_count = 7
        self.frame_time = 0
        self.frame_per_action = 0.05

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
        # 적 총알은 빨간색 틴트를 적용 (optional)
        EnemyBullet.images[self.frame].rotate_draw(math.radians(self.angle), self.x, self.y, self.width, self.height)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, group, other):
        if group == 'enemy_bullet:player':
            game_world.remove_object(self)


# 폭발탄 클래스 (Explosive Bullet)
class ExplosiveBullet:
    """폭발 효과가 있는 특수 총알 - 지연식 폭발"""
    images = None

    def __init__(self, x, y, angle, speed=250, damage=15, explosion_radius=80):
        self.x, self.y = x, y
        self.start_x, self.start_y = x, y  # 시작 위치 저장
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.explosion_radius = explosion_radius  # 폭발 반경
        self.width, self.height = 50, 50  # 폭발탄은 크게

        # 지연 폭발 설정
        self.explode_distance = 200  # 200px 비행 후 폭발 (짧은 거리)
        self.has_exploded = False

        # 폭발탄용 이미지 (기본 총알보다 크게)
        if ExplosiveBullet.images is None:
            ExplosiveBullet.images = []
            for i in range(1, 8):
                frame_file = f'05.VFX/VFX_Bullet/VFX_Bullet_1/VFX_Bullet_1_{i:04d}.png'
                ExplosiveBullet.images.append(load_image(frame_file))

        # 애니메이션 관련
        self.frame = 0
        self.frame_count = 7
        self.frame_time = 0
        self.frame_per_action = 0.05

        # 방향 계산
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

        # 비행 거리 계산
        dx = self.x - self.start_x
        dy = self.y - self.start_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # 일정 거리 비행 후 폭발
        if distance >= self.explode_distance and not self.has_exploded:
            self.explode()

        # 화면 밖으로 나가면 삭제
        if self.x < 0 or self.x > get_canvas_width() or self.y < 0 or self.y > get_canvas_height():
            game_world.remove_object(self)

    def explode(self):
        """폭발 생성"""
        if not self.has_exploded:
            from explosion import Explosion
            explosion = Explosion(self.x, self.y, self.damage, self.explosion_radius)
            game_world.add_object(explosion, 2)
            self.has_exploded = True
            game_world.remove_object(self)

    def draw(self):
        # 폭발탄은 좀 더 밝게 표시
        ExplosiveBullet.images[self.frame].rotate_draw(math.radians(self.angle), self.x, self.y, self.width, self.height)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        # 적과 충돌해도 즉시 폭발하지 않음 (지연식이므로 무시)
        pass
