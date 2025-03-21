# 导入必要的库
import pygame  # 游戏开发主要库
import sys     # 系统相关功能
from pygame.locals import *  # pygame常量，如事件类型等
from snake import Snake, Food  # 导入蛇和食物类
from pygame.math import Vector2  # 导入向量类

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

# 游戏难度常量
EASY = 'easy'      # 简单模式
MEDIUM = 'medium'  # 中等模式
HARD = 'hard'      # 困难模式

class Game:
    """游戏主类，负责管理游戏状态和主循环"""
    def __init__(self):
        """初始化游戏"""
        self.state = MENU          # 初始状态设为菜单
        self.clock = pygame.time.Clock()  # 创建时钟对象控制游戏帧率
        self.snake = Snake()
        self.food = Food(GRID_WIDTH, GRID_HEIGHT)
        self.score = 0
        self.difficulty = MEDIUM    # 默认难度为中等
        self.speed = {
            EASY: 5,    # 简单模式速度
            MEDIUM: 15,  # 中等模式速度
            HARD: 20     # 困难模式速度
        }
        
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
            self.clock.tick(self.speed[self.difficulty])  # 根据难度调整游戏速度
    
    def show_menu(self):
        """显示游戏菜单界面"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 如果点击关闭窗口
                pygame.quit()       # 退出pygame
                sys.exit()          # 退出程序
            elif event.type == KEYDOWN:
                if event.key == K_1:      # 按1键选择简单难度
                    self.difficulty = EASY
                elif event.key == K_2:    # 按2键选择中等难度
                    self.difficulty = MEDIUM
                elif event.key == K_3:    # 按3键选择困难难度
                    self.difficulty = HARD
                elif event.key == K_SPACE:  # 按空格键开始游戏
                    self.state = PLAYING
                    self.snake = Snake()
                    self.food = Food(GRID_WIDTH, GRID_HEIGHT)
                    self.score = 0
            
        window.fill(BLACK)  # 填充黑色背景
        
        # 创建字体对象
        title_font = pygame.font.Font(None, 74)
        menu_font = pygame.font.Font(None, 48)
        
        # 渲染文本
        title = title_font.render('Snake Game', True, WHITE)
        difficulty_text = menu_font.render('Select Difficulty:', True, WHITE)
        easy_text = menu_font.render('1 - Easy', True, WHITE if self.difficulty == EASY else (128, 128, 128))
        medium_text = menu_font.render('2 - Medium', True, WHITE if self.difficulty == MEDIUM else (128, 128, 128))
        hard_text = menu_font.render('3 - Hard', True, WHITE if self.difficulty == HARD else (128, 128, 128))
        start_text = menu_font.render('Press SPACE to Start', True, WHITE)
        
        # 计算文本位置
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/4))
        difficulty_rect = difficulty_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*2/5))
        easy_rect = easy_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*2/4))
        medium_rect = medium_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*2.5/4))
        hard_rect = hard_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*3/4))
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*3.5/4))
        
        # 绘制文本
        window.blit(title, title_rect)
        window.blit(difficulty_text, difficulty_rect)
        window.blit(easy_text, easy_rect)
        window.blit(medium_text, medium_rect)
        window.blit(hard_text, hard_rect)
        window.blit(start_text, start_rect)
    
    def play_game(self):
        """游戏主要逻辑实现"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 如果点击关闭窗口
                pygame.quit()       # 退出pygame
                sys.exit()          # 退出程序
            elif event.type == KEYDOWN:
                if event.key == K_UP and self.snake.direction.y != 1:
                    self.snake.direction = Vector2(0, -1)
                elif event.key == K_DOWN and self.snake.direction.y != -1:
                    self.snake.direction = Vector2(0, 1)
                elif event.key == K_LEFT and self.snake.direction.x != 1:
                    self.snake.direction = Vector2(-1, 0)
                elif event.key == K_RIGHT and self.snake.direction.x != -1:
                    self.snake.direction = Vector2(1, 0)
                elif event.key == K_ESCAPE:  # ESC键暂停
                    self.state = MENU
            
        window.fill(BLACK)  # 填充黑色背景
        
        # 移动蛇
        self.snake.move()
        
        # 检查是否吃到食物
        if self.snake.body[0] == self.food.pos:
            self.snake.grow()
            self.food.randomize_position()
            self.score += 1
        
        # 检查碰撞
        if self.snake.check_collision(GRID_WIDTH, GRID_HEIGHT):
            self.state = GAME_OVER
        
        # 绘制蛇和食物
        self.snake.draw(window)
        self.food.draw(window)
        
        # 显示分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        window.blit(score_text, (10, 10))
    
    def show_game_over(self):
        """显示游戏结束界面"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 如果点击关闭窗口
                pygame.quit()       # 退出pygame
                sys.exit()          # 退出程序
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # 按空格键重新开始
                    self.state = PLAYING
                    self.snake.reset()
                    self.food.randomize_position()
                    self.score = 0
            
        window.fill(BLACK)  # 填充黑色背景
        
        # 创建字体对象
        font = pygame.font.Font(None, 64)
        game_over_text = font.render('Game Over', True, WHITE)
        score_text = font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = font.render('Press SPACE to Restart', True, WHITE)
        
        # 计算文本位置使其居中
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/4))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*3/4))
        
        # 绘制文本
        window.blit(game_over_text, game_over_rect)
        window.blit(score_text, score_rect)
        window.blit(restart_text, restart_rect)

if __name__ == '__main__':
    game = Game()
    game.run()