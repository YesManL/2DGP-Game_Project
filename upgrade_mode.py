from pico2d import *
import game_framework
import game_world

selected_upgrade = 0
upgrades = []
font = None
title_font = None

def init():
    global selected_upgrade, upgrades, font, title_font
    selected_upgrade = 0

    # 폰트 로드 (시스템 기본 폰트 사용)
    try:
        font = load_font('C:/Windows/Fonts/arial.ttf', 20)
        title_font = load_font('C:/Windows/Fonts/arial.ttf', 40)
    except:
        font = None
        title_font = None

    # 업그레이드 옵션들
    upgrades = [
        {'name': 'Damage +10', 'desc': 'Increase bullet damage', 'stat': 'damage'},
        {'name': 'Fire Rate +20%', 'desc': 'Shoot faster', 'stat': 'fire_rate'},
        {'name': 'HP +20', 'desc': 'Increase max HP', 'stat': 'hp'},
        {'name': 'Speed +15%', 'desc': 'Move faster', 'stat': 'speed'}
    ]

def finish():
    pass

def update():
    pass

def draw():
    # 기존 게임 화면을 그대로 두고 그 위에 오버레이
    import play_mode

    # 먼저 게임 화면 그리기 (일시정지된 상태)
    clear_canvas()
    game_world.render()

    # 반투명 어두운 배경 오버레이 (사각형으로 표현)
    draw_rectangle(0, 0, 800, 600)

    # 타이틀 배경 (회색)
    draw_rectangle(200, 450, 600, 550)

    # 타이틀 텍스트
    if title_font:
        title_font.draw(280, 490, 'UPGRADE', (255, 255, 255))

    # 업그레이드 옵션들
    for i, upgrade in enumerate(upgrades):
        y = 380 - i * 80

        # 옵션 박스
        if i == selected_upgrade:
            # 선택된 옵션 (밝은 파란색 느낌으로 더 큰 박스)
            draw_rectangle(180, y - 30, 620, y + 30)
        else:
            # 일반 옵션 (어두운 회색)
            draw_rectangle(200, y - 25, 600, y + 25)

        # 업그레이드 텍스트
        if font:
            font.draw(250, y + 5, upgrade['name'], (255, 255, 255))
            if i == selected_upgrade:
                font.draw(250, y - 15, upgrade['desc'], (200, 200, 200))

    # 안내 메시지 배경
    draw_rectangle(200, 50, 600, 100)
    if font:
        font.draw(220, 70, 'Press ENTER to select', (255, 255, 255))

    update_canvas()

def handle_events():
    global selected_upgrade
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_UP or event.key == SDLK_w:
                selected_upgrade = (selected_upgrade - 1) % len(upgrades)
            elif event.key == SDLK_DOWN or event.key == SDLK_s:
                selected_upgrade = (selected_upgrade + 1) % len(upgrades)
            elif event.key == SDLK_RETURN or event.key == SDLK_SPACE:
                apply_upgrade()

def apply_upgrade():
    """선택한 업그레이드 적용"""
    import play_mode

    upgrade = upgrades[selected_upgrade]
    player = play_mode.player

    if upgrade['stat'] == 'damage':
        player.bullet_damage += 10
    elif upgrade['stat'] == 'fire_rate':
        player.fire_rate = max(0.05, player.fire_rate * 0.8)  # 20% 빠르게
    elif upgrade['stat'] == 'hp':
        player.max_hp += 20
        player.hp = min(player.hp + 20, player.max_hp)
    elif upgrade['stat'] == 'speed':
        player.max_speed *= 1.15

    # 플레이어 입력 상태 초기화
    player.reset_input_state()

    # 업그레이드 완료 후 게임으로 복귀
    play_mode.game_paused = False
    game_framework.pop_mode()

def pause():
    pass

def resume():
    pass
