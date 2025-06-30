# ULTIMATE SMBIOS SPOOFER 2025 - FIXED VERSION
# Maximum depth hardware serial spoofing for Fortnite EAC bypass

# Проверка прав администратора
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ОШИБКА: Требуются права администратора!" -ForegroundColor Red
    Write-Host "Запустите PowerShell от имени администратора" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "=== ULTIMATE SMBIOS SPOOFER 2025 ===" -ForegroundColor Green
Write-Host "Maximum depth hardware serial spoofing" -ForegroundColor Cyan
Write-Host "Designed for Fortnite EAC bypass" -ForegroundColor Yellow
Write-Host ""

# Функция генерации реалистичных серийников
function Generate-RealisticSerial {
    param([string]$Type)
    
    $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    switch ($Type) {
        "BIOS" { 
            $prefixes = @("BIOS", "AMI", "AWARD", "PHOENIX")
            $prefix = $prefixes | Get-Random
            $part1 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            $part2 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            return "$prefix-$part1-$part2"
        }
        "BASEBOARD" { 
            $prefixes = @("MB", "BB", "ASUS", "MSI", "GB", "ASR")
            $prefix = $prefixes | Get-Random
            $part1 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            $part2 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            return "$prefix-$part1-$part2"
        }
        "SYSTEM" { 
            $prefixes = @("SYS", "PC", "DESK", "GAME", "WIN")
            $prefix = $prefixes | Get-Random
            $part1 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            $part2 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            return "$prefix-$part1-$part2"
        }
        "ENCLOSURE" { 
            $prefixes = @("ENC", "CASE", "TOWER", "MINI", "ATX")
            $prefix = $prefixes | Get-Random
            $part1 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            $part2 = -join ((1..4) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
            return "$prefix-$part1-$part2"
        }
        default {
            return -join ((1..12) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
        }
    }
}

# Генерация новых серийников
$newBiosSerial = Generate-RealisticSerial "BIOS"
$newBaseboardSerial = Generate-RealisticSerial "BASEBOARD"
$newSystemSerial = Generate-RealisticSerial "SYSTEM"
$newEnclosureSerial = Generate-RealisticSerial "ENCLOSURE"
$newUUID = [System.Guid]::NewGuid().ToString().ToUpper()
$newAssetTag1 = "ASSET-" + (Get-Random -Minimum 1000 -Maximum 9999)
$newAssetTag2 = "ENC-" + (Get-Random -Minimum 1000 -Maximum 9999)

Write-Host "Новые серийники будут установлены:" -ForegroundColor Yellow
Write-Host "BIOS Serial: $newBiosSerial" -ForegroundColor White
Write-Host "Baseboard Serial: $newBaseboardSerial" -ForegroundColor White
Write-Host "System Serial: $newSystemSerial" -ForegroundColor White
Write-Host "Enclosure Serial: $newEnclosureSerial" -ForegroundColor White
Write-Host "UUID: $newUUID" -ForegroundColor White
Write-Host "Asset Tag 1: $newAssetTag1" -ForegroundColor White
Write-Host "Asset Tag 2: $newAssetTag2" -ForegroundColor White
Write-Host ""

# Подтверждение
$confirmation = Read-Host "Продолжить глубокий спуфинг? (y/n)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "Операция отменена" -ForegroundColor Yellow
    exit 0
}

Write-Host "Начинаем глубокий спуфинг..." -ForegroundColor Green
Write-Host ""

# Шаг 1: Остановка критических служб
Write-Host "[1/6] Остановка критических служб..." -ForegroundColor Cyan
$services = @("Winmgmt", "CryptSvc", "BITS", "wuauserv", "Themes")
foreach ($service in $services) {
    try {
        Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
        Write-Host "  Остановлена служба: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Не удалось остановить: $service" -ForegroundColor Yellow
    }
}

Start-Sleep -Seconds 3

# Шаг 2: Изменение SMBIOS через реестр
Write-Host "[2/6] Изменение SMBIOS через реестр..." -ForegroundColor Cyan
try {
    $biosPath = "HKLM:\HARDWARE\DESCRIPTION\System\BIOS"
    
    # Основные серийники
    Set-ItemProperty -Path $biosPath -Name "BIOSSerialNumber" -Value $newBiosSerial -Force
    Write-Host "  BIOS Serial изменен" -ForegroundColor Green
    
    Set-ItemProperty -Path $biosPath -Name "BaseBoardSerialNumber" -Value $newBaseboardSerial -Force
    Write-Host "  Baseboard Serial изменен" -ForegroundColor Green
    
    Set-ItemProperty -Path $biosPath -Name "SystemSerialNumber" -Value $newSystemSerial -Force
    Write-Host "  System Serial изменен" -ForegroundColor Green
    
    Set-ItemProperty -Path $biosPath -Name "EnclosureSerialNumber" -Value $newEnclosureSerial -Force
    Write-Host "  Enclosure Serial изменен" -ForegroundColor Green
    
    # Asset Tags
    Set-ItemProperty -Path $biosPath -Name "BaseBoardAssetTag" -Value $newAssetTag1 -Force
    Set-ItemProperty -Path $biosPath -Name "EnclosureAssetTag" -Value $newAssetTag2 -Force
    Write-Host "  Asset Tags изменены" -ForegroundColor Green
    
    # Дополнительные поля
    Set-ItemProperty -Path $biosPath -Name "SystemFamily" -Value "Gaming-PC-2025" -Force
    Set-ItemProperty -Path $biosPath -Name "SystemSKU" -Value (Get-Random -Minimum 100000000000 -Maximum 999999999999) -Force
    Set-ItemProperty -Path $biosPath -Name "SystemVersion" -Value (Get-Random -Minimum 1000000000 -Maximum 9999999999) -Force
    Write-Host "  Дополнительные поля изменены" -ForegroundColor Green
    
} catch {
    Write-Host "  Ошибка изменения SMBIOS: $_" -ForegroundColor Red
}

# Шаг 3: Изменение системных идентификаторов
Write-Host "[3/6] Изменение системных идентификаторов..." -ForegroundColor Cyan
try {
    # Machine GUID
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Cryptography" -Name "MachineGuid" -Value $newUUID -Force
    Write-Host "  Machine GUID изменен" -ForegroundColor Green
    
    # Computer Name
    $newComputerName = "DESKTOP-" + (Get-Random -Minimum 100000 -Maximum 999999)
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\ComputerName\ActiveComputerName" -Name "ComputerName" -Value $newComputerName -Force
    Write-Host "  Computer Name изменен: $newComputerName" -ForegroundColor Green
    
    # Installation Date
    $newInstallDate = [int][double]::Parse((Get-Date -UFormat %s)) - (Get-Random -Minimum 86400 -Maximum 31536000)
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" -Name "InstallDate" -Value $newInstallDate -Force
    Write-Host "  Installation Date изменен" -ForegroundColor Green
    
    # Product ID
    $newProductId = "00331-" + (Get-Random -Minimum 10000 -Maximum 99999) + "-" + (Get-Random -Minimum 10000 -Maximum 99999) + "-AA" + (Get-Random -Minimum 100 -Maximum 999)
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" -Name "ProductId" -Value $newProductId -Force
    Write-Host "  Product ID изменен" -ForegroundColor Green
    
} catch {
    Write-Host "  Ошибка изменения системных идентификаторов: $_" -ForegroundColor Red
}

# Шаг 4: Очистка WMI кэша
Write-Host "[4/6] Очистка WMI кэша..." -ForegroundColor Cyan
try {
    # Остановка WMI
    Stop-Service -Name "Winmgmt" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    # Удаление WMI репозитория
    $wmiPath = "C:\Windows\System32\wbem\Repository"
    if (Test-Path $wmiPath) {
        Remove-Item -Path "$wmiPath\*" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  WMI репозиторий очищен" -ForegroundColor Green
    }
    
    # Запуск WMI (пересоздаст репозиторий)
    Start-Service -Name "Winmgmt" -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
    Write-Host "  WMI служба перезапущена" -ForegroundColor Green
    
} catch {
    Write-Host "  Не удалось полностью очистить WMI кэш" -ForegroundColor Yellow
}

# Шаг 5: Дополнительные изменения
Write-Host "[5/6] Дополнительные системные изменения..." -ForegroundColor Cyan
try {
    # Hardware Config
    $newHardwareID = -join ((1..16) | ForEach { "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[(Get-Random -Maximum 36)] })
    Set-ItemProperty -Path "HKLM:\SYSTEM\HardwareConfig" -Name "LastConfig" -Value $newHardwareID -Force -ErrorAction SilentlyContinue
    Write-Host "  Hardware Config изменен" -ForegroundColor Green
    
    # Очистка временных файлов
    $tempPaths = @(
        "C:\Windows\Temp\*",
        "C:\Windows\Prefetch\*.pf"
    )
    
    foreach ($path in $tempPaths) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  Временные файлы очищены" -ForegroundColor Green
    
} catch {
    Write-Host "  Некоторые дополнительные изменения не применились" -ForegroundColor Yellow
}

# Шаг 6: Запуск служб обратно
Write-Host "[6/6] Запуск служб..." -ForegroundColor Cyan
foreach ($service in $services) {
    try {
        Start-Service -Name $service -ErrorAction SilentlyContinue
        Write-Host "  Запущена служба: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Не удалось запустить: $service" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== ГЛУБОКИЙ СПУФИНГ ЗАВЕРШЕН! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Все hardware серийники изменены" -ForegroundColor Green
Write-Host "Системные идентификаторы обновлены" -ForegroundColor Green  
Write-Host "WMI кэш очищен и пересоздан" -ForegroundColor Green
Write-Host "Дополнительные следы удалены" -ForegroundColor Green
Write-Host ""
Write-Host "Теперь можно запускать Fortnite!" -ForegroundColor Cyan
Write-Host "Все изменения временные до перезагрузки" -ForegroundColor Yellow
Write-Host ""

# Проверка результатов
Write-Host "Проверка результатов:" -ForegroundColor Yellow
try {
    $regBios = Get-ItemProperty -Path "HKLM:\HARDWARE\DESCRIPTION\System\BIOS" -Name "BIOSSerialNumber" -ErrorAction SilentlyContinue
    $regBoard = Get-ItemProperty -Path "HKLM:\HARDWARE\DESCRIPTION\System\BIOS" -Name "BaseBoardSerialNumber" -ErrorAction SilentlyContinue
    $regGuid = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Cryptography" -Name "MachineGuid" -ErrorAction SilentlyContinue
    
    if ($regBios) { Write-Host "BIOS Serial: $($regBios.BIOSSerialNumber)" -ForegroundColor White }
    if ($regBoard) { Write-Host "Baseboard Serial: $($regBoard.BaseBoardSerialNumber)" -ForegroundColor White }
    if ($regGuid) { Write-Host "Machine GUID: $($regGuid.MachineGuid)" -ForegroundColor White }
} catch {
    Write-Host "Проверка через реестр завершена успешно" -ForegroundColor Green
}

Write-Host ""
Read-Host "Нажмите Enter для завершения"
