from pico2d import *

class UI:
    def __init__(self, player):
        self.player = player
        # Windows 기본 폰트 사용
        self.font = load_font('C:/Windows/Fonts/arial.ttf', 20)
        self.wave = 1
        self.enemies_killed = 0

    def update(self):
        pass

    def draw(self):
        # HP 표시
        self.font.draw(10, get_canvas_height() - 30, f'HP: {self.player.hp}/{self.player.max_hp}', (255, 255, 255))

        # HP 바 그리기
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = get_canvas_height() - 55

        # 배경 (검은색)
        draw_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height)

        # HP (빨간색)
        hp_ratio = self.player.hp / self.player.max_hp
        if hp_ratio > 0:
            draw_rectangle(bar_x, bar_y, bar_x + bar_width * hp_ratio, bar_y + bar_height)

        # 웨이브 정보
        self.font.draw(get_canvas_width() - 150, get_canvas_height() - 30, f'Wave: {self.wave}', (255, 255, 255))

        # 적 처치 수
        self.font.draw(get_canvas_width() - 150, get_canvas_height() - 60, f'Kills: {self.enemies_killed}', (255, 255, 255))
