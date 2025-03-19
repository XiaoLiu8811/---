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
        self.head_up = pygame.Surface((20, 20), pygame.SRCALPHA)
        # 绘制方形底部（与身体相连的部分）
        pygame.draw.rect(self.head_up, (144, 238, 144), (2, 10, 16, 8))
        # 绘制半圆形顶部
        pygame.draw.ellipse(self.head_up, (144, 238, 144), (2, 2, 16, 16))
        # 添加眼睛（黑色）
        pygame.draw.ellipse(self.head_up, (0, 0, 0), (4, 5, 5, 5))
        pygame.draw.ellipse(self.head_up, (0, 0, 0), (10, 5, 5, 5))
        # 添加分叉舌头（红色）
        # 主舌头
        pygame.draw.rect(self.head_up, (255, 0, 0), (8, -2, 4, 6))
        # 左分叉
        pygame.draw.line(self.head_up, (255, 0, 0), (8, -2), (6, -6), 2)
        # 右分叉
        pygame.draw.line(self.head_up, (255, 0, 0), (12, -2), (14, -6), 2)

        # 通过旋转创建其他方向的蛇头图像
        self.head_down = pygame.transform.rotate(self.head_up, 180)
        self.head_right = pygame.transform.rotate(self.head_up, -90)
        self.head_left = pygame.transform.rotate(self.head_up, 90)
        
        # 创建并设置蛇身体的图像（浅绿色）
        self.body_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.body_surface, (144, 238, 144), (2, 2, 16, 16))
        
        # 创建蛇尾的不同方向的图像（浅绿色）
        self.tail_up = pygame.Surface((20, 20), pygame.SRCALPHA)
        # 绘制方形底部（与身体相连的部分）
        pygame.draw.rect(self.tail_up, (144, 238, 144), (2, 10, 16, 8))
        # 绘制半圆形顶部
        pygame.draw.ellipse(self.tail_up, (144, 238, 144), (2, 2, 16, 16))
        
        # 通过旋转创建其他方向的蛇尾图像
        self.tail_down = pygame.transform.rotate(self.tail_up, 180)
        self.tail_right = pygame.transform.rotate(self.tail_up, -90)
        self.tail_left = pygame.transform.rotate(self.tail_up, 90)
    
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
        
        # 绘制蛇身和连接部分
        for i in range(1, len(self.body)):
            current = self.body[i]
            prev = self.body[i-1]
            
            # 绘制当前节点
            segment_rect = pygame.Rect(current.x * 20, current.y * 20, 20, 20)
            if i == len(self.body) - 1:  # 如果是尾部
                # 计算尾部移动方向（使用倒数第二个节点和最后一个节点的位置差）
                tail_direction = self.body[-2] - self.body[-1]
                # 根据尾部移动方向选择对应的尾部图像
                if tail_direction == Vector2(0, 1):      # 尾部向上移动
                    window.blit(self.tail_up, segment_rect)
                elif tail_direction == Vector2(0, -1):   # 尾部向下移动
                    window.blit(self.tail_down, segment_rect)
                elif tail_direction == Vector2(-1, 0):   # 尾部向右移动
                    window.blit(self.tail_right, segment_rect)
                else:                                    # 尾部向左移动
                    window.blit(self.tail_left, segment_rect)
            else:
                window.blit(self.body_surface, segment_rect)
            
            # 绘制与前一个节点的连接
            if current.x == prev.x:  # 垂直连接
                connect_rect = pygame.Rect(
                    current.x * 20 + 2,
                    min(current.y, prev.y) * 20 + 16,
                    16,
                    abs(current.y - prev.y) * 20 - 12
                )
                pygame.draw.rect(window, (144, 238, 144), connect_rect)
            else:  # 水平连接
                connect_rect = pygame.Rect(
                    min(current.x, prev.x) * 20 + 16,
                    current.y * 20 + 2,
                    abs(current.x - prev.x) * 20 - 12,
                    16
                )
                pygame.draw.rect(window, (144, 238, 144), connect_rect)
    
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
    
    def shrink(self):
        """将蛇的长度减半"""
        if len(self.body) > 3:  # 保持最小长度为3
            self.body = self.body[:len(self.body)//2]
    
    def double(self):
        """将蛇的长度翻倍"""
        old_body = self.body[:]
        for segment in old_body[1:]:
            self.body.append(segment)
    
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
    # 食物类型常量
    NORMAL = 'normal'  # 普通食物（红色圆形）
    POISON = 'poison'  # 毒药（绿色菱形）
    STAR = 'star'     # 星星（金色五角星）
    
    def __init__(self, grid_width, grid_height):
        """初始化食物
        
        Args:
            grid_width (int): 游戏区域的宽度（格子数）
            grid_height (int): 游戏区域的高度（格子数）
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.normal_pos = self.randomize_position()  # 普通食物位置
        self.poison_positions = []  # 毒药位置列表
        self.star_pos = None  # 星星位置
        self.poison_spawn_times = []  # 毒药出现时间列表
        self.star_spawn_time = 0  # 星星出现时间
        self.rotation = 0  # 星星旋转角度
        
        # 创建不同类型食物的表面对象
        self.surfaces = {}
        
        # 普通食物（红色圆形）
        normal_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(normal_surface, (255, 0, 0), (10, 10), 6)
        self.surfaces[self.NORMAL] = normal_surface
        
        # 毒药（绿色菱形）
        poison_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        points = [(10, 4), (16, 10), (10, 16), (4, 10)]
        pygame.draw.polygon(poison_surface, (0, 255, 0), points)
        self.surfaces[self.POISON] = poison_surface
        
        # 星星（金色五角星）
        star_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        points = [
            (10, 2),   # 顶点
            (12, 8),   # 右上内点
            (18, 8),   # 右上外点
            (13, 12),  # 右下内点
            (15, 18),  # 右下外点
            (10, 14),  # 底部内点
            (5, 18),   # 左下外点
            (7, 12),   # 左下内点
            (2, 8),    # 左上外点
            (8, 8)     # 左上内点
        ]
        pygame.draw.polygon(star_surface, (255, 215, 0), points)
        self.surfaces[self.STAR] = star_surface
    
    def draw(self, window):
        """在窗口上绘制食物
        
        Args:
            window: pygame窗口对象
        """
        # 绘制普通食物
        normal_rect = pygame.Rect(self.normal_pos.x * 20, self.normal_pos.y * 20, 20, 20)
        window.blit(self.surfaces[self.NORMAL], normal_rect)
        
        # 绘制毒药
        for pos in self.poison_positions:
            poison_rect = pygame.Rect(pos.x * 20, pos.y * 20, 20, 20)
            window.blit(self.surfaces[self.POISON], poison_rect)
        
        # 绘制星星
        if self.star_pos is not None:
            star_rect = pygame.Rect(self.star_pos.x * 20, self.star_pos.y * 20, 20, 20)
            # 旋转星星
            self.rotation = (self.rotation + 2) % 360
            rotated_surface = pygame.transform.rotate(self.surfaces[self.STAR], self.rotation)
            # 获取旋转后的表面的新尺寸
            new_rect = rotated_surface.get_rect(center=star_rect.center)
            window.blit(rotated_surface, new_rect)
    
    def randomize_position(self):
        """随机生成一个新的食物位置
        
        Returns:
            Vector2: 新的食物位置坐标
        """
        return Vector2(randint(0, self.grid_width - 1), randint(0, self.grid_height - 1))
    
    def spawn_poison(self, snake_body):
        """生成新的毒药
        
        Args:
            snake_body: 蛇身体的位置列表
        """
        if len(self.poison_positions) < 5:  # 最多5个毒药
            # 生成新位置，确保不与蛇身重叠
            while True:
                new_pos = self.randomize_position()
                if new_pos not in snake_body:  # 检查是否与蛇身重叠
                    self.poison_positions.append(new_pos)
                    self.poison_spawn_times.append(pygame.time.get_ticks())
                    break
    
    def spawn_star(self):
        """生成新的星星"""
        if self.star_pos is None:  # 只能有一个星星
            self.star_pos = self.randomize_position()
            self.star_spawn_time = pygame.time.get_ticks()
    
    def update(self):
        """更新食物状态"""
        current_time = pygame.time.get_ticks()
        
        # 更新毒药状态（10秒后消失）
        for i in range(len(self.poison_positions) - 1, -1, -1):
            if current_time - self.poison_spawn_times[i] > 10000:  # 10秒 = 10000毫秒
                self.poison_positions.pop(i)
                self.poison_spawn_times.pop(i)
        
        # 更新星星状态（58秒后消失）
        if self.star_pos is not None and current_time - self.star_spawn_time > 58000:  # 58秒 = 58000毫秒
            self.star_pos = None