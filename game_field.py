# game_field.py
import pygame
import sys
import copy


class GameField:
    def __init__(self, binary_number=None):
        pygame.init()
        # Размеры игрового поля
        self.FIELD_WIDTH = 700
        self.FIELD_HEIGHT = 700
        # Пространство для информации
        self.INFO_WIDTH = 200
        # Общая ширина окна
        self.WINDOW_WIDTH = self.FIELD_WIDTH + self.INFO_WIDTH
        self.WINDOW_HEIGHT = self.FIELD_HEIGHT

        self.CELL_SIZE = 7
        self.GRID_WIDTH = 100  # Явно задаем количество ячеек
        self.GRID_HEIGHT = 100  # Явно задаем количество ячеек

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (240, 240, 240)

        # Создаем окно и поверхности
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Игровое поле - Игра Жизнь")
        self.game_surface = pygame.Surface((self.FIELD_WIDTH, self.FIELD_HEIGHT))
        self.info_surface = pygame.Surface((self.INFO_WIDTH, self.WINDOW_HEIGHT))

        # Инициализация поля
        self.grid = [[0 for x in range(self.GRID_WIDTH)]
                     for y in range(self.GRID_HEIGHT)]

        # Заполняем поле двоичными числами, если они переданы
        if binary_number:
            self.fill_grid_with_binary(binary_number)

        # Флаги работы
        self.running = True
        self.paused = True
        self.clock = pygame.time.Clock()
        self.generation_speed = 10
        self.generation_count = 0  # Добавляем счетчик поколений

    def fill_grid_with_binary(self, binary_number):
        """Заполнение поля двоичными числами"""
        binary_str = binary_number.replace('.', '')
        binary_str = binary_str[:10000]

        index = 0
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if index < len(binary_str):
                    self.grid[y][x] = int(binary_str[index])
                    index += 1

    def get_neighbors(self, x, y):
        """Получение количества живых соседей с учетом замкнутости поля"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                next_x = (x + dx) % self.GRID_WIDTH
                next_y = (y + dy) % self.GRID_HEIGHT
                count += self.grid[next_y][next_x]
        return count

    def update_grid(self):
        """Обновление состояния клеток по правилам игры Жизнь"""
        new_grid = copy.deepcopy(self.grid)
        changes = False  # Флаг для отслеживания изменений

        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                neighbors = self.get_neighbors(x, y)
                if self.grid[y][x] == 1:  # Живая клетка
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y][x] = 0  # Умирает
                        changes = True
                else:  # Мертвая клетка
                    if neighbors == 3:
                        new_grid[y][x] = 1  # Оживает
                        changes = True

        self.grid = new_grid
        if changes:  # Увеличиваем счетчик только если были изменения
            self.generation_count += 1

    def draw_grid(self):
        """Отрисовка игрового поля"""
        self.game_surface.fill(self.WHITE)

        # Рисуем заполненные ячейки
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.game_surface, self.BLACK,
                                     (x * self.CELL_SIZE,
                                      y * self.CELL_SIZE,
                                      self.CELL_SIZE - 1,
                                      self.CELL_SIZE - 1))

        # Рисуем линии сетки
        for x in range(0, self.FIELD_WIDTH, self.CELL_SIZE):
            pygame.draw.line(self.game_surface, self.GRAY, (x, 0), (x, self.FIELD_HEIGHT))
        for y in range(0, self.FIELD_HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.game_surface, self.GRAY, (0, y), (self.FIELD_WIDTH, y))

    def draw_info(self):
        """Отрисовка информационной панели"""
        self.info_surface.fill(self.LIGHT_GRAY)

        # Рисуем разделительную линию
        pygame.draw.line(self.info_surface, self.GRAY,
                         (self.INFO_WIDTH - 1, 0),
                         (self.INFO_WIDTH - 1, self.WINDOW_HEIGHT), 2)

        font = pygame.font.Font(None, 24)
        info_texts = [
            "Управление:",
            "",
            "ПРОБЕЛ - Пауза/Старт",
            "ВВЕРХ/ВНИЗ - Изменить",
            "скорость",
            "R - Сброс поколений",
            "ESC - Выход",
            "",
            f"Скорость: {self.generation_speed}",
            "поколений/сек",
            "",
            "Статус:",
            ('Пауза' if self.paused else 'Работает'),
            "",
            "Поколение:",
            str(self.generation_count)
        ]

        for i, text in enumerate(info_texts):
            surface = font.render(text, True, self.BLACK)
            self.info_surface.blit(surface, (20, 20 + i * 25))

    def handle_input(self):
        """Обработка пользовательского ввода"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.generation_speed = min(60, self.generation_speed + 5)
                elif event.key == pygame.K_DOWN:
                    self.generation_speed = max(1, self.generation_speed - 5)
                elif event.key == pygame.K_r:  # Добавляем сброс счетчика поколений
                    self.generation_count = 0

    def run(self):
        """Основной цикл игрового поля"""
        while self.running:
            self.handle_input()

            if not self.paused:
                self.update_grid()

            # Отрисовка всех элементов
            self.draw_grid()
            self.draw_info()

            # Отображаем обе поверхности на основном экране
            self.screen.blit(self.info_surface, (0, 0))
            self.screen.blit(self.game_surface, (self.INFO_WIDTH, 0))

            pygame.display.flip()
            self.clock.tick(self.generation_speed)

        pygame.quit()