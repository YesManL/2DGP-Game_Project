from pico2d import *
import game_framework
import play_mode
import shop_mode
import math
from resource_path import resource_path

animation_time = 0
selected_button = 0  # 0: Play, 1: Shop
button_press_sound = None  # 버튼 선택 사운드
start_buy_sound = None  # 시작/구매 사운드

def init():
    global image, font, bg_image, button_image, animation_time, selected_button
    global button_press_sound, start_buy_sound, bg_tile
    image = None
    bg_image = None
    button_image = None
    bg_tile = None
    animation_time = 0
    selected_button = 0

    # 사운드 로드
    if button_press_sound is None:
        try:
            button_press_sound = load_wav(resource_path('SFX/Button_Press.mp3'))
            button_press_sound.set_volume(40)
        except:
            pass

    if start_buy_sound is None:
        try:
            start_buy_sound = load_wav(resource_path('SFX/Start_Buy.mp3'))
            start_buy_sound.set_volume(50)
        except:
            pass

    # 배경 타일 로드
    try:
        bg_tile = load_image(resource_path('./02.배경&프랍/4.맵/PNG/Maptile_1.png'))
    except:
        pass

    try:
        image = load_image(resource_path('./99.etc/Title2.png'))
    except:
        pass

    try:
        bg_image = load_image(resource_path('./04.GUI/Titlescene_2.png'))
    except:
        pass

    try:
        button_image = load_image(resource_path('./04.GUI/PNG/GUI_Main_Button_1.png'))
    except:
        pass

    # Windows 기본 폰트 사용
    font = load_font('C:/Windows/Fonts/arial.ttf', 40)

def finish():
    pass

def handle_events():
    global selected_button
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE or event.key == SDLK_RETURN:
                if selected_button == 0:
                    # Start 버튼만 Start_Buy 사운드 재생
                    if start_buy_sound:
                        start_buy_sound.play()
                    game_framework.change_mode(play_mode)
                else:
                    # 상점 버튼은 Button_Press 사운드 재생
                    if button_press_sound:
                        button_press_sound.play()
                    # 상점은 오버레이이므로 push_mode 사용
                    game_framework.push_mode(shop_mode)
            elif event.key == SDLK_UP or event.key == SDLK_w:
                # 버튼 선택 변경 시 사운드 재생
                if button_press_sound:
                    button_press_sound.play()
                selected_button = 0
            elif event.key == SDLK_DOWN or event.key == SDLK_s:
                # 버튼 선택 변경 시 사운드 재생
                if button_press_sound:
                    button_press_sound.play()
                selected_button = 1

def draw():
    global selected_button, bg_tile
    clear_canvas()

    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()

    # Maptile_1로 배경 채우기
    if bg_tile:
        tile_width = bg_tile.w
        tile_height = bg_tile.h

        # 화면을 타일로 채우기 (타일을 반복해서 그리기)
        cols = (canvas_width // tile_width) + 2
        rows = (canvas_height // tile_height) + 2

        for row in range(rows):
            for col in range(cols):
                x = col * tile_width
                y = row * tile_height
                bg_tile.draw(x, y, tile_width, tile_height)

    # 로고
    if image:
        logo_height = get_canvas_height() * 0.4  # 40%로 줄임
        aspect_ratio = image.w / image.h
        logo_width = logo_height * aspect_ratio

        # 약간의 바운스 효과
        bounce = math.sin(animation_time * 2) * 5
        image.draw(get_canvas_width() // 2, get_canvas_height() // 2 + 120 + bounce, logo_width, logo_height)
    else:
        font.draw(get_canvas_width() // 2 - 150, get_canvas_height() // 2, 'SAND RAIDER', (255, 255, 255))

    # Play 버튼
    play_y = 200
    if button_image:
        if selected_button == 0:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08  # 선택된 버튼 맥박 효과
            button_image.draw(get_canvas_width() // 2, play_y, int(250 * button_scale), int(70 * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, play_y, 250, 70)

    # Play 텍스트 (저장된 게임이 있으면 Continue로 표시)
    play_color = (255, 255, 100) if selected_button == 0 else (255, 255, 255)
    if shop_mode.GameData.has_saved_game:
        font.draw(get_canvas_width() // 2 - 100, play_y - 15, 'CONTINUE', play_color)
        # 저장된 웨이브 정보 표시
        wave_font = load_font('C:/Windows/Fonts/arial.ttf', 16)
        wave_font.draw(get_canvas_width() // 2 - 80, play_y - 35, f'Wave {shop_mode.GameData.saved_wave}', (200, 200, 200))
    else:
        font.draw(get_canvas_width() // 2 - 60, play_y - 15, 'PLAY', play_color)

    # Shop 버튼
    shop_y = 120
    if button_image:
        if selected_button == 1:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08  # 선택된 버튼 맥박 효과
            button_image.draw(get_canvas_width() // 2, shop_y, int(250 * button_scale), int(70 * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, shop_y, 250, 70)

    # Shop 텍스트
    shop_color = (255, 255, 100) if selected_button == 1 else (255, 255, 255)
    font.draw(get_canvas_width() // 2 - 60, shop_y - 15, 'SHOP', shop_color)

    # 안내 텍스트
    small_font = load_font('C:/Windows/Fonts/arial.ttf', 20)
    alpha = int((math.sin(animation_time * 4) + 1) * 127.5)
    text_color = (255, 255, min(255, alpha + 100))
    small_font.draw(get_canvas_width() // 2 - 150, 50, 'Arrow Keys + Enter to Select', text_color)

    update_canvas()

def update():
    global animation_time
    animation_time += game_framework.frame_time

def pause():
    pass

def resume():
    pass
