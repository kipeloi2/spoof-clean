@echo off
echo ===============================================
echo    ULTIMATE SMBIOS TOOLS BUILDER 2025
echo    Maximum Depth Hardware Spoofing
echo    Fortnite EAC Bypass Specialized
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

:: Создание специализированных директорий
echo [INFO] Создание директорий для Ultimate Tools...
if not exist "ultimate_tools" mkdir ultimate_tools
if not exist "ultimate_tools\logs" mkdir ultimate_tools\logs
if not exist "ultimate_tools\backups" mkdir ultimate_tools\backups
if not exist "ultimate_tools\profiles" mkdir ultimate_tools\profiles

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

:: Компиляция SMBIOS Deep Spoofer
echo.
echo [INFO] Компиляция SMBIOS Deep Spoofer...
echo [INFO] Применение максимальных оптимизаций...

g++ -std=c++17 -O3 -march=native -mtune=native ^
    -static-libgcc -static-libstdc++ ^
    -DUNICODE -D_UNICODE ^
    -DSMBIOS_DEEP_SPOOF ^
    -DMAX_EAC_BYPASS ^
    -I. ^
    -o ultimate_tools/smbios_deep_spoofer.exe ^
    smbios_deep_spoofer.cpp ^
    -ladvapi32 -lshell32 -luser32 -lpsapi -lkernel32

if %errorLevel% neq 0 (
    echo [ERROR] Ошибка компиляции SMBIOS Deep Spoofer!
    echo [INFO] Проверьте код и зависимости
    pause
    exit /b 1
)

echo [SUCCESS] SMBIOS Deep Spoofer скомпилирован успешно!

:: Компиляция основного Fortnite спуффера
echo [INFO] Компиляция основного Fortnite спуффера...
g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ ^
    -DUNICODE -D_UNICODE ^
    -DFORTNITE_OPTIMIZED ^
    -I. ^
    -o ultimate_tools/fortnite_spoofer.exe ^
    fortnite_spoofer_simple.cpp ^
    -liphlpapi -lsetupapi -lcfgmgr32 -ladvapi32 ^
    -lshell32 -luser32 -lpsapi -lkernel32

if %errorLevel% neq 0 (
    echo [WARNING] Основной спуффер не скомпилирован (не критично)
) else (
    echo [SUCCESS] Основной Fortnite спуффер скомпилирован!
)

:: Копирование PowerShell скриптов
echo [INFO] Копирование PowerShell скриптов...
copy "ultimate_smbios_spoof.ps1" "ultimate_tools\" >nul
copy "fortnite_gui.py" "ultimate_tools\" >nul
copy "config.json" "ultimate_tools\" >nul
copy "fortnite_config_2025.json" "ultimate_tools\" >nul

:: Создание Ultimate лаунчера
echo [INFO] Создание Ultimate лаунчера...
echo @echo off > ultimate_tools\ultimate_launcher.bat
echo title Ultimate SMBIOS Tools 2025 - Maximum EAC Bypass >> ultimate_tools\ultimate_launcher.bat
echo color 0A >> ultimate_tools\ultimate_launcher.bat
echo echo. >> ultimate_tools\ultimate_launcher.bat
echo echo ================================================ >> ultimate_tools\ultimate_launcher.bat
echo echo    🔥 ULTIMATE SMBIOS TOOLS 2025 🔥 >> ultimate_tools\ultimate_launcher.bat
echo echo    Maximum Depth Hardware Spoofing >> ultimate_tools\ultimate_launcher.bat
echo echo    Fortnite EAC Bypass Specialized >> ultimate_tools\ultimate_launcher.bat
echo echo ================================================ >> ultimate_tools\ultimate_launcher.bat
echo echo. >> ultimate_tools\ultimate_launcher.bat
echo echo ⚠️  ВНИМАНИЕ: Эти инструменты изменяют ВСЕ серийники! >> ultimate_tools\ultimate_launcher.bat
echo echo ⚠️  Используйте только если обычный спуффер не помог! >> ultimate_tools\ultimate_launcher.bat
echo echo. >> ultimate_tools\ultimate_launcher.bat
echo echo Выберите инструмент: >> ultimate_tools\ultimate_launcher.bat
echo echo. >> ultimate_tools\ultimate_launcher.bat
echo echo 1. 🔥 SMBIOS Deep Spoofer (C++ - Максимальная мощность) >> ultimate_tools\ultimate_launcher.bat
echo echo 2. 💻 PowerShell Ultimate Spoofer (PS1 - Глубокий доступ) >> ultimate_tools\ultimate_launcher.bat
echo echo 3. 🎮 Обычный Fortnite Spoofer (Стандартный) >> ultimate_tools\ultimate_launcher.bat
echo echo 4. 🖥️  GUI Интерфейс (Python) >> ultimate_tools\ultimate_launcher.bat
echo echo 5. 🔍 Проверка системы >> ultimate_tools\ultimate_launcher.bat
echo echo 6. 💾 Создать точку восстановления >> ultimate_tools\ultimate_launcher.bat
echo echo 7. 🚪 Выход >> ultimate_tools\ultimate_launcher.bat
echo echo. >> ultimate_tools\ultimate_launcher.bat
echo :start >> ultimate_tools\ultimate_launcher.bat
echo set /p choice="Введите номер (1-7): " >> ultimate_tools\ultimate_launcher.bat
echo. >> ultimate_tools\ultimate_launcher.bat
echo if "%%choice%%"=="1" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [INFO] Запуск SMBIOS Deep Spoofer... >> ultimate_tools\ultimate_launcher.bat
echo     echo [WARNING] Это изменит ВСЕ hardware серийники! >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo     smbios_deep_spoofer.exe >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo ) else if "%%choice%%"=="2" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [INFO] Запуск PowerShell Ultimate Spoofer... >> ultimate_tools\ultimate_launcher.bat
echo     echo [WARNING] Это изменит ВСЕ hardware серийники! >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo     powershell -ExecutionPolicy Bypass -File ultimate_smbios_spoof.ps1 >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo ) else if "%%choice%%"=="3" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [INFO] Запуск обычного Fortnite спуффера... >> ultimate_tools\ultimate_launcher.bat
echo     fortnite_spoofer.exe >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo ) else if "%%choice%%"=="4" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [INFO] Запуск GUI интерфейса... >> ultimate_tools\ultimate_launcher.bat
echo     python fortnite_gui.py >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo ) else if "%%choice%%"=="5" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [INFO] Проверка системы... >> ultimate_tools\ultimate_launcher.bat
echo     smbios_deep_spoofer.exe --check >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo ) else if "%%choice%%"=="6" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [INFO] Создание точки восстановления... >> ultimate_tools\ultimate_launcher.bat
echo     powershell -Command "Checkpoint-Computer -Description 'Ultimate SMBIOS Tools Backup' -RestorePointType 'MODIFY_SETTINGS'" >> ultimate_tools\ultimate_launcher.bat
echo     echo [SUCCESS] Точка восстановления создана! >> ultimate_tools\ultimate_launcher.bat
echo     pause >> ultimate_tools\ultimate_launcher.bat
echo ) else if "%%choice%%"=="7" ( >> ultimate_tools\ultimate_launcher.bat
echo     echo Goodbye! >> ultimate_tools\ultimate_launcher.bat
echo     exit >> ultimate_tools\ultimate_launcher.bat
echo ) else ( >> ultimate_tools\ultimate_launcher.bat
echo     echo [ERROR] Неверный выбор! >> ultimate_tools\ultimate_launcher.bat
echo     timeout /t 2 /nobreak ^>nul >> ultimate_tools\ultimate_launcher.bat
echo     cls >> ultimate_tools\ultimate_launcher.bat
echo     goto start >> ultimate_tools\ultimate_launcher.bat
echo ) >> ultimate_tools\ultimate_launcher.bat

:: Создание README для Ultimate Tools
echo [INFO] Создание документации...
echo ULTIMATE SMBIOS TOOLS 2025 > ultimate_tools\README_ULTIMATE.txt
echo ================================= >> ultimate_tools\README_ULTIMATE.txt
echo. >> ultimate_tools\README_ULTIMATE.txt
echo 🔥 МАКСИМАЛЬНО МОЩНЫЕ ИНСТРУМЕНТЫ ДЛЯ SMBIOS СПУФИНГА >> ultimate_tools\README_ULTIMATE.txt
echo 🎯 СПЕЦИАЛЬНО ДЛЯ FORTNITE EAC BYPASS >> ultimate_tools\README_ULTIMATE.txt
echo 💀 ИЗМЕНЯЮТ ВСЕ HARDWARE СЕРИЙНИКИ >> ultimate_tools\README_ULTIMATE.txt
echo. >> ultimate_tools\README_ULTIMATE.txt
echo ИНСТРУМЕНТЫ: >> ultimate_tools\README_ULTIMATE.txt
echo ============ >> ultimate_tools\README_ULTIMATE.txt
echo smbios_deep_spoofer.exe     - C++ инструмент максимальной мощности >> ultimate_tools\README_ULTIMATE.txt
echo ultimate_smbios_spoof.ps1   - PowerShell скрипт глубокого доступа >> ultimate_tools\README_ULTIMATE.txt
echo fortnite_spoofer.exe        - Обычный Fortnite спуффер >> ultimate_tools\README_ULTIMATE.txt
echo ultimate_launcher.bat       - Лаунчер всех инструментов >> ultimate_tools\README_ULTIMATE.txt
echo. >> ultimate_tools\README_ULTIMATE.txt
echo ИСПОЛЬЗОВАНИЕ: >> ultimate_tools\README_ULTIMATE.txt
echo ============== >> ultimate_tools\README_ULTIMATE.txt
echo 1. ОБЯЗАТЕЛЬНО создайте точку восстановления! >> ultimate_tools\README_ULTIMATE.txt
echo 2. Закройте Fortnite полностью >> ultimate_tools\README_ULTIMATE.txt
echo 3. ПКМ на ultimate_launcher.bat -^> "Запуск от имени администратора" >> ultimate_tools\README_ULTIMATE.txt
echo 4. Выберите нужный инструмент >> ultimate_tools\README_ULTIMATE.txt
echo 5. Дождитесь завершения >> ultimate_tools\README_ULTIMATE.txt
echo 6. Запустите Fortnite >> ultimate_tools\README_ULTIMATE.txt
echo. >> ultimate_tools\README_ULTIMATE.txt
echo ОСОБЕННОСТИ ULTIMATE TOOLS: >> ultimate_tools\README_ULTIMATE.txt
echo ============================ >> ultimate_tools\README_ULTIMATE.txt
echo ✅ Изменяют ВСЕ hardware серийники (BIOS, Baseboard, System, Enclosure) >> ultimate_tools\README_ULTIMATE.txt
echo ✅ Глубокая очистка WMI кэша >> ultimate_tools\README_ULTIMATE.txt
echo ✅ Остановка и перезапуск критических служб >> ultimate_tools\README_ULTIMATE.txt
echo ✅ Множественные методы спуфинга >> ultimate_tools\README_ULTIMATE.txt
echo ✅ Реалистичные серийники в стиле 2025 года >> ultimate_tools\README_ULTIMATE.txt
echo ✅ Максимальная совместимость с Windows 11 24H2 >> ultimate_tools\README_ULTIMATE.txt
echo. >> ultimate_tools\README_ULTIMATE.txt
echo ⚠️ ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ: >> ultimate_tools\README_ULTIMATE.txt
echo ========================= >> ultimate_tools\README_ULTIMATE.txt
echo • Эти инструменты ОЧЕНЬ мощные - используйте только если обычный спуффер не помог >> ultimate_tools\README_ULTIMATE.txt
echo • ОБЯЗАТЕЛЬНО создавайте точку восстановления перед использованием >> ultimate_tools\README_ULTIMATE.txt
echo • Все изменения временные - отменяются после перезагрузки >> ultimate_tools\README_ULTIMATE.txt
echo • Используйте только на свой страх и риск >> ultimate_tools\README_ULTIMATE.txt
echo • Только для образовательных целей >> ultimate_tools\README_ULTIMATE.txt

:: Проверка сборки
echo [INFO] Проверка сборки Ultimate Tools...
if exist "ultimate_tools\smbios_deep_spoofer.exe" (
    echo [SUCCESS] ✅ smbios_deep_spoofer.exe создан
) else (
    echo [ERROR] ❌ smbios_deep_spoofer.exe не найден!
)

if exist "ultimate_tools\ultimate_smbios_spoof.ps1" (
    echo [SUCCESS] ✅ ultimate_smbios_spoof.ps1 скопирован
) else (
    echo [ERROR] ❌ ultimate_smbios_spoof.ps1 не найден!
)

if exist "ultimate_tools\ultimate_launcher.bat" (
    echo [SUCCESS] ✅ ultimate_launcher.bat создан
) else (
    echo [ERROR] ❌ ultimate_launcher.bat не найден!
)

echo.
echo ===============================================
echo        🔥 ULTIMATE SMBIOS TOOLS ГОТОВЫ! 🔥
echo ===============================================
echo.
echo 📁 Все файлы находятся в папке 'ultimate_tools\'
echo 🚀 Запустите: ultimate_launcher.bat (от имени администратора)
echo.
echo 💀 ВНИМАНИЕ: Эти инструменты ОЧЕНЬ мощные!
echo 💀 Они изменяют ВСЕ hardware серийники!
echo 💀 Используйте только если обычный спуффер не помог!
echo.
echo 🔥 ВОЗМОЖНОСТИ ULTIMATE TOOLS:
echo   • SMBIOS Deep Spoofer (C++) - максимальная мощность
echo   • PowerShell Ultimate Spoofer - глубокий системный доступ
echo   • Изменение всех серийников (BIOS, Baseboard, System, Enclosure)
echo   • Очистка WMI кэша и перезапуск служб
echo   • Реалистичные серийники 2025 года
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
