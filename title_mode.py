from pico2d import *
import game_framework
import play_mode
import shop_mode
import tutorial_mode
import option_mode
from option_mode import VolumeSettings
import math
from resource_path import resource_path

animation_time = 0
selected_button = 0  # 0: Play, 1: Shop, 2: Tutorial, 3: Option, 4: Quit
button_press_sound = None  # 버튼 선택 사운드
start_buy_sound = None  # 시작/구매 사운드

# 버튼 위치 및 크기 정의
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 55
BUTTON_POSITIONS = {
    0: 385,  # Play
    1: 310,  # Shop
    2: 235,  # Tutorial
    3: 160,  # Option
    4: 85    # Quit
}

def is_mouse_on_button(mx, my, button_y):
    """마우스가 버튼 위에 있는지 확인"""
    canvas_width = get_canvas_width()
    button_x = canvas_width // 2

    # 버튼 영역 계산
    left = button_x - BUTTON_WIDTH // 2
    right = button_x + BUTTON_WIDTH // 2
    top = button_y + BUTTON_HEIGHT // 2
    bottom = button_y - BUTTON_HEIGHT // 2

    return left <= mx <= right and bottom <= my <= top

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
            button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
        except:
            pass

    if start_buy_sound is None:
        try:
            start_buy_sound = load_wav(resource_path('SFX/Start_Buy.mp3'))
            start_buy_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.005))
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

    # Windows 기본 폰트 사용 (한글 지원) - 크기 축소
    font = load_font('C:/Windows/Fonts/malgun.ttf', 32)

def finish():
    pass

def handle_events():
    global selected_button
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            # 마우스 움직임 - 버튼 위에 있으면 해당 버튼 선택
            mx, my = event.x, get_canvas_height() - event.y
            for button_id, button_y in BUTTON_POSITIONS.items():
                if is_mouse_on_button(mx, my, button_y):
                    if selected_button != button_id:
                        selected_button = button_id
                        if button_press_sound:
                            button_press_sound.play()
                    break
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # 마우스 클릭 - 버튼 위에서 클릭하면 해당 버튼 실행
            if event.button == SDL_BUTTON_LEFT:
                mx, my = event.x, get_canvas_height() - event.y
                for button_id, button_y in BUTTON_POSITIONS.items():
                    if is_mouse_on_button(mx, my, button_y):
                        # 버튼 실행
                        execute_button(button_id)
                        break
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE or event.key == SDLK_RETURN:
                execute_button(selected_button)
            elif event.key == SDLK_UP or event.key == SDLK_w:
                # 버튼 선택 변경 시 사운드 재생
                if button_press_sound:
                    button_press_sound.play()
                selected_button = (selected_button - 1) % 5
            elif event.key == SDLK_DOWN or event.key == SDLK_s:
                # 버튼 선택 변경 시 사운드 재생
                if button_press_sound:
                    button_press_sound.play()
                selected_button = (selected_button + 1) % 5

def execute_button(button_id):
    """버튼 실행 함수"""
    if button_id == 0:
        # Start 버튼만 Start_Buy 사운드 재생
        if start_buy_sound:
            start_buy_sound.play()
        game_framework.change_mode(play_mode)
    elif button_id == 1:
        # 상점 버튼은 Button_Press 사운드 재생
        if button_press_sound:
            button_press_sound.play()
        # 상점은 오버레이이므로 push_mode 사용
        game_framework.push_mode(shop_mode)
    elif button_id == 2:
        # 튜토리얼 버튼은 Button_Press 사운드 재생
        if button_press_sound:
            button_press_sound.play()
        # 튜토리얼은 오버레이이므로 push_mode 사용
        game_framework.push_mode(tutorial_mode)
    elif button_id == 3:
        # 옵션 버튼은 Button_Press 사운드 재생
        if button_press_sound:
            button_press_sound.play()
        # 옵션은 오버레이이므로 push_mode 사용
        game_framework.push_mode(option_mode)
    elif button_id == 4:
        # 종료 버튼 - Button_Press 사운드 재생 후 게임 종료
        if button_press_sound:
            button_press_sound.play()
        game_framework.quit()

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

    # 로고 - 크기 축소 및 위치 조정
    if image:
        logo_height = get_canvas_height() * 0.28  # 32%에서 28%로 축소
        aspect_ratio = image.w / image.h
        logo_width = logo_height * aspect_ratio

        # 약간의 바운스 효과
        bounce = math.sin(animation_time * 2) * 5
        image.draw(get_canvas_width() // 2, get_canvas_height() // 2 + 210 + bounce, logo_width, logo_height)
    else:
        font.draw(get_canvas_width() // 2 - 120, get_canvas_height() // 2 + 90, 'SAND RAIDER', (255, 255, 255))

    # 버튼 크기 축소 (250x70 -> 200x55)
    button_width = 200
    button_height = 55

    # Play 버튼
    play_y = BUTTON_POSITIONS[0]
    if button_image:
        if selected_button == 0:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08
            button_image.draw(get_canvas_width() // 2, play_y, int(BUTTON_WIDTH * button_scale), int(BUTTON_HEIGHT * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, play_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Play 텍스트 - 중앙 정렬 (폰트 32px 기준)
    play_color = (255, 255, 100) if selected_button == 0 else (255, 255, 255)
    if shop_mode.GameData.has_saved_game:
        font.draw(get_canvas_width() // 2 - 68, play_y - 6, '계속하기', play_color)
        # 저장된 웨이브 정보 표시
        wave_font = load_font('C:/Windows/Fonts/malgun.ttf', 14)
        wave_text = f'웨이브 {shop_mode.GameData.saved_wave}'
        wave_font.draw(get_canvas_width() // 2 - 32, play_y - 28, wave_text, (0, 0, 0))
    else:
        font.draw(get_canvas_width() // 2 - 68, play_y - 6, '게임 시작', play_color)

    # Shop 버튼
    shop_y = BUTTON_POSITIONS[1]
    if button_image:
        if selected_button == 1:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08
            button_image.draw(get_canvas_width() // 2, shop_y, int(BUTTON_WIDTH * button_scale), int(BUTTON_HEIGHT * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, shop_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Shop 텍스트 - 중앙 정렬 (폰트 32px 기준)
    shop_color = (255, 255, 100) if selected_button == 1 else (255, 255, 255)
    font.draw(get_canvas_width() // 2 - 34, shop_y - 6, '상점', shop_color)

    # Tutorial 버튼
    tutorial_y = BUTTON_POSITIONS[2]
    if button_image:
        if selected_button == 2:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08
            button_image.draw(get_canvas_width() // 2, tutorial_y, int(BUTTON_WIDTH * button_scale), int(BUTTON_HEIGHT * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, tutorial_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Tutorial 텍스트 - 중앙 정렬 (폰트 32px 기준)
    tutorial_color = (255, 255, 100) if selected_button == 2 else (255, 255, 255)
    font.draw(get_canvas_width() // 2 - 51, tutorial_y - 6, '조작법', tutorial_color)

    # Option 버튼
    option_y = BUTTON_POSITIONS[3]
    if button_image:
        if selected_button == 3:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08
            button_image.draw(get_canvas_width() // 2, option_y, int(BUTTON_WIDTH * button_scale), int(BUTTON_HEIGHT * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, option_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Option 텍스트 - 중앙 정렬 (폰트 32px 기준)
    option_color = (255, 255, 100) if selected_button == 3 else (255, 255, 255)
    font.draw(get_canvas_width() // 2 - 34, option_y - 6, '옵션', option_color)

    # Quit 버튼
    quit_y = BUTTON_POSITIONS[4]
    if button_image:
        if selected_button == 4:
            button_scale = 1.0 + math.sin(animation_time * 5) * 0.08
            button_image.draw(get_canvas_width() // 2, quit_y, int(BUTTON_WIDTH * button_scale), int(BUTTON_HEIGHT * button_scale))
        else:
            button_image.draw(get_canvas_width() // 2, quit_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Quit 텍스트 - 중앙 정렬 (폰트 32px 기준)
    quit_color = (255, 100, 100) if selected_button == 4 else (200, 200, 200)
    font.draw(get_canvas_width() // 2 - 34, quit_y - 6, '종료', quit_color)

    # 안내 텍스트 - 크기 키우고 아래로 이동
    small_font = load_font('C:/Windows/Fonts/malgun.ttf', 18)
    small_font.draw(get_canvas_width() // 2 - 105, 35, '방향키 + Enter 로 선택', (255, 255, 100))

    update_canvas()

def update():
    global animation_time
    animation_time += game_framework.frame_time

def pause():
    pass

def resume():
    pass
