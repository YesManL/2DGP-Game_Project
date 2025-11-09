from pico2d import *
import game_framework
import game_world
import math

class Enemy:
    def __init__(self, x, y, target):
        self.x, self.y = x, y
        self.width, self.height = 30, 30  # 크기 고정
        self.speed = 50
        self.target = target
        self.hp = 30
        self.max_hp = 30
        self.hit_flash = 0  # 피격 시 빨강게 깜빡임
        self.is_dead = False  # 죽음 상태 플래그

        # 임시 이미지 (나중에 적 이미지로 교체)
        self.image = None

    def update(self):
        # 플레이어를 향해 이동
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            self.x += (dx / distance) * self.speed * game_framework.frame_time
            self.y += (dy / distance) * self.speed * game_framework.frame_time

        # 피격 플래시 감소
        if self.hit_flash > 0:
            self.hit_flash -= game_framework.frame_time

    def draw(self):
        # 피격 시 더 밝은 빨간색으로 표시
        if self.hit_flash > 0:
            pass

        # 빨간색 사각형으로 표시 (크기 고정 15픽셀)
        draw_rectangle(self.x - 15, self.y - 15, self.x + 15, self.y + 15)

        # HP 바 표시
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 1.0:
            # HP 바 배경
            bar_y = self.y + 20
            draw_rectangle(self.x - 15, bar_y, self.x + 15, bar_y + 3)
            # HP 바
            if hp_ratio > 0:
                bar_width = 30 * hp_ratio
                draw_rectangle(self.x - 15, bar_y, self.x - 15 + bar_width, bar_y + 3)

    def get_bb(self):
        # 충돌 박스도 고정 크기로
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

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
