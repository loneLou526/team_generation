import random
import pandas as pd
import os
from itertools import zip_longest

class TeamGenerator:
    def __init__(self):
        pass

    def move_rows(self, df, move_map):
        """
        Перемещает строки в DataFrame на новые позиции.

        Аргументы:
        df — исходный DataFrame
        move_map — словарь, где ключ — текущий индекс строки, а значение — новый индекс

        Возвращает:
        DataFrame с перемещёнными строками
        """
        rows_to_move = df.loc[list(move_map.keys())].copy()  # Копируем строки, которые нужно переместить
        df = df.drop(move_map.keys(), errors="ignore").reset_index(drop=True)  # Добавлен `errors="ignore"`

        for old_index, new_index in sorted(move_map.items(), key=lambda x: x[1]):
            if old_index not in rows_to_move.index:
                continue  # Пропускаем, если индекс уже удалён

            part1 = df.iloc[:new_index]
            part2 = df.iloc[new_index:]
            df = pd.concat([part1, rows_to_move.loc[[old_index]], part2], ignore_index=True)

        return df

    def create_shaffle_table(self, file_name):
        df = pd.read_excel(file_name)

        keys = list(range(0, df.shape[0]))
        values = list(range(0, df.shape[0]))
        random.shuffle(values)

        # Словарь, где ключ — текущий индекс строки, а значение — новый индекс
        move_map = {k: v for k, v in zip(keys, values)}

        df = self.move_rows(df, move_map)

        df.to_excel("uploaded_files/shaffle_table.xlsx", index=False)

    def generate_team_name(self):
        """Генерирует случайное название команды из 3 слогов."""
        syllables = ["ka", "ra", "mo", "to", "li", "za", "no", "pe", "fu", "bi"]
        name = "".join(random.choices(syllables, k=3)).capitalize()
        return name

    def generate_team(self, file_name, quantity):
        self.create_shaffle_table(file_name)

        # Читаем перемешанный список
        df = pd.read_excel("uploaded_files/shaffle_table.xlsx")
        original_count = len(df)  # Количество участников в оригинальной таблице
        print(f"Оригинальное количество участников: {original_count}")

        while True:
            participants = df['ФИ'].tolist()

            # Разбиваем участников на команды
            teams = [list(filter(None, team)) for team in zip_longest(*[iter(participants)] * quantity, fillvalue=None)]

            # Находим максимальную длину списка (чтобы все столбцы были одинаковой длины)
            max_team_size = max(len(team) for team in teams)

            # Создаём структуру данных для финального DataFrame
            formatted_data = {}
            for i, team in enumerate(teams):
                team_name = self.generate_team_name()
                # Выравниваем список до max_team_size
                formatted_data[team_name] = team + [""] * (max_team_size - len(team))

            result_df = pd.DataFrame(formatted_data)

            # Правильный подсчёт участников (исключаем NaN и пустые строки)
            generated_count = sum(1 for x in result_df.values.flatten() if pd.notna(x) and x != "")

            print(f"Попытка генерации: {generated_count} участников в командах")

            if generated_count == original_count:
                break  # Выходим из цикла, если все участники распределены

            print("Ошибка: не все участники попали в команды или добавились лишние. Повторная генерация...")

        # Сохраняем исправленный файл
        output_file = os.path.join('uploaded_files', "teams.xlsx")
        result_df.to_excel(output_file, index=False)

        print(f"Финальный файл сохранён. Участников: {generated_count}")
        return output_file