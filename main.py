from pico2d import open_canvas, close_canvas
import game_framework
import title_mode

# 게임 윈도우 생성 (800x600)
open_canvas(800, 600)

# 게임 시작 - 타이틀 화면부터
game_framework.run(title_mode)

# 게임 종료 시 윈도우 닫기
close_canvas()
