from pico2d import *
import game_framework
import game_world
import math
import random

class Enemy:
    image = None  # Bandit_AR 이미지

    def __init__(self, x, y, target, wave=1):
        self.x, self.y = x, y
        self.width, self.height = 80, 80  # Bandit_AR 크기
        self.speed = 50 + (wave - 1) * 5  # 웨이브마다 속도 증가
        self.target = target

        # 웨이브에 따라 HP 증가
        self.max_hp = 30 + (wave - 1) * 50
        self.hp = self.max_hp
        self.hit_flash = 0  # 피격 시 빨강게 깜빡임
        self.is_dead = False  # 죽음 상태 플래그

        # Bandit_AR 이미지 로드
        if Enemy.image is None:
            Enemy.image = load_image('01.캐릭터&몬스터&애니메이션/적/Bandit_AR/스파인/PNG/Bandit_AR_2.png')

        # 총알 발사 관련
        self.fire_cooldown = 0
        self.fire_rate = 2.0  # 2초마다 발사
        self.attack_range = 300  # 공격 사거리

        # 플레이어를 향한 각도
        self.angle = 0

    def update(self):
        # 플레이어를 향해 이동
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 플레이어를 향한 각도 계산 (라디안으로 저장)
        self.angle = math.atan2(dy, dx)

        # 공격 사거리 밖이면 플레이어에게 접근
        if distance > self.attack_range:
            if distance > 0:
                self.x += (dx / distance) * self.speed * game_framework.frame_time
                self.y += (dy / distance) * self.speed * game_framework.frame_time

        # 공격 사거리 안이면 총알 발사
        if distance <= self.attack_range:
            self.fire_cooldown -= game_framework.frame_time
            if self.fire_cooldown <= 0:
                self.fire_bullet()
                self.fire_cooldown = self.fire_rate

        # 피격 플래시 감소
        if self.hit_flash > 0:
            self.hit_flash -= game_framework.frame_time

    def fire_bullet(self):
        """플레이어를 향해 총알 발사 - 총구 위치에서 발사"""
        from bullet import EnemyBullet

        # 플레이어 방향으로 총알 생성
        dx = self.target.x - self.x
        dy = self.target.y - self.y

        # 총구 위치 계산 (적 이미지의 앞쪽 끝)
        gun_length = 35  # 총구까지의 거리
        gun_x = self.x + math.cos(self.angle) * gun_length
        gun_y = self.y + math.sin(self.angle) * gun_length

        # 총알 각도는 degree로 변환하고 이미지 회전 보정 (-90도)
        bullet_angle = math.degrees(self.angle) - 90

        bullet = EnemyBullet(gun_x, gun_y, bullet_angle, speed=200, damage=5)
        game_world.add_object(bullet, 2)  # 총알 레이어에 추가
        game_world.add_collision_pair('enemy_bullet:player', bullet, None)

    def draw(self):
        # 이미지 회전 각도
        # Bandit_AR 이미지는 기본적으로 위쪽을 향하고 있으므로 -90도 보정 필요
        draw_angle = self.angle - math.pi / 2  # 90도를 라디안으로 빼기

        # 피격 시 깜빡임 효과 (밝게 표시)
        if self.hit_flash > 0:
            # 피격 시에는 흰색으로 밝게 표시
            Enemy.image.clip_composite_draw(0, 0, Enemy.image.w, Enemy.image.h,
                                           draw_angle, '',
                                           self.x, self.y,
                                           self.width, self.height)
            # 추가로 빨간색 사각형 오버레이
            draw_rectangle(self.x - self.width//2, self.y - self.height//2,
                         self.x + self.width//2, self.y + self.height//2)
        else:
            Enemy.image.rotate_draw(draw_angle, self.x, self.y, self.width, self.height)

        # HP 바 표시
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 1.0:
            # HP 바 배경 (검은색)
            bar_y = self.y + 50
            bar_width = 60
            draw_rectangle(self.x - bar_width//2, bar_y, self.x + bar_width//2, bar_y + 5)

            # HP 바 (빨간색)
            if hp_ratio > 0:
                filled_width = bar_width * hp_ratio
                draw_rectangle(self.x - bar_width//2, bar_y,
                             self.x - bar_width//2 + filled_width, bar_y + 5)

    def get_bb(self):
        # 충돌 박스
        half_w = self.width // 2
        half_h = self.height // 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'player:enemy':
            pass
        elif group == 'bullet:enemy':
            # 총알의 데미지만큼 HP 감소
            damage = other.damage if hasattr(other, 'damage') else 10
            self.hp -= damage
            self.hit_flash = 0.1  # 0.1초간 피격 표시
            if self.hp <= 0 and not self.is_dead:
                # 적이 죽으면 카운트 증가 (한 번만)
                self.is_dead = True
                import play_mode
                play_mode.increase_kill_count()
                game_world.remove_object(self)
