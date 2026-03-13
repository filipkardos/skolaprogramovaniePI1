import pygame
import math
import random
from typing import List, Tuple

pygame.init()

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# World map (1 = wall, 0 = empty)
WORLD_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0.05
        self.health = 100
        self.ammo = 100
        self.weapon_frame = 0
        self.is_shooting = False

    def move(self, forward, strafe):
        new_x = self.x + math.cos(self.angle) * forward * self.speed - math.sin(self.angle) * strafe * self.speed
        new_y = self.y + math.sin(self.angle) * forward * self.speed + math.cos(self.angle) * strafe * self.speed
        
        # Simple collision detection
        if 0 < new_x < len(WORLD_MAP[0]) - 0.5 and 0 < new_y < len(WORLD_MAP) - 0.5:
            if WORLD_MAP[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y

    def rotate(self, angle):
        self.angle += angle

    def shoot(self):
        if self.ammo > 0:
            self.is_shooting = True
            self.weapon_frame = 0
            self.ammo -= 1


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 30
        self.speed = 0.02
        self.size = 0.3
        self.distance = 0
        self.angle_to_player = 0

    def move(self, player_x, player_y):
        # Move towards player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 1:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
            # Collision with walls
            if WORLD_MAP[int(self.y)][int(self.x)] == 1:
                self.x -= (dx / distance) * self.speed
                self.y -= (dy / distance) * self.speed
        
        self.distance = distance
        self.angle_to_player = math.atan2(dy, dx)

    def draw(self, surface, screen_width, screen_height, player_angle):
        if self.distance > 0:
            # Calculate sprite position on screen
            angle_diff = self.angle_to_player - player_angle
            
            # Normalize angle
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            sprite_x = screen_width / 2 + angle_diff * (screen_width / 2) / math.tan(math.radians(30))
            
            # Size based on distance
            sprite_size = max(5, 50 / self.distance)
            sprite_y = screen_height / 2
            
            if 0 < sprite_x < screen_width:
                color = RED
                if self.health <= 0:
                    color = DARK_GRAY
                
                pygame.draw.circle(surface, color, (int(sprite_x), int(sprite_y)), int(sprite_size))
                # Draw health bar above enemy
                pygame.draw.line(surface, GREEN, (sprite_x - sprite_size, sprite_y - sprite_size - 10),
                               (sprite_x + sprite_size, sprite_y - sprite_size - 10), 2)
                health_width = (sprite_size * 2) * max(0, self.health / 30)
                pygame.draw.line(surface, RED, (sprite_x - sprite_size, sprite_y - sprite_size - 10),
                               (sprite_x - sprite_size + health_width, sprite_y - sprite_size - 10), 2)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("DOOM - Python Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        self.player = Player(4.5, 4.5)
        self.enemies: List[Enemy] = []
        self.running = True
        self.game_over = False
        self.score = 0
        
        # Spawn enemies
        self.spawn_enemies(5)

    def spawn_enemies(self, count):
        for _ in range(count):
            while True:
                x = random.uniform(1, len(WORLD_MAP[0]) - 1)
                y = random.uniform(1, len(WORLD_MAP) - 1)
                if WORLD_MAP[int(y)][int(x)] == 0:
                    self.enemies.append(Enemy(x, y))
                    break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

        keys = pygame.key.get_pressed()
        forward = (keys[pygame.K_w] - keys[pygame.K_s])
        strafe = (keys[pygame.K_d] - keys[pygame.K_a])
        self.player.move(forward, strafe)
        
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click to shoot
            self.player.shoot()
        
        # Mouse look
        mouse_rel = pygame.mouse.get_rel()
        self.player.rotate(mouse_rel[0] * 0.01)
        
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def raycasting(self):
        # Create 3D view
        fov = math.radians(60)
        half_fov = fov / 2
        num_rays = SCREEN_WIDTH
        
        walls = []
        for col in range(num_rays):
            angle = self.player.angle - half_fov + (col / num_rays) * fov
            
            # Raycast
            distance = self.cast_ray(angle)
            walls.append(distance)
        
        return walls

    def cast_ray(self, angle):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        
        # DDA algorithm for raycasting
        x = self.player.x
        y = self.player.y
        
        max_distance = 20
        step = 0.01
        
        for _ in range(int(max_distance / step)):
            x += cos_a * step
            y += sin_a * step
            
            if x < 0 or x >= len(WORLD_MAP[0]) or y < 0 or y >= len(WORLD_MAP):
                return max_distance
            
            if WORLD_MAP[int(y)][int(x)] == 1:
                distance = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
                # Fix fish-eye effect
                distance *= math.cos(angle - self.player.angle)
                return distance
        
        return max_distance

    def render(self, walls):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw ceiling and floor
        pygame.draw.line(self.screen, GRAY, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        
        # Draw walls
        for col, distance in enumerate(walls):
            if distance > 0:
                wall_height = min(int(SCREEN_HEIGHT / (distance + 0.0001)), SCREEN_HEIGHT)
                color_intensity = max(50, 255 - int(distance * 30))
                color = (color_intensity, 0, 0)
                
                y_start = (SCREEN_HEIGHT - wall_height) // 2
                pygame.draw.line(self.screen, color, (col, y_start), (col, y_start + wall_height), 1)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.player.angle)
        
        # Draw weapon (simple rectangle)
        if self.player.is_shooting:
            self.player.weapon_frame += 1
            if self.player.weapon_frame > 5:
                self.player.is_shooting = False
        
        weapon_y = SCREEN_HEIGHT - 100
        weapon_x = SCREEN_WIDTH - 80
        pygame.draw.rect(self.screen, YELLOW, (weapon_x, weapon_y, 60, 80))
        
        # Check collisions with enemies
        for enemy in self.enemies:
            if self.player.is_shooting and enemy.distance < 10:
                if abs(self.player.angle - enemy.angle_to_player) < 0.3:
                    enemy.health -= 25
                    if enemy.health <= 0:
                        self.score += 100
        
        # Draw HUD
        health_text = self.font.render(f"Health: {max(0, self.player.health)}", True, GREEN)
        ammo_text = self.font.render(f"Ammo: {self.player.ammo}", True, YELLOW)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        enemies_text = self.font.render(f"Enemies: {len([e for e in self.enemies if e.health > 0])}", True, RED)
        
        self.screen.blit(health_text, (10, 10))
        self.screen.blit(ammo_text, (10, 40))
        self.screen.blit(score_text, (10, 70))
        self.screen.blit(enemies_text, (10, 100))
        
        # Check game over
        if self.player.health <= 0:
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

    def update(self):
        # Update enemies
        for enemy in self.enemies:
            enemy.move(self.player.x, self.player.y)
            
            # Enemy attacks player
            if enemy.distance < 1 and enemy.health > 0:
                self.player.health -= 0.1
        
        # Check if all enemies are dead
        if all(e.health <= 0 for e in self.enemies):
            if len(self.enemies) > 0:
                self.spawn_enemies(len(self.enemies) + 1)

    def run(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        while self.running:
            self.handle_input()
            self.update()
            walls = self.raycasting()
            self.render(walls)
            self.clock.tick(FPS)
        
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()