import pygame
import random
import sys

pygame.init()
FONT = pygame.font.SysFont(None, 28)
BIGFONT = pygame.font.SysFont(None, 36)

# настройки игры
BOARD_N = 4          # размер доски 4х4 (пятнашки)
TILE_SIZE = 80       # размер одной плитки в пикселях
MARGIN = 20          # отступы от краёв экрана
GAP = 10             # расстояние между плитками

# цвета
BG = (30, 30, 30)            # фон
TILE_COLOR = (200, 200, 200) # цвет плиток
EMPTY_COLOR = (50, 50, 50)   # цвет пустой клетки (0)
TEXT_COLOR = (10, 10, 10)    # цвет цифр на плитках
WIN_COLOR = (0, 200, 0)      # цвет текста при победе

# проверка, решаема ли конфигурация плиток
def is_solvable(tiles, n):
    inv_count = 0
    arr = [t for t in tiles if t != 0]
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    # координата пустой клетки снизу
    blank_row_from_bottom = n - (tiles.index(0) // n)
    # условие решаемости
    if n % 2 == 1:
        return inv_count % 2 == 0
    else:
        return (inv_count + blank_row_from_bottom) % 2 == 0

# Класс доски — каждая доска хранит своё состояние плиток
class Board:
    def __init__(self, n=4, pos=(0,0)):
        self.n = n              # размер доски (n x n)
        self.pos = pos          # где рисовать доску (координаты на экране)
        self.reset()            # сразу создаём новую раскладку

    def reset(self):
        # генерируем случайную решаемую раскладку
        while True:
            self.tiles = list(range(1, self.n*self.n)) + [0]
            random.shuffle(self.tiles)
            if is_solvable(self.tiles, self.n):
                break
        self.moves = 0              # счётчик ходов

    def draw(self, surface):
        # рисуем плитки на экране
        x0, y0 = self.pos
        w = self.n
        for idx, val in enumerate(self.tiles):
            rx = idx % w   # колонка
            ry = idx // w  # строка
            # прямоугольник плитки
            tile_rect = pygame.Rect(x0 + rx*(TILE_SIZE+GAP), y0 + ry*(TILE_SIZE+GAP), TILE_SIZE, TILE_SIZE)
            if val == 0:
                # пустая клетка
                pygame.draw.rect(surface, EMPTY_COLOR, tile_rect, border_radius=6)
            else:
                # плитка с числом
                pygame.draw.rect(surface, TILE_COLOR, tile_rect, border_radius=6)
                txt = BIGFONT.render(str(val), True, TEXT_COLOR)
                txt_r = txt.get_rect(center=tile_rect.center)
                surface.blit(txt, txt_r)

    def try_move(self, idx):
        # попытка сдвинуть плитку по индексу
        blank = self.tiles.index(0)         # где находится пустая клетка
        bx, by = blank % self.n, blank // self.n
        ix, iy = idx % self.n, idx // self.n
        # плитка может двигаться только если она рядом с пустой
        if abs(bx - ix) + abs(by - iy) == 1:
            # меняем местами выбранную плитку и пустую
            self.tiles[blank], self.tiles[idx] = self.tiles[idx], self.tiles[blank]
            self.moves += 1
            return True
        return False

    def click(self, mouse_pos):
        # обработка клика мышкой
        x0, y0 = self.pos
        mx, my = mouse_pos
        w = self.n
        rx = (mx - x0) // (TILE_SIZE + GAP)
        ry = (my - y0) // (TILE_SIZE + GAP)
        if 0 <= rx < w and 0 <= ry < w:
            idx = ry * w + rx
            return self.try_move(idx)
        return False

    def move_by_key(self, key, controls):
        # обработка управления с клавиатуры
        blank = self.tiles.index(0)
        x, y = blank % self.n, blank // self.n
        target = None
        # проверяем какая кнопка нажата и где можно сдвинуть пустую клетку
        if key == controls['left'] and x < self.n - 1:
            target = blank + 1
        elif key == controls['right'] and x > 0:
            target = blank - 1
        elif key == controls['up'] and y < self.n - 1:
            target = blank + self.n
        elif key == controls['down'] and y > 0:
            target = blank - self.n
        if target is not None:
            return self.try_move(target)
        return False

    def is_solved(self):
        # проверка победы: числа идут по порядку, последняя клетка = 0
        return self.tiles == list(range(1, self.n*self.n)) + [0]

# размеры окна (рассчитываются для 2 досок)
SCREEN_W = 2*(TILE_SIZE*BOARD_N + (BOARD_N-1)*GAP) + 3*MARGIN
SCREEN_H = TILE_SIZE*BOARD_N + (BOARD_N-1)*GAP + 2*MARGIN + 100
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Пятнашки — два игрока')
clock = pygame.time.Clock()

def game_loop():
    # создаём две доски: левую и правую
    left_x = MARGIN
    right_x = SCREEN_W - (BOARD_N*TILE_SIZE + (BOARD_N-1)*GAP) - MARGIN
    y = MARGIN
    b1 = Board(BOARD_N, pos=(left_x, y))
    b2 = Board(BOARD_N, pos=(right_x, y))
    boards = [b1, b2]

    # управление для игроков
    controls1 = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}
    controls2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}

    winner = None  # сюда запишем номер победившего игрока

    while True:
        screen.fill(BG)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                # проверяем, какую кнопку нажал игрок 1
                b1.move_by_key(event.key, controls1)
                # проверяем, какую кнопку нажал игрок 2
                b2.move_by_key(event.key, controls2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for b in boards:
                    b.click((mx,my))

        # проверяем победу, если ещё никто не выиграл
        if winner is None:
            if b1.is_solved():
                winner = 1
            elif b2.is_solved():
                winner = 2

        # рисуем обе доски и счётчики ходов
        for i, b in enumerate(boards):
            b.draw(screen)
            px, py = b.pos
            moves_txt = FONT.render(f'Игрок {i+1} — Ходы: {b.moves}', True, (220,220,220))
            screen.blit(moves_txt, (px, SCREEN_H - 60))

        # если есть победитель — пишем сообщение в центре экрана
        if winner is not None:
            win_txt = BIGFONT.render(f'Игрок {winner} победил!', True, WIN_COLOR)
            win_r = win_txt.get_rect(center=(SCREEN_W//2, SCREEN_H-30))
            screen.blit(win_txt, win_r)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    game_loop()
