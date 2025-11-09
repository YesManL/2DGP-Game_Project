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
spawn_interval = 2.0  # 2초마다 적 생성
wave = 1
enemies_killed = 0

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
    global player, ui, spawn_timer, wave, enemies_killed

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

def update():
    global spawn_timer, spawn_interval, enemies_killed

    # 플레이어가 죽었는지 체크
    if player.hp <= 0:
        import gameover_mode
        gameover_mode.set_score(enemies_killed)
        game_framework.change_mode(gameover_mode)
        return

    game_world.update()

    # 적 생성 타이머
    spawn_timer += game_framework.frame_time
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        spawn_enemy()

    # 충돌 페어 설정
    # 총알과 적 충돌
    bullets = [obj for obj in game_world.world[2]]
    enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]

    for bullet in bullets:
        for enemy in enemies:
            game_world.add_collision_pair('bullet:enemy', bullet, enemy)

    # 플레이어와 적 충돌
    for enemy in enemies:
        game_world.add_collision_pair('player:enemy', player, enemy)

    game_world.handle_collisions()

    # UI 업데이트
    ui.enemies_killed = enemies_killed
    ui.wave = wave

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

    enemy = Enemy(x, y, player)
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
    pass

def resume():
    pass
