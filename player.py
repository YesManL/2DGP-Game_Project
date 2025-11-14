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

        # 후륜 자동차 물리 시스템
        self.chassis_angle = 0  # 차체 각도 (이동 방향)
        self.turret_angle = 0   # 터렛 각도 (마우스 방향)
        self.wheel_angle = 0    # 앞바퀴 각도 (조향 각도)
        self.velocity = 0  # 현재 속도
        self.acceleration = 0  # 가속도 (-1: 후진, 0: 정지, 1: 전진)
        self.steering = 0  # 조향 (-1: 좌회전, 0: 직진, 1: 우회전)

        # 자동차 물리 파라미터
        self.max_speed = RUN_SPEED_PPS  # 최대 속도
        self.acceleration_rate = 150  # 가속도
        self.deceleration_rate = 200  # 감속도 (브레이크나 마찰)
        self.turn_speed = 120  # 회전 속도 (도/초)
        self.friction = 100  # 마찰력
        self.max_wheel_angle = 30  # 앞바퀴 최대 회전 각도

        # 이미지 로드
        self.chassis_image = None  # 차체 이미지
        self.turret_image = None   # 터렛 이미지
        self.front_tire_image = None  # 앞바퀴 이미지
        self.rear_tire_image = None  # 뒷바퀴 이미지

        self.image_width = 100  # 80에서 100으로 증가
        self.image_height = 100  # 80에서 100으로 증가
        self.turret_width = 40  # 32에서 40으로 증가 (비율 유지)
        self.turret_height = 60  # 48에서 60으로 증가 (비율 유지)
        self.tire_width = 20  # 타이어 크기
        self.tire_height = 20

        try:
            self.chassis_image = load_image('./01.캐릭터&몬스터&애니메이션/차량/Vehicle/Vehicle_S_2/Vehicle_S_2_Chassis_1.png')
            self.turret_image = load_image('./01.캐릭터&몬스터&애니메이션/차량/무장/PNG/Turret_S_5.png')
            self.front_tire_image = load_image('./01.캐릭터&몬스터&애니메이션/차량/Vehicle/Vehicle_S_2/Vehicle_S_2_Tire_1.png')
            self.rear_tire_image = load_image('./01.캐릭터&몬스터&애니메이션/차량/Vehicle/Vehicle_S_2/Vehicle_S_2_Tire_2.png')
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
        dt = game_framework.frame_time

        # 속도 업데이트 (가속/감속)
        if self.acceleration != 0:
            self.velocity += self.acceleration * self.acceleration_rate * dt
            # 최대 속도 제한
            self.velocity = clamp(-self.max_speed * 0.7, self.velocity, self.max_speed)
        else:
            # 마찰력으로 자연스럽게 감속
            if abs(self.velocity) > 0:
                friction_decel = self.friction * dt
                if self.velocity > 0:
                    self.velocity = max(0, self.velocity - friction_decel)
                else:
                    self.velocity = min(0, self.velocity + friction_decel)

        # 앞바퀴 각도 업데이트 (조향 입력에 따라)
        target_wheel_angle = self.steering * self.max_wheel_angle
        wheel_turn_speed = 180  # 바퀴 회전 속도 (도/초)

        # 부드럽게 목표 각도로 이동
        if abs(target_wheel_angle - self.wheel_angle) > 1:
            if target_wheel_angle > self.wheel_angle:
                self.wheel_angle += wheel_turn_speed * dt
            else:
                self.wheel_angle -= wheel_turn_speed * dt
            self.wheel_angle = clamp(-self.max_wheel_angle, self.wheel_angle, self.max_wheel_angle)
        else:
            self.wheel_angle = target_wheel_angle

        # 조향 (회전) - 속도가 있을 때만 회전 가능
        if self.steering != 0 and abs(self.velocity) > 10:
            # 속도에 비례하여 회전 (속도가 빠를수록 더 잘 돔)
            turn_factor = self.velocity / self.max_speed
            self.chassis_angle += self.steering * self.turn_speed * turn_factor * dt

        # 위치 업데이트 (차체 각도 방향으로 이동)
        rad = math.radians(self.chassis_angle + 90)
        self.x += math.cos(rad) * self.velocity * dt
        self.y += math.sin(rad) * self.velocity * dt

        # 화면 경계 체크
        canvas_width = get_canvas_width()
        canvas_height = get_canvas_height()
        self.x = clamp(25, self.x, canvas_width - 25)
        self.y = clamp(25, self.y, canvas_height - 25)

        # 발사 쿨다운 감소
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

        # 무적 시간 감소
        if self.invincible_time > 0:
            self.invincible_time -= dt

        # 자동 연사
        if self.is_firing and self.fire_cooldown <= 0:
            self.fire()

    def draw(self):
        # 무적 시간일 때 깜빡임 효과 - 완전히 사라지지 않고 투명하게
        if self.invincible_time > 0 and int(self.invincible_time * 10) % 2 == 0:
            # 깜빡임 시에도 반투명으로 표시
            pass

        if self.chassis_image:
            # 바퀴 위치 계산 (차체 기준)
            chassis_rad = math.radians(self.chassis_angle + 90)

            # 앞바퀴 위치 (차체 앞쪽, 좌우 양쪽)
            front_offset = 25  # 차체 중심에서 앞쪽으로 얼마나 떨어져 있는지
            side_offset = 20   # 좌우로 얼마나 떨어져 있는지

            # 좌측 앞바퀴
            front_left_x = self.x + math.cos(chassis_rad) * front_offset - math.sin(chassis_rad) * side_offset
            front_left_y = self.y + math.sin(chassis_rad) * front_offset + math.cos(chassis_rad) * side_offset

            # 우측 앞바퀴
            front_right_x = self.x + math.cos(chassis_rad) * front_offset + math.sin(chassis_rad) * side_offset
            front_right_y = self.y + math.sin(chassis_rad) * front_offset - math.cos(chassis_rad) * side_offset

            # 뒷바퀴 위치 (차체 뒤쪽, 좌우 양쪽)
            rear_offset = -25  # 차체 중심에서 뒤쪽으로

            # 좌측 뒷바퀴
            rear_left_x = self.x + math.cos(chassis_rad) * rear_offset - math.sin(chassis_rad) * side_offset
            rear_left_y = self.y + math.sin(chassis_rad) * rear_offset + math.cos(chassis_rad) * side_offset

            # 우측 뒷바퀴
            rear_right_x = self.x + math.cos(chassis_rad) * rear_offset + math.sin(chassis_rad) * side_offset
            rear_right_y = self.y + math.sin(chassis_rad) * rear_offset - math.cos(chassis_rad) * side_offset

            # 뒷바퀴 먼저 그리기 (차체 아래)
            if self.rear_tire_image:
                # 왼쪽 뒷바퀴 - 좌우반전
                self.rear_tire_image.composite_draw(0, 'h', rear_left_x, rear_left_y, self.tire_width, self.tire_height)
                # 회전 적용을 위해 rotate + flip
                self.rear_tire_image.clip_composite_draw(0, 0, self.rear_tire_image.w, self.rear_tire_image.h,
                                                         math.radians(self.chassis_angle), 'h',
                                                         rear_left_x, rear_left_y,
                                                         self.tire_width, self.tire_height)
                # 오른쪽 뒷바퀴 - 일반
                self.rear_tire_image.rotate_draw(math.radians(self.chassis_angle), rear_right_x, rear_right_y, self.tire_width, self.tire_height)

            # 차체 그리기
            self.chassis_image.rotate_draw(math.radians(self.chassis_angle), self.x, self.y, self.image_width, self.image_height)

            # 앞바퀴 그리기 (차체 위, 차체 각도 + 바퀴 조향 각도)
            if self.front_tire_image:
                front_wheel_angle = self.chassis_angle + self.wheel_angle
                # 왼쪽 앞바퀴 - 좌우반전
                self.front_tire_image.clip_composite_draw(0, 0, self.front_tire_image.w, self.front_tire_image.h,
                                                          math.radians(front_wheel_angle), 'h',
                                                          front_left_x, front_left_y,
                                                          self.tire_width, self.tire_height)
                # 오른쪽 앞바퀴 - 일반
                self.front_tire_image.rotate_draw(math.radians(front_wheel_angle), front_right_x, front_right_y, self.tire_width, self.tire_height)

            # 터렛 그리기 - y 좌표를 3픽셀 아래로 조정
            if self.turret_image:
                self.turret_image.rotate_draw(math.radians(self.turret_angle), self.x, self.y - 3, self.turret_width, self.turret_height)
        else:
            # 이미지가 없으면 사각형으로 표시
            draw_rectangle(self.x - 25, self.y - 25, self.x + 25, self.y + 25)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_w:
                self.acceleration = 1  # 전진
            elif event.key == SDLK_s:
                self.acceleration = -1  # 후진
            elif event.key == SDLK_a:
                self.steering = 1  # 좌회전
            elif event.key == SDLK_d:
                self.steering = -1  # 우회전
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                if self.acceleration > 0:
                    self.acceleration = 0
            elif event.key == SDLK_s:
                if self.acceleration < 0:
                    self.acceleration = 0
            elif event.key == SDLK_a:
                if self.steering > 0:
                    self.steering = 0
            elif event.key == SDLK_d:
                if self.steering < 0:
                    self.steering = 0
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

            # 포신 끝에서 총알 발사 (터렛 길이의 약 80% 위치)
            turret_length = 30  # 포신 길이
            rad = math.radians(self.turret_angle + 90)
            bullet_x = self.x + math.cos(rad) * turret_length
            bullet_y = self.y + math.sin(rad) * turret_length

            bullet = Bullet(bullet_x, bullet_y, self.turret_angle, self.bullet_speed, self.bullet_damage)
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
        self.acceleration = 0
        self.steering = 0
        self.is_firing = False
