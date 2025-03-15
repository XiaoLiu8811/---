# 导入必要的库
import pygame  # 游戏开发主要库
import sys     # 系统相关功能
from pygame.locals import *  # pygame常量，如事件类型等

# 初始化Pygame
pygame.init()

# 游戏窗口和网格设置
WINDOW_WIDTH = 800    # 窗口宽度（像素）
WINDOW_HEIGHT = 600   # 窗口高度（像素）
GRID_SIZE = 20        # 每个网格的大小（像素）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE    # 横向网格数量
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 纵向网格数量

# 颜色定义（RGB格式）
BLACK = (0, 0, 0)      # 背景色
WHITE = (255, 255, 255) # 文本色
RED = (255, 0, 0)      # 食物颜色
GREEN = (0, 255, 0)    # 蛇身颜色

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')  # 设置窗口标题

# 游戏状态常量
MENU = 'menu'          # 菜单状态
PLAYING = 'playing'    # 游戏进行状态
GAME_OVER = 'game_over' # 游戏结束状态

class Game:
    """游戏主类，负责管理游戏状态和主循环"""
    def __init__(self):
        """初始化游戏"""
        self.state = MENU          # 初始状态设为菜单
        self.clock = pygame.time.Clock()  # 创建时钟对象控制游戏帧率
        
    def run(self):
        """游戏主循环"""
        while True:
            # 根据当前状态执行相应的游戏逻辑
            if self.state == MENU:
                self.show_menu()
            elif self.state == PLAYING:
                self.play_game()
            elif self.state == GAME_OVER:
                self.show_game_over()
            
            pygame.display.update()  # 更新屏幕显示
            self.clock.tick(60)      # 限制游戏帧率为60FPS
    
    def show_menu(self):
        """显示游戏菜单界面"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 如果点击关闭窗口
                pygame.quit()       # 退出pygame
                sys.exit()          # 退出程序
            
        window.fill(BLACK)  # 填充黑色背景
        # TODO: 添加菜单界面实现（标题、开始按钮等）
    
    def play_game(self):
        """游戏主要逻辑实现"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 如果点击关闭窗口
                pygame.quit()       # 退出pygame
                sys.exit()          # 退出程序
            
        window.fill(BLACK)  # 填充黑色背景
        # TODO: 添加游戏逻辑实现（蛇的移动、食物生成、碰撞检测等）
    
    def show_game_over(self):
        """显示游戏结束界面"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 如果点击关闭窗口
                pygame.quit()       # 退出pygame
                sys.exit()          # 退出程序
            
        window.fill(BLACK)  # 填充黑色背景
        # TODO: 添加游戏结束界面实现（显示分数、重新开始按钮等）

if __name__ == '__main__':
    game = Game()
    game.run()