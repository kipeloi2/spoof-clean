#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Spoofer v2.0 - Test Suite
Тесты для проверки функциональности спуффера
"""

import unittest
import os
import sys
import json
import subprocess
import tempfile
from utils import *

class TestSystemUtils(unittest.TestCase):
    """Тесты системных утилит"""
    
    def test_admin_check(self):
        """Тест проверки прав администратора"""
        result = SystemUtils.is_admin()
        self.assertIsInstance(result, bool)
        print(f"Admin rights: {result}")
    
    def test_windows_version(self):
        """Тест получения версии Windows"""
        version = SystemUtils.get_windows_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)
        print(f"Windows version: {version}")
    
    def test_system_info(self):
        """Тест получения информации о системе"""
        info = SystemUtils.get_system_info()
        self.assertIsInstance(info, dict)
        self.assertIn('os', info)
        self.assertIn('cpu_count', info)
        self.assertIn('memory', info)
        print(f"System info: {info}")

class TestCryptoUtils(unittest.TestCase):
    """Тесты криптографических утилит"""
    
    def test_random_string_generation(self):
        """Тест генерации случайных строк"""
        # Тест с разными длинами
        for length in [8, 16, 32]:
            random_str = CryptoUtils.generate_random_string(length)
            self.assertEqual(len(random_str), length)
            self.assertTrue(random_str.isalnum())
            print(f"Random string ({length}): {random_str}")
    
    def test_hwid_generation(self):
        """Тест генерации HWID"""
        hwid = CryptoUtils.generate_hwid()
        self.assertIsInstance(hwid, str)
        # Проверяем формат XXXX-XXXX-XXXX-XXXXXXXXXXXX
        parts = hwid.split('-')
        self.assertEqual(len(parts), 4)
        self.assertEqual(len(parts[0]), 8)
        self.assertEqual(len(parts[1]), 4)
        self.assertEqual(len(parts[2]), 4)
        self.assertEqual(len(parts[3]), 12)
        print(f"Generated HWID: {hwid}")
    
    def test_disk_serial_generation(self):
        """Тест генерации серийного номера диска"""
        serial = CryptoUtils.generate_disk_serial()
        self.assertEqual(len(serial), 16)
        self.assertTrue(serial.isalnum())
        print(f"Generated disk serial: {serial}")
    
    def test_hash_functions(self):
        """Тест функций хеширования"""
        test_string = "Game Spoofer Test"
        
        # MD5
        md5_hash = CryptoUtils.hash_string(test_string, 'md5')
        self.assertEqual(len(md5_hash), 32)
        print(f"MD5 hash: {md5_hash}")
        
        # SHA1
        sha1_hash = CryptoUtils.hash_string(test_string, 'sha1')
        self.assertEqual(len(sha1_hash), 40)
        print(f"SHA1 hash: {sha1_hash}")
        
        # SHA256
        sha256_hash = CryptoUtils.hash_string(test_string, 'sha256')
        self.assertEqual(len(sha256_hash), 64)
        print(f"SHA256 hash: {sha256_hash}")

class TestNetworkUtils(unittest.TestCase):
    """Тесты сетевых утилит"""
    
    def test_mac_generation(self):
        """Тест генерации MAC адреса"""
        mac = NetworkUtils.generate_random_mac()
        self.assertIsInstance(mac, str)
        # Проверяем формат XX:XX:XX:XX:XX:XX
        parts = mac.split(':')
        self.assertEqual(len(parts), 6)
        for part in parts:
            self.assertEqual(len(part), 2)
            int(part, 16)  # Должно быть hex
        print(f"Generated MAC: {mac}")
    
    def test_network_adapters(self):
        """Тест получения сетевых адаптеров"""
        adapters = NetworkUtils.get_network_adapters()
        self.assertIsInstance(adapters, list)
        print(f"Network adapters found: {len(adapters)}")
        for adapter in adapters[:3]:  # Показываем первые 3
            print(f"  - {adapter}")

class TestProfileManager(unittest.TestCase):
    """Тесты менеджера профилей"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.temp_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(self.temp_dir)
    
    def test_save_and_load_profile(self):
        """Тест сохранения и загрузки профиля"""
        test_profile = {
            'name': 'Test Game',
            'hwid': CryptoUtils.generate_hwid(),
            'mac': NetworkUtils.generate_random_mac(),
            'disk_serial': CryptoUtils.generate_disk_serial()
        }
        
        # Сохранение
        result = self.profile_manager.save_profile('test', test_profile)
        self.assertTrue(result)
        
        # Загрузка
        loaded_profile = self.profile_manager.load_profile('test')
        self.assertIsNotNone(loaded_profile)
        self.assertEqual(loaded_profile['name'], test_profile['name'])
        self.assertEqual(loaded_profile['hwid'], test_profile['hwid'])
        print(f"Profile saved and loaded successfully: {loaded_profile['name']}")
    
    def test_list_profiles(self):
        """Тест получения списка профилей"""
        # Создаем несколько тестовых профилей
        for i in range(3):
            profile = {'name': f'Test Game {i}', 'hwid': CryptoUtils.generate_hwid()}
            self.profile_manager.save_profile(f'test{i}', profile)
        
        profiles = self.profile_manager.list_profiles()
        self.assertGreaterEqual(len(profiles), 3)
        print(f"Profiles found: {profiles}")
    
    def test_delete_profile(self):
        """Тест удаления профиля"""
        # Создаем профиль
        profile = {'name': 'Delete Test', 'hwid': CryptoUtils.generate_hwid()}
        self.profile_manager.save_profile('delete_test', profile)
        
        # Проверяем что он существует
        loaded = self.profile_manager.load_profile('delete_test')
        self.assertIsNotNone(loaded)
        
        # Удаляем
        result = self.profile_manager.delete_profile('delete_test')
        self.assertTrue(result)
        
        # Проверяем что удален
        loaded = self.profile_manager.load_profile('delete_test')
        self.assertIsNone(loaded)
        print("Profile deleted successfully")

class TestGameDetector(unittest.TestCase):
    """Тесты детектора игр"""
    
    def test_get_running_games(self):
        """Тест получения запущенных игр"""
        games = GameDetector.get_running_games()
        self.assertIsInstance(games, list)
        print(f"Running games: {games if games else 'None'}")
    
    def test_specific_game_check(self):
        """Тест проверки конкретной игры"""
        # Тестируем несколько популярных игр
        test_games = ['valorant', 'fortnite', 'apex', 'cs2']
        
        for game in test_games:
            is_running = GameDetector.is_game_running(game)
            print(f"{game.capitalize()} running: {is_running}")

class TestFileUtils(unittest.TestCase):
    """Тесты файловых утилит"""
    
    def test_temp_cleanup(self):
        """Тест очистки временных файлов"""
        # Создаем временный файл для теста
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b"Test data")
        temp_file.close()
        
        # Проверяем что файл существует
        self.assertTrue(os.path.exists(temp_file.name))
        
        # Тестируем безопасное удаление
        result = FileUtils.secure_delete_file(temp_file.name)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(temp_file.name))
        print("Secure file deletion test passed")

class TestLogger(unittest.TestCase):
    """Тесты системы логирования"""
    
    def test_logging(self):
        """Тест логирования"""
        temp_log = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        temp_log.close()
        
        logger = Logger(temp_log.name)
        
        # Тестируем разные уровни логирования
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        logger.success("Test success message")
        
        # Проверяем что лог файл создан и содержит записи
        self.assertTrue(os.path.exists(temp_log.name))
        
        with open(temp_log.name, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test info message", content)
            self.assertIn("Test warning message", content)
            self.assertIn("Test error message", content)
            self.assertIn("Test success message", content)
        
        os.unlink(temp_log.name)
        print("Logging test passed")

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        print("\n=== INTEGRATION TEST ===")
        
        # 1. Проверка системы
        system_info = SystemUtils.get_system_info()
        print(f"System check: {system_info['os']}")
        
        # 2. Генерация данных
        hwid = CryptoUtils.generate_hwid()
        mac = NetworkUtils.generate_random_mac()
        disk_serial = CryptoUtils.generate_disk_serial()
        
        print(f"Generated HWID: {hwid}")
        print(f"Generated MAC: {mac}")
        print(f"Generated Disk Serial: {disk_serial}")
        
        # 3. Создание профиля
        temp_dir = tempfile.mkdtemp()
        profile_manager = ProfileManager(temp_dir)
        
        profile_data = {
            'name': 'Integration Test',
            'hwid': hwid,
            'mac': mac,
            'disk_serial': disk_serial,
            'created': str(datetime.now())
        }
        
        result = profile_manager.save_profile('integration_test', profile_data)
        self.assertTrue(result)
        print("Profile created successfully")
        
        # 4. Проверка детектора игр
        running_games = GameDetector.get_running_games()
        print(f"Games detected: {running_games if running_games else 'None'}")
        
        # 5. Логирование
        logger = Logger(os.path.join(temp_dir, 'test.log'))
        logger.success("Integration test completed successfully")
        
        print("=== INTEGRATION TEST PASSED ===")

def run_tests():
    """Запуск всех тестов"""
    print("Game Spoofer v2.0 - Test Suite")
    print("=" * 50)
    
    # Создаем test suite
    test_suite = unittest.TestSuite()
    
    # Добавляем тесты
    test_classes = [
        TestSystemUtils,
        TestCryptoUtils,
        TestNetworkUtils,
        TestProfileManager,
        TestGameDetector,
        TestFileUtils,
        TestLogger,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Результаты
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nSuccess rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
