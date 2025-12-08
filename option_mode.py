from pico2d import *
import game_framework
from resource_path import resource_path

# 볼륨 설정 저장
class VolumeSettings:
    master_volume = 50  # 0~100 (기본값 50%)
    sfx_volume = 50  # 0~100 (기본값 50%)
    music_volume = 50  # 0~100 (기본값 50%)

button_press_sound = None
bg_tile = None
slider_bg_image = None  # 슬라이더 배경 이미지
slider_fill_image = None  # 슬라이더 채우기 이미지
selected_slider = 0  # 0: Master, 1: SFX, 2: Music
animation_time = 0

def init():
    global button_press_sound, bg_tile, selected_slider, animation_time
    global slider_bg_image, slider_fill_image

    selected_slider = 0
    animation_time = 0

    # 사운드 로드
    if button_press_sound is None:
        try:
            button_press_sound = load_wav(resource_path('SFX/Button_Press.mp3'))
            button_press_sound.set_volume(int(VolumeSettings.sfx_volume * 0.4))
        except:
            pass

    # 배경 타일 로드
    try:
        bg_tile = load_image(resource_path('./02.배경&프랍/4.맵/PNG/Maptile_1.png'))
    except:
        pass

    # GUI 이미지 로드 (슬라이더용)
    try:
        slider_bg_image = load_image(resource_path('./04.GUI/PNG/GUI_Display_Panel_1.png'))
    except:
        pass

    try:
        slider_fill_image = load_image(resource_path('./04.GUI/PNG/GUI_Display_Panel_1.png'))
    except:
        pass

def finish():
    pass

def handle_events():
    global selected_slider
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                if button_press_sound:
                    button_press_sound.play()
                game_framework.pop_mode()
            elif event.key == SDLK_UP or event.key == SDLK_w:
                if button_press_sound:
                    button_press_sound.play()
                selected_slider = (selected_slider - 1) % 3
            elif event.key == SDLK_DOWN or event.key == SDLK_s:
                if button_press_sound:
                    button_press_sound.play()
                selected_slider = (selected_slider + 1) % 3
            elif event.key == SDLK_LEFT or event.key == SDLK_a:
                # 볼륨 감소
                if button_press_sound:
                    button_press_sound.play()
                if selected_slider == 0:
                    VolumeSettings.master_volume = max(0, VolumeSettings.master_volume - 5)
                elif selected_slider == 1:
                    VolumeSettings.sfx_volume = max(0, VolumeSettings.sfx_volume - 5)
                elif selected_slider == 2:
                    VolumeSettings.music_volume = max(0, VolumeSettings.music_volume - 5)
                update_all_volumes()
            elif event.key == SDLK_RIGHT or event.key == SDLK_d:
                # 볼륨 증가
                if button_press_sound:
                    button_press_sound.play()
                if selected_slider == 0:
                    VolumeSettings.master_volume = min(100, VolumeSettings.master_volume + 5)
                elif selected_slider == 1:
                    VolumeSettings.sfx_volume = min(100, VolumeSettings.sfx_volume + 5)
                elif selected_slider == 2:
                    VolumeSettings.music_volume = min(100, VolumeSettings.music_volume + 5)
                update_all_volumes()

def update_all_volumes():
    """모든 사운드의 볼륨을 업데이트"""
    # 옵션 모드 버튼 사운드
    if button_press_sound:
        button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))

    # title_mode 사운드 업데이트
    try:
        import title_mode
        if title_mode.button_press_sound:
            title_mode.button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
        if title_mode.start_buy_sound:
            title_mode.start_buy_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.005))
    except:
        pass

    # shop_mode 사운드 업데이트
    try:
        import shop_mode
        if shop_mode.button_press_sound:
            shop_mode.button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
        if shop_mode.start_buy_sound:
            shop_mode.start_buy_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.005))
    except:
        pass

    # tutorial_mode 사운드 업데이트
    try:
        import tutorial_mode
        if tutorial_mode.button_press_sound:
            tutorial_mode.button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
    except:
        pass

    # upgrade_mode 사운드 업데이트
    try:
        import upgrade_mode
        if upgrade_mode.button_press_sound:
            upgrade_mode.button_press_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
    except:
        pass

    # player 사운드 업데이트
    try:
        from player import Player
        if Player.fire_sound:
            Player.fire_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.0035))
        if Player.get_hit_sound:
            Player.get_hit_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
    except:
        pass

    # enemy 사운드 업데이트
    try:
        from enemy import Enemy, BossBanditRPG
        if Enemy.death_sounds:
            for sound in Enemy.death_sounds:
                sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.003))
        if Enemy.ar_fire_sound:
            Enemy.ar_fire_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.0025))
        if BossBanditRPG.rpg_fire_sound:
            BossBanditRPG.rpg_fire_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.0035))
    except:
        pass

    # item 사운드 업데이트
    try:
        from item import HPItem
        if HPItem.item_get_sound:
            HPItem.item_get_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.003))
    except:
        pass

    # explosion 사운드 업데이트
    try:
        from explosion import Explosion
        if Explosion.explosion_sound:
            Explosion.explosion_sound.set_volume(int(VolumeSettings.sfx_volume * VolumeSettings.master_volume * 0.004))
    except:
        pass

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

    # 폰트 로드
    title_font = load_font('C:/Windows/Fonts/malgun.ttf', 50)
    heading_font = load_font('C:/Windows/Fonts/malgun.ttf', 28)
    content_font = load_font('C:/Windows/Fonts/malgun.ttf', 22)
    small_font = load_font('C:/Windows/Fonts/malgun.ttf', 18)

    # 제목
    title_font.draw(canvas_width // 2 - 100, canvas_height - 80, '옵션', (255, 255, 100))

    # 슬라이더 시작 위치
    y_start = canvas_height - 180
    slider_width = 400
    slider_height = 20

    # Master Volume
    y_pos = y_start
    color = (255, 255, 100) if selected_slider == 0 else (255, 255, 255)
    heading_font.draw(150, y_pos + 10, '전체 볼륨', color)

    # 슬라이더 배경
    draw_slider_bg(canvas_width // 2, y_pos - 20, slider_width, slider_height, selected_slider == 0)
    # 슬라이더 채우기
    draw_slider_fill(canvas_width // 2, y_pos - 20, slider_width, slider_height, VolumeSettings.master_volume)
    # 퍼센트 표시
    content_font.draw(canvas_width // 2 + slider_width // 2 + 30, y_pos - 30, f'{VolumeSettings.master_volume}%', color)

    # SFX Volume
    y_pos -= 100
    color = (255, 255, 100) if selected_slider == 1 else (255, 255, 255)
    heading_font.draw(150, y_pos + 10, '효과음 볼륨', color)

    draw_slider_bg(canvas_width // 2, y_pos - 20, slider_width, slider_height, selected_slider == 1)
    draw_slider_fill(canvas_width // 2, y_pos - 20, slider_width, slider_height, VolumeSettings.sfx_volume)
    content_font.draw(canvas_width // 2 + slider_width // 2 + 30, y_pos - 30, f'{VolumeSettings.sfx_volume}%', color)

    # Music Volume
    y_pos -= 100
    color = (255, 255, 100) if selected_slider == 2 else (255, 255, 255)
    heading_font.draw(150, y_pos + 10, '배경음 볼륨', color)

    draw_slider_bg(canvas_width // 2, y_pos - 20, slider_width, slider_height, selected_slider == 2)
    draw_slider_fill(canvas_width // 2, y_pos - 20, slider_width, slider_height, VolumeSettings.music_volume)
    content_font.draw(canvas_width // 2 + slider_width // 2 + 30, y_pos - 30, f'{VolumeSettings.music_volume}%', color)

    # 안내 텍스트
    small_font.draw(canvas_width // 2 - 180, 60, '↑↓: 항목 선택 | ←→: 볼륨 조절', (255, 255, 100))
    small_font.draw(canvas_width // 2 - 120, 30, 'ESC: 돌아가기', (255, 255, 100))

    update_canvas()

def draw_slider_bg(x, y, width, height, selected):
    """슬라이더 배경 그리기"""
    if slider_bg_image:
        # 선택된 슬라이더는 약간 크게
        if selected:
            slider_bg_image.draw(x, y, width, height)
        else:
            slider_bg_image.draw(x, y, width, height)

def draw_slider_fill(x, y, width, height, volume):
    """슬라이더 채우기 그리기"""
    fill_width = int(width * volume / 100)

    if fill_width > 0 and slider_fill_image:
        # clip_draw를 사용하여 비율만큼만 그리기
        fill_ratio = volume / 100
        clip_width = int(slider_fill_image.w * fill_ratio)

        # 볼륨에 따라 색상 틴트 (tint 기능이 있다면)
        slider_fill_image.clip_draw(0, 0, clip_width, slider_fill_image.h,
                                    x - width // 2 + fill_width // 2, y,
                                    fill_width, height)

def update():
    global animation_time
    animation_time += game_framework.frame_time

def pause():
    pass

def resume():
    pass

