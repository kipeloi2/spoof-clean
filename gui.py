#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import json
import os
import sys
import ctypes
from datetime import datetime
import random
import string

class GameSpooferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Spoofer v2.0 - Windows 11 24H2")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Проверяем права администратора
        if not self.is_admin():
            messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")
            sys.exit(1)
        
        # Переменные состояния
        self.spoofing_active = tk.BooleanVar()
        self.auto_clean = tk.BooleanVar(value=True)
        self.current_profile = tk.StringVar(value="Custom")
        
        # Создаем интерфейс
        self.create_widgets()
        self.load_config()
        
    def is_admin(self):
        """Проверка прав администратора"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главное меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить профиль", command=self.save_profile)
        file_menu.add_command(label="Загрузить профиль", command=self.load_profile)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Game Spoofer v2.0", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Статус
        status_frame = ttk.LabelFrame(main_frame, text="Статус", padding="10")
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Готов к работе", 
                                     foreground="green")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Профили игр
        profile_frame = ttk.LabelFrame(main_frame, text="Профили игр", padding="10")
        profile_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(profile_frame, text="Выберите игру:").grid(row=0, column=0, sticky=tk.W)
        
        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.current_profile,
                                         values=["Custom", "Valorant", "Fortnite", "Apex Legends", 
                                                "Call of Duty Warzone", "PUBG", "CS2"])
        self.profile_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_change)
        
        profile_frame.columnconfigure(1, weight=1)
        
        # Настройки спуфинга
        spoof_frame = ttk.LabelFrame(main_frame, text="Настройки спуфинга", padding="10")
        spoof_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # HWID
        ttk.Label(spoof_frame, text="Hardware ID:").grid(row=0, column=0, sticky=tk.W)
        self.hwid_var = tk.StringVar()
        self.hwid_entry = ttk.Entry(spoof_frame, textvariable=self.hwid_var, width=40)
        self.hwid_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        ttk.Button(spoof_frame, text="Генерировать", 
                  command=self.generate_hwid).grid(row=0, column=2, padx=(5, 0))
        
        # MAC Address
        ttk.Label(spoof_frame, text="MAC Address:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.mac_var = tk.StringVar()
        self.mac_entry = ttk.Entry(spoof_frame, textvariable=self.mac_var, width=40)
        self.mac_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(5, 0))
        ttk.Button(spoof_frame, text="Генерировать", 
                  command=self.generate_mac).grid(row=1, column=2, padx=(5, 0), pady=(5, 0))
        
        # Disk Serial
        ttk.Label(spoof_frame, text="Disk Serial:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.disk_var = tk.StringVar()
        self.disk_entry = ttk.Entry(spoof_frame, textvariable=self.disk_var, width=40)
        self.disk_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(5, 0))
        ttk.Button(spoof_frame, text="Генерировать", 
                  command=self.generate_disk_serial).grid(row=2, column=2, padx=(5, 0), pady=(5, 0))
        
        spoof_frame.columnconfigure(1, weight=1)
        
        # Дополнительные опции
        options_frame = ttk.LabelFrame(main_frame, text="Дополнительные опции", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(options_frame, text="Автоматическая очистка временных файлов", 
                       variable=self.auto_clean).grid(row=0, column=0, sticky=tk.W)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="Запустить спуфинг", 
                                      command=self.start_spoofing, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Остановить", 
                                     command=self.stop_spoofing, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Очистить логи", 
                  command=self.clear_logs).pack(side=tk.LEFT)
        
        # Лог
        log_frame = ttk.LabelFrame(main_frame, text="Лог операций", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Инициализация
        self.log("Программа запущена")
        self.log("Windows 11 24H2 поддерживается")
        
    def generate_hwid(self):
        """Генерация случайного HWID"""
        hwid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        hwid += '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        hwid += '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        hwid += '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        self.hwid_var.set(hwid)
        self.log(f"Сгенерирован новый HWID: {hwid}")
        
    def generate_mac(self):
        """Генерация случайного MAC адреса"""
        mac = ':'.join(['%02x' % random.randint(0, 255) for _ in range(6)])
        # Делаем первый байт четным для корректного MAC
        mac = mac[:1] + str(random.randint(0, 7) * 2) + mac[2:]
        self.mac_var.set(mac.upper())
        self.log(f"Сгенерирован новый MAC: {mac.upper()}")
        
    def generate_disk_serial(self):
        """Генерация случайного серийного номера диска"""
        serial = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        self.disk_var.set(serial)
        self.log(f"Сгенерирован новый серийный номер диска: {serial}")
        
    def on_profile_change(self, event=None):
        """Обработка смены профиля"""
        profile = self.current_profile.get()
        self.log(f"Выбран профиль: {profile}")
        
        if profile != "Custom":
            # Автоматическая генерация для выбранной игры
            self.generate_hwid()
            self.generate_mac()
            self.generate_disk_serial()
        
    def start_spoofing(self):
        """Запуск процесса спуфинга"""
        if not self.hwid_var.get() or not self.mac_var.get() or not self.disk_var.get():
            messagebox.showwarning("Предупреждение", 
                                 "Заполните все поля или используйте кнопки генерации!")
            return
        
        self.log("=== НАЧАЛО СПУФИНГА ===")
        self.log(f"Профиль: {self.current_profile.get()}")
        self.log(f"HWID: {self.hwid_var.get()}")
        self.log(f"MAC: {self.mac_var.get()}")
        self.log(f"Disk Serial: {self.disk_var.get()}")
        
        # Запускаем спуфинг в отдельном потоке
        threading.Thread(target=self._run_spoofing, daemon=True).start()
        
        # Обновляем интерфейс
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.spoofing_active.set(True)
        self.status_label.config(text="Спуфинг активен", foreground="orange")
        
    def _run_spoofing(self):
        """Выполнение спуфинга"""
        try:
            # Запускаем основную программу
            result = subprocess.run([
                "main.exe", "--gui",
                "--hwid", self.hwid_var.get(),
                "--mac", self.mac_var.get(),
                "--disk", self.disk_var.get()
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log("✓ Спуфинг выполнен успешно!")
                self.status_label.config(text="Спуфинг завершен", foreground="green")
            else:
                self.log(f"✗ Ошибка спуфинга: {result.stderr}")
                self.status_label.config(text="Ошибка спуфинга", foreground="red")
                
        except subprocess.TimeoutExpired:
            self.log("✗ Превышено время ожидания")
            self.status_label.config(text="Таймаут", foreground="red")
        except FileNotFoundError:
            self.log("✗ Файл main.exe не найден. Скомпилируйте проект.")
            self.status_label.config(text="Файл не найден", foreground="red")
        except Exception as e:
            self.log(f"✗ Неожиданная ошибка: {str(e)}")
            self.status_label.config(text="Ошибка", foreground="red")
        
        # Возвращаем кнопки в исходное состояние
        self.root.after(0, self._reset_buttons)
        
    def _reset_buttons(self):
        """Сброс состояния кнопок"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.spoofing_active.set(False)
        
    def stop_spoofing(self):
        """Остановка спуфинга"""
        self.log("Остановка спуфинга...")
        self._reset_buttons()
        self.status_label.config(text="Остановлено", foreground="red")
        
    def clear_logs(self):
        """Очистка логов"""
        self.log_text.delete(1.0, tk.END)
        
    def log(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def save_profile(self):
        """Сохранение профиля"""
        profile_data = {
            "name": self.current_profile.get(),
            "hwid": self.hwid_var.get(),
            "mac": self.mac_var.get(),
            "disk_serial": self.disk_var.get(),
            "auto_clean": self.auto_clean.get()
        }
        
        filename = f"profiles/{self.current_profile.get()}.json"
        os.makedirs("profiles", exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            self.log(f"Профиль сохранен: {filename}")
            messagebox.showinfo("Успех", "Профиль сохранен!")
        except Exception as e:
            self.log(f"Ошибка сохранения профиля: {str(e)}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить профиль: {str(e)}")
            
    def load_profile(self):
        """Загрузка профиля"""
        # Здесь можно добавить диалог выбора файла
        pass
        
    def load_config(self):
        """Загрузка конфигурации"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.auto_clean.set(config.get("auto_clean", True))
                    self.log("Конфигурация загружена")
        except Exception as e:
            self.log(f"Ошибка загрузки конфигурации: {str(e)}")
            
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """Game Spoofer v2.0

Временный спуффер для игр
Поддержка Windows 11 24H2

Возможности:
• Спуфинг Hardware ID
• Спуфинг MAC адресов
• Спуфинг серийных номеров дисков
• Очистка временных файлов
• Профили для популярных игр

⚠️ Изменения действуют до перезагрузки
⚠️ Используйте на свой страх и риск

Разработано для образовательных целей."""
        
        messagebox.showinfo("О программе", about_text)

def main():
    root = tk.Tk()
    app = GameSpooferGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
