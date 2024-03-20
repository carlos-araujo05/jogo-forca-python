import sys
import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.mixer.init()
som_sucesso = pygame.mixer.Sound("success.wav")
som_gameover = pygame.mixer.Sound("gameover.wav")

# Cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Definição da janela
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jogo da forca")

# Lista de palavras para o jogo
words_to_draw = [
    {
        "Linguagem programação": ["PYTHON", "JAVA", "JAVASCRIPT", "RUBY", "PHP", "MYSQL"]
    },
    {
        "País": ["BRASIL", "AFRICA", "COREIA", "ARGENTINA", "PARAGUAY", "JAPAO", "CHINA", "ESTADOS UNIDOS", "ALEMANHA"]
    },
    {
        "Esporte": ["FUTEBOL", "BASQUETE", "VOLEI", "HANDEBOL", "BASEBALL", "NATACAO"],
    }
]

word_dict = random.choice(words_to_draw)

# Seleciona uma palavra aleatória
category, word_list = list(word_dict.items())[0]
word = random.choice(word_list)

# Conjunto de letras adivinhadas
guessed_letters = set()

# Número de tentativas erradas
wrong_guesses = 0

# Coordenadas do ponto inicial do desenho do boneco
hangman_start_x = 250
hangman_start_y = 150

# Tamanho do boneco
hangman_size = 50

# Função para desenhar a forca


def draw_hangman():
    pygame.draw.line(screen, white, (125, 500), (275, 500), 5)
    pygame.draw.line(screen, white, (200, 500), (200, 100), 5)
    pygame.draw.line(screen, white, (200, 100), (300, 100), 5)
    pygame.draw.line(screen, white, (300, 100), (300, 150), 5)

# Função para desenhar o boneco


def draw_hangman_figure():
    # Cabeça
    if wrong_guesses >= 1:
        pygame.draw.circle(screen, white, (hangman_start_x + hangman_size,
                           hangman_start_y + hangman_size), hangman_size, 2)
    # Corpo
    if wrong_guesses >= 2:
        pygame.draw.line(screen, white, (hangman_start_x + hangman_size, hangman_start_y + 2 *
                         hangman_size), (hangman_start_x + hangman_size, hangman_start_y + 4 * hangman_size), 2)
    # Braço esquerdo
    if wrong_guesses >= 3:
        pygame.draw.line(screen, white, (hangman_start_x + hangman_size, hangman_start_y +
                         2 * hangman_size), (hangman_start_x, hangman_start_y + 3 * hangman_size), 2)
    # Braço direito
    if wrong_guesses >= 4:
        pygame.draw.line(screen, white, (hangman_start_x + hangman_size, hangman_start_y + 2 *
                         hangman_size), (hangman_start_x + 2 * hangman_size, hangman_start_y + 3 * hangman_size), 2)
    # Perna esquerda
    if wrong_guesses >= 5:
        pygame.draw.line(screen, white, (hangman_start_x + hangman_size, hangman_start_y +
                         4 * hangman_size), (hangman_start_x, hangman_start_y + 6 * hangman_size), 2)
    # Perna direita
    if wrong_guesses >= 6:
        pygame.draw.line(screen, white, (hangman_start_x + hangman_size, hangman_start_y + 4 *
                         hangman_size), (hangman_start_x + 2 * hangman_size, hangman_start_y + 6 * hangman_size), 2)

# Função para desenhar a palavra


def draw_word():
    display_word = ""
    for letter in word:
        if letter in guessed_letters or letter == " ":
            display_word += letter + " "
        else:
            display_word += "_ "

    font = pygame.font.Font(None, 48)
    text = font.render(display_word, True, white)
    screen.blit(text, (325, 470))

# Função para desenhar as letras já adivinhadas
def draw_guessed_letters():
    guessed_str = ", ".join(sorted(guessed_letters))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Letras Digitadas: {guessed_str}", True, white)
    screen.blit(text, (15, 15))
    mostrar_dica()


# Função para verificar se o jogador ganhou
def check_win():
    return all(letter in guessed_letters or letter == " " for letter in word)

# Função para verificar se o jogador perdeu
def check_loss():
    return wrong_guesses == 6


def select_word():
    word_dict = random.choice(words_to_draw)
    category, word_list = list(word_dict.items())[0]
    return category, random.choice(word_list)
    # return random.choice(words_to_draw)


palavra_escolhida = select_word()


def reset_game():
    global category, word, guessed_letters, wrong_guesses, palavra_escolhida
    category, word = palavra_escolhida
    guessed_letters = set()
    wrong_guesses = 0
    # palavra_escolhida = select_word()


def show_end_message(message):
    font = pygame.font.Font(None, 72)
    text_color = red if "perdeu" in message else green
    text = font.render(message, True, text_color)
    screen.blit(text, (275, 250))
    if "perdeu" in message:
        font = pygame.font.Font(None, 48)
        lost_next = font.render(
            f"A palavra era {palavra_escolhida[1]}", True, red)
        screen.blit(lost_next, (275, 320))
    pygame.display.flip()


def show_restart_popup():
    root = tk.Tk()
    root.withdraw()
    restart = messagebox.askquestion("Fim de jogo", "Deseja jogar novamente?")
    return restart


def mostrar_dica():
    font = pygame.font.Font(None, 24)
    hint_text = f"Dica: {category}"
    text = font.render(hint_text, True, white)
    screen.blit(text, (15, 50))


# Loop principal do jogo
while True:
    reset_game()  # Reinicia o jogo

    # Loop interno para controlar um único jogo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key).upper()
                    if letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter not in word:
                            wrong_guesses += 1

        # Limpa a tela
        screen.fill(black)

        # Desenha a forca
        draw_hangman()

        # Desenha o boneco
        draw_hangman_figure()

        # Desenha a palavra
        draw_word()

        # Desenha as letras já adivinhadas
        draw_guessed_letters()

        # Verifica se o jogador ganhou
        if check_win():
            show_end_message("Você venceu!")
            som_sucesso.play()
            restart_choice = show_restart_popup()
            if restart_choice == "yes":
                palavra_escolhida = select_word()
                break  # Reinicia o jogo
            else:
                pygame.quit()
                sys.exit()

        # Verifica se o jogador perdeu
        elif check_loss():
            som_gameover.play()
            show_end_message("Você perdeu!")
            restart_choice = show_restart_popup()
            if restart_choice == "yes":
                palavra_escolhida = select_word()
                break  # Sai do loop interno
            else:
                pygame.quit()
                sys.exit()

        # Atualiza a tela
        pygame.display.flip()
