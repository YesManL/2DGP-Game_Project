from pico2d import *

class Minimap:
    def __init__(self, x, y, width, height):
        """
        미니맵 초기화
        x, y: 미니맵 중심 좌표
        width, height: 미니맵 크기
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # 미니맵 이미지 로드
        self.map_bg = None
        self.map_fill = None
        self.map_line = None
        self.marker_player = None
        self.marker_enemy = None

        try:
            self.map_bg = load_image('./04.GUI/PNG/GUI_Map.png')
            self.map_fill = load_image('./04.GUI/PNG/GUI_Map_Fill.png')
            self.map_line = load_image('./04.GUI/PNG/GUI_Map_Line.png')
            self.marker_player = load_image('./04.GUI/PNG/GUI_Marker_Player.png')
            self.marker_enemy = load_image('./04.GUI/PNG/GUI_Marker_Enmy.png')
        except:
            pass

        # 게임 월드 크기 (캔버스 크기와 동일)
        self.world_width = get_canvas_width()
        self.world_height = get_canvas_height()

        # 미니맵 스케일 (게임 월드 좌표 -> 미니맵 좌표)
        self.scale_x = (self.width - 20) / self.world_width  # 여백 10px씩
        self.scale_y = (self.height - 20) / self.world_height

    def world_to_minimap(self, world_x, world_y):
        """게임 월드 좌표를 미니맵 좌표로 변환"""
        # 미니맵의 좌하단 기준점
        minimap_left = self.x - self.width // 2 + 10
        minimap_bottom = self.y - self.height // 2 + 10

        # 월드 좌표를 미니맵 좌표로 변환
        minimap_x = minimap_left + world_x * self.scale_x
        minimap_y = minimap_bottom + world_y * self.scale_y

        return minimap_x, minimap_y

    def draw(self, player, enemies):
        """미니맵 그리기"""
        # 미니맵 배경
        if self.map_bg:
            self.map_bg.draw(self.x, self.y, self.width, self.height)

        # 미니맵 채우기 (어두운 배경)
        if self.map_fill:
            self.map_fill.draw(self.x, self.y, self.width - 10, self.height - 10)

        # 적 마커 그리기 (플레이어보다 먼저 그려서 플레이어가 위에 표시되도록)
        if self.marker_enemy and enemies:
            for enemy in enemies:
                if hasattr(enemy, 'x') and hasattr(enemy, 'y'):
                    map_x, map_y = self.world_to_minimap(enemy.x, enemy.y)
                    self.marker_enemy.draw(map_x, map_y, 8, 8)

        # 플레이어 마커 그리기
        if self.marker_player and player:
            if hasattr(player, 'x') and hasattr(player, 'y'):
                map_x, map_y = self.world_to_minimap(player.x, player.y)
                self.marker_player.draw(map_x, map_y, 10, 10)

        # 미니맵 테두리 (가장 마지막에 그려서 모든 것 위에 표시)
        if self.map_line:
            self.map_line.draw(self.x, self.y, self.width, self.height)

    def update(self):
        pass

