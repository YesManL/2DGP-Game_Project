from pico2d import *
import game_framework
import title_mode
import math

# 모듈 레벨 변수
font = None
title_font = None
score = 0
bg_image = None
display_panel = None
button_image = None
skull_icon = None
animation_time = 0

def init():
    global font, title_font, bg_image, display_panel, button_image, skull_icon, animation_time
    # Windows 기본 폰트 사용
    font = load_font('C:/Windows/Fonts/arial.ttf', 30)
    title_font = load_font('C:/Windows/Fonts/arial.ttf', 60)
    animation_time = 0

    # GUI 이미지 로드
    try:
        display_panel = load_image('./04.GUI/PNG/Display_12.png')
        button_image = load_image('./04.GUI/PNG/GUI_Main_Button_1.png')
        skull_icon = load_image('./03.아이템&아이콘/PNG/Item_10.png')
    except:
        pass

def finish():
    pass

def set_score(kills):
    global score
    score = kills

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                game_framework.change_mode(title_mode)

def draw():
    clear_canvas()

    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()

    # 어두운 배경
    draw_rectangle(0, 0, canvas_width, canvas_height)

    # 타이틀 패널 - 흔들리는 효과
    shake_x = math.sin(animation_time * 10) * 2
    shake_y = math.cos(animation_time * 10) * 2

    if display_panel:
        display_panel.draw(canvas_width // 2 + shake_x, canvas_height // 2 + 100 + shake_y, 500, 100)

    # GAME OVER 텍스트 - 흔들림
    if title_font:
        title_font.draw(int(canvas_width // 2 - 170 + shake_x), int(canvas_height // 2 + 80 + shake_y), 'GAME OVER', (255, 50, 50))

    # 스코어 패널 - 펄스 효과
    scale = 1.0 + math.sin(animation_time * 3) * 0.03
    if display_panel:
        display_panel.draw(canvas_width // 2, canvas_height // 2, int(400 * scale), int(80 * scale))

    # 스컬 아이콘 - 회전 효과
    rotation = math.sin(animation_time * 2) * 10
    if skull_icon:
        skull_icon.rotate_draw(rotation * 3.14159 / 180, canvas_width // 2 - 120, canvas_height // 2, 50, 50)

    # 스코어 텍스트
    if font:
        font.draw(canvas_width // 2 - 60, canvas_height // 2 - 10, f'Kills: {score}', (255, 255, 255))

    # 재시작 버튼 - 맥박 효과
    button_scale = 1.0 + math.sin(animation_time * 4) * 0.05
    if button_image:
        button_image.draw(canvas_width // 2, canvas_height // 2 - 120, int(300 * button_scale), int(60 * button_scale))

    # 재시작 텍스트 - 깜빡임
    alpha = int((math.sin(animation_time * 5) + 1) * 127.5)
    text_color = (255, 255, min(255, alpha + 100))
    if font:
        font.draw(canvas_width // 2 - 140, canvas_height // 2 - 130, 'Press SPACE to Restart', text_color)

    update_canvas()

def update():
    global animation_time
    animation_time += game_framework.frame_time

def pause():
    pass

def resume():
    pass
