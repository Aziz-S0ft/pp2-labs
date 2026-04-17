import pygame
import os
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KBTU Music Player")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 32, bold=True)
playlist = ["song1.mp3", "song2.mp3", "song3.mp3"] 
current_track_index = 0

def play_song():
    pygame.mixer.music.load(playlist[current_track_index])
    pygame.mixer.music.play()

is_playing = False

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not is_playing:
                    play_song()
                    is_playing = True
                else:
                    pygame.mixer.music.unpause()
            
            elif event.key == pygame.K_s:
                pygame.mixer.music.pause()
            
            elif event.key == pygame.K_n:
                current_track_index = (current_track_index + 1) % len(playlist)
                play_song()
                is_playing = True
                
            elif event.key == pygame.K_b:
                current_track_index = (current_track_index - 1) % len(playlist)
                play_song()
                is_playing = True
                
            elif event.key == pygame.K_q:
                running = False

    track_text = title_font.render(f"Track: {playlist[current_track_index]}", True, BLACK)
    screen.blit(track_text, (50, 100))

    status = "Playing" if pygame.mixer.music.get_busy() else "Paused/Stopped"
    status_text = font.render(f"Status: {status}", True, GREEN if is_playing else BLACK)
    screen.blit(status_text, (50, 150))

    controls_help = [
        "P - Play/Unpause",
        "S - Pause (Stop)",
        "N - Next Track",
        "B - Previous Track",
        "Q - Quit"
    ]
    
    for i, line in enumerate(controls_help):
        help_surface = font.render(line, True, (100, 100, 100))
        screen.blit(help_surface, (50, 220 + (i * 30)))

    pygame.display.flip()

pygame.quit()