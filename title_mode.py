from pico2d import *
import game_framework
import play_mode

def init():
    global image, font
    image = None
    try:
        image = load_image('./99.etc/Title2.png')
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
    if image:
        # 로고의 원본 비율을 유지하면서 적절한 크기로 표시
        # 이미지 원본 비율 유지 (세로를 기준으로 크기 결정)
        logo_height = get_canvas_height() * 0.4  # 화면 높이의 40%
        # 원본 이미지의 가로세로 비율을 유지
        aspect_ratio = image.w / image.h
        logo_width = logo_height * aspect_ratio

        # 로고를 화면 중앙 상단에 배치
        image.draw(get_canvas_width() // 2, get_canvas_height() // 2 + 50, logo_width, logo_height)
    else:
        font.draw(get_canvas_width() // 2 - 150, get_canvas_height() // 2, 'SAND RAIDER', (255, 255, 255))

    # 텍스트를 화면 하단으로 이동
    font.draw(get_canvas_width() // 2 - 200, 100, 'Press SPACE to Start', (255, 255, 0))
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
