import pygame

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class New_Grid: 
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.grid = [[(255, 255, 255) for _ in range(length)] for _ in range(height)]
        '''
        Same as :
        self.grid = []
        for _ in range(height):
            row = []
            for _ in range(length):
                row.append([255, 255, 255])

            self.grid.append(row)

        [[255,255,255]*length]*height doesn't work though (list comprehension).
        '''

class New_Pen:
    def __init__(self, size):
        self.size = size
        self.color = (0,0,0)
        self.tool = 'pen'
    
    def valid(self, grid, position, start_color):
        if position.x < 0 or position.x > grid.length-1 or position.y < 0 or position.y > grid.height-1:
            return False
        else:
            if grid.grid[position.y][position.x] == start_color:
                return True
            return False

    '''
    THIS DOESN'T WORK ! Never found the problem.
    def recursive_fill(self, grid, position, start_color, new_color):
        # Crashes if it's not an enclosed area. Maybe, if first use, try to make a square around the grid before filling everything or iterate through each cell to color them.
        if position.x < grid.length-1 and position.x >= 0 and position.y < grid.height-1 and position.y >= 0:
            if grid.grid[position.y][position.x] == start_color and start_color != new_color:
                grid.grid[position.y][position.x] = new_color
                self.fill(grid, Vector2(position.x, position.y+1), start_color, new_color)
                self.fill(grid, Vector2(position.x, position.y-1), start_color, new_color)
                self.fill(grid, Vector2(position.x+1, position.y), start_color, new_color)
                self.fill(grid, Vector2(position.x-1, position.y), start_color, new_color)'''

    def iterative_fill(self, grid, position, start_color, new_color):
        if position.x < 0 or position.x > grid.length:
            return
        if position.y < 0 or position.y > grid.height:
            return
        if grid.grid[position.y][position.x] == new_color:
            return
        
        grid.grid[position.y][position.x] = new_color
        queue = []
        queue.append(Vector2(position.x, position.y))

        while len(queue) > 0:
            x = queue[0].x
            y = queue[0].y
            del queue[0]

            if self.valid(grid, Vector2(x, y+1), start_color):
                grid.grid[y+1][x] = new_color
                queue.append(Vector2(x, y+1))
            if self.valid(grid, Vector2(x, y-1), start_color):
                grid.grid[y-1][x] = new_color
                queue.append(Vector2(x, y-1))
            if self.valid(grid, Vector2(x+1, y), start_color):
                grid.grid[y][x+1] = new_color
                queue.append(Vector2(x+1, y))
            if self.valid(grid, Vector2(x-1, y), start_color):
                grid.grid[y][x-1] = new_color
                queue.append(Vector2(x-1, y))

class New_Button:
    def __init__(self, position, dimension, color, action, text='', image=None):
        self.position = position
        self.dimension = dimension
        self.color = color
        self.text = text
        self.action = action
        self.image = image
    
    def draw(self, surface, outline=None): 
        if outline:
            pygame.draw.rect(surface, outline, (self.position.x, self.position.y, self.dimension.x, self.dimension.y), 0)
            pygame.draw.rect(surface, self.color, (self.position.x+2, self.position.y+2, self.dimension.x-4 if self.dimension.x <= 22 else self.dimension.x-5, self.dimension.y-4), 0)
        else:
            pygame.draw.rect(surface, self.color, (self.position.x, self.position.y, self.dimension.x, self.dimension.y), 0)

        if self.image != None:
            surface.blit(self.image, (self.position.x + (self.dimension.x/2 - self.image.get_width()/2), self.position.y + (self.dimension.y/2 - self.image.get_height()/2)))

        if self.text != '':
            font = pygame.font.SysFont('SegoeUI', 20)
            text = font.render(self.text, 1, (0,0,0))
            surface.blit(text, (self.position.x + (self.dimension.x/2 - text.get_width()/2), self.position.y + (self.dimension.y/2 - text.get_height()/2) - 1))

    def is_over(self, pos):
        # pos is the mouse position or a Vector2(x,y)
        if pos.x > self.position.x and pos.x < self.position.x + self.dimension.x:
            if pos.y > self.position.y and pos.y < self.position.y + self.dimension.y:
                return True
        return False

class New_Slider:
    def __init__(self, bar_position, length, direction, bar_color, slider_color, min_value, max_value):
        self.bar_position = bar_position
        self.length = length
        self.direction = direction
        self.bar_color = bar_color
        self.slider_color = slider_color
        self.value = min_value
        self.min_value = min_value
        self.max_value = max_value

        self.slider_position = Vector2(bar_position.x - (7 if self.direction == 'vertical' else 0), bar_position.y - (7 if self.direction == 'horizontal' else 0))
        self.slider_isPressed = False
           
    def draw(self, surface):  
        pygame.draw.rect(surface, self.bar_color, (self.bar_position.x, self.bar_position.y, self.length if self.direction == 'horizontal' else 6, self.length if self.direction == 'vertical' else 6), 0)
        pygame.draw.rect(surface, self.slider_color, (self.slider_position.x, self.slider_position.y, 10 if self.direction == 'horizontal' else 20, 20 if self.direction == 'horizontal' else 10), 0)

    def is_over(self, pos):
        # pos is the mouse position or a Vector2(x,y)
        if pos.x > self.slider_position.x and pos.x < self.slider_position.x + 10 if self.direction == 'horizontal' else 20:
            if pos.y > self.slider_position.y and pos.y < self.slider_position.y + 20 if self.direction == 'horizontal' else 10:
                return True
        return False






