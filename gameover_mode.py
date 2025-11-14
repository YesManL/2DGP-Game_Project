from pico2d import *
import game_framework
import title_mode

# 모듈 레벨 변수
font = None
score = 0

def init():
    global font
    # Windows 기본 폰트 사용
    font = load_font('C:/Windows/Fonts/arial.ttf', 40)

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
    font.draw(get_canvas_width() // 2 - 100, get_canvas_height() // 2 + 50, 'GAME OVER', (255, 0, 0))
    font.draw(get_canvas_width() // 2 - 120, get_canvas_height() // 2 - 20, f'Kills: {score}', (255, 255, 255))
    font.draw(get_canvas_width() // 2 - 200, get_canvas_height() // 2 - 100, 'Press SPACE to Restart', (255, 255, 0))
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
