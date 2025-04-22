import pygame
import random
import sys
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de Esquivar Obstáculos")

# Reloj para controlar el FPS
clock = pygame.time.Clock()
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Configuración del jugador
player_size = 50
player_speed = 7
player_rect = pygame.Rect(width // 2 - player_size // 2, height // 2 - player_size // 2, player_size, player_size)

# Configuración de los obstáculos
obstacle_size = 50
base_obstacle_speed = 7  # Aumentada la velocidad inicial
initial_obstacle_spawn_delay = 1200  # Más rápido desde el inicio
obstacles = []

# Puntaje y mejor puntaje
score = 0
highscore = 0
highscore_file = "highscore.txt"

# Fuente para mostrar el puntaje
font = pygame.font.SysFont("Arial", 24)

def load_highscore():
    """Carga el mejor puntaje desde un archivo."""
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(score):
    """Guarda el mejor puntaje en un archivo."""
    with open(highscore_file, "w") as f:
        f.write(str(score))

def spawn_obstacles(num=1):
    """Crea 'num' obstáculos en posiciones aleatorias desde arriba, izquierda o derecha."""
    for _ in range(num):
        direction = random.choice(["top", "left", "right"])  
        
        if direction == "top":
            x, y = random.randint(0, width - obstacle_size), -obstacle_size
            speed_x, speed_y = 0, base_obstacle_speed + score // 10  # Aumenta velocidad con el puntaje
        elif direction == "left":
            x, y = -obstacle_size, random.randint(0, height - obstacle_size)
            speed_x, speed_y = base_obstacle_speed + score // 10, 0
        else:  
            x, y = width, random.randint(0, height - obstacle_size)
            speed_x, speed_y = -(base_obstacle_speed + score // 10), 0  

        rect = pygame.Rect(x, y, obstacle_size, obstacle_size)
        obstacles.append({"rect": rect, "speed_x": speed_x, "speed_y": speed_y})

def move_obstacles():
    """Mueve los obstáculos y elimina los que salen de pantalla."""
    global score
    for obs in obstacles:
        obs["rect"].x += obs["speed_x"]
        obs["rect"].y += obs["speed_y"]

    # Incrementa el puntaje por cada obstáculo esquivado
    passed_obstacles = [obs for obs in obstacles if obs["rect"].y > height or obs["rect"].x > width or obs["rect"].x < -obstacle_size]
    score += len(passed_obstacles)

    # Mantiene solo los obstáculos en pantalla
    obstacles[:] = [obs for obs in obstacles if obs["rect"].y <= height and -obstacle_size <= obs["rect"].x <= width]

def draw_obstacles():
    """Dibuja todos los obstáculos en la pantalla."""
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs["rect"])

def check_collisions():
    """Verifica si el jugador colisiona con algún obstáculo."""
    for obs in obstacles:
        if player_rect.colliderect(obs["rect"]):
            return True
    return False

def display_score():
    """Muestra el puntaje actual y el mejor puntaje."""
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    highscore_text = font.render("Highscore: " + str(highscore), True, BLACK)
    screen.blit(highscore_text, (10, 40))

def game_over_screen():
    """Pantalla de Game Over que muestra el puntaje y permite reiniciar o salir."""
    global highscore
    if score > highscore:
        highscore = score
        save_highscore(highscore)
    
    screen.fill(WHITE)
    game_over_text = font.render("Game Over! Score: " + str(score), True, BLACK)
    restart_text = font.render("Presiona R para reiniciar o Q para salir", True, BLACK)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 30))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 10))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def reset_game():
    """Reinicia las variables del juego."""
    global score, obstacles, player_rect
    score = 0
    obstacles = []
    player_rect.x = width // 2 - player_size // 2
    player_rect.y = height // 2 - player_size // 2

def main():
    global score, obstacles, highscore
    highscore = load_highscore()
    running_game = True

    while running_game:
        reset_game()
        last_obstacle_spawn_time = pygame.time.get_ticks()

        playing = True
        while playing:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.x > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.x < width - player_size:
                player_rect.x += player_speed
            if keys[pygame.K_UP] and player_rect.y > 0:
                player_rect.y -= player_speed
            if keys[pygame.K_DOWN] and player_rect.y < height - player_size:
                player_rect.y += player_speed

            # Ajuste de dificultad
            current_spawn_delay = max(300, initial_obstacle_spawn_delay - score * 3)  # Obstáculos más seguidos
            num_to_spawn = min(8, 2 + score // 10)  # Más enemigos en pantalla

            current_time = pygame.time.get_ticks()
            if current_time - last_obstacle_spawn_time > current_spawn_delay:
                spawn_obstacles(num_to_spawn)
                last_obstacle_spawn_time = current_time

            move_obstacles()

            if check_collisions():
                playing = False

            # Dibuja todo en pantalla
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, player_rect)
            draw_obstacles()
            display_score()
            pygame.display.flip()

        game_over_screen()

if __name__ == "__main__":
    main()
    pygame.quit()  