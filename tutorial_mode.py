from pico2d import *
import game_framework
from resource_path import resource_path
from option_mode import VolumeSettings

button_press_sound = None
bg_tile = None

def init():
    global button_press_sound, bg_tile

    # 사운드 로드
    if button_press_sound is None:
        try:
            button_press_sound = load_wav(resource_path('SFX/Button_Press.mp3'))
            button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
        except:
            pass

    # 배경 타일 로드
    try:
        bg_tile = load_image(resource_path('./02.배경&프랍/4.맵/PNG/Maptile_1.png'))
    except:
        pass

def finish():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE or event.key == SDLK_RETURN or event.key == SDLK_SPACE:
                if button_press_sound:
                    button_press_sound.play()
                game_framework.pop_mode()

def draw():
    clear_canvas()

    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()

    # 배경 타일로 채우기
    if bg_tile:
        tile_width = bg_tile.w
        tile_height = bg_tile.h
        cols = (canvas_width // tile_width) + 2
        rows = (canvas_height // tile_height) + 2

        for row in range(rows):
            for col in range(cols):
                x = col * tile_width
                y = row * tile_height
                bg_tile.draw(x, y, tile_width, tile_height)


    # 폰트 로드 - 한글 지원 폰트 사용 (크기 축소)
    title_font = load_font('C:/Windows/Fonts/malgun.ttf', 40)
    heading_font = load_font('C:/Windows/Fonts/malgun.ttf', 24)
    content_font = load_font('C:/Windows/Fonts/malgun.ttf', 18)
    small_font = load_font('C:/Windows/Fonts/malgun.ttf', 20)

    # 제목 - 중앙 상단
    title_font.draw(canvas_width // 2 - 120, canvas_height - 50, '게임 조작법', (255, 255, 100))

    # 조작법 섹션 시작 위치 (더 위로)
    y_pos = canvas_height - 100
    x_left = 120  # 왼쪽 여백 줄임

    # 이동 조작
    heading_font.draw(x_left, y_pos, '[ 이동 조작 ]', (100, 255, 100))
    y_pos -= 38
    content_font.draw(x_left + 20, y_pos, 'W / 위 화살표     - 전진', (0, 0, 0))
    y_pos -= 30
    content_font.draw(x_left + 20, y_pos, 'S / 아래 화살표   - 후진', (0, 0, 0))
    y_pos -= 30
    content_font.draw(x_left + 20, y_pos, 'A / 왼쪽 화살표   - 왼쪽 회전', (0, 0, 0))
    y_pos -= 30
    content_font.draw(x_left + 20, y_pos, 'D / 오른쪽 화살표 - 오른쪽 회전', (0, 0, 0))

    y_pos -= 45

    # 전투 조작
    heading_font.draw(x_left, y_pos, '[ 전투 조작 ]', (255, 100, 100))
    y_pos -= 38
    content_font.draw(x_left + 20, y_pos, '마우스            - 포탑 조준', (0, 0, 0))
    y_pos -= 30
    content_font.draw(x_left + 20, y_pos, '좌클릭            - 무기 발사', (0, 0, 0))

    y_pos -= 45

    # 게임 진행
    heading_font.draw(x_left, y_pos, '[ 게임 진행 ]', (100, 200, 255))
    y_pos -= 38
    content_font.draw(x_left + 20, y_pos, '• 적의 웨이브를 생존하고 아이템을 수집하세요', (0, 0, 0))
    y_pos -= 30
    content_font.draw(x_left + 20, y_pos, '• 웨이브 사이에 차량을 업그레이드하세요', (0, 0, 0))
    y_pos -= 30
    content_font.draw(x_left + 20, y_pos, '• 상점에서 코인을 사용해 영구 업그레이드를 구매하세요', (0, 0, 0))

    # 하단 안내 - 더 눈에 띄게
    small_font.draw(canvas_width // 2 - 185, 30, 'ESC, ENTER, SPACE 키를 눌러 돌아가기', (255, 255, 100))

    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass

