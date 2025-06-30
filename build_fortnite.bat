@echo off
echo ===============================================
echo    FORTNITE ULTIMATE SPOOFER 2025
echo    Specialized Build Script for Fortnite
echo    Maximum EAC Bypass Optimization
echo ===============================================
echo.

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Запустите скрипт от имени администратора!
    echo [INFO] ПКМ на файле -^> "Запуск от имени администратора"
    pause
    exit /b 1
)

:: Создание специализированных директорий для Fortnite
echo [INFO] Создание директорий для Fortnite спуффера...
if not exist "build_fortnite" mkdir build_fortnite
if not exist "fortnite_profiles" mkdir fortnite_profiles
if not exist "fortnite_backups" mkdir fortnite_backups
if not exist "fortnite_logs" mkdir fortnite_logs

:: Проверка наличия компилятора
echo [INFO] Проверка компилятора C++...
where g++ >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Компилятор g++ не найден!
    echo [INFO] Установите MinGW-w64 или Visual Studio Build Tools
    echo [INFO] Рекомендуется: https://www.mingw-w64.org/downloads/
    pause
    exit /b 1
)

:: Проверка версии компилятора
echo [INFO] Версия компилятора:
g++ --version | findstr "g++"

:: Компиляция специализированного Fortnite спуффера
echo.
echo [INFO] Компиляция Fortnite Ultimate Spoofer...
echo [INFO] Применение оптимизаций для EAC bypass...

echo [INFO] Trying simple version first...
g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ ^
    -DUNICODE -D_UNICODE ^
    -DFORTNITE_OPTIMIZED ^
    -DEAC_BYPASS_2025 ^
    -I. ^
    -o build_fortnite/fortnite_spoofer.exe ^
    fortnite_spoofer_simple.cpp ^
    -liphlpapi -lsetupapi -lcfgmgr32 -ladvapi32 ^
    -lshell32 -luser32 -lpsapi -lkernel32

if %errorLevel% neq 0 (
    echo [WARNING] Simple version failed, trying advanced version...
    g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ ^
        -DUNICODE -D_UNICODE ^
        -DFORTNITE_OPTIMIZED ^
        -DEAC_BYPASS_2025 ^
        -I. ^
        -o build_fortnite/fortnite_spoofer.exe ^
        fortnite_spoofer.cpp ^
        -liphlpapi -lsetupapi -lcfgmgr32 -ladvapi32 ^
        -lshell32 -luser32 -lpsapi -lkernel32
)

if %errorLevel% neq 0 (
    echo [ERROR] Ошибка компиляции Fortnite спуффера!
    echo [INFO] Проверьте код и зависимости
    pause
    exit /b 1
)

echo [SUCCESS] Fortnite спуффер скомпилирован успешно!

:: Компиляция основного спуффера (для совместимости)
echo [INFO] Компиляция основного спуффера...
g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ ^
    -DUNICODE -D_UNICODE ^
    -I. ^
    -o build_fortnite/main.exe ^
    main.cpp ^
    -liphlpapi -lsetupapi -lcfgmgr32 -ladvapi32 -lshell32 -luser32

if %errorLevel% neq 0 (
    echo [WARNING] Основной спуффер не скомпилирован (не критично)
) else (
    echo [SUCCESS] Основной спуффер скомпилирован!
)

:: Проверка Python для GUI
echo [INFO] Проверка Python для GUI...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Python не найден!
    echo [INFO] GUI будет недоступен без Python 3.8+
    echo [INFO] Скачайте с https://www.python.org/downloads/
) else (
    echo [SUCCESS] Python найден!
    python --version
    
    :: Установка зависимостей Python
    echo [INFO] Установка зависимостей Python...
    python -m pip install --upgrade pip
    python -m pip install psutil pywin32 wmi
    
    :: Создание исполняемого GUI файла
    echo [INFO] Проверка PyInstaller...
    python -m pip show pyinstaller >nul 2>&1
    if %errorLevel% neq 0 (
        echo [INFO] Установка PyInstaller...
        python -m pip install pyinstaller
    )
    
    echo [INFO] Создание исполняемого GUI файла...
    pyinstaller --onefile --windowed ^
        --name="FortniteUltimateSpoofer" ^
        --icon=fortnite_icon.ico ^
        --add-data="config.json;." ^
        fortnite_gui.py
    
    if exist "dist\FortniteUltimateSpoofer.exe" (
        copy "dist\FortniteUltimateSpoofer.exe" "build_fortnite\fortnite_gui.exe" >nul
        echo [SUCCESS] GUI исполняемый файл создан!
    ) else (
        echo [WARNING] GUI исполняемый файл не создан
        copy "fortnite_gui.py" "build_fortnite\" >nul
    )
)

:: Копирование необходимых файлов
echo [INFO] Копирование файлов...
copy "config.json" "build_fortnite\" >nul
copy "spoofer.h" "build_fortnite\" >nul
copy "utils.py" "build_fortnite\" >nul
copy "fortnite_gui.py" "build_fortnite\" >nul
copy "requirements.txt" "build_fortnite\" >nul

:: Создание специализированного лаунчера для Fortnite
echo [INFO] Создание Fortnite лаунчера...
echo @echo off > build_fortnite\fortnite_launcher.bat
echo title Fortnite Ultimate Spoofer 2025 >> build_fortnite\fortnite_launcher.bat
echo color 0A >> build_fortnite\fortnite_launcher.bat
echo echo. >> build_fortnite\fortnite_launcher.bat
echo echo ================================================ >> build_fortnite\fortnite_launcher.bat
echo echo    🎮 FORTNITE ULTIMATE SPOOFER 2025 🎮 >> build_fortnite\fortnite_launcher.bat
echo echo    Максимальная защита от EAC >> build_fortnite\fortnite_launcher.bat
echo echo    Windows 11 24H2 Optimized >> build_fortnite\fortnite_launcher.bat
echo echo ================================================ >> build_fortnite\fortnite_launcher.bat
echo echo. >> build_fortnite\fortnite_launcher.bat
echo echo ⚠️  ВАЖНО: Закройте Fortnite перед использованием! >> build_fortnite\fortnite_launcher.bat
echo echo. >> build_fortnite\fortnite_launcher.bat
echo echo Выберите режим запуска: >> build_fortnite\fortnite_launcher.bat
echo echo. >> build_fortnite\fortnite_launcher.bat
echo echo 1. 🖥️  GUI Режим (Рекомендуется) >> build_fortnite\fortnite_launcher.bat
echo echo 2. 💻 Консольный режим >> build_fortnite\fortnite_launcher.bat
echo echo 3. 🧹 Только очистка >> build_fortnite\fortnite_launcher.bat
echo echo 4. 🔍 Проверка статуса >> build_fortnite\fortnite_launcher.bat
echo echo 5. 💾 Создать точку восстановления >> build_fortnite\fortnite_launcher.bat
echo echo 6. 🚪 Выход >> build_fortnite\fortnite_launcher.bat
echo echo. >> build_fortnite\fortnite_launcher.bat
echo :start >> build_fortnite\fortnite_launcher.bat
echo set /p choice="Введите номер (1-6): " >> build_fortnite\fortnite_launcher.bat
echo. >> build_fortnite\fortnite_launcher.bat
echo if "%%choice%%"=="1" ( >> build_fortnite\fortnite_launcher.bat
echo     echo [INFO] Запуск GUI режима... >> build_fortnite\fortnite_launcher.bat
echo     if exist fortnite_gui.exe ( >> build_fortnite\fortnite_launcher.bat
echo         start fortnite_gui.exe >> build_fortnite\fortnite_launcher.bat
echo     ) else if exist fortnite_gui.py ( >> build_fortnite\fortnite_launcher.bat
echo         python fortnite_gui.py >> build_fortnite\fortnite_launcher.bat
echo     ) else ( >> build_fortnite\fortnite_launcher.bat
echo         echo [ERROR] GUI файлы не найдены! >> build_fortnite\fortnite_launcher.bat
echo         pause >> build_fortnite\fortnite_launcher.bat
echo     ) >> build_fortnite\fortnite_launcher.bat
echo ) else if "%%choice%%"=="2" ( >> build_fortnite\fortnite_launcher.bat
echo     echo [INFO] Запуск консольного режима... >> build_fortnite\fortnite_launcher.bat
echo     fortnite_spoofer.exe >> build_fortnite\fortnite_launcher.bat
echo     pause >> build_fortnite\fortnite_launcher.bat
echo ) else if "%%choice%%"=="3" ( >> build_fortnite\fortnite_launcher.bat
echo     echo [INFO] Режим очистки... >> build_fortnite\fortnite_launcher.bat
echo     fortnite_spoofer.exe --clean >> build_fortnite\fortnite_launcher.bat
echo     pause >> build_fortnite\fortnite_launcher.bat
echo ) else if "%%choice%%"=="4" ( >> build_fortnite\fortnite_launcher.bat
echo     echo [INFO] Проверка статуса... >> build_fortnite\fortnite_launcher.bat
echo     fortnite_spoofer.exe --check >> build_fortnite\fortnite_launcher.bat
echo     pause >> build_fortnite\fortnite_launcher.bat
echo ) else if "%%choice%%"=="5" ( >> build_fortnite\fortnite_launcher.bat
echo     echo [INFO] Создание точки восстановления... >> build_fortnite\fortnite_launcher.bat
echo     powershell -Command "Checkpoint-Computer -Description 'Fortnite Spoofer Backup' -RestorePointType 'MODIFY_SETTINGS'" >> build_fortnite\fortnite_launcher.bat
echo     echo [SUCCESS] Точка восстановления создана! >> build_fortnite\fortnite_launcher.bat
echo     pause >> build_fortnite\fortnite_launcher.bat
echo ) else if "%%choice%%"=="6" ( >> build_fortnite\fortnite_launcher.bat
echo     echo Goodbye! >> build_fortnite\fortnite_launcher.bat
echo     exit >> build_fortnite\fortnite_launcher.bat
echo ) else ( >> build_fortnite\fortnite_launcher.bat
echo     echo [ERROR] Неверный выбор! >> build_fortnite\fortnite_launcher.bat
echo     timeout /t 2 /nobreak ^>nul >> build_fortnite\fortnite_launcher.bat
echo     cls >> build_fortnite\fortnite_launcher.bat
echo     goto start >> build_fortnite\fortnite_launcher.bat
echo ) >> build_fortnite\fortnite_launcher.bat

:: Создание README для Fortnite версии
echo [INFO] Создание документации...
echo FORTNITE ULTIMATE SPOOFER 2025 > build_fortnite\README_FORTNITE.txt
echo ================================= >> build_fortnite\README_FORTNITE.txt
echo. >> build_fortnite\README_FORTNITE.txt
echo 🎮 СПЕЦИАЛЬНО ОПТИМИЗИРОВАН ДЛЯ FORTNITE >> build_fortnite\README_FORTNITE.txt
echo 🛡️ МАКСИМАЛЬНАЯ ЗАЩИТА ОТ EASYANTICHEAT >> build_fortnite\README_FORTNITE.txt
echo 🚀 ПОДДЕРЖКА WINDOWS 11 24H2 >> build_fortnite\README_FORTNITE.txt
echo. >> build_fortnite\README_FORTNITE.txt
echo ФАЙЛЫ: >> build_fortnite\README_FORTNITE.txt
echo ======= >> build_fortnite\README_FORTNITE.txt
echo fortnite_spoofer.exe    - Основной спуффер для Fortnite >> build_fortnite\README_FORTNITE.txt
echo fortnite_gui.exe        - Графический интерфейс >> build_fortnite\README_FORTNITE.txt
echo fortnite_launcher.bat   - Лаунчер (ЗАПУСКАТЬ ЭТОТ ФАЙЛ) >> build_fortnite\README_FORTNITE.txt
echo config.json             - Конфигурация >> build_fortnite\README_FORTNITE.txt
echo. >> build_fortnite\README_FORTNITE.txt
echo БЫСТРЫЙ СТАРТ: >> build_fortnite\README_FORTNITE.txt
echo ============== >> build_fortnite\README_FORTNITE.txt
echo 1. Закройте Fortnite полностью >> build_fortnite\README_FORTNITE.txt
echo 2. ПКМ на fortnite_launcher.bat -^> "Запуск от имени администратора" >> build_fortnite\README_FORTNITE.txt
echo 3. Выберите "1" для GUI режима >> build_fortnite\README_FORTNITE.txt
echo 4. Нажмите "ЗАПУСТИТЬ СПУФИНГ" >> build_fortnite\README_FORTNITE.txt
echo 5. Дождитесь завершения >> build_fortnite\README_FORTNITE.txt
echo 6. Запустите Fortnite >> build_fortnite\README_FORTNITE.txt
echo. >> build_fortnite\README_FORTNITE.txt
echo ОСОБЕННОСТИ FORTNITE ВЕРСИИ: >> build_fortnite\README_FORTNITE.txt
echo ============================ >> build_fortnite\README_FORTNITE.txt
echo ✅ Специальные алгоритмы обхода EAC 2025 >> build_fortnite\README_FORTNITE.txt
echo ✅ Реалистичные серийные номера оборудования >> build_fortnite\README_FORTNITE.txt
echo ✅ Глубокая очистка следов Fortnite и Epic Games >> build_fortnite\README_FORTNITE.txt
echo ✅ SMBIOS и PCI устройства спуфинг >> build_fortnite\README_FORTNITE.txt
echo ✅ WMI запросы модификация >> build_fortnite\README_FORTNITE.txt
echo ✅ Автоматический запуск Fortnite после спуфинга >> build_fortnite\README_FORTNITE.txt
echo ✅ Быстрые профили (Competitive, Casual, Streamer) >> build_fortnite\README_FORTNITE.txt
echo. >> build_fortnite\README_FORTNITE.txt
echo ⚠️ ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ: >> build_fortnite\README_FORTNITE.txt
echo ========================= >> build_fortnite\README_FORTNITE.txt
echo • ОБЯЗАТЕЛЬНО создайте точку восстановления >> build_fortnite\README_FORTNITE.txt
echo • Изменения действуют только до перезагрузки >> build_fortnite\README_FORTNITE.txt
echo • Используйте только на свой страх и риск >> build_fortnite\README_FORTNITE.txt
echo • Не используйте читы вместе со спуффером >> build_fortnite\README_FORTNITE.txt
echo • Программа для образовательных целей >> build_fortnite\README_FORTNITE.txt
echo. >> build_fortnite\README_FORTNITE.txt
echo 🆘 ВОССТАНОВЛЕНИЕ: >> build_fortnite\README_FORTNITE.txt
echo ================== >> build_fortnite\README_FORTNITE.txt
echo При проблемах: >> build_fortnite\README_FORTNITE.txt
echo 1. Перезагрузите систему >> build_fortnite\README_FORTNITE.txt
echo 2. Используйте точку восстановления >> build_fortnite\README_FORTNITE.txt
echo 3. Запустите: sfc /scannow >> build_fortnite\README_FORTNITE.txt

:: Проверка сборки
echo [INFO] Проверка сборки...
if exist "build_fortnite\fortnite_spoofer.exe" (
    echo [SUCCESS] ✅ fortnite_spoofer.exe создан
) else (
    echo [ERROR] ❌ fortnite_spoofer.exe не найден!
)

if exist "build_fortnite\fortnite_launcher.bat" (
    echo [SUCCESS] ✅ fortnite_launcher.bat создан
) else (
    echo [ERROR] ❌ fortnite_launcher.bat не найден!
)

if exist "build_fortnite\config.json" (
    echo [SUCCESS] ✅ config.json скопирован
) else (
    echo [ERROR] ❌ config.json не найден!
)

echo.
echo ===============================================
echo           🎮 FORTNITE SPOOFER ГОТОВ! 🎮
echo ===============================================
echo.
echo 📁 Все файлы находятся в папке 'build_fortnite\'
echo 🚀 Запустите: fortnite_launcher.bat (от имени администратора)
echo.
echo 🎯 СПЕЦИАЛЬНЫЕ ВОЗМОЖНОСТИ ДЛЯ FORTNITE:
echo   • Обход EasyAntiCheat 2025
echo   • Реалистичные Hardware ID
echo   • Глубокая очистка следов
echo   • Автозапуск игры
echo   • Быстрые профили
echo.
echo ⚠️  ПОМНИТЕ:
echo   • Создайте точку восстановления
echo   • Закройте Fortnite перед использованием
echo   • Изменения временные (до перезагрузки)
echo   • Используйте ответственно
echo.
echo 🔗 GitHub: https://github.com/kipeloi2/spoof-clean
echo.

pause
