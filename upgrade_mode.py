from pico2d import *
import game_framework
import random

# 업그레이드 옵션들 (영문으로 변경)
UPGRADES = {
    'damage': {
        'name': 'Damage UP',
        'description': 'Bullet damage +10',
        'icon': '[DMG]'
    },
    'fire_rate': {
        'name': 'Fire Rate UP',
        'description': 'Fire speed +20%',
        'icon': '[SPD]'
    },
    'speed': {
        'name': 'Move Speed UP',
        'description': 'Movement +15%',
        'icon': '[MOV]'
    },
    'max_hp': {
        'name': 'Max HP UP',
        'description': 'Max HP +20',
        'icon': '[HP+]'
    },
    'hp_heal': {
        'name': 'Heal',
        'description': 'Restore HP 50',
        'icon': '[HEL]'
    },
    'bullet_speed': {
        'name': 'Bullet Speed UP',
        'description': 'Bullet speed +20%',
        'icon': '[BUL]'
    }
}

selected_upgrades = []
selected_index = 0
font = None
small_font = None
title_font = None

def init():
    global selected_upgrades, selected_index, font, small_font, title_font
    font = load_font('C:/Windows/Fonts/arial.ttf', 28)
    small_font = load_font('C:/Windows/Fonts/arial.ttf', 20)
    title_font = load_font('C:/Windows/Fonts/arial.ttf', 50)

    # 3개의 랜덤 업그레이드 선택
    upgrade_keys = list(UPGRADES.keys())
    random.shuffle(upgrade_keys)
    selected_upgrades = upgrade_keys[:3]
    selected_index = 0

def finish():
    pass

def handle_events():
    global selected_index
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # ESC로는 닫을 수 없음 (업그레이드 필수 선택)
                pass
            elif event.key == SDLK_UP or event.key == SDLK_w:
                selected_index = (selected_index - 1) % 3
            elif event.key == SDLK_DOWN or event.key == SDLK_s:
                selected_index = (selected_index + 1) % 3
            elif event.key == SDLK_SPACE or event.key == SDLK_RETURN:
                apply_upgrade(selected_upgrades[selected_index])
                game_framework.pop_mode()

def apply_upgrade(upgrade_key):
    import play_mode
    player = play_mode.player

    if upgrade_key == 'damage':
        player.bullet_damage += 10
    elif upgrade_key == 'fire_rate':
        player.fire_rate *= 0.8  # 발사 간격 감소 = 연사속도 증가
    elif upgrade_key == 'speed':
        player.max_speed *= 1.15  # 후륜 자동차 시스템의 최대 속도 증가
        player.speed *= 1.15  # 기존 speed 변수도 같이 증가 (호환성)
    elif upgrade_key == 'max_hp':
        player.max_hp += 20
        player.hp = min(player.hp + 20, player.max_hp)
    elif upgrade_key == 'hp_heal':
        player.hp = min(player.hp + 50, player.max_hp)
    elif upgrade_key == 'bullet_speed':
        player.bullet_speed *= 1.2

    # 업그레이드 적용 후 입력 상태 초기화
    player.reset_input_state()

def draw():
    # 게임 화면을 배경으로 그리기 (멈춘 상태)
    import play_mode
    clear_canvas()
    play_mode.draw()

    # 반투명 어두운 오버레이 (사각형 여러 개로 표현)
    for i in range(10):
        draw_rectangle(0, 0, get_canvas_width(), get_canvas_height())

    # 제목
    title_font.draw(get_canvas_width() // 2 - 150, get_canvas_height() - 100, 'LEVEL UP!', (255, 255, 0))

    # 업그레이드 옵션들
    y_start = get_canvas_height() // 2 + 100
    for i, upgrade_key in enumerate(selected_upgrades):
        upgrade = UPGRADES[upgrade_key]
        y = y_start - i * 130

        # 선택된 항목 강조 (밝은 테두리)
        if i == selected_index:
            # 밝은 노란색 박스
            for j in range(3):
                draw_rectangle(120 - j, y - 60 - j, get_canvas_width() - 120 + j, y + 50 + j)
        else:
            # 어두운 회색 박스
            draw_rectangle(120, y - 60, get_canvas_width() - 120, y + 50)

        # 업그레이드 정보
        font.draw(150, y + 15, f'{upgrade["icon"]} {upgrade["name"]}', (255, 255, 255))
        small_font.draw(150, y - 15, upgrade["description"], (200, 200, 200))

    # 조작 안내
    small_font.draw(get_canvas_width() // 2 - 180, 60, 'W/S: Select  SPACE: Choose', (255, 255, 255))

    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
