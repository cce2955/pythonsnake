import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define game colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Define game variables
cell_size = 20
game_font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# Define the Snake class
class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "RIGHT"
        self.body = [(x, y), (x-cell_size, y), (x-(2*cell_size), y)]
    
    def move(self):
        if self.direction == "UP":
            self.y -= cell_size
        elif self.direction == "DOWN":
            self.y += cell_size
        elif self.direction == "LEFT":
            self.x -= cell_size
        elif self.direction == "RIGHT":
            self.x += cell_size
        
        # Add the new head to the beginning of the body
        self.body.insert(0, (self.x, self.y))
        
        # Remove the tail if the snake didn't eat the food
        if len(self.body) > 1 and self.body[0] != food_position:
            self.body.pop()
    
    def draw(self):
        for pos in self.body:
            pygame.draw.rect(window, green, (pos[0], pos[1], cell_size, cell_size))

# Define the Food class
class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        x = random.randrange(0, window_width-cell_size, cell_size)
        y = random.randrange(0, window_height-cell_size, cell_size)
        return (x, y)
    
    def draw(self):
        pygame.draw.rect(window, red, (self.position[0], self.position[1], cell_size, cell_size))

# Create the Snake and Food objects
snake = Snake(window_width//2, window_height//2)
food = Food()
food_position = food.position

# Define the game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_s and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_a and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_d and snake.direction != "LEFT":
                snake.direction = "RIGHT"
            elif event.key == pygame.K_r and game_over:
                # Reset the game
                snake = Snake(window_width//2, window_height//2)
                food = Food()
                food_position = food.position
                game_over = False
    
    # Move the Snake
    snake.move()
    
    # Check if the Snake hit the wall or itself
if (snake.x < 0 or snake.x >= window_width or
    snake.y < 0 or snake.y >= window_height or
    snake.body[0] in snake.body[1:]):
    game_over = True

# Check if the Snake ate the Food
if snake.body[0] == food_position:
    food = Food()
    food_position = food.position

# Draw the game objects
window.fill(black)
snake.draw()
food.draw()

# Draw the score
score_text = game_font.render("Score: " + str(len(snake.body)-3), True, white)
window.blit(score_text, (10, 10))

# Update the display
pygame.display.update()

# Set the game speed
clock.tick(10)

# Check if the game is over
if game_over:
    # Draw the game over message
    game_over_text = game_font.render("Game Over! Press R to restart.", True, white)
    window.blit(game_over_text, (window_width//2-game_over_text.get_width()//2, window_height//2-game_over_text.get_height()//2))
    
    # Update the display
    pygame.display.update()
    
    # Wait for the user to press the R key
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset the game
                    snake = Snake(window_width//2, window_height//2)
                    food = Food()
                    food_position = food.position
                    game_over = False