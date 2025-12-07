from pico2d import *
import game_framework
import game_world
from resource_path import resource_path

class HPItem:
    """HP 회복 아이템"""
    image = None
    item_get_sound = None  # 아이템 획득 사운드

    def __init__(self, x, y):
        if not HPItem.image:
            HPItem.image = load_image(resource_path('03.아이템&아이콘/PNG/Item_9.png'))

        # 아이템 획득 사운드 로드
        if not HPItem.item_get_sound:
            HPItem.item_get_sound = load_wav(resource_path('SFX/Player/Item_Get.mp3'))
            HPItem.item_get_sound.set_volume(30)

        self.x, self.y = x, y
        self.width, self.height = 30, 30
        self.hp_recovery = 10  # 회복량

        # 깜빡이는 효과
        self.blink_timer = 0
        self.visible = True

        # 생존 시간 (10초 후 사라짐)
        self.lifetime = 10.0

    def update(self):
        self.lifetime -= game_framework.frame_time
        if self.lifetime <= 0:
            game_world.remove_object(self)
            return

        # 깜빡이는 효과
        self.blink_timer += game_framework.frame_time
        if self.blink_timer >= 0.3:
            self.visible = not self.visible
            self.blink_timer = 0

    def draw(self):
        if self.visible:
            HPItem.image.draw(self.x, self.y, self.width, self.height)

    def get_bb(self):
        """충돌 박스 반환"""
        return self.x - self.width // 2, self.y - self.height // 2, \
               self.x + self.width // 2, self.y + self.height // 2

    def handle_collision(self, group, other):
        """플레이어와 충돌 시 HP 회복"""
        if group == 'player:item':
            # 아이템 획득 사운드 재생
            if HPItem.item_get_sound:
                HPItem.item_get_sound.play()

            # 플레이어 HP 회복
            if other.hp < other.max_hp:
                other.hp = min(other.max_hp, other.hp + self.hp_recovery)
            # 아이템 제거
            game_world.remove_object(self)

