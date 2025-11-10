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
        # 로고 크기를 화면의 60% 크기로 조정
        logo_width = get_canvas_width() * 0.6
        logo_height = get_canvas_height() * 0.6
        image.draw(get_canvas_width() // 2, get_canvas_height() // 2, logo_width, logo_height)
    else:
        font.draw(get_canvas_width() // 2 - 150, get_canvas_height() // 2, 'SAND RAIDER', (255, 255, 255))

    font.draw(get_canvas_width() // 2 - 200, get_canvas_height() // 2 - 100, 'Press SPACE to Start', (255, 255, 0))
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
