from pico2d import *
import game_framework
import game_world
import math

# Player 이동 속도 설정
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.speed = RUN_SPEED_PPS
        self.dir_x, self.dir_y = 0, 0
        self.angle = 0  # 마우스 방향으로 회전

        # 이미지 로드
        self.image = None
        self.image_width = 60  # 적절한 크기로 설정
        self.image_height = 60

        try:
            self.image = load_image('./01.캐릭터&몬스터&애니메이션/차량/Vehicle/Vehicle_M_1/Vehicle_M_1_Chasis.png')
            # 이미지가 너무 크면 스케일 다운
        except:
            # 이미지 로드 실패 시 기본 크기 사용
            pass

        self.hp = 100
        self.max_hp = 100
        self.fire_cooldown = 0
        self.fire_rate = 0.2  # 초당 발사 간격
        self.is_firing = False  # 마우스 버튼이 눌려있는지
        self.invincible_time = 0  # 무적 시간
        self.invincible_duration = 1.0  # 1초 무적

    def update(self):
        # 이동 처리
        self.x += self.dir_x * self.speed * game_framework.frame_time
        self.y += self.dir_y * self.speed * game_framework.frame_time

        # 화면 경계 체크
        canvas_width = get_canvas_width()
        canvas_height = get_canvas_height()

        self.x = clamp(25, self.x, canvas_width - 25)
        self.y = clamp(25, self.y, canvas_height - 25)

        # 발사 쿨다운 감소
        if self.fire_cooldown > 0:
            self.fire_cooldown -= game_framework.frame_time

        # 무적 시간 감소
        if self.invincible_time > 0:
            self.invincible_time -= game_framework.frame_time

        # 자동 연사
        if self.is_firing and self.fire_cooldown <= 0:
            self.fire()

    def draw(self):
        # 무적 시간일 때 깜빡임 효과
        if self.invincible_time > 0 and int(self.invincible_time * 10) % 2 == 0:
            return

        if self.image:
            # 적절한 크기로 회전하여 그리기
            self.image.rotate_draw(math.radians(self.angle), self.x, self.y, self.image_width, self.image_height)
        else:
            # 이미지가 없으면 사각형으로 표시
            draw_rectangle(self.x - 25, self.y - 25, self.x + 25, self.y + 25)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_w:
                self.dir_y += 1
            elif event.key == SDLK_s:
                self.dir_y -= 1
            elif event.key == SDLK_a:
                self.dir_x -= 1
            elif event.key == SDLK_d:
                self.dir_x += 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                self.dir_y -= 1
            elif event.key == SDLK_s:
                self.dir_y += 1
            elif event.key == SDLK_a:
                self.dir_x += 1
            elif event.key == SDLK_d:
                self.dir_x -= 1
        elif event.type == SDL_MOUSEMOTION:
            # 마우스 위치로 회전
            mx, my = event.x, get_canvas_height() - event.y
            dx = mx - self.x
            dy = my - self.y
            self.angle = math.degrees(math.atan2(dy, dx)) - 90
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                self.is_firing = True
                self.fire()
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                self.is_firing = False

    def fire(self):
        if self.fire_cooldown <= 0:
            from bullet import Bullet
            bullet = Bullet(self.x, self.y, self.angle)
            game_world.add_object(bullet, 2)
            self.fire_cooldown = self.fire_rate

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def handle_collision(self, group, other):
        if group == 'player:enemy' and self.invincible_time <= 0:
            self.hp -= 5
            self.invincible_time = self.invincible_duration
