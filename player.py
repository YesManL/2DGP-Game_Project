from pico2d import *
import game_framework
import game_world
import math

# Player 이동 속도 설정
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0  # 15에서 10으로 더 감소
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.speed = RUN_SPEED_PPS
        self.dir_x, self.dir_y = 0, 0
        self.chassis_angle = 0  # 차체 각도 (이동 방향)
        self.turret_angle = 0   # 터렛 각도 (마우스 방향)

        # 이미지 로드
        self.chassis_image = None  # 차체 이미지
        self.turret_image = None   # 터렛 이미지
        self.image_width = 100  # 80에서 100으로 증가
        self.image_height = 100  # 80에서 100으로 증가
        self.turret_width = 40  # 32에서 40으로 증가 (비율 유지)
        self.turret_height = 60  # 48에서 60으로 증가 (비율 유지)

        try:
            self.chassis_image = load_image('./01.캐릭터&몬스터&애니메이션/차량/Vehicle/Vehicle_S_2/Vehicle_S_2_Chassis_1.png')
            self.turret_image = load_image('./01.캐릭터&몬스터&애니메이션/차량/무장/PNG/Turret_S_5.png')
        except:
            pass

        self.hp = 100
        self.max_hp = 100
        self.fire_cooldown = 0
        self.fire_rate = 0.2  # 초당 발사 간격
        self.is_firing = False  # 마우스 버튼이 눌려있는지
        self.invincible_time = 0  # 무적 시간
        self.invincible_duration = 1.0  # 1초 무적

        # 업그레이드 가능한 스탯들
        self.bullet_damage = 10  # 총알 데미지
        self.bullet_speed = 300  # 총알 속도
        self.level = 1

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
        # 무적 시간일 때 깜빡임 효과 - 완전히 사라지지 않고 투명하게
        if self.invincible_time > 0 and int(self.invincible_time * 10) % 2 == 0:
            # 깜빡임 시에도 반투명으로 표시
            pass

        if self.chassis_image:
            # 차체 그리기
            self.chassis_image.rotate_draw(math.radians(self.chassis_angle), self.x, self.y, self.image_width, self.image_height)

            # 터렛 그리기 - y 좌표를 3픽셀 아래로 조정
            if self.turret_image:
                self.turret_image.rotate_draw(math.radians(self.turret_angle), self.x, self.y - 3, self.turret_width, self.turret_height)
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
            # 마우스 위치로 터렛 회전
            mx, my = event.x, get_canvas_height() - event.y
            dx = mx - self.x
            dy = my - self.y
            self.turret_angle = math.degrees(math.atan2(dy, dx)) - 90
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
            bullet = Bullet(self.x, self.y, self.turret_angle, self.bullet_speed, self.bullet_damage)
            game_world.add_object(bullet, 2)
            self.fire_cooldown = self.fire_rate

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def handle_collision(self, group, other):
        if group == 'player:enemy' and self.invincible_time <= 0:
            self.hp -= 5
            self.invincible_time = self.invincible_duration

    def reset_input_state(self):
        """입력 상태 초기화 - 업그레이드 화면 후 호출"""
        self.dir_x = 0
        self.dir_y = 0
        self.is_firing = False
