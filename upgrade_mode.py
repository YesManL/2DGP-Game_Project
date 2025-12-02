from pico2d import *
import game_framework
import game_world
import math

selected_upgrade = 0
upgrades = []
font = None
title_font = None
bg_overlay = None
button_base = None
button_selected = None
display_panel = None
icon_images = {}
animation_time = 0

def init():
    global selected_upgrade, upgrades, font, title_font, bg_overlay, button_base, button_selected, display_panel, icon_images, animation_time
    selected_upgrade = 0
    animation_time = 0

    # 폰트 로드 (시스템 기본 폰트 사용)
    try:
        font = load_font('C:/Windows/Fonts/arial.ttf', 20)
        title_font = load_font('C:/Windows/Fonts/arial.ttf', 40)
    except:
        font = None
        title_font = None

    # GUI 이미지 로드
    try:
        button_base = load_image('./04.GUI/PNG/GUI_Main_Button_1_Base.png')
        button_selected = load_image('./04.GUI/PNG/GUI_Main_Button_1.png')
        display_panel = load_image('./04.GUI/PNG/Display_12.png')

        # 아이콘 이미지들
        icon_images['damage'] = load_image('./03.아이템&아이콘/PNG/Item_3.png')
        icon_images['fire_rate'] = load_image('./03.아이템&아이콘/PNG/Item_4.png')
        icon_images['hp'] = load_image('./03.아이템&아이콘/PNG/Item_5.png')
        icon_images['speed'] = load_image('./03.아이템&아이콘/PNG/Item_6.png')
    except:
        pass

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
    global animation_time
    animation_time += game_framework.frame_time

def draw():
    # 기존 게임 화면을 그대로 두고 그 위에 오버레이
    import play_mode

    # 먼저 게임 화면 그리기 (일시정지된 상태)
    clear_canvas()
    game_world.render()

    # 반투명 어두운 배경 오버레이
    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()

    # 어두운 오버레이 (직사각형)
    draw_rectangle(0, 0, canvas_width, canvas_height)

    # 타이틀 패널 - 맥박 효과
    title_scale = 1.0 + math.sin(animation_time * 3) * 0.02
    if display_panel:
        display_panel.draw(canvas_width // 2, canvas_height - 80, int(400 * title_scale), int(80 * title_scale))

    # 타이틀 텍스트
    if title_font:
        title_font.draw(canvas_width // 2 - 100, canvas_height - 90, 'UPGRADE', (255, 255, 0))

    # 업그레이드 옵션들
    for i, upgrade in enumerate(upgrades):
        y = canvas_height - 200 - i * 90

        # 옵션 버튼
        if i == selected_upgrade:
            # 선택된 옵션 - 맥박 효과
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.05
            if button_selected:
                button_selected.draw(canvas_width // 2, y, int(500 * button_scale), int(70 * button_scale))

            # 아이콘도 회전 효과
            if upgrade['stat'] in icon_images:
                icon_rotation = math.sin(animation_time * 3) * 10
                icon_images[upgrade['stat']].rotate_draw(icon_rotation * 3.14159 / 180, canvas_width // 2 - 200, y, 40, 40)
        else:
            # 일반 옵션
            if button_base:
                button_base.draw(canvas_width // 2, y, 500, 70)

            # 일반 아이콘
            if upgrade['stat'] in icon_images:
                icon_images[upgrade['stat']].draw(canvas_width // 2 - 200, y, 40, 40)

        # 업그레이드 텍스트
        if font:
            font.draw(canvas_width // 2 - 160, y + 5, upgrade['name'], (255, 255, 255))
            font_size = 16
            desc_font = load_font('C:/Windows/Fonts/arial.ttf', font_size)
            desc_font.draw(canvas_width // 2 - 160, y - 15, upgrade['desc'], (200, 200, 200))

    # 안내 메시지 - 깜빡임 효과
    alpha = int((math.sin(animation_time * 4) + 1) * 127.5)
    text_color = (255, 255, min(255, alpha + 100))

    if display_panel:
        display_panel.draw(canvas_width // 2, 80, 400, 60)
    if font:
        font.draw(canvas_width // 2 - 150, 75, 'Press ENTER to select', text_color)

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

    # 레벨 업!
    player.level += 1

    # 플레이어 입력 상태 초기화
    player.reset_input_state()

    # 업그레이드 완료 후 게임으로 복귀
    play_mode.game_paused = False
    game_framework.pop_mode()

def pause():
    pass

def resume():
    pass
