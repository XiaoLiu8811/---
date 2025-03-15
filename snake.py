# 导入必要的库
import pygame                # pygame游戏库
from pygame.math import Vector2  # 用于处理二维向量
from random import randint      # 用于生成随机数

class Snake:
    """蛇类，负责管理蛇的移动、生长和绘制"""
    def __init__(self):
        """初始化蛇的属性"""
        # 初始化蛇身体，包含三个节点，每个节点用Vector2表示位置
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)  # 初始移动方向：向右
        self.new_block = False          # 是否需要增加新的身体节点
        
        # 创建并设置蛇头的不同方向的图像
        self.head_up = pygame.Surface((20, 20))
        self.head_up.fill((0, 255, 0))  # 设置蛇头颜色
        # 通过旋转创建其他方向的蛇头图像
        self.head_down = pygame.transform.rotate(self.head_up, 180)
        self.head_right = pygame.transform.rotate(self.head_up, -90)
        self.head_left = pygame.transform.rotate(self.head_up, 90)
        
        # 创建并设置蛇身体的图像
        self.body_surface = pygame.Surface((20, 20))
        self.body_surface.fill((0, 200, 0))  # 设置蛇身颜色
    
    def draw(self, window):
        """在窗口上绘制蛇"""
        # 绘制蛇头
        head_rect = pygame.Rect(self.body[0].x * 20, self.body[0].y * 20, 20, 20)
        
        # 根据移动方向选择对应的蛇头图像
        if self.direction == Vector2(0, -1):      # 向上移动
            window.blit(self.head_up, head_rect)
        elif self.direction == Vector2(0, 1):     # 向下移动
            window.blit(self.head_down, head_rect)
        elif self.direction == Vector2(1, 0):     # 向右移动
            window.blit(self.head_right, head_rect)
        else:                                     # 向左移动
            window.blit(self.head_left, head_rect)
        
        # 绘制蛇身
        for segment in self.body[1:]:
            segment_rect = pygame.Rect(segment.x * 20, segment.y * 20, 20, 20)
            window.blit(self.body_surface, segment_rect)
    
    def move(self):
        """移动蛇的位置"""
        if self.new_block:
            # 如果需要增长，复制整个身体并在头部添加新节点
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            # 正常移动：删除尾部，在头部添加新节点
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
    
    def grow(self):
        """标记蛇需要生长"""
        self.new_block = True
    
    def reset(self):
        """重置蛇的位置和方向到初始状态"""
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
    
    def check_collision(self, grid_width, grid_height):
        """检查碰撞
        
        Args:
            grid_width (int): 游戏区域的宽度（格子数）
            grid_height (int): 游戏区域的高度（格子数）
        
        Returns:
            bool: 如果发生碰撞返回True，否则返回False
        """
        # 检查是否撞墙
        if not 0 <= self.body[0].x < grid_width or not 0 <= self.body[0].y < grid_height:
            return True
        
        # 检查是否撞到自己
        for segment in self.body[1:]:
            if segment == self.body[0]:
                return True
        
        return False

class Food:
    """食物类，负责管理食物的位置和显示"""
    def __init__(self, grid_width, grid_height):
        """初始化食物
        
        Args:
            grid_width (int): 游戏区域的宽度（格子数）
            grid_height (int): 游戏区域的高度（格子数）
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.randomize_position()  # 随机生成初始位置
        # 创建食物的表面对象并设置颜色
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((255, 0, 0))  # 设置为红色
    
    def draw(self, window):
        """在窗口上绘制食物
        
        Args:
            window: pygame窗口对象
        """
        food_rect = pygame.Rect(self.position.x * 20, self.position.y * 20, 20, 20)
        window.blit(self.surface, food_rect)
    
    def randomize_position(self):
        """随机生成一个新的食物位置
        
        Returns:
            Vector2: 新的食物位置坐标
        """
        return Vector2(randint(0, self.grid_width - 1), randint(0, self.grid_height - 1))