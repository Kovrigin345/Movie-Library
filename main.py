import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для хранения данных
DATA_FILE = 'movies.json'

# Основной список фильмов
movies = []

# --- Функции для работы с данными ---

def load_data():
    global movies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                movies = json.load(f)
        except json.JSONDecodeError:
            movies = []
    update_table()

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def update_table(filtered_list=None):
    for row in tree.get_children():
        tree.delete(row)
    data_to_show = filtered_list if filtered_list is not None else movies
    for movie in data_to_show:
        tree.insert('', tk.END, values=(movie['title'], movie['genre'], movie['year'], movie['rating']))

def add_movie():
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year_str = year_entry.get().strip()
    rating_str = rating_entry.get().strip()

    if not title or not genre or not year_str or not rating_str:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return
    try:
        year = int(year_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть числом.")
        return
    try:
        rating = float(rating_str)
        if not (0 <= rating <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
        return

    movie = {'title': title, 'genre': genre, 'year': year, 'rating': rating}
    movies.append(movie)
    update_table()
    save_data()

    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

def apply_filter():
    genre_filter_value = genre_filter.get().strip().lower()
    year_filter_value = year_filter.get().strip()

    filtered = []
    for m in movies:
        match_genre = True
        match_year = True
        if genre_filter_value:
            match_genre = genre_filter_value in m['genre'].lower()
        if year_filter_value:
            try:
                yf = int(year_filter_value)
                match_year = (m['year'] == yf)
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом.")
                return
        if match_genre and match_year:
            filtered.append(m)
    update_table(filtered)

def clear_filter():
    genre_filter.delete(0, tk.END)
    year_filter.delete(0, tk.END)
    update_table()

# --- Создание интерфейса ---

root = tk.Tk()
root.title("Movie Library")
root.geometry("800x600")

tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
title_entry = tk.Entry(root, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
genre_entry = tk.Entry(root, width=30)
genre_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
year_entry = tk.Entry(root, width=10)
year_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
rating_entry = tk.Entry(root, width=10)
rating_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Добавить фильм", command=add_movie)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show='headings', height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

filter_frame = tk.Frame(root)
filter_frame.grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5, pady=5)
genre_filter = tk.Entry(filter_frame, width=15)
genre_filter.grid(row=0, column=1, padx=5, pady=5)

tk.Label(filter_frame, text="по году:").grid(row=0, column=2, padx=5, pady=5)
year_filter = tk.Entry(filter_frame, width=10)
year_filter.grid(row=0, column=3, padx=5, pady=5)

filter_button = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
filter_button.grid(row=0, column=4, padx=5, pady=5)

clear_button = tk.Button(filter_frame, text="Очистить", command=clear_filter)
clear_button.grid(row=0, column=5, padx=5, pady=5)

# Загрузка данных при запуске
load_data()

# Установка обработчика закрытия окна
def on_closing():
    save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Запуск GUI
root.mainloop()