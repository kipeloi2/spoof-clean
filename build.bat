@echo off
echo ===============================================
echo    Game Spoofer v2.0 - Build Script
echo    Windows 11 24H2 Support
echo ===============================================
echo.

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Запустите скрипт от имени администратора!
    pause
    exit /b 1
)

:: Создание директорий
echo [INFO] Создание директорий...
if not exist "build" mkdir build
if not exist "profiles" mkdir profiles
if not exist "backups" mkdir backups
if not exist "logs" mkdir logs

:: Проверка наличия компилятора
echo [INFO] Проверка компилятора...
where g++ >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Компилятор g++ не найден!
    echo [INFO] Установите MinGW-w64 или Visual Studio Build Tools
    pause
    exit /b 1
)

:: Компиляция основного приложения
echo [INFO] Компиляция main.cpp...
g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ ^
    -DUNICODE -D_UNICODE ^
    -I. ^
    -o build/main.exe ^
    main.cpp ^
    -liphlpapi -lsetupapi -lcfgmgr32 -ladvapi32 -lshell32 -luser32 -lkernel32

if %errorLevel% neq 0 (
    echo [ERROR] Ошибка компиляции main.cpp!
    pause
    exit /b 1
)

echo [SUCCESS] main.exe скомпилирован успешно!

:: Проверка Python
echo [INFO] Проверка Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python не найден!
    echo [INFO] Установите Python 3.8 или новее
    pause
    exit /b 1
)

:: Установка зависимостей Python
echo [INFO] Установка зависимостей Python...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
) else (
    echo [INFO] requirements.txt не найден, создаем...
    echo tkinter > requirements.txt
    echo psutil >> requirements.txt
)

:: Создание исполняемого файла GUI (опционально)
echo [INFO] Создание GUI исполняемого файла...
where pyinstaller >nul 2>&1
if %errorLevel% equ 0 (
    echo [INFO] PyInstaller найден, создаем GUI.exe...
    pyinstaller --onefile --windowed --name="GameSpooferGUI" gui.py
    if exist "dist\GameSpooferGUI.exe" (
        copy "dist\GameSpooferGUI.exe" "build\gui.exe"
        echo [SUCCESS] GUI.exe создан успешно!
    )
) else (
    echo [WARNING] PyInstaller не найден, GUI будет запускаться через Python
)

:: Копирование файлов
echo [INFO] Копирование файлов...
copy "config.json" "build\" >nul
copy "spoofer.h" "build\" >nul
if exist "gui.py" copy "gui.py" "build\" >nul

:: Создание launcher.bat
echo [INFO] Создание launcher.bat...
echo @echo off > build\launcher.bat
echo echo Game Spoofer v2.0 - Launcher >> build\launcher.bat
echo echo. >> build\launcher.bat
echo echo 1. Запуск с GUI >> build\launcher.bat
echo echo 2. Запуск в консоли >> build\launcher.bat
echo echo 3. Выход >> build\launcher.bat
echo echo. >> build\launcher.bat
echo set /p choice="Выберите опцию (1-3): " >> build\launcher.bat
echo. >> build\launcher.bat
echo if "%%choice%%"=="1" ( >> build\launcher.bat
echo     if exist gui.exe ( >> build\launcher.bat
echo         start gui.exe >> build\launcher.bat
echo     ) else ( >> build\launcher.bat
echo         python gui.py >> build\launcher.bat
echo     ) >> build\launcher.bat
echo ) else if "%%choice%%"=="2" ( >> build\launcher.bat
echo     main.exe >> build\launcher.bat
echo ) else if "%%choice%%"=="3" ( >> build\launcher.bat
echo     exit >> build\launcher.bat
echo ) else ( >> build\launcher.bat
echo     echo Неверный выбор! >> build\launcher.bat
echo     pause >> build\launcher.bat
echo     goto start >> build\launcher.bat
echo ) >> build\launcher.bat

:: Создание README для build
echo [INFO] Создание README...
echo Game Spoofer v2.0 - Build > build\README.txt
echo ========================== >> build\README.txt
echo. >> build\README.txt
echo Файлы: >> build\README.txt
echo - main.exe          : Основное приложение >> build\README.txt
echo - gui.exe/gui.py    : Графический интерфейс >> build\README.txt
echo - launcher.bat      : Лаунчер >> build\README.txt
echo - config.json       : Конфигурация >> build\README.txt
echo. >> build\README.txt
echo Запуск: >> build\README.txt
echo 1. Запустите launcher.bat от имени администратора >> build\README.txt
echo 2. Выберите нужный режим >> build\README.txt
echo. >> build\README.txt
echo ВНИМАНИЕ: >> build\README.txt
echo - Требуются права администратора >> build\README.txt
echo - Изменения действуют до перезагрузки >> build\README.txt
echo - Используйте на свой страх и риск >> build\README.txt

:: Проверка сборки
echo [INFO] Проверка сборки...
if exist "build\main.exe" (
    echo [SUCCESS] main.exe найден
) else (
    echo [ERROR] main.exe не найден!
)

if exist "build\config.json" (
    echo [SUCCESS] config.json найден
) else (
    echo [ERROR] config.json не найден!
)

echo.
echo ===============================================
echo           СБОРКА ЗАВЕРШЕНА!
echo ===============================================
echo.
echo Файлы находятся в папке 'build\'
echo Запустите launcher.bat от имени администратора
echo.
echo ВАЖНО:
echo - Программа работает только с правами администратора
echo - Изменения временные (до перезагрузки)
echo - Поддерживается Windows 11 24H2
echo - Создайте точку восстановления перед использованием
echo.

pause
