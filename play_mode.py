from pico2d import *
import game_framework
import game_world
import random

from background import Background
from player import Player
from enemy import Enemy, BossBanditHG, BossBanditRPG
from ui import UI
from resource_path import resource_path

player = None
ui = None
spawn_timer = 0
spawn_interval = 3.0  # 적 스폰 간격 (2.0 -> 3.0으로 증가)
wave = 1
enemies_killed = 0
enemies_per_wave = 10  # 웨이브당 처치해야 할 적 수
wave_complete = False
game_paused = False  # 레벨업 시 일시정지
cursor_image = None
mouse_x, mouse_y = 400, 300

def handle_events():
    global mouse_x, mouse_y, wave, enemies_killed, player_gold
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # 게임 상태 저장 후 타이틀 화면으로 이동
            import title_mode
            import shop_mode
            # 현재 게임 상태 저장
            shop_mode.GameData.player_gold = player_gold
            shop_mode.GameData.saved_wave = wave
            shop_mode.GameData.saved_kills = enemies_killed
            shop_mode.GameData.has_saved_game = True
            game_framework.change_mode(title_mode)
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, get_canvas_height() - event.y
            if player:
                player.handle_event(event)
        else:
            if player:
                player.handle_event(event)

def init():
    global player, ui, spawn_timer, wave, enemies_killed, enemies_per_wave, wave_complete, game_paused, cursor_image, mouse_x, mouse_y, player_gold

    # 커서 이미지 로드
    try:
        cursor_image = load_image(resource_path('./04.GUI/PNG/Cursor_Targeting.png'))
    except:
        cursor_image = None

    # SDL 커서 숨기기
    SDL_ShowCursor(SDL_DISABLE)

    # 폭발 이펙트 이미지 미리 로드 (렉 방지)
    from explosion import Explosion, BossExplosion
    from bullet import ExplosiveBullet
    from enemy import BossExplosiveBullet

    if Explosion.images is None:
        Explosion.images = []
        for i in range(1, 11):
            try:
                img = load_image(resource_path(f'./05.VFX/VFX_Explosion/VFX_Explosion_1/VFX_Explosion_1_{i:04d}.png'))
                Explosion.images.append(img)
            except:
                pass

    if BossExplosion.images is None:
        BossExplosion.images = []
        for i in range(1, 11):
            try:
                img = load_image(resource_path(f'./05.VFX/VFX_Explosion/VFX_Explosion_1/VFX_Explosion_1_{i:04d}.png'))
                BossExplosion.images.append(img)
            except:
                pass

    # 폭발탄 이미지 미리 로드
    if ExplosiveBullet.images is None:
        ExplosiveBullet.images = []
        for i in range(1, 8):
            try:
                frame_file = f'05.VFX/VFX_Bullet/VFX_Bullet_1/VFX_Bullet_1_{i:04d}.png'
                ExplosiveBullet.images.append(load_image(frame_file))
            except:
                pass

    if BossExplosiveBullet.images is None:
        BossExplosiveBullet.images = []
        for i in range(1, 8):
            try:
                frame_file = f'05.VFX/VFX_Bullet/VFX_Bullet_1/VFX_Bullet_1_{i:04d}.png'
                BossExplosiveBullet.images.append(load_image(frame_file))
            except:
                pass

    # 배경 생성
    background = Background()
    game_world.add_object(background, 0)

    # 플레이어 생성
    player = Player()
    game_world.add_object(player, 1)

    # 선택한 무기 적용
    import shop_mode
    player.weapon_type = shop_mode.GameData.selected_weapon

    # 타이틀 상점에서 구매한 아이템 적용 (구매 횟수만큼 효과 중첩)
    for item_id in shop_mode.GameData.purchased_items:
        item = shop_mode.items[item_id]
        count = shop_mode.GameData.item_counts.get(item_id, 1)

        # 구매 횟수만큼 효과 적용
        for _ in range(count):
            if item['name'] == 'HP Boost':
                player.max_hp += 50
                player.hp = player.max_hp
            elif item['name'] == 'Speed Up':
                player.max_speed *= 1.2
            elif item['name'] == 'Damage Up':
                player.bullet_damage = int(player.bullet_damage * 1.3)
            elif item['name'] == 'Fire Rate':
                player.fire_rate = max(0.05, player.fire_rate * 0.75)

    # UI 생성
    ui = UI(player)
    game_world.add_object(ui, 3)

    spawn_timer = 0

    # 저장된 게임이 있으면 복원, 없으면 새 게임
    if shop_mode.GameData.has_saved_game:
        wave = shop_mode.GameData.saved_wave
        enemies_killed = shop_mode.GameData.saved_kills
        # 웨이브에 따라 적 수 계산
        enemies_per_wave = 10 + (wave - 1) * 30
    else:
        wave = 1
        enemies_killed = 0
        enemies_per_wave = 10

    wave_complete = False
    game_paused = False
    mouse_x, mouse_y = 400, 300
    # 타이틀 상점에서 사용한 후 남은 골드로 시작
    player_gold = shop_mode.GameData.player_gold


def update():
    global spawn_timer, spawn_interval, enemies_killed, wave, enemies_per_wave, wave_complete, game_paused

    # 게임이 일시정지 상태면 업데이트 안 함
    if game_paused:
        return

    # 플레이어가 죽었는지 체크
    if player.hp <= 0:
        import gameover_mode
        import shop_mode
        # gameover_mode의 score를 직접 설정
        gameover_mode.score = enemies_killed
        # 획득한 골드를 GameData에 저장 (다음 게임에도 유지)
        shop_mode.GameData.player_gold = player_gold
        # 게임오버 시 저장된 게임 상태 초기화
        shop_mode.GameData.has_saved_game = False
        shop_mode.GameData.saved_wave = 1
        shop_mode.GameData.saved_kills = 0
        game_framework.change_mode(gameover_mode)
        return

    # 웨이브 완료 체크
    if enemies_killed >= enemies_per_wave and not wave_complete:
        wave_complete = True
        next_wave()

    game_world.update()

    # 적 생성 타이머
    spawn_timer += game_framework.frame_time
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        spawn_enemy()

    # 충돌 페어 설정
    from bullet import EnemyBullet
    from enemy import BossExplosiveBullet
    from explosion import BossExplosion
    from item import HPItem

    bullets = [obj for obj in game_world.world[2] if not isinstance(obj, EnemyBullet) and not isinstance(obj, BossExplosiveBullet)]
    enemy_bullets = [obj for obj in game_world.world[2] if isinstance(obj, (EnemyBullet, BossExplosiveBullet, BossExplosion))]
    enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]
    items = [obj for obj in game_world.world[2] if isinstance(obj, HPItem)]

    # 플레이어 총알 vs 적 (보스 포함)
    for bullet in bullets:
        for enemy in enemies:
            game_world.add_collision_pair('bullet:enemy', bullet, enemy)

    # 플레이어 vs 적 (보스 포함)
    for enemy in enemies:
        game_world.add_collision_pair('player:enemy', player, enemy)

    # 적 총알 (보스 총알 포함) vs 플레이어
    for enemy_bullet in enemy_bullets:
        game_world.add_collision_pair('enemy_bullet:player', enemy_bullet, player)

    # 플레이어 vs HP 아이템
    for item in items:
        game_world.add_collision_pair('player:item', player, item)

    game_world.handle_collisions()

    # UI 업데이트
    ui.enemies_killed = enemies_killed
    ui.wave = wave
    ui.enemies_needed = enemies_per_wave - enemies_killed

def next_wave():
    global wave, enemies_per_wave, wave_complete, spawn_interval, game_paused, player_gold

    wave += 1

    # 웨이브마다 적 수 증가 (웨이브 1: 10, 웨이브 2: 40, 웨이브 3: 70...)
    enemies_per_wave = 10 + (wave - 1) * 30
    # 적 스폰 속도 매우 빠르게 증가 (최소 0.1초)
    spawn_interval = max(0.1, 3.0 - (wave - 1) * 0.3)

    wave_complete = False

    # 상점으로 이동 (골드를 상점에 동기화)
    game_paused = True
    import shop_mode
    shop_mode.GameData.player_gold = player_gold
    game_framework.push_mode(shop_mode)

def spawn_enemy():
    # 화면 가장자리에서 적 생성
    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()

    side = random.randint(0, 3)  # 0:위, 1:오른쪽, 2:아래, 3:왼쪽

    if side == 0:  # 위
        x = random.randint(0, canvas_width)
        y = canvas_height
    elif side == 1:  # 오른쪽
        x = canvas_width
        y = random.randint(0, canvas_height)
    elif side == 2:  # 아래
        x = random.randint(0, canvas_width)
        y = 0
    else:  # 왼쪽
        x = 0
        y = random.randint(0, canvas_height)

    # 특수몹 스폰 확률 계산 (웨이브가 높을수록 증가)
    # 웨이브 1: 10%, 웨이브 2: 15%, 웨이브 3: 20%...
    special_chance = min(0.1 + (wave - 1) * 0.05, 0.3)  # 최대 30%

    if random.random() < special_chance:
        # 특수몹 스폰 (50% 확률로 HG 또는 RPG)
        enemy_type = random.randint(0, 1)

        if enemy_type == 0:
            # Bandit_HG (샷건)
            enemy = BossBanditHG(x, y, player, wave)
        else:
            # Bandit_RPG (폭발탄)
            enemy = BossBanditRPG(x, y, player, wave)
    else:
        # 일반 적 스폰
        enemy = Enemy(x, y, player)
        # 웨이브가 높을수록 적 체력/속도 극극대폭 증가
        enemy.hp = 30 + (wave - 1) * 100  # 기본 30, 웨이브당 +100 (극대폭 증가!)
        enemy.max_hp = enemy.hp
        enemy.speed = 50 + (wave - 1) * 20  # 기본 50, 웨이브당 +20 (매우 빠르게)


    game_world.add_object(enemy, 1)


def increase_kill_count():
    global enemies_killed
    enemies_killed += 1

def add_gold(amount):
    """골드 추가 함수"""
    global player_gold
    player_gold += amount

def draw():
    clear_canvas()
    game_world.render()

    # 커스텀 커서 그리기 (가장 마지막에 그려서 모든 것 위에 표시)
    if cursor_image:
        cursor_image.draw(mouse_x, mouse_y, 50, 50)

    update_canvas()

def finish():
    game_world.clear()
    SDL_ShowCursor(SDL_ENABLE)  # 게임 종료 시 커서 다시 보이기

def pause():
    global game_paused
    game_paused = True

def resume():
    global game_paused
    game_paused = False
