from pico2d import *
from minimap import Minimap
from resource_path import resource_path

class UI:
    def __init__(self, player):
        self.player = player
        # Windows 기본 폰트 사용
        self.font = load_font('C:/Windows/Fonts/malgun.ttf', 20)
        self.small_font = load_font('C:/Windows/Fonts/malgun.ttf', 16)
        self.title_font = load_font('C:/Windows/Fonts/malgun.ttf', 16)
        self.wave = 1
        self.enemies_killed = 0
        self.enemies_needed = 0  # 웨이브 완료까지 남은 적 수

        # GUI 이미지 로드
        self.hp_bar_base = None
        self.hp_bar_fill = None
        self.display_panel = None
        self.top_line = None
        self.icon_wave = None
        self.icon_kill = None
        self.profile_icon = None
        self.diamond_icon = None

        try:
            self.hp_bar_base = load_image(resource_path('./04.GUI/PNG/Display_2_Base.png'))
            self.hp_bar_fill = load_image(resource_path('./04.GUI/PNG/Display_2_Fill.png'))
            self.display_panel = load_image(resource_path('./04.GUI/PNG/Display_1.png'))
            self.top_line = load_image(resource_path('./04.GUI/PNG/GUI_topline_1.png'))
            self.icon_wave = load_image(resource_path('./03.아이템&아이콘/PNG/Item_1.png'))
            self.icon_kill = load_image(resource_path('./03.아이템&아이콘/PNG/Item_2.png'))
            self.profile_icon = load_image(resource_path('./04.GUI/PNG/Profile_Icon.png'))
            self.diamond_icon = load_image(resource_path('./04.GUI/PNG/GUI_Diamond_1.png'))
        except:
            pass

        # 미니맵 생성 (우측 하단)
        canvas_width = get_canvas_width()
        canvas_height = get_canvas_height()
        minimap_size = 150
        minimap_margin = 20
        self.minimap = Minimap(
            canvas_width - minimap_size // 2 - minimap_margin,
            minimap_size // 2 + minimap_margin,
            minimap_size,
            minimap_size
        )

    def update(self):
        pass

    def draw(self):
        canvas_width = get_canvas_width()
        canvas_height = get_canvas_height()

        # 상단 라인
        if self.top_line:
            self.top_line.draw(canvas_width // 2, canvas_height - 20, canvas_width, 40)

        # 좌측 상단 - 플레이어 프로필 영역
        profile_x = 80
        profile_y = canvas_height - 50

        if self.profile_icon:
            self.profile_icon.draw(profile_x - 60, profile_y, 50, 50)

        # 웨이브 레벨 표시 (프로필 하단)
        if self.diamond_icon:
            self.diamond_icon.draw(profile_x - 35, profile_y - 25, 20, 20)
        self.small_font.draw(profile_x - 25, profile_y - 30, f'Lv.{self.wave}', (255, 255, 100))

        # HP 디스플레이
        hp_x = 150
        hp_y = canvas_height - 50

        if self.hp_bar_base and self.hp_bar_fill:
            # HP 바 베이스
            self.hp_bar_base.draw(hp_x, hp_y, 200, 40)

            # HP 바 채우기 (비율에 따라)
            hp_ratio = max(0, self.player.hp / self.player.max_hp)
            if hp_ratio > 0:
                # clip_draw를 사용하여 비율만큼만 그리기
                fill_width = int(self.hp_bar_fill.w * hp_ratio)
                self.hp_bar_fill.clip_draw(0, 0, fill_width, self.hp_bar_fill.h,
                                          hp_x - (200 * (1 - hp_ratio)) // 2, hp_y,
                                          200 * hp_ratio, 40)

        # HP 텍스트
        self.font.draw(hp_x - 70, hp_y - 5, f'{int(self.player.hp)}/{self.player.max_hp}', (255, 255, 255))

        # 우측 상단 정보 패널
        info_x = canvas_width - 150
        info_y = canvas_height - 50

        # 웨이브 정보
        if self.display_panel:
            self.display_panel.draw(info_x, info_y, 250, 35)

        if self.icon_wave:
            self.icon_wave.draw(info_x - 100, info_y, 25, 25)

        # 웨이브 번호 표시
        self.font.draw(info_x - 80, info_y - 5, f'웨이브: {self.wave}', (255, 255, 255))

        # 처치 수 정보
        if self.display_panel:
            self.display_panel.draw(info_x, info_y - 40, 250, 35)

        if self.icon_kill:
            self.icon_kill.draw(info_x - 100, info_y - 40, 25, 25)

        self.font.draw(info_x - 80, info_y - 45, f'처치: {self.enemies_killed}', (255, 255, 255))

        # 남은 적 수
        if self.enemies_needed > 0:
            if self.display_panel:
                self.display_panel.draw(info_x, info_y - 80, 250, 35)
            self.font.draw(info_x - 80, info_y - 85, f'남은 적: {self.enemies_needed}', (255, 255, 0))

        # 골드 표시 (좌측 하단)
        import play_mode
        gold_x = 100
        gold_y = 50
        if self.display_panel:
            self.display_panel.draw(gold_x, gold_y, 180, 40)
        if self.diamond_icon:
            self.diamond_icon.draw(gold_x - 60, gold_y, 25, 25)
        self.font.draw(gold_x - 40, gold_y - 5, f'골드: {play_mode.player_gold}', (255, 215, 0))

        # 미니맵 그리기 (게임 월드에서 적 목록을 가져와야 함)
        from enemy import Enemy
        import game_world
        enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]
        self.minimap.draw(self.player, enemies)
