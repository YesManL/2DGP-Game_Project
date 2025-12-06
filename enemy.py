from pico2d import *
import game_framework
import game_world
import math
import random

class Enemy:
    images = []  # Bandit_AR 이미지 리스트 (여러 변형)
    leg_images = []  # 다리 애니메이션 이미지
    death_sounds = []  # 적 죽음 사운드
    ar_fire_sound = None  # AR 발사 사운드

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

        # Bandit_AR 이미지 로드 (여러 변형 중 랜덤 선택)
        if not Enemy.images:
            # 다양한 Bandit_AR 스프라이트 로드 (1, 2, 3, 4, 5번 사용)
            for i in [1, 2, 3, 4, 5]:
                Enemy.images.append(load_image(f'01.캐릭터&몬스터&애니메이션/적/Bandit_AR/스파인/PNG/Bandit_AR_{i}.png'))

        # 다리 애니메이션 이미지 로드
        if not Enemy.leg_images:
            for i in [1, 2, 3]:
                Enemy.leg_images.append(load_image(f'01.캐릭터&몬스터&애니메이션/적/Bandit_AR/스파인/PNG/Bandit_Leg_{i}.png'))

        # 죽음 사운드 로드
        if not Enemy.death_sounds:
            for i in [1, 2, 3]:
                sound = load_wav(f'SFX/Enemy/Enemy_Dead_{i}.mp3')
                sound.set_volume(30)  # 볼륨 설정 (0~128)
                Enemy.death_sounds.append(sound)

        # AR 발사 사운드 로드
        if not Enemy.ar_fire_sound:
            Enemy.ar_fire_sound = load_wav('SFX/Enemy/AR_Fire.mp3')
            Enemy.ar_fire_sound.set_volume(25)

        # 각 적마다 랜덤하게 이미지 선택
        self.image = random.choice(Enemy.images)

        # 다리 애니메이션
        self.leg_frame = 0
        self.leg_frame_time = 0
        self.leg_animation_speed = 0.1  # 프레임당 시간

        # 총알 발사 관련
        self.fire_cooldown = 0
        self.fire_rate = 2.0  # 2초마다 발사
        self.attack_range = 300  # 공격 사거리

        # 플레이어를 향한 각도
        self.angle = 0

        # 보스 여부
        self.is_boss = False
        self.gold_reward = 10  # 기본 적 처치 시 골드

    def update(self):
        # 플레이어를 향해 이동
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 플레이어를 향한 각도 계산 (라디안으로 저장)
        self.angle = math.atan2(dy, dx)

        # 이동 여부 체크
        is_moving = False

        # 공격 사거리 밖이면 플레이어에게 접근
        if distance > self.attack_range:
            if distance > 0:
                self.x += (dx / distance) * self.speed * game_framework.frame_time
                self.y += (dy / distance) * self.speed * game_framework.frame_time
                is_moving = True

        # 이동 중일 때만 다리 애니메이션 업데이트
        if is_moving:
            self.leg_frame_time += game_framework.frame_time
            if self.leg_frame_time >= self.leg_animation_speed:
                self.leg_frame = (self.leg_frame + 1) % 3  # 0, 1, 2 순환
                self.leg_frame_time = 0
        else:
            # 정지 시 기본 프레임
            self.leg_frame = 0
            self.leg_frame_time = 0

        # 공격 사거리 안이면 총알 발사 (단, 화면 안에 있을 때만)
        if distance <= self.attack_range and self.is_on_screen():
            self.fire_cooldown -= game_framework.frame_time
            if self.fire_cooldown <= 0:
                self.fire_bullet()
                self.fire_cooldown = self.fire_rate

        # 피격 플래시 감소
        if self.hit_flash > 0:
            self.hit_flash -= game_framework.frame_time

    def is_on_screen(self):
        """적이 화면 안에 있는지 확인"""
        canvas_width = get_canvas_width()
        canvas_height = get_canvas_height()

        # 여유 공간을 둬서 화면 경계 근처에서도 총을 쏠 수 있게 함
        margin = 50

        return (-margin <= self.x <= canvas_width + margin and
                -margin <= self.y <= canvas_height + margin)

    def fire_bullet(self):
        """플레이어를 향해 총알 발사 - 총구 위치에서 발사"""
        from bullet import EnemyBullet

        # AR 발사 사운드 재생
        if Enemy.ar_fire_sound:
            Enemy.ar_fire_sound.play()

        # 플레이어 방향으로 총알 생성
        dx = self.target.x - self.x
        dy = self.target.y - self.y

        # 총구 위치 계산 (적 이미지의 앞쪽 끝)
        # 적의 크기가 80x80이고, 이미지 중심에서 총구까지의 거리 계산
        gun_length = 45  # 35에서 45로 증가하여 총구 끝에서 정확히 발사
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

        # 다리를 몸통보다 약간 뒤쪽/아래쪽에 위치시키기 위한 오프셋 계산
        # 회전 방향의 반대쪽으로 약간 이동
        leg_offset = -8  # 음수면 뒤쪽으로 이동
        leg_x = self.x + math.cos(self.angle) * leg_offset
        leg_y = self.y + math.sin(self.angle) * leg_offset

        # 1. 다리 먼저 그리기 (뒤에 있어야 함)
        Enemy.leg_images[self.leg_frame].rotate_draw(draw_angle, leg_x, leg_y, self.width, self.height)

        # 2. 몸통 그리기 (위에 덮어서 그려짐)
        # 피격 시 깜빡임 효과 (밝게 표시)
        if self.hit_flash > 0:
            # 피격 시에는 흰색으로 밝게 표시
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h,
                                           draw_angle, '',
                                           self.x, self.y,
                                           self.width, self.height)
        else:
            self.image.rotate_draw(draw_angle, self.x, self.y, self.width, self.height)

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
                # 적이 죽으면 카운트 증가 및 골드 지급 (한 번만)
                self.is_dead = True

                # 죽음 사운드 랜덤 재생
                if Enemy.death_sounds:
                    death_sound = random.choice(Enemy.death_sounds)
                    death_sound.play()

                import play_mode
                play_mode.increase_kill_count()
                play_mode.add_gold(self.gold_reward)  # 적에 따라 다른 골드 지급

                # 일정 확률로 HP 회복 아이템 드롭 (30% 확률)
                if random.random() < 0.3:
                    from item import HPItem
                    item = HPItem(self.x, self.y)
                    game_world.add_object(item, 2)  # 아이템 레이어에 추가

                game_world.remove_object(self)


# 특수몹: Bandit_HG (샷건 사용)
class BossBanditHG(Enemy):
    boss_images = []
    boss_leg_images = []

    def __init__(self, x, y, target, wave=1):
        super().__init__(x, y, target, wave)

        # Bandit_HG 이미지 로드 (여러 변형 중 랜덤 선택)
        if not BossBanditHG.boss_images:
            # 다양한 Bandit_HG 스프라이트 로드 (1, 2, 3, 4, 5번 사용)
            for i in [1, 2, 3, 4, 5]:
                BossBanditHG.boss_images.append(load_image(f'01.캐릭터&몬스터&애니메이션/적/Bandit_HG/스파인/PNG/Bandit_HG_{i}.png'))

        # 다리 애니메이션 이미지 로드
        if not BossBanditHG.boss_leg_images:
            for i in [1, 2, 3]:
                BossBanditHG.boss_leg_images.append(load_image(f'01.캐릭터&몬스터&애니메이션/적/Bandit_HG/스파인/PNG/Bandit_Leg_{i}.png'))

        # 각 특수몹마다 랜덤하게 이미지 선택
        self.image = random.choice(BossBanditHG.boss_images)

        # 특수몹 설정 (일반 몹보다 강하지만 너무 강하진 않게)
        self.is_boss = False  # 보스가 아니라 특수몹
        self.width, self.height = 90, 90  # 일반 적보다 약간 크게
        self.max_hp = 80 + (wave - 1) * 120  # 일반 적보다 조금 높은 HP
        self.hp = self.max_hp
        self.speed = 45 + (wave - 1) * 18  # 일반 적과 비슷한 속도
        self.fire_rate = 1.8  # 빠른 공격 속도
        self.attack_range = 300  # 공격 사거리
        self.gold_reward = 30  # 특수몹은 30골드 지급

        # 샷건 패턴 (3발 산탄)
        self.bullet_spread = 30  # 총알 퍼짐 각도
        self.bullets_per_shot = 3  # 한 번에 3발

    def fire_bullet(self):
        """샷건 패턴: 3발의 산탄 발사"""
        from bullet import EnemyBullet

        # AR 발사 사운드 재생 (샷건도 일반 총 사운드 사용)
        if Enemy.ar_fire_sound:
            Enemy.ar_fire_sound.play()

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        # 총구 위치 계산
        gun_length = 55
        gun_x = self.x + math.cos(self.angle) * gun_length
        gun_y = self.y + math.sin(self.angle) * gun_length

        # 기본 각도 (degree)
        base_angle = math.degrees(self.angle) - 90

        # 3발의 총알을 퍼지게 발사
        for i in range(self.bullets_per_shot):
            # -30, 0, +30도 각도로 발사
            offset = (i - 1) * self.bullet_spread
            bullet_angle = base_angle + offset

            bullet = EnemyBullet(gun_x, gun_y, bullet_angle, speed=250, damage=10)
            game_world.add_object(bullet, 2)
            game_world.add_collision_pair('enemy_bullet:player', bullet, None)

    def draw(self):
        # 특수몹 이미지로 그리기
        draw_angle = self.angle - math.pi / 2

        # 다리를 몸통보다 약간 뒤쪽/아래쪽에 위치시키기 위한 오프셋 계산
        leg_offset = -8  # 음수면 뒤쪽으로 이동
        leg_x = self.x + math.cos(self.angle) * leg_offset
        leg_y = self.y + math.sin(self.angle) * leg_offset

        # 1. 다리 먼저 그리기 (뒤에 있어야 함)
        BossBanditHG.boss_leg_images[self.leg_frame].rotate_draw(draw_angle, leg_x, leg_y, self.width, self.height)

        # 2. 몸통 그리기 (위에 덮어서 그려짐)
        if self.hit_flash > 0:
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h,
                                           draw_angle, '',
                                           self.x, self.y,
                                           self.width, self.height)
        else:
            self.image.rotate_draw(draw_angle, self.x, self.y, self.width, self.height)

        # HP 바 표시 (일반 적보다 약간 큰 HP 바, 오렌지색)
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 1.0:
            bar_y = self.y + 55
            bar_width = 70

            # HP 바 배경 (검은색)
            draw_rectangle(self.x - bar_width//2, bar_y, self.x + bar_width//2, bar_y + 6)

            # HP 바 (오렌지색 - 특수몹)
            if hp_ratio > 0:
                filled_width = bar_width * hp_ratio
                draw_rectangle(self.x - bar_width//2, bar_y,
                             self.x - bar_width//2 + filled_width, bar_y + 6)


# 특수몹: Bandit_RPG (폭발탄 사용)
class BossBanditRPG(Enemy):
    boss_images = []
    boss_leg_images = []
    rpg_fire_sound = None  # RPG 발사 사운드

    def __init__(self, x, y, target, wave=1):
        super().__init__(x, y, target, wave)

        # Bandit_RPG 이미지 로드 (여러 변형 중 랜덤 선택)
        if not BossBanditRPG.boss_images:
            # 다양한 Bandit_RPG 스프라이트 로드 (1, 2, 3, 4, 5번 사용)
            for i in [1, 2, 3, 4, 5]:
                BossBanditRPG.boss_images.append(load_image(f'01.캐릭터&몬스터&애니메이션/적/Bandit_RPG/스파인/PNG/Bandit_RPG_{i}.png'))

        # 다리 애니메이션 이미지 로드
        if not BossBanditRPG.boss_leg_images:
            for i in [1, 2, 3]:
                BossBanditRPG.boss_leg_images.append(load_image(f'01.캐릭터&몬스터&애니메이션/적/Bandit_RPG/스파인/PNG/Bandit_Leg_{i}.png'))

        # RPG 발사 사운드 로드
        if not BossBanditRPG.rpg_fire_sound:
            BossBanditRPG.rpg_fire_sound = load_wav('SFX/Enemy/RPG_Fire.mp3')
            BossBanditRPG.rpg_fire_sound.set_volume(35)  # RPG는 좀 더 크게

        # 각 특수몹마다 랜덤하게 이미지 선택
        self.image = random.choice(BossBanditRPG.boss_images)

        # 특수몹 설정 (RPG는 HG보다 조금 더 강력)
        self.is_boss = False  # 보스가 아니라 특수몹
        self.width, self.height = 95, 95  # HG보다 약간 크게
        self.max_hp = 100 + (wave - 1) * 140  # HG보다 조금 높은 HP
        self.hp = self.max_hp
        self.speed = 40 + (wave - 1) * 15  # HG보다 조금 느림 (중화기 느낌)
        self.fire_rate = 2.2  # 느린 공격 속도 (폭발탄은 강력하므로)
        self.attack_range = 350  # 긴 사거리 (원거리 무기)
        self.gold_reward = 40  # 특수몹은 40골드 지급 (RPG가 더 어려우므로)

    def fire_bullet(self):
        """폭발탄 발사"""
        from bullet import ExplosiveBullet

        # RPG 발사 사운드 재생
        if BossBanditRPG.rpg_fire_sound:
            BossBanditRPG.rpg_fire_sound.play()

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        # 총구 위치 계산
        gun_length = 60  # RPG는 더 길게
        gun_x = self.x + math.cos(self.angle) * gun_length
        gun_y = self.y + math.sin(self.angle) * gun_length

        # 총알 각도
        bullet_angle = math.degrees(self.angle) - 90

        # 폭발탄 생성 (적 전용 - 플레이어를 향해)
        bullet = BossExplosiveBullet(gun_x, gun_y, bullet_angle, speed=200, damage=20, explosion_radius=100)
        game_world.add_object(bullet, 2)
        game_world.add_collision_pair('enemy_bullet:player', bullet, None)

    def draw(self):
        # 특수몹 이미지로 그리기
        draw_angle = self.angle - math.pi / 2

        # 다리를 몸통보다 약간 뒤쪽/아래쪽에 위치시키기 위한 오프셋 계산
        leg_offset = -8  # 음수면 뒤쪽으로 이동
        leg_x = self.x + math.cos(self.angle) * leg_offset
        leg_y = self.y + math.sin(self.angle) * leg_offset

        # 1. 다리 먼저 그리기 (뒤에 있어야 함)
        BossBanditRPG.boss_leg_images[self.leg_frame].rotate_draw(draw_angle, leg_x, leg_y, self.width, self.height)

        # 2. 몸통 그리기 (위에 덮어서 그려짐)
        if self.hit_flash > 0:
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h,
                                           draw_angle, '',
                                           self.x, self.y,
                                           self.width, self.height)
        else:
            self.image.rotate_draw(draw_angle, self.x, self.y, self.width, self.height)

        # HP 바 표시 (일반 적보다 약간 큰 HP 바, 빨간색)
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 1.0:
            bar_y = self.y + 58
            bar_width = 75

            # HP 바 배경 (검은색)
            draw_rectangle(self.x - bar_width//2, bar_y, self.x + bar_width//2, bar_y + 6)

            # HP 바 (빨간색 - 특수몹)
            if hp_ratio > 0:
                filled_width = bar_width * hp_ratio
                draw_rectangle(self.x - bar_width//2, bar_y,
                             self.x - bar_width//2 + filled_width, bar_y + 6)


# 보스 전용 폭발탄 (적이 사용)
class BossExplosiveBullet:
    """보스가 사용하는 폭발탄 - 플레이어에게 데미지"""
    images = None

    def __init__(self, x, y, angle, speed=200, damage=20, explosion_radius=100):
        self.x, self.y = x, y
        self.start_x, self.start_y = x, y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.explosion_radius = explosion_radius
        self.width, self.height = 50, 50

        self.explode_distance = 250  # 비행 거리
        self.has_exploded = False

        # 이미지 로드
        if BossExplosiveBullet.images is None:
            BossExplosiveBullet.images = []
            for i in range(1, 8):
                frame_file = f'05.VFX/VFX_Bullet/VFX_Bullet_1/VFX_Bullet_1_{i:04d}.png'
                BossExplosiveBullet.images.append(load_image(frame_file))

        # 애니메이션
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

        # 애니메이션
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
        """폭발 생성 - 플레이어에게 범위 데미지"""
        if not self.has_exploded:
            from explosion import BossExplosion

            self.has_exploded = True
            explosion = BossExplosion(self.x, self.y, self.damage, self.explosion_radius)
            game_world.add_object(explosion, 2)
            game_world.add_collision_pair('enemy_bullet:player', explosion, None)

            game_world.remove_object(self)

    def draw(self):
        BossExplosiveBullet.images[self.frame].rotate_draw(math.radians(self.angle), self.x, self.y, self.width, self.height)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'enemy_bullet:player':
            # 충돌 시 즉시 폭발
            if not self.has_exploded:
                self.explode()


