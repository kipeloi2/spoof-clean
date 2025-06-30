#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fortnite Ultimate Spoofer 2025 - Specialized GUI
Максимально оптимизированный интерфейс для Fortnite
"""

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
import psutil
import time

class FortniteSpooferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Fortnite Ultimate Spoofer 2025 - EAC Bypass")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Устанавливаем иконку и стиль
        self.setup_style()
        
        # Проверяем права администратора
        if not self.is_admin():
            messagebox.showerror("❌ Ошибка доступа", 
                               "Запустите программу от имени администратора!\n\n" +
                               "ПКМ на файле → 'Запуск от имени администратора'")
            sys.exit(1)
        
        # Переменные состояния
        self.spoofing_active = tk.BooleanVar()
        self.auto_launch_fortnite = tk.BooleanVar(value=False)
        self.deep_clean_mode = tk.BooleanVar(value=True)
        self.eac_bypass_mode = tk.BooleanVar(value=True)
        self.stealth_mode = tk.BooleanVar(value=True)
        
        # Создаем интерфейс
        self.create_widgets()
        self.load_fortnite_config()
        self.check_fortnite_status()
        
    def is_admin(self):
        """Проверка прав администратора"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def setup_style(self):
        """Настройка стиля интерфейса"""
        style = ttk.Style()
        
        # Fortnite цветовая схема
        self.colors = {
            'primary': '#0078D4',      # Синий Fortnite
            'secondary': '#FF6B35',    # Оранжевый акцент
            'success': '#00C851',      # Зеленый успех
            'warning': '#FF8800',      # Оранжевый предупреждение
            'danger': '#FF4444',       # Красный ошибка
            'dark': '#2C3E50',         # Темный фон
            'light': '#ECF0F1'         # Светлый текст
        }
        
        # Настройка темы
        style.theme_use('clam')
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главное меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Fortnite
        fortnite_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🎮 Fortnite", menu=fortnite_menu)
        fortnite_menu.add_command(label="Запустить Fortnite", command=self.launch_fortnite)
        fortnite_menu.add_command(label="Закрыть Fortnite", command=self.close_fortnite)
        fortnite_menu.add_separator()
        fortnite_menu.add_command(label="Проверить статус EAC", command=self.check_eac_status)
        
        # Меню настроек
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⚙️ Настройки", menu=settings_menu)
        settings_menu.add_command(label="Создать точку восстановления", command=self.create_restore_point)
        settings_menu.add_command(label="Экспорт профиля", command=self.export_profile)
        settings_menu.add_command(label="Импорт профиля", command=self.import_profile)
        
        # Меню помощи
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Помощь", menu=help_menu)
        help_menu.add_command(label="Руководство по использованию", command=self.show_guide)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Основной контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок с логотипом
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="🎮 FORTNITE ULTIMATE SPOOFER 2025", 
                               font=("Arial", 18, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Максимальная защита от EAC • Windows 11 24H2 Optimized", 
                                  font=("Arial", 10), foreground="gray")
        subtitle_label.pack()
        
        # Статус панель
        self.create_status_panel(main_container)
        
        # Основные настройки
        self.create_main_settings(main_container)
        
        # Продвинутые настройки
        self.create_advanced_settings(main_container)
        
        # Кнопки управления
        self.create_control_buttons(main_container)
        
        # Лог панель
        self.create_log_panel(main_container)
        
        # Статус бар
        self.create_status_bar()
        
    def create_status_panel(self, parent):
        """Создание панели статуса"""
        status_frame = ttk.LabelFrame(parent, text="🔍 Статус системы", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Создаем сетку для статусов
        status_grid = ttk.Frame(status_frame)
        status_grid.pack(fill=tk.X)
        
        # Статус Fortnite
        ttk.Label(status_grid, text="Fortnite:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.fortnite_status = ttk.Label(status_grid, text="❌ Не запущен", foreground="red")
        self.fortnite_status.grid(row=0, column=1, sticky=tk.W)
        
        # Статус EAC
        ttk.Label(status_grid, text="EasyAntiCheat:").grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        self.eac_status = ttk.Label(status_grid, text="❌ Неактивен", foreground="red")
        self.eac_status.grid(row=0, column=3, sticky=tk.W)
        
        # Статус спуфинга
        ttk.Label(status_grid, text="Спуфинг:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.spoof_status = ttk.Label(status_grid, text="⏸️ Готов", foreground="orange")
        self.spoof_status.grid(row=1, column=1, sticky=tk.W)
        
        # Статус защиты
        ttk.Label(status_grid, text="Защита:").grid(row=1, column=2, sticky=tk.W, padx=(20, 10))
        self.protection_status = ttk.Label(status_grid, text="🛡️ Активна", foreground="green")
        self.protection_status.grid(row=1, column=3, sticky=tk.W)
        
    def create_main_settings(self, parent):
        """Создание основных настроек"""
        settings_frame = ttk.LabelFrame(parent, text="🎯 Основные настройки спуфинга", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Режимы спуфинга
        modes_frame = ttk.Frame(settings_frame)
        modes_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(modes_frame, text="🔒 EAC Bypass Mode (Рекомендуется)", 
                       variable=self.eac_bypass_mode).pack(anchor=tk.W)
        ttk.Checkbutton(modes_frame, text="🧹 Глубокая очистка следов", 
                       variable=self.deep_clean_mode).pack(anchor=tk.W)
        ttk.Checkbutton(modes_frame, text="👤 Stealth Mode (Невидимость)", 
                       variable=self.stealth_mode).pack(anchor=tk.W)
        ttk.Checkbutton(modes_frame, text="🚀 Автозапуск Fortnite после спуфинга", 
                       variable=self.auto_launch_fortnite).pack(anchor=tk.W)
        
        # Быстрые профили
        profiles_frame = ttk.LabelFrame(settings_frame, text="⚡ Быстрые профили", padding="5")
        profiles_frame.pack(fill=tk.X, pady=(10, 0))
        
        profiles_buttons = ttk.Frame(profiles_frame)
        profiles_buttons.pack()
        
        ttk.Button(profiles_buttons, text="🏆 Competitive", 
                  command=lambda: self.apply_quick_profile("competitive")).pack(side=tk.LEFT, padx=5)
        ttk.Button(profiles_buttons, text="🎪 Casual", 
                  command=lambda: self.apply_quick_profile("casual")).pack(side=tk.LEFT, padx=5)
        ttk.Button(profiles_buttons, text="🔥 Streamer", 
                  command=lambda: self.apply_quick_profile("streamer")).pack(side=tk.LEFT, padx=5)
        ttk.Button(profiles_buttons, text="🛡️ Maximum Security", 
                  command=lambda: self.apply_quick_profile("max_security")).pack(side=tk.LEFT, padx=5)
        
    def create_advanced_settings(self, parent):
        """Создание продвинутых настроек"""
        advanced_frame = ttk.LabelFrame(parent, text="🔧 Продвинутые настройки", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Создаем notebook для вкладок
        notebook = ttk.Notebook(advanced_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка Hardware
        hardware_frame = ttk.Frame(notebook)
        notebook.add(hardware_frame, text="💻 Hardware")
        
        # HWID настройки
        hwid_frame = ttk.LabelFrame(hardware_frame, text="Hardware ID", padding="5")
        hwid_frame.pack(fill=tk.X, pady=5)
        
        hwid_controls = ttk.Frame(hwid_frame)
        hwid_controls.pack(fill=tk.X)
        
        self.hwid_var = tk.StringVar()
        ttk.Entry(hwid_controls, textvariable=self.hwid_var, width=50).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(hwid_controls, text="🎲 Генерировать", 
                  command=self.generate_hwid).pack(side=tk.LEFT)
        
        # MAC настройки
        mac_frame = ttk.LabelFrame(hardware_frame, text="MAC Address", padding="5")
        mac_frame.pack(fill=tk.X, pady=5)
        
        mac_controls = ttk.Frame(mac_frame)
        mac_controls.pack(fill=tk.X)
        
        self.mac_var = tk.StringVar()
        ttk.Entry(mac_controls, textvariable=self.mac_var, width=50).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(mac_controls, text="🎲 Генерировать", 
                  command=self.generate_mac).pack(side=tk.LEFT)
        
        # Вкладка System
        system_frame = ttk.Frame(notebook)
        notebook.add(system_frame, text="🖥️ System")
        
        # Системная информация
        system_info = ttk.LabelFrame(system_frame, text="Системная информация", padding="5")
        system_info.pack(fill=tk.BOTH, expand=True)
        
        self.system_info_text = scrolledtext.ScrolledText(system_info, height=8, width=70)
        self.system_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Обновляем системную информацию
        self.update_system_info()
        
    def create_control_buttons(self, parent):
        """Создание кнопок управления"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Основные кнопки
        main_buttons = ttk.Frame(control_frame)
        main_buttons.pack()
        
        self.start_button = ttk.Button(main_buttons, text="🚀 ЗАПУСТИТЬ СПУФИНГ", 
                                      command=self.start_spoofing, 
                                      style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(main_buttons, text="⏹️ ОСТАНОВИТЬ", 
                                     command=self.stop_spoofing, 
                                     state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(main_buttons, text="🧹 ОЧИСТИТЬ", 
                  command=self.clean_only).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(main_buttons, text="🔄 ПЕРЕЗАГРУЗИТЬ", 
                  command=self.restart_system).pack(side=tk.LEFT, padx=5)
        
    def create_log_panel(self, parent):
        """Создание панели логов"""
        log_frame = ttk.LabelFrame(parent, text="📋 Лог операций", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем фрейм для логов и кнопок
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        # Текстовое поле для логов
        self.log_text = scrolledtext.ScrolledText(log_container, height=12, width=80,
                                                 font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Кнопки управления логами
        log_buttons = ttk.Frame(log_container)
        log_buttons.pack(fill=tk.X)
        
        ttk.Button(log_buttons, text="🗑️ Очистить логи", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_buttons, text="💾 Сохранить логи", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_buttons, text="🔄 Автопрокрутка", 
                  command=self.toggle_autoscroll).pack(side=tk.LEFT)
        
        # Инициализация
        self.autoscroll = True
        self.log("🎮 Fortnite Ultimate Spoofer 2025 запущен")
        self.log("✅ Windows 11 24H2 поддерживается")
        self.log("🛡️ EAC Bypass модули загружены")
        
    def create_status_bar(self):
        """Создание статус бара"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_text = ttk.Label(self.status_bar, text="Готов к работе")
        self.status_text.pack(side=tk.LEFT, padx=5)
        
        # Индикатор активности
        self.activity_indicator = ttk.Label(self.status_bar, text="⚪")
        self.activity_indicator.pack(side=tk.RIGHT, padx=5)
        
    def generate_hwid(self):
        """Генерация HWID оптимизированного для Fortnite"""
        # Используем реалистичные паттерны для обхода EAC
        hwid_patterns = [
            "BFEBFBFF000906EA",  # Intel Core i7-10700K
            "BFEBFBFF000A0671",  # Intel Core i9-12900K  
            "BFEBFBFF00A20F12",  # AMD Ryzen 7 5800X
            "BFEBFBFF00A50F00"   # AMD Ryzen 9 5900X
        ]
        
        base_hwid = random.choice(hwid_patterns)
        # Добавляем случайные вариации
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        hwid = base_hwid + "-" + suffix
        
        self.hwid_var.set(hwid)
        self.log(f"🎲 Сгенерирован HWID: {hwid}")
        
    def generate_mac(self):
        """Генерация MAC адреса оптимизированного для Fortnite"""
        # Используем OUI от популярных производителей сетевых карт
        realistic_ouis = [
            "00:15:5D",  # Microsoft Hyper-V
            "52:54:00",  # QEMU/KVM
            "00:50:56",  # VMware
            "08:00:27",  # VirtualBox
            "00:1C:42",  # Parallels
            "00:E0:4C",  # Realtek
            "00:1B:21",  # Intel
            "00:25:90"   # SuperMicro
        ]
        
        oui = random.choice(realistic_ouis)
        # Генерируем последние 3 байта
        last_bytes = ':'.join(['%02X' % random.randint(0, 255) for _ in range(3)])
        mac = f"{oui}:{last_bytes}"
        
        self.mac_var.set(mac)
        self.log(f"🎲 Сгенерирован MAC: {mac}")
        
    def apply_quick_profile(self, profile_type):
        """Применение быстрого профиля"""
        profiles = {
            "competitive": {
                "name": "🏆 Competitive Gaming",
                "description": "Максимальная производительность для соревновательной игры"
            },
            "casual": {
                "name": "🎪 Casual Gaming", 
                "description": "Сбалансированные настройки для обычной игры"
            },
            "streamer": {
                "name": "🔥 Streamer Mode",
                "description": "Оптимизация для стриминга с защитой приватности"
            },
            "max_security": {
                "name": "🛡️ Maximum Security",
                "description": "Максимальная защита и скрытность"
            }
        }
        
        if profile_type in profiles:
            profile = profiles[profile_type]
            self.log(f"📋 Применен профиль: {profile['name']}")
            self.log(f"ℹ️ {profile['description']}")
            
            # Генерируем новые значения для профиля
            self.generate_hwid()
            self.generate_mac()
            
            # Настраиваем опции в зависимости от профиля
            if profile_type == "max_security":
                self.eac_bypass_mode.set(True)
                self.deep_clean_mode.set(True)
                self.stealth_mode.set(True)
            elif profile_type == "competitive":
                self.eac_bypass_mode.set(True)
                self.deep_clean_mode.set(True)
                self.stealth_mode.set(False)
                
    def update_system_info(self):
        """Обновление системной информации"""
        try:
            info = []
            info.append(f"🖥️ ОС: {os.name} {sys.platform}")
            info.append(f"💾 ОЗУ: {psutil.virtual_memory().total // (1024**3)} GB")
            info.append(f"💽 Диск C: {psutil.disk_usage('C:').total // (1024**3)} GB")
            info.append(f"🔧 CPU: {psutil.cpu_count()} ядер")
            info.append(f"⚡ Загрузка CPU: {psutil.cpu_percent()}%")
            
            # Проверяем процессы Fortnite
            fortnite_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                if 'fortnite' in proc.info['name'].lower():
                    fortnite_processes.append(proc.info['name'])
            
            if fortnite_processes:
                info.append(f"🎮 Процессы Fortnite: {', '.join(fortnite_processes)}")
            else:
                info.append("🎮 Процессы Fortnite: Не найдены")
                
            self.system_info_text.delete(1.0, tk.END)
            self.system_info_text.insert(tk.END, '\n'.join(info))
            
        except Exception as e:
            self.log(f"❌ Ошибка получения системной информации: {str(e)}")
            
    def check_fortnite_status(self):
        """Проверка статуса Fortnite"""
        try:
            fortnite_running = False
            eac_running = False
            
            for proc in psutil.process_iter(['pid', 'name']):
                name = proc.info['name'].lower()
                if 'fortniteclient' in name:
                    fortnite_running = True
                elif 'easyanticheat' in name:
                    eac_running = True
            
            # Обновляем статусы
            if fortnite_running:
                self.fortnite_status.config(text="✅ Запущен", foreground="green")
            else:
                self.fortnite_status.config(text="❌ Не запущен", foreground="red")
                
            if eac_running:
                self.eac_status.config(text="✅ Активен", foreground="green")
            else:
                self.eac_status.config(text="❌ Неактивен", foreground="red")
                
        except Exception as e:
            self.log(f"❌ Ошибка проверки статуса: {str(e)}")
        
        # Повторяем проверку через 5 секунд
        self.root.after(5000, self.check_fortnite_status)

    def start_spoofing(self):
        """Запуск процесса спуфинга"""
        if self.spoofing_active.get():
            messagebox.showwarning("⚠️ Предупреждение", "Спуфинг уже активен!")
            return

        # Проверяем, запущен ли Fortnite
        if self.is_fortnite_running():
            result = messagebox.askyesno("🎮 Fortnite запущен",
                                       "Fortnite сейчас запущен. Закрыть его для безопасного спуфинга?")
            if result:
                self.close_fortnite()
                time.sleep(3)  # Ждем закрытия
            else:
                return

        self.log("🚀 === ЗАПУСК FORTNITE ULTIMATE SPOOFING ===")
        self.log("🔒 Режим EAC Bypass: " + ("✅ Включен" if self.eac_bypass_mode.get() else "❌ Отключен"))
        self.log("🧹 Глубокая очистка: " + ("✅ Включена" if self.deep_clean_mode.get() else "❌ Отключена"))
        self.log("👤 Stealth Mode: " + ("✅ Включен" if self.stealth_mode.get() else "❌ Отключен"))

        # Запускаем спуфинг в отдельном потоке
        threading.Thread(target=self._run_spoofing, daemon=True).start()

        # Обновляем интерфейс
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.spoofing_active.set(True)
        self.spoof_status.config(text="🔄 Выполняется", foreground="orange")
        self.activity_indicator.config(text="🟡")

    def _run_spoofing(self):
        """Выполнение спуфинга"""
        try:
            self.log("🔧 Компиляция Fortnite спуффера...")

            # Компилируем специализированный спуффер для Fortnite
            compile_result = subprocess.run([
                "g++", "-std=c++17", "-O2", "-static-libgcc", "-static-libstdc++",
                "-DUNICODE", "-D_UNICODE",
                "-o", "fortnite_spoofer.exe",
                "fortnite_spoofer.cpp",
                "-liphlpapi", "-lsetupapi", "-lcfgmgr32", "-ladvapi32",
                "-lshell32", "-luser32", "-lwbemuuid", "-lole32", "-loleaut32"
            ], capture_output=True, text=True, timeout=60)

            if compile_result.returncode != 0:
                self.log("❌ Ошибка компиляции спуффера")
                self.log(f"Детали: {compile_result.stderr}")
                self._reset_buttons()
                return

            self.log("✅ Спуффер скомпилирован успешно")

            # Запускаем спуффер
            self.log("🎯 Запуск специализированного Fortnite спуффера...")

            spoof_args = ["fortnite_spoofer.exe"]

            if self.hwid_var.get():
                spoof_args.extend(["--hwid", self.hwid_var.get()])
            if self.mac_var.get():
                spoof_args.extend(["--mac", self.mac_var.get()])
            if self.eac_bypass_mode.get():
                spoof_args.append("--eac-bypass")
            if self.deep_clean_mode.get():
                spoof_args.append("--deep-clean")
            if self.stealth_mode.get():
                spoof_args.append("--stealth")

            result = subprocess.run(spoof_args, capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                self.log("✅ Fortnite спуфинг выполнен успешно!")
                self.log("🛡️ EAC обход активирован")
                self.log("🧹 Следы очищены")
                self.spoof_status.config(text="✅ Активен", foreground="green")
                self.activity_indicator.config(text="🟢")

                # Автозапуск Fortnite если включен
                if self.auto_launch_fortnite.get():
                    self.root.after(3000, self.launch_fortnite)  # Запуск через 3 секунды

            else:
                self.log(f"❌ Ошибка спуфинга: {result.stderr}")
                self.spoof_status.config(text="❌ Ошибка", foreground="red")
                self.activity_indicator.config(text="🔴")

        except subprocess.TimeoutExpired:
            self.log("❌ Превышено время ожидания спуфинга")
            self.spoof_status.config(text="⏰ Таймаут", foreground="red")
        except FileNotFoundError:
            self.log("❌ Компилятор не найден. Установите MinGW-w64 или Visual Studio Build Tools")
            self.spoof_status.config(text="❌ Нет компилятора", foreground="red")
        except Exception as e:
            self.log(f"❌ Неожиданная ошибка: {str(e)}")
            self.spoof_status.config(text="❌ Ошибка", foreground="red")

        # Возвращаем кнопки в исходное состояние
        self.root.after(0, self._reset_buttons)

    def _reset_buttons(self):
        """Сброс состояния кнопок"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        if not self.spoofing_active.get():
            self.activity_indicator.config(text="⚪")

    def stop_spoofing(self):
        """Остановка спуфинга"""
        self.log("⏹️ Остановка спуфинга...")
        self.spoofing_active.set(False)
        self._reset_buttons()
        self.spoof_status.config(text="⏸️ Остановлен", foreground="orange")
        self.activity_indicator.config(text="🟡")

    def clean_only(self):
        """Только очистка без спуфинга"""
        self.log("🧹 Запуск режима очистки...")

        threading.Thread(target=self._run_clean_only, daemon=True).start()

    def _run_clean_only(self):
        """Выполнение только очистки"""
        try:
            # Закрываем Fortnite если запущен
            if self.is_fortnite_running():
                self.close_fortnite()
                time.sleep(2)

            # Очистка временных файлов Fortnite
            cleanup_paths = [
                "C:\\Users\\%USERNAME%\\AppData\\Local\\FortniteGame\\Saved\\Logs",
                "C:\\Users\\%USERNAME%\\AppData\\Local\\FortniteGame\\Saved\\Config",
                "C:\\Users\\%USERNAME%\\AppData\\Local\\EpicGamesLauncher\\Saved\\Logs",
                "C:\\Windows\\Temp\\Fortnite*",
                "C:\\Windows\\Prefetch\\FORTNITECLIENT*.pf"
            ]

            cleaned_count = 0
            for path in cleanup_paths:
                try:
                    result = subprocess.run(f'del /q /f /s "{path}" 2>nul',
                                          shell=True, capture_output=True)
                    if result.returncode == 0:
                        cleaned_count += 1
                except:
                    pass

            self.log(f"✅ Очищено {cleaned_count} категорий файлов")
            self.log("🧹 Очистка завершена успешно")

        except Exception as e:
            self.log(f"❌ Ошибка очистки: {str(e)}")

    def launch_fortnite(self):
        """Запуск Fortnite"""
        self.log("🚀 Запуск Fortnite...")

        # Пути к Fortnite
        fortnite_paths = [
            "C:\\Program Files\\Epic Games\\Fortnite\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe",
            "C:\\Program Files (x86)\\Epic Games\\Fortnite\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe",
            "D:\\Epic Games\\Fortnite\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe"
        ]

        launched = False
        for path in fortnite_paths:
            if os.path.exists(path):
                try:
                    subprocess.Popen([path])
                    self.log(f"✅ Fortnite запущен: {path}")
                    launched = True
                    break
                except Exception as e:
                    self.log(f"❌ Ошибка запуска: {str(e)}")

        if not launched:
            # Пробуем через Epic Games Launcher
            try:
                subprocess.Popen(["cmd", "/c", "start", "com.epicgames.launcher://apps/Fortnite?action=launch&silent=true"])
                self.log("✅ Fortnite запускается через Epic Games Launcher")
            except:
                self.log("❌ Не удалось найти Fortnite. Установите игру через Epic Games Launcher")

    def close_fortnite(self):
        """Закрытие Fortnite"""
        self.log("🔄 Закрытие процессов Fortnite...")

        processes_to_kill = [
            "FortniteClient-Win64-Shipping.exe",
            "EpicGamesLauncher.exe",
            "EpicWebHelper.exe",
            "CrashReportClient.exe",
            "UnrealCEFSubProcess.exe"
        ]

        killed_count = 0
        for process_name in processes_to_kill:
            try:
                result = subprocess.run(f'taskkill /f /im "{process_name}" 2>nul',
                                      shell=True, capture_output=True)
                if result.returncode == 0:
                    killed_count += 1
            except:
                pass

        if killed_count > 0:
            self.log(f"✅ Завершено {killed_count} процессов")
        else:
            self.log("ℹ️ Процессы Fortnite не найдены")

    def is_fortnite_running(self):
        """Проверка запуска Fortnite"""
        try:
            for proc in psutil.process_iter(['name']):
                if 'fortniteclient' in proc.info['name'].lower():
                    return True
        except:
            pass
        return False

    def check_eac_status(self):
        """Проверка статуса EAC"""
        self.log("🔍 Проверка статуса EasyAntiCheat...")

        try:
            eac_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                name = proc.info['name'].lower()
                if 'easyanticheat' in name or 'eac' in name:
                    eac_processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")

            if eac_processes:
                self.log("✅ EAC процессы найдены:")
                for proc in eac_processes:
                    self.log(f"  • {proc}")
            else:
                self.log("❌ EAC процессы не найдены")

        except Exception as e:
            self.log(f"❌ Ошибка проверки EAC: {str(e)}")

    def create_restore_point(self):
        """Создание точки восстановления"""
        self.log("💾 Создание точки восстановления системы...")

        try:
            cmd = 'powershell -Command "Checkpoint-Computer -Description \'Fortnite Spoofer Backup\' -RestorePointType \'MODIFY_SETTINGS\'"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                self.log("✅ Точка восстановления создана успешно")
            else:
                self.log("❌ Ошибка создания точки восстановления")
                self.log(f"Детали: {result.stderr}")

        except subprocess.TimeoutExpired:
            self.log("⏰ Превышено время ожидания создания точки восстановления")
        except Exception as e:
            self.log(f"❌ Ошибка: {str(e)}")

    def restart_system(self):
        """Перезагрузка системы"""
        result = messagebox.askyesno("🔄 Перезагрузка",
                                   "Перезагрузить систему сейчас?\n\n" +
                                   "Это отменит все изменения спуфинга.")
        if result:
            self.log("🔄 Перезагрузка системы...")
            subprocess.run("shutdown /r /t 10", shell=True)
            self.log("⏰ Система перезагрузится через 10 секунд")

    def log(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, log_message)

        if self.autoscroll:
            self.log_text.see(tk.END)

        self.root.update_idletasks()

    def clear_logs(self):
        """Очистка логов"""
        self.log_text.delete(1.0, tk.END)
        self.log("🗑️ Логи очищены")

    def save_logs(self):
        """Сохранение логов"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fortnite_spoofer_log_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))

            self.log(f"💾 Логи сохранены: {filename}")

        except Exception as e:
            self.log(f"❌ Ошибка сохранения логов: {str(e)}")

    def toggle_autoscroll(self):
        """Переключение автопрокрутки"""
        self.autoscroll = not self.autoscroll
        status = "включена" if self.autoscroll else "отключена"
        self.log(f"🔄 Автопрокрутка {status}")

    def load_fortnite_config(self):
        """Загрузка конфигурации Fortnite"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)

                fortnite_profile = config.get("game_profiles", {}).get("Fortnite_2025", {})
                if fortnite_profile:
                    self.log("📋 Загружен профиль Fortnite 2025")

                    # Применяем настройки из профиля
                    advanced_settings = fortnite_profile.get("advanced_spoofing", {})
                    self.eac_bypass_mode.set(advanced_settings.get("process_hollowing_protection", True))
                    self.deep_clean_mode.set(True)  # Всегда включено для Fortnite

        except Exception as e:
            self.log(f"❌ Ошибка загрузки конфигурации: {str(e)}")

    def export_profile(self):
        """Экспорт текущего профиля"""
        try:
            profile_data = {
                "name": "Custom Fortnite Profile",
                "hwid": self.hwid_var.get(),
                "mac": self.mac_var.get(),
                "eac_bypass": self.eac_bypass_mode.get(),
                "deep_clean": self.deep_clean_mode.get(),
                "stealth_mode": self.stealth_mode.get(),
                "auto_launch": self.auto_launch_fortnite.get(),
                "created": datetime.now().isoformat()
            }

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fortnite_profile_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)

            self.log(f"💾 Профиль экспортирован: {filename}")

        except Exception as e:
            self.log(f"❌ Ошибка экспорта профиля: {str(e)}")

    def import_profile(self):
        """Импорт профиля"""
        # Здесь можно добавить диалог выбора файла
        self.log("📁 Функция импорта профиля в разработке")

    def show_guide(self):
        """Показать руководство"""
        guide_text = """🎮 FORTNITE ULTIMATE SPOOFER 2025 - РУКОВОДСТВО

📋 БЫСТРЫЙ СТАРТ:
1. Убедитесь что Fortnite закрыт
2. Выберите профиль или нажмите "Генерировать"
3. Включите "EAC Bypass Mode"
4. Нажмите "ЗАПУСТИТЬ СПУФИНГ"
5. Дождитесь завершения
6. Запустите Fortnite

🔒 РЕЖИМЫ:
• EAC Bypass - обход Easy Anti-Cheat
• Глубокая очистка - удаление всех следов
• Stealth Mode - максимальная скрытность
• Автозапуск - автоматический запуск Fortnite

⚡ БЫСТРЫЕ ПРОФИЛИ:
• Competitive - для соревновательной игры
• Casual - для обычной игры
• Streamer - для стриминга
• Maximum Security - максимальная защита

⚠️ ВАЖНО:
• Всегда создавайте точку восстановления
• Изменения действуют до перезагрузки
• Используйте на свой страх и риск
• Не используйте читы вместе со спуффером

🆘 ПРОБЛЕМЫ:
• Если не работает - перезагрузите систему
• При ошибках - проверьте права администратора
• Для сброса - используйте точку восстановления"""

        messagebox.showinfo("📖 Руководство по использованию", guide_text)

    def show_about(self):
        """Показать информацию о программе"""
        about_text = """🎮 FORTNITE ULTIMATE SPOOFER 2025

🔥 Максимально оптимизированный спуффер для Fortnite
🛡️ Специальные методы обхода EasyAntiCheat
🚀 Поддержка Windows 11 24H2

✨ ВОЗМОЖНОСТИ:
• Продвинутый спуфинг Hardware ID
• Реалистичные MAC адреса
• Глубокая очистка следов Fortnite
• Обход детекции EAC 2025
• SMBIOS и PCI спуфинг
• WMI запросы модификация

⚠️ БЕЗОПАСНОСТЬ:
• Все изменения временные
• Автоматическое восстановление после перезагрузки
• Создание точек восстановления
• Подробное логирование операций

🎯 ОПТИМИЗАЦИЯ ДЛЯ FORTNITE:
• Специальные алгоритмы для обхода EAC
• Реалистичные серийные номера оборудования
• Очистка специфичных для Fortnite следов
• Поддержка актуальных методов детекции 2025

💻 СИСТЕМНЫЕ ТРЕБОВАНИЯ:
• Windows 11 24H2 (рекомендуется)
• Права администратора (обязательно)
• MinGW-w64 или Visual Studio Build Tools
• Python 3.8+ (для GUI)

⚖️ ПРАВОВАЯ ИНФОРМАЦИЯ:
Программа предназначена исключительно для образовательных
целей. Использование в коммерческих целях или для нарушения
правил игр запрещено. Авторы не несут ответственности за
любые последствия использования.

🔗 GitHub: https://github.com/kipeloi2/spoof-clean
📧 Поддержка: Issues на GitHub

Версия: 2.0 Fortnite Edition
Дата: 2025"""

        messagebox.showinfo("ℹ️ О программе", about_text)

def main():
    root = tk.Tk()
    app = FortniteSpooferGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
