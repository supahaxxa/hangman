from datetime import datetime
from random import choice
import pygame


BLACK = (0, 0, 0)
GREEN = (94, 172, 100)
GREY = (80, 80, 80)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = (930, 720)

x = 0
y = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

with open("word.txt", 'r') as file:
	everything = file.read().split()
	word = choice(everything)

letters = ''
wrongs = 0
stick = pygame.image.load("stick.png")
font = pygame.font.SysFont("Monospace", 42)


def draw_hangman(n):
	# drawing head
	if n >= 1:
		pygame.draw.circle(screen, WHITE, (465, 75), 50, 12)
	# drawing body
	if n >= 2:
		stick_copy = pygame.transform.rotate(stick, 90)
		stick_copy = pygame.transform.scale_by(stick_copy, 0.125)
		screen.blit(stick_copy, (459, 128))
	# drawing left arm
	if n >= 3:
		stick_copy = pygame.transform.rotate(stick, 45)
		stick_copy = pygame.transform.scale_by(stick_copy, 0.125)
		screen.blit(stick_copy, (380, 124))
	# drawing right arm
	if n >= 4:
		stick_copy = pygame.transform.rotate(stick, 135)
		stick_copy = pygame.transform.scale_by(stick_copy, 0.125)
		screen.blit(stick_copy, (471, 124))
	# drawing left leg
	if n >= 5:
		stick_copy = pygame.transform.rotate(stick, 45)
		stick_copy = pygame.transform.scale_by(stick_copy, 0.125)
		screen.blit(stick_copy, (384, 224))
	# drawing right leg
	if n >= 6:
		stick_copy = pygame.transform.rotate(stick, 135)
		stick_copy = pygame.transform.scale_by(stick_copy, 0.125)
		screen.blit(stick_copy, (467, 224))


def draw_slots(n):
	total_width = (48 * n) + (6 * (n - 1))
	left = (WIDTH - total_width) // 2
	for i in range(n):
		pygame.draw.rect(screen, GREY, pygame.Rect(left, 420, 48, 72), border_radius=8)

		if word[i] in letters:
			text = font.render(word[i], True, GREEN)
			text_rect = text.get_rect()
			text_rect.center = (left + 24, 456)
			screen.blit(text, text_rect)

		left += 54


def complete():
	for i in word:
		if i not in letters:
			return False
	return True


start = datetime.now()
stamped = False
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print(word)
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				print(word)
				quit()
			if pygame.K_a <= event.key <= pygame.K_z and (not complete() or wrongs < 6):
				if chr(event.key) not in letters:
					letters += chr(event.key)
					if chr(event.key) not in word:
						wrongs += 1

	screen.fill(BLACK)

	draw_hangman(wrongs)
	draw_slots(len(word))

	if wrongs >= 6 and not stamped:
		start = datetime.now()
		stamped = True
	if complete() and not stamped:
		start = datetime.now()
		stamped = True
	if (datetime.now() - start).seconds > 1 and complete():
		quit()
	if (datetime.now() - start).seconds > 1 and wrongs >= 6:
		print(word)
		quit()

	pygame.display.update()
