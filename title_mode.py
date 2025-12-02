from pico2d import *
import game_framework
import play_mode
import math

animation_time = 0

def init():
    global image, font, bg_image, button_image, animation_time
    image = None
    bg_image = None
    button_image = None
    animation_time = 0

    try:
        image = load_image('./99.etc/Title2.png')
    except:
        pass

    try:
        bg_image = load_image('./04.GUI/Titlescene_2.png')
    except:
        pass

    try:
        button_image = load_image('./04.GUI/PNG/GUI_Main_Button_1.png')
    except:
        pass

    # Windows 기본 폰트 사용
    font = load_font('C:/Windows/Fonts/arial.ttf', 40)

def finish():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                game_framework.change_mode(play_mode)

def draw():
    clear_canvas()

    # 배경 이미지
    if bg_image:
        bg_image.draw(get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())

    # 로고
    if image:
        logo_height = get_canvas_height() * 0.5  # 화면 높이의 50%로 증가
        aspect_ratio = image.w / image.h
        logo_width = logo_height * aspect_ratio

        # 약간의 바운스 효과
        bounce = math.sin(animation_time * 2) * 5
        image.draw(get_canvas_width() // 2, get_canvas_height() // 2 + 80 + bounce, logo_width, logo_height)
    else:
        font.draw(get_canvas_width() // 2 - 150, get_canvas_height() // 2, 'SAND RAIDER', (255, 255, 255))

    # 시작 버튼
    if button_image:
        button_scale = 1.0 + math.sin(animation_time * 3) * 0.05  # 맥박 효과
        button_image.draw(get_canvas_width() // 2, 150, int(200 * button_scale), int(60 * button_scale))

    # 텍스트 - 깜빡이는 효과
    alpha = int((math.sin(animation_time * 4) + 1) * 127.5)  # 0~255 범위
    text_color = (255, 255, min(255, alpha + 100))
    font.draw(get_canvas_width() // 2 - 200, 140, 'Press SPACE to Start', text_color)
    update_canvas()

def update():
    global animation_time
    animation_time += game_framework.frame_time

def pause():
    pass

def resume():
    pass
