from pico2d import *
import game_framework
import math

# 플레이어가 선택할 수 있는 아이템/무기
class GameData:
    """게임 전역 데이터 - 플레이어가 선택한 무기와 아이템"""
    selected_weapon = 0  # 0: 기본 총, 1: 샷건, 2: 레이저
    selected_items = []  # 현재 적용 대기 중인 아이템 (웨이브 완료 후)
    purchased_items = []  # 영구 구매한 아이템 (타이틀 상점)
    purchased_weapons = [0]  # 구매한 무기 목록 (Basic Gun은 기본 소유)
    item_counts = {}  # 아이템별 구매 횟수 {item_id: count}
    player_gold = 1000  # 플레이어 골드

    # 게임 진행 상태 저장
    saved_wave = 1  # 저장된 웨이브
    saved_kills = 0  # 저장된 처치 수
    has_saved_game = False  # 저장된 게임이 있는지 여부

# 상점 아이템 데이터
weapons = [
    {'name': 'Basic Gun', 'desc': 'Standard weapon', 'price': 0, 'icon_id': 3},
    {'name': 'Shotgun', 'desc': 'Spread shot', 'price': 500, 'icon_id': 4},
    {'name': 'Explosive Gun', 'desc': 'Area explosion', 'price': 800, 'icon_id': 5}
]

items = [
    {'name': 'HP Boost', 'desc': '+50 Max HP', 'price': 300, 'icon_id': 5},
    {'name': 'Speed Up', 'desc': '+20% Speed', 'price': 250, 'icon_id': 6},
    {'name': 'Damage Up', 'desc': '+30% Damage', 'price': 400, 'icon_id': 3},
    {'name': 'Fire Rate', 'desc': '+25% Fire Rate', 'price': 350, 'icon_id': 4},
    {'name': 'HP Refill', 'desc': 'Full HP Restore', 'price': 200, 'icon_id': 7}
]

# 상점 UI 변수
animation_time = 0
font = None
title_font = None
button_image = None
button_selected = None
display_panel = None
icon_images = {}
gold_icon = None
selected_tab = 0  # 0: 무기, 1: 아이템
selected_index = 0

def init():
    global animation_time, font, title_font, button_image, button_selected, display_panel, icon_images, gold_icon
    global selected_tab, selected_index

    animation_time = 0
    selected_tab = 0
    selected_index = 0

    # 폰트 로드
    try:
        font = load_font('C:/Windows/Fonts/arial.ttf', 20)
        title_font = load_font('C:/Windows/Fonts/arial.ttf', 40)
    except:
        font = None
        title_font = None

    # GUI 이미지 로드
    try:
        button_image = load_image('./04.GUI/PNG/GUI_Main_Button_1_Base.png')
        button_selected = load_image('./04.GUI/PNG/GUI_Main_Button_1.png')
        display_panel = load_image('./04.GUI/PNG/Display_12.png')
        gold_icon = load_image('./04.GUI/PNG/GUI_gold_1.png')

        # 아이템 아이콘들 로드
        for i in range(1, 11):
            try:
                icon_images[i] = load_image(f'./03.아이템&아이콘/PNG/Item_{i}.png')
            except:
                pass
    except:
        pass

def finish():
    pass

def handle_events():
    global selected_tab, selected_index
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # 상점 종료하고 플레이로 복귀 (골드와 아이템 적용)
                apply_items_and_return()
            elif event.key == SDLK_LEFT:
                selected_tab = 0  # 무기 탭
            elif event.key == SDLK_RIGHT:
                selected_tab = 1  # 아이템 탭
            elif event.key == SDLK_UP or event.key == SDLK_w:
                if selected_tab == 0:
                    selected_index = (selected_index - 1) % len(weapons)
                else:
                    selected_index = (selected_index - 1) % len(items)
            elif event.key == SDLK_DOWN or event.key == SDLK_s:
                if selected_tab == 0:
                    selected_index = (selected_index + 1) % len(weapons)
                else:
                    selected_index = (selected_index + 1) % len(items)
            elif event.key == SDLK_RETURN or event.key == SDLK_SPACE:
                purchase_item()

def apply_items_and_return():
    """구매한 아이템을 플레이어에게 적용하고 복귀"""
    import play_mode

    # 플레이어가 있는지 확인 (게임 중인지 확인)
    if play_mode.player is None:
        # 타이틀에서 상점에 온 경우 - 타이틀로 복귀
        # change_mode 대신 pop_mode 사용 (스택에서 안전하게 제거)
        game_framework.pop_mode()
        return

    # 게임 중인 경우 - 골드 동기화 및 아이템 적용
    play_mode.player_gold = GameData.player_gold

    # 무기 변경 적용
    player = play_mode.player
    player.weapon_type = GameData.selected_weapon

    # 구매한 아이템 효과 적용
    for item_id in GameData.selected_items:
        item = items[item_id]
        if item['name'] == 'HP Boost':
            player.max_hp += 50
            player.hp = min(player.hp + 50, player.max_hp)
        elif item['name'] == 'Speed Up':
            player.max_speed *= 1.2
        elif item['name'] == 'Damage Up':
            player.bullet_damage = int(player.bullet_damage * 1.3)
        elif item['name'] == 'Fire Rate':
            player.fire_rate = max(0.05, player.fire_rate * 0.75)
        elif item['name'] == 'HP Refill':
            # 즉시 체력 풀충전
            player.hp = player.max_hp

    # 구매한 아이템 리스트 초기화 (중복 적용 방지)
    GameData.selected_items = []

    # 플레이어 입력 상태 초기화
    player.reset_input_state()

    # 플레이 모드로 복귀
    play_mode.game_paused = False
    game_framework.pop_mode()

def purchase_item():
    """아이템/무기 구매"""
    global selected_index, selected_tab

    if selected_tab == 0:  # 무기 구매 - 한 번만 구매, 이후엔 무료 교체
        weapon = weapons[selected_index]

        # 이미 구매한 무기면 무료로 교체
        if selected_index in GameData.purchased_weapons:
            GameData.selected_weapon = selected_index
        # 구매하지 않은 무기면 골드로 구매
        elif GameData.player_gold >= weapon['price']:
            GameData.player_gold -= weapon['price']
            GameData.purchased_weapons.append(selected_index)
            GameData.selected_weapon = selected_index
    else:  # 아이템 구매 - 무제한 구매 가능
        item = items[selected_index]
        # 골드가 충분하면 무제한 구매 가능
        if GameData.player_gold >= item['price']:
            GameData.player_gold -= item['price']

            # HP Refill은 카운트하지 않음 (즉시 효과만)
            if item['name'] != 'HP Refill':
                # 구매 횟수 증가
                if selected_index not in GameData.item_counts:
                    GameData.item_counts[selected_index] = 0
                GameData.item_counts[selected_index] += 1

                # 첫 구매 시 purchased_items에 추가
                if selected_index not in GameData.purchased_items:
                    GameData.purchased_items.append(selected_index)

            # 적용 대기 목록에 추가 (웨이브 완료 시 적용용)
            GameData.selected_items.append(selected_index)

def draw():
    clear_canvas()

    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()

    # 어두운 배경 (깜빡임 방지를 위해 게임 화면 그리기 제거)
    from pico2d import draw_rectangle
    draw_rectangle(0, 0, canvas_width, canvas_height)

    # 타이틀
    if display_panel:
        display_panel.draw(canvas_width // 2, canvas_height - 60, 300, 80)
    if title_font:
        title_font.draw(canvas_width // 2 - 70, canvas_height - 70, 'SHOP', (255, 215, 0))

    # 골드 표시
    if display_panel:
        display_panel.draw(canvas_width - 120, canvas_height - 60, 200, 50)
    if gold_icon:
        gold_icon.draw(canvas_width - 180, canvas_height - 60, 30, 30)
    if font:
        font.draw(canvas_width - 150, canvas_height - 70, f'{GameData.player_gold}G', (255, 215, 0))

    # 탭 버튼 (무기 / 아이템)
    tab_y = canvas_height - 140

    # 무기 탭
    if selected_tab == 0:
        if button_selected:
            button_selected.draw(canvas_width // 2 - 120, tab_y, 200, 50)
    else:
        if button_image:
            button_image.draw(canvas_width // 2 - 120, tab_y, 200, 50)
    if font:
        font.draw(canvas_width // 2 - 170, tab_y - 10, 'Weapons', (255, 255, 255))

    # 아이템 탭
    if selected_tab == 1:
        if button_selected:
            button_selected.draw(canvas_width // 2 + 120, tab_y, 200, 50)
    else:
        if button_image:
            button_image.draw(canvas_width // 2 + 120, tab_y, 200, 50)
    if font:
        font.draw(canvas_width // 2 + 80, tab_y - 10, 'Items', (255, 255, 255))

    # 아이템 목록 표시
    items_to_show = weapons if selected_tab == 0 else items
    start_y = canvas_height - 200  # 230에서 200으로 올림

    for i, item in enumerate(items_to_show):
        y = start_y - i * 75  # 90에서 75로 간격 축소

        # 화면 밖으로 나가면 그리지 않음
        if y < 80:
            continue

        # 선택된 아이템 - 애니메이션 제거 (깜빡임 방지)
        if i == selected_index:
            if button_selected:
                button_selected.draw(canvas_width // 2, y, 600, 60)  # 높이도 70에서 60으로 축소
        else:
            if button_image:
                button_image.draw(canvas_width // 2, y, 600, 60)

        # 아이콘
        if item['icon_id'] in icon_images:
            icon_images[item['icon_id']].draw(canvas_width // 2 - 250, y, 40, 40)

        # 아이템 정보
        if font:
            font.draw(canvas_width // 2 - 200, y + 10, item['name'], (255, 255, 255))
            # 작은 폰트 - init에서 로드한 것 사용 (매번 로드하지 않음)
            small_font = load_font('C:/Windows/Fonts/arial.ttf', 16)
            small_font.draw(canvas_width // 2 - 200, y - 10, item['desc'], (200, 200, 200))

            # 가격 표시
            price_color = (255, 215, 0) if GameData.player_gold >= item['price'] else (255, 100, 100)
            font.draw(canvas_width // 2 + 150, y - 5, f"{item['price']}G", price_color)

            # 구매 여부 표시
            if selected_tab == 0:  # 무기 탭
                if i == GameData.selected_weapon:
                    font.draw(canvas_width // 2 + 220, y - 5, '[Equipped]', (100, 255, 100))
                elif i in GameData.purchased_weapons:
                    font.draw(canvas_width // 2 + 220, y - 5, '[Owned]', (150, 150, 255))
            elif selected_tab == 1:  # 아이템 탭
                # HP Refill은 카운트 표시 안함
                if items[i]['name'] != 'HP Refill' and i in GameData.purchased_items:
                    # 구매 횟수 표시
                    count = GameData.item_counts.get(i, 0)
                    font.draw(canvas_width // 2 + 220, y - 5, f'x{count}', (100, 255, 100))

    # 하단 안내 메시지
    if display_panel:
        display_panel.draw(canvas_width // 2, 40, 700, 50)
    if font:
        # 깜빡임 제거 - 고정된 색상 사용
        text_color = (200, 200, 200)
        font.draw(canvas_width // 2 - 320, 35, 'Arrow Keys: Navigate | Enter: Buy | ESC: Continue Play', text_color)

    update_canvas()

def update():
    global animation_time
    animation_time += game_framework.frame_time

def pause():
    pass

def resume():
    pass

