#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Spoofer v2.0 - Utilities
Дополнительные утилиты для работы со спуффером
"""

import os
import sys
import json
import subprocess
import winreg
import ctypes
import psutil
import time
from datetime import datetime
import hashlib
import random
import string

class SystemUtils:
    """Утилиты для работы с системой"""
    
    @staticmethod
    def is_admin():
        """Проверка прав администратора"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def get_windows_version():
        """Получение версии Windows"""
        try:
            import platform
            return platform.platform()
        except:
            return "Unknown"
    
    @staticmethod
    def get_system_info():
        """Получение информации о системе"""
        info = {
            "os": SystemUtils.get_windows_version(),
            "cpu_count": psutil.cpu_count(),
            "memory": psutil.virtual_memory().total // (1024**3),  # GB
            "disk_usage": psutil.disk_usage('C:').total // (1024**3),  # GB
            "admin": SystemUtils.is_admin()
        }
        return info
    
    @staticmethod
    def create_restore_point(description="Game Spoofer Backup"):
        """Создание точки восстановления"""
        try:
            cmd = f'powershell -Command "Checkpoint-Computer -Description \'{description}\' -RestorePointType \'MODIFY_SETTINGS\'"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

class RegistryUtils:
    """Утилиты для работы с реестром"""
    
    @staticmethod
    def read_registry_value(hkey, subkey, value_name):
        """Чтение значения из реестра"""
        try:
            with winreg.OpenKey(hkey, subkey) as key:
                value, _ = winreg.QueryValueEx(key, value_name)
                return value
        except:
            return None
    
    @staticmethod
    def write_registry_value(hkey, subkey, value_name, value, value_type=winreg.REG_SZ):
        """Запись значения в реестр"""
        try:
            with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, value_name, 0, value_type, value)
                return True
        except:
            return False
    
    @staticmethod
    def backup_registry_key(hkey, subkey, backup_file):
        """Резервное копирование ключа реестра"""
        try:
            cmd = f'reg export "HKEY_LOCAL_MACHINE\\{subkey}" "{backup_file}"'
            result = subprocess.run(cmd, shell=True, capture_output=True)
            return result.returncode == 0
        except:
            return False

class NetworkUtils:
    """Утилиты для работы с сетью"""
    
    @staticmethod
    def get_network_adapters():
        """Получение списка сетевых адаптеров"""
        adapters = []
        try:
            import wmi
            c = wmi.WMI()
            for adapter in c.Win32_NetworkAdapter():
                if adapter.MACAddress:
                    adapters.append({
                        'name': adapter.Name,
                        'mac': adapter.MACAddress,
                        'enabled': adapter.NetEnabled
                    })
        except:
            # Альтернативный способ через ipconfig
            try:
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                # Парсинг вывода ipconfig (упрощенная версия)
                pass
            except:
                pass
        
        return adapters
    
    @staticmethod
    def generate_random_mac():
        """Генерация случайного MAC адреса"""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        # Делаем первый байт четным (локальный адрес)
        mac[0] = mac[0] & 0xfe
        return ':'.join(['%02x' % x for x in mac]).upper()

class FileUtils:
    """Утилиты для работы с файлами"""
    
    @staticmethod
    def clean_temp_directories():
        """Очистка временных директорий"""
        temp_dirs = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            'C:\\Windows\\Temp',
            'C:\\Windows\\Prefetch'
        ]
        
        cleaned_files = 0
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                os.remove(file_path)
                                cleaned_files += 1
                            except:
                                pass
                except:
                    pass
        
        return cleaned_files
    
    @staticmethod
    def secure_delete_file(file_path, passes=3):
        """Безопасное удаление файла"""
        if not os.path.exists(file_path):
            return False
        
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'r+b') as file:
                for _ in range(passes):
                    file.seek(0)
                    file.write(os.urandom(file_size))
                    file.flush()
                    os.fsync(file.fileno())
            
            os.remove(file_path)
            return True
        except:
            return False

class CryptoUtils:
    """Утилиты для криптографии"""
    
    @staticmethod
    def generate_random_string(length, chars=None):
        """Генерация случайной строки"""
        if chars is None:
            chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_hwid():
        """Генерация Hardware ID"""
        parts = [
            CryptoUtils.generate_random_string(8),
            CryptoUtils.generate_random_string(4),
            CryptoUtils.generate_random_string(4),
            CryptoUtils.generate_random_string(12)
        ]
        return '-'.join(parts)
    
    @staticmethod
    def generate_disk_serial():
        """Генерация серийного номера диска"""
        return CryptoUtils.generate_random_string(16)
    
    @staticmethod
    def hash_string(text, algorithm='sha256'):
        """Хеширование строки"""
        if algorithm == 'md5':
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(text.encode()).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(text.encode()).hexdigest()
        else:
            return None

class ProfileManager:
    """Менеджер профилей"""
    
    def __init__(self, profiles_dir="profiles"):
        self.profiles_dir = profiles_dir
        os.makedirs(profiles_dir, exist_ok=True)
    
    def save_profile(self, name, profile_data):
        """Сохранение профиля"""
        try:
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def load_profile(self, name):
        """Загрузка профиля"""
        try:
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def list_profiles(self):
        """Список профилей"""
        profiles = []
        try:
            for file in os.listdir(self.profiles_dir):
                if file.endswith('.json'):
                    profiles.append(file[:-5])  # Убираем .json
        except:
            pass
        return profiles
    
    def delete_profile(self, name):
        """Удаление профиля"""
        try:
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            os.remove(file_path)
            return True
        except:
            return False

class Logger:
    """Система логирования"""
    
    def __init__(self, log_file="logs/spoofer.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Запись в лог"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except:
            pass
        
        # Также выводим в консоль
        print(f"[{level}] {message}")
    
    def info(self, message):
        self.log(message, "INFO")
    
    def warning(self, message):
        self.log(message, "WARNING")
    
    def error(self, message):
        self.log(message, "ERROR")
    
    def success(self, message):
        self.log(message, "SUCCESS")

class GameDetector:
    """Детектор запущенных игр"""
    
    GAME_PROCESSES = {
        'valorant': ['VALORANT-Win64-Shipping.exe', 'RiotClientServices.exe'],
        'fortnite': ['FortniteClient-Win64-Shipping.exe', 'EpicGamesLauncher.exe'],
        'apex': ['r5apex.exe', 'Origin.exe'],
        'warzone': ['ModernWarfare.exe', 'Warzone.exe'],
        'pubg': ['TslGame.exe', 'PUBG.exe'],
        'cs2': ['cs2.exe', 'steam.exe']
    }
    
    @staticmethod
    def get_running_games():
        """Получение списка запущенных игр"""
        running_games = []
        
        try:
            for process in psutil.process_iter(['pid', 'name']):
                process_name = process.info['name'].lower()
                
                for game, processes in GameDetector.GAME_PROCESSES.items():
                    for game_process in processes:
                        if game_process.lower() in process_name:
                            if game not in running_games:
                                running_games.append(game)
        except:
            pass
        
        return running_games
    
    @staticmethod
    def is_game_running(game_name):
        """Проверка запуска конкретной игры"""
        return game_name.lower() in GameDetector.get_running_games()

# Пример использования
if __name__ == "__main__":
    # Тестирование утилит
    logger = Logger()
    logger.info("Testing Game Spoofer utilities")
    
    # Информация о системе
    system_info = SystemUtils.get_system_info()
    logger.info(f"System info: {system_info}")
    
    # Генерация случайных значений
    hwid = CryptoUtils.generate_hwid()
    mac = NetworkUtils.generate_random_mac()
    disk_serial = CryptoUtils.generate_disk_serial()
    
    logger.info(f"Generated HWID: {hwid}")
    logger.info(f"Generated MAC: {mac}")
    logger.info(f"Generated Disk Serial: {disk_serial}")
    
    # Проверка запущенных игр
    running_games = GameDetector.get_running_games()
    if running_games:
        logger.warning(f"Running games detected: {', '.join(running_games)}")
    else:
        logger.info("No games currently running")
    
    logger.success("Utilities test completed")
