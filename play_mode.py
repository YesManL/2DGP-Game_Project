from pico2d import *
import game_framework
import game_world
import random

from background import Background
from player import Player
from enemy import Enemy
from ui import UI

player = None
ui = None
spawn_timer = 0
spawn_interval = 2.0  # 적 스폰 간격
wave = 1
enemies_killed = 0
enemies_per_wave = 10  # 웨이브당 처치해야 할 적 수
wave_complete = False
game_paused = False  # 레벨업 시 일시정지

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if player:
                player.handle_event(event)

def init():
    global player, ui, spawn_timer, wave, enemies_killed, enemies_per_wave, wave_complete, game_paused

    # 배경 생성
    background = Background()
    game_world.add_object(background, 0)

    # 플레이어 생성
    player = Player()
    game_world.add_object(player, 1)

    # UI 생성
    ui = UI(player)
    game_world.add_object(ui, 3)

    spawn_timer = 0
    wave = 1
    enemies_killed = 0
    enemies_per_wave = 10
    wave_complete = False
    game_paused = False

def update():
    global spawn_timer, spawn_interval, enemies_killed, wave, enemies_per_wave, wave_complete, game_paused

    # 게임이 일시정지 상태면 업데이트 안 함
    if game_paused:
        return

    # 플레이어가 죽었는지 체크
    if player.hp <= 0:
        import gameover_mode
        gameover_mode.set_score(enemies_killed)
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
    bullets = [obj for obj in game_world.world[2]]
    enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]

    for bullet in bullets:
        for enemy in enemies:
            game_world.add_collision_pair('bullet:enemy', bullet, enemy)

    for enemy in enemies:
        game_world.add_collision_pair('player:enemy', player, enemy)

    game_world.handle_collisions()

    # UI 업데이트
    ui.enemies_killed = enemies_killed
    ui.wave = wave
    ui.enemies_needed = enemies_per_wave - enemies_killed

def next_wave():
    global wave, enemies_per_wave, wave_complete, spawn_interval, game_paused

    wave += 1
    enemies_per_wave += 30  # 웨이브마다 30마리씩 증가 (25에서 증가!)
    wave_complete = False

    # 적 스폰 속도 매우 빠르게 증가 (최소 0.1초)
    spawn_interval = max(0.1, spawn_interval - 0.3)

    # 레벨업 화면으로 전환
    game_paused = True
    import upgrade_mode
    game_framework.push_mode(upgrade_mode)

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

    # 웨이브가 높을수록 적 체력/속도 극극대폭 증가
    enemy = Enemy(x, y, player)
    enemy.hp = 30 + (wave - 1) * 100  # 기본 30, 웨이브당 +100 (극대폭 증가!)
    enemy.max_hp = enemy.hp
    enemy.speed = 50 + (wave - 1) * 20  # 기본 50, 웨이브당 +20 (매우 빠르게)

    # 웨이브가 높으면 적 크기도 더 크게 증가
    if wave >= 3:
        enemy.width = 30 + (wave - 2) * 8
        enemy.height = 30 + (wave - 2) * 8

    game_world.add_object(enemy, 1)

def increase_kill_count():
    global enemies_killed
    enemies_killed += 1

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    global game_paused
    game_paused = True

def resume():
    global game_paused
    game_paused = False
