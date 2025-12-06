from pico2d import *
import game_framework
import game_world

class Explosion:
    """폭발 이펙트 - 애니메이션 재생 후 광역 피해"""
    images = None  # 폭발 애니메이션 프레임
    explosion_sound = None  # 폭발 사운드

    def __init__(self, x, y, damage, radius):
        self.x, self.y = x, y
        self.damage = damage  # 광역 피해량
        self.radius = radius  # 폭발 반경

        # 폭발 사운드 로드
        if Explosion.explosion_sound is None:
            Explosion.explosion_sound = load_wav('SFX/Player/Explosion.mp3')
            Explosion.explosion_sound.set_volume(40)

        # 폭발 사운드 재생 (생성 시 즉시)
        if Explosion.explosion_sound:
            Explosion.explosion_sound.play()

        # 폭발 애니메이션
        if Explosion.images is None:
            Explosion.images = []
            for i in range(1, 11):  # 10프레임
                try:
                    img = load_image(f'./05.VFX/VFX_Explosion/VFX_Explosion_1/VFX_Explosion_1_{i:04d}.png')
                    Explosion.images.append(img)
                except:
                    pass

        self.frame = 0
        self.frame_speed = 20  # 초당 20프레임 (빠른 애니메이션)
        self.time = 0
        self.is_dead = False
        self.has_dealt_damage = False  # 피해를 이미 입혔는지

    def update(self):
        self.time += game_framework.frame_time
        self.frame = int(self.time * self.frame_speed)

        # 첫 프레임에서 광역 피해 (한 번만)
        if not self.has_dealt_damage and self.frame >= 2:
            self.deal_area_damage()
            self.has_dealt_damage = True

        # 애니메이션 끝나면 제거
        if self.frame >= len(Explosion.images):
            self.is_dead = True
            game_world.remove_object(self)

    def deal_area_damage(self):
        """폭발 반경 내의 모든 적에게 피해"""
        from enemy import Enemy
        enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]

        for enemy in enemies:
            # 적과의 거리 계산
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # 폭발 반경 내에 있으면 피해
            if distance <= self.radius:
                enemy.hp -= self.damage
                enemy.hit_flash = 0.1

                # 적이 죽었는지 확인
                if enemy.hp <= 0 and not enemy.is_dead:
                    enemy.is_dead = True
                    import play_mode
                    play_mode.increase_kill_count()
                    play_mode.add_gold(10)
                    game_world.remove_object(enemy)

    def draw(self):
        if self.frame < len(Explosion.images):
            # 폭발 이펙트 크기 (반경의 2배)
            size = self.radius * 2
            Explosion.images[self.frame].draw(self.x, self.y, size, size)

            # 디버그: 폭발 반경 표시 (원)
            # draw_rectangle(self.x - self.radius, self.y - self.radius,
            #               self.x + self.radius, self.y + self.radius)

    def get_bb(self):
        # 충돌 박스는 필요 없음
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass


# 보스용 폭발 (플레이어에게 데미지)
class BossExplosion:
    """보스 폭발탄 - 플레이어에게 광역 피해"""
    images = None

    def __init__(self, x, y, damage, radius):
        self.x, self.y = x, y
        self.damage = damage
        self.radius = radius

        # 폭발 사운드 재생 (Explosion 클래스의 사운드 사용)
        if Explosion.explosion_sound:
            Explosion.explosion_sound.play()

        # 폭발 애니메이션 (동일한 이미지 사용)
        if BossExplosion.images is None:
            BossExplosion.images = []
            for i in range(1, 11):
                try:
                    img = load_image(f'./05.VFX/VFX_Explosion/VFX_Explosion_1/VFX_Explosion_1_{i:04d}.png')
                    BossExplosion.images.append(img)
                except:
                    pass

        self.frame = 0
        self.frame_speed = 20
        self.time = 0
        self.is_dead = False
        self.has_dealt_damage = False

    def update(self):
        self.time += game_framework.frame_time
        self.frame = int(self.time * self.frame_speed)

        # 첫 프레임에서 플레이어에게 피해
        if not self.has_dealt_damage and self.frame >= 2:
            self.deal_area_damage()
            self.has_dealt_damage = True

        # 애니메이션 끝나면 제거
        if self.frame >= len(BossExplosion.images):
            self.is_dead = True
            game_world.remove_object(self)

    def deal_area_damage(self):
        """폭발 반경 내의 플레이어에게 피해"""
        import play_mode
        player = play_mode.player

        if player:
            # 플레이어와의 거리 계산
            dx = player.x - self.x
            dy = player.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # 폭발 반경 내에 있으면 피해
            if distance <= self.radius:
                player.hp -= self.damage

    def draw(self):
        if self.frame < len(BossExplosion.images):
            # 폭발 이펙트 크기 (반경의 2배)
            size = self.radius * 2
            BossExplosion.images[self.frame].draw(self.x, self.y, size, size)

    def get_bb(self):
        # 충돌 박스 (광역)
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

    def handle_collision(self, group, other):
        # 폭발은 충돌해도 사라지지 않음 (애니메이션이 끝날 때까지 지속)
        pass

