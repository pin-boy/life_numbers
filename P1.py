import tkinter as tk
from tkinter import ttk, scrolledtext
import mpmath
from decimal import Decimal, getcontext
from game_field import GameField


class NumberCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор чисел")
        self.root.geometry("700x700")

        # Настройка точности вычислений
        mpmath.mp.dps = 10001  # Дополнительный знак для округления
        getcontext().prec = 10001  # Для decimal

        self.create_main_window()

    def create_main_window(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))

        btn_pi = ttk.Button(self.root, text="Число Пи",
                            command=self.calculate_pi)
        btn_pi.pack(pady=20)

        btn_e = ttk.Button(self.root, text="Число Эйлера",
                           command=self.calculate_e)
        btn_e.pack(pady=20)

        btn_irrational = ttk.Button(self.root, text="Иррациональные числа",
                                    command=self.show_irrational_window)
        btn_irrational.pack(pady=20)

    def decimal_to_binary(self, decimal_str):
        """Преобразование десятичного числа в двоичное с сохранением точности"""
        # Разделяем число на целую и дробную части
        if '.' in decimal_str:
            integer_part, decimal_part = decimal_str.split('.')
        else:
            integer_part, decimal_part = decimal_str, '0'

        # Конвертируем целую часть
        integer_binary = bin(int(integer_part))[2:]

        # Конвертируем дробную часть
        decimal_value = Decimal('0.' + decimal_part)
        binary_fraction = []

        # Увеличиваем количество итераций для большей точности
        for _ in range(10000):
            decimal_value *= 2
            if decimal_value >= 1:
                binary_fraction.append('1')
                decimal_value -= 1
            else:
                binary_fraction.append('0')

            # Если дошли до нуля, прекращаем
            if decimal_value == 0:
                break

        # Собираем результат
        binary_result = integer_binary + '.' + ''.join(binary_fraction)
        return binary_result

    def show_result(self, title, number):
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("800x700")

        # Создаем фрейм для текстового поля и кнопок
        frame = ttk.Frame(result_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создаем текстовое поле с прокруткой
        text_area = scrolledtext.ScrolledText(frame,
                                              width=70,
                                              height=30,
                                              font=('Courier', 10),
                                              wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        # Сохраняем исходное значение в строковом виде
        original_value = str(number)
        current_value = original_value
        is_binary = False

        # Вставляем значение в текстовое поле
        text_area.insert(tk.INSERT, original_value)
        text_area.configure(state='disabled')

        def convert_to_binary():
            nonlocal current_value, is_binary
            # Очищаем текстовое поле
            text_area.configure(state='normal')
            text_area.delete(1.0, tk.END)

            # Преобразуем число в двоичную систему
            binary = self.decimal_to_binary(current_value)
            current_value = binary
            is_binary = True

            # Вставляем двоичное представление
            text_area.insert(tk.INSERT, binary)
            text_area.configure(state='disabled')

            # Меняем текст кнопки и её функционал
            convert_btn.configure(text="Показать десятичное значение",
                                  command=show_decimal)

        def show_decimal():
            nonlocal current_value, is_binary
            # Возвращаем десятичное представление
            text_area.configure(state='normal')
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.INSERT, original_value)
            text_area.configure(state='disabled')

            current_value = original_value
            is_binary = False

            # Возвращаем исходный текст кнопки и функционал
            convert_btn.configure(text="Преобразовать в двоичную систему",
                                  command=convert_to_binary)

        def merge_number():
            nonlocal current_value
            # Очищаем текстовое поле
            text_area.configure(state='normal')
            text_area.delete(1.0, tk.END)

            # Убираем точку из числа
            merged_value = current_value.replace('.', '')
            current_value = merged_value

            # Вставляем объединенное представление
            text_area.insert(tk.INSERT, merged_value)
            text_area.configure(state='disabled')

            # Обновляем состояние кнопок
            merge_btn.configure(text="Вернуть десятичную точку",
                                command=restore_decimal_point)

        def restore_decimal_point():
            nonlocal current_value
            text_area.configure(state='normal')
            text_area.delete(1.0, tk.END)

            if is_binary:
                # Для двоичного числа
                current_value = self.decimal_to_binary(original_value)
            else:
                # Для десятичного числа
                current_value = original_value

            text_area.insert(tk.INSERT, current_value)
            text_area.configure(state='disabled')

            # Возвращаем исходный текст кнопки
            merge_btn.configure(text="Слияние числа",
                                command=merge_number)

        # Создаем фрейм для кнопок
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        # Создаем кнопку преобразования
        convert_btn = ttk.Button(button_frame,
                                 text="Преобразовать в двоичную систему",
                                 command=convert_to_binary)
        convert_btn.pack(side=tk.LEFT, padx=5)

        # Создаем кнопку слияния
        merge_btn = ttk.Button(button_frame,
                               text="Слияние числа",
                               command=merge_number)
        merge_btn.pack(side=tk.LEFT, padx=5)

        # Добавить в метод show_result класса NumberCalculator:
        def create_game_field():
            # Получаем текущее значение из text_area
            binary_value = current_value
            if not is_binary:
                # Если значение не в двоичной системе, преобразуем его
                binary_value = self.decimal_to_binary(current_value)

            # Создаем игровое поле и передаем двоичное число
            game = GameField(binary_value)
            game.run()

        # Создаем кнопку игрового поля
        game_btn = ttk.Button(button_frame,
                              text="Создать игровое поле",
                              command=create_game_field)
        game_btn.pack(side=tk.LEFT, padx=5)

    def calculate_pi(self):
        pi = mpmath.pi
        self.show_result("Значение числа Пи", pi)

    def calculate_e(self):
        e = mpmath.e
        self.show_result("Значение числа Эйлера", e)

    def show_irrational_window(self):
        irr_window = tk.Toplevel(self.root)
        irr_window.title("Вычисление иррационального числа")
        irr_window.geometry("400x300")

        ttk.Label(irr_window, text="Введите целое число:").pack(pady=10)
        number_entry = ttk.Entry(irr_window)
        number_entry.pack(pady=5)

        ttk.Label(irr_window, text="Введите степень корня:").pack(pady=10)
        root_entry = ttk.Entry(irr_window)
        root_entry.pack(pady=5)

        def calculate_root():
            try:
                number = int(number_entry.get())
                root = int(root_entry.get())

                if root <= 0:
                    raise ValueError("Степень корня должна быть положительной")

                result = mpmath.root(number, root)
                self.show_result(f"Корень {root}-й степени из {number}", result)

            except ValueError as e:
                error_label.config(text=str(e))
                return

        ttk.Button(irr_window, text="Вычислить",
                   command=calculate_root).pack(pady=20)

        error_label = ttk.Label(irr_window, text="", foreground="red")
        error_label.pack(pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    calculator = NumberCalculator()
    calculator.run()