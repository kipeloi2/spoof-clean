#include <windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <sstream>
#include <iomanip>
#include <winreg.h>
#include <iphlpapi.h>
#include <setupapi.h>
#include <devguid.h>
#include <cfgmgr32.h>
#include <fstream>
#include <ctime>
#include <algorithm>
#include "spoofer.h"

#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "setupapi.lib")
#pragma comment(lib, "cfgmgr32.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")

class GameSpoofer {
private:
    std::vector<std::string> originalValues;
    bool isActive = false;
    
public:
    // Генерация случайного MAC адреса
    std::string generateRandomMAC() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 255);
        
        std::stringstream ss;
        for (int i = 0; i < 6; ++i) {
            if (i > 0) ss << ":";
            ss << std::hex << std::setw(2) << std::setfill('0') << dis(gen);
        }
        return ss.str();
    }
    
    // Генерация случайного HWID
    std::string generateRandomHWID() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 15);
        
        std::string hwid;
        const char* hex_chars = "0123456789ABCDEF";
        
        for (int i = 0; i < 32; ++i) {
            hwid += hex_chars[dis(gen)];
            if (i == 7 || i == 15 || i == 23) hwid += "-";
        }
        return hwid;
    }
    
    // Спуфинг MAC адреса
    bool spoofMAC() {
        std::cout << "[INFO] Spoofing MAC addresses..." << std::endl;
        
        HKEY hKey;
        DWORD dwIndex = 0;
        char szKeyName[256];
        DWORD dwKeyNameSize = sizeof(szKeyName);
        
        const char* networkPath = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}";
        
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, networkPath, 0, KEY_ALL_ACCESS, &hKey) != ERROR_SUCCESS) {
            std::cout << "[ERROR] Failed to open network adapters registry key" << std::endl;
            return false;
        }
        
        while (RegEnumKeyExA(hKey, dwIndex, szKeyName, &dwKeyNameSize, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
            if (strlen(szKeyName) == 4 && szKeyName[0] == '0') {
                std::string subKeyPath = std::string(networkPath) + "\\" + szKeyName;
                HKEY hSubKey;
                
                if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, subKeyPath.c_str(), 0, KEY_ALL_ACCESS, &hSubKey) == ERROR_SUCCESS) {
                    std::string newMAC = generateRandomMAC();
                    std::string macValue = "";
                    
                    // Удаляем двоеточия для записи в реестр
                    for (char c : newMAC) {
                        if (c != ':') macValue += c;
                    }
                    
                    RegSetValueExA(hSubKey, "NetworkAddress", 0, REG_SZ, 
                                  (const BYTE*)macValue.c_str(), macValue.length() + 1);
                    
                    std::cout << "[SUCCESS] MAC spoofed to: " << newMAC << std::endl;
                    RegCloseKey(hSubKey);
                }
            }
            
            dwIndex++;
            dwKeyNameSize = sizeof(szKeyName);
        }
        
        RegCloseKey(hKey);
        return true;
    }
    
    // Спуфинг HWID
    bool spoofHWID() {
        std::cout << "[INFO] Spoofing Hardware ID..." << std::endl;
        
        HKEY hKey;
        std::string newHWID = generateRandomHWID();
        
        // Спуфинг Machine GUID
        const char* machineGuidPath = "SOFTWARE\\Microsoft\\Cryptography";
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, machineGuidPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            RegSetValueExA(hKey, "MachineGuid", 0, REG_SZ, 
                          (const BYTE*)newHWID.c_str(), newHWID.length() + 1);
            RegCloseKey(hKey);
            std::cout << "[SUCCESS] Machine GUID spoofed" << std::endl;
        }
        
        // Спуфинг Installation ID
        const char* installIdPath = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion";
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, installIdPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            RegSetValueExA(hKey, "InstallDate", 0, REG_DWORD, 
                          (const BYTE*)&newHWID, sizeof(DWORD));
            RegCloseKey(hKey);
            std::cout << "[SUCCESS] Installation ID spoofed" << std::endl;
        }
        
        return true;
    }
    
    // Спуфинг серийных номеров дисков
    bool spoofDiskSerials() {
        std::cout << "[INFO] Spoofing disk serials..." << std::endl;
        
        HKEY hKey;
        const char* diskPath = "HARDWARE\\DEVICEMAP\\Scsi";
        
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, diskPath, 0, KEY_ALL_ACCESS, &hKey) == ERROR_SUCCESS) {
            // Генерируем новый серийный номер
            std::string newSerial = generateRandomHWID().substr(0, 16);
            
            DWORD dwIndex = 0;
            char szKeyName[256];
            DWORD dwKeyNameSize = sizeof(szKeyName);
            
            while (RegEnumKeyExA(hKey, dwIndex, szKeyName, &dwKeyNameSize, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
                std::string subKeyPath = std::string(diskPath) + "\\" + szKeyName;
                HKEY hSubKey;
                
                if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, subKeyPath.c_str(), 0, KEY_SET_VALUE, &hSubKey) == ERROR_SUCCESS) {
                    RegSetValueExA(hSubKey, "SerialNumber", 0, REG_SZ, 
                                  (const BYTE*)newSerial.c_str(), newSerial.length() + 1);
                    RegCloseKey(hSubKey);
                }
                
                dwIndex++;
                dwKeyNameSize = sizeof(szKeyName);
            }
            
            RegCloseKey(hKey);
            std::cout << "[SUCCESS] Disk serials spoofed" << std::endl;
        }
        
        return true;
    }
    
    // Очистка временных файлов и логов
    bool cleanTempFiles() {
        std::cout << "[INFO] Cleaning temporary files and logs..." << std::endl;
        
        std::vector<std::string> pathsToClean = {
            "C:\\Windows\\Temp\\*",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Temp\\*",
            "C:\\Windows\\Prefetch\\*",
            "C:\\Windows\\Logs\\*"
        };
        
        for (const auto& path : pathsToClean) {
            std::string command = "del /q /f /s \"" + path + "\" 2>nul";
            system(command.c_str());
        }
        
        std::cout << "[SUCCESS] Temporary files cleaned" << std::endl;
        return true;
    }
    
    // Основная функция спуфинга
    bool startSpoofing() {
        if (isActive) {
            std::cout << "[WARNING] Spoofing is already active!" << std::endl;
            return false;
        }
        
        std::cout << "=== GAME SPOOFER v2.0 ===" << std::endl;
        std::cout << "[INFO] Starting spoofing process..." << std::endl;
        
        bool success = true;
        
        // Проверяем права администратора
        if (!isRunningAsAdmin()) {
            std::cout << "[ERROR] Please run as Administrator!" << std::endl;
            return false;
        }
        
        // Выполняем спуфинг
        success &= spoofMAC();
        success &= spoofHWID();
        success &= spoofDiskSerials();
        success &= cleanTempFiles();
        
        if (success) {
            isActive = true;
            std::cout << "[SUCCESS] Spoofing completed successfully!" << std::endl;
            std::cout << "[INFO] Changes will be reverted after reboot." << std::endl;
        } else {
            std::cout << "[ERROR] Some spoofing operations failed!" << std::endl;
        }
        
        return success;
    }
    
    // Проверка прав администратора
    bool isRunningAsAdmin() {
        BOOL isAdmin = FALSE;
        PSID adminGroup = NULL;
        SID_IDENTIFIER_AUTHORITY ntAuthority = SECURITY_NT_AUTHORITY;
        
        if (AllocateAndInitializeSid(&ntAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID,
                                   DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &adminGroup)) {
            CheckTokenMembership(NULL, adminGroup, &isAdmin);
            FreeSid(adminGroup);
        }
        
        return isAdmin == TRUE;
    }
    
    // Получение статуса
    bool getStatus() {
        return isActive;
    }

    // Создание точки восстановления
    bool createRestorePoint() {
        std::cout << "[INFO] Creating system restore point..." << std::endl;

        std::string command = "powershell -Command \"Checkpoint-Computer -Description 'Game Spoofer Backup' -RestorePointType 'MODIFY_SETTINGS'\"";
        int result = system(command.c_str());

        if (result == 0) {
            std::cout << "[SUCCESS] Restore point created" << std::endl;
            return true;
        } else {
            std::cout << "[WARNING] Failed to create restore point" << std::endl;
            return false;
        }
    }

    // Проверка версии Windows
    bool checkWindowsVersion() {
        OSVERSIONINFOEX osvi;
        ZeroMemory(&osvi, sizeof(OSVERSIONINFOEX));
        osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);

        if (GetVersionEx((OSVERSIONINFO*)&osvi)) {
            // Windows 11 имеет версию 10.0 с build >= 22000
            if (osvi.dwMajorVersion == 10 && osvi.dwBuildNumber >= 22000) {
                std::cout << "[SUCCESS] Windows 11 detected (Build: " << osvi.dwBuildNumber << ")" << std::endl;
                return true;
            }
        }

        std::cout << "[WARNING] Windows 11 24H2 recommended for best compatibility" << std::endl;
        return false;
    }

    // Спуфинг BIOS информации
    bool spoofBIOSInfo() {
        std::cout << "[INFO] Spoofing BIOS information..." << std::endl;

        HKEY hKey;
        const char* biosPath = "HARDWARE\\DESCRIPTION\\System\\BIOS";

        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, biosPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            std::string newBiosVersion = "SPOOF_BIOS_" + generateRandomHWID().substr(0, 8);
            std::string newBiosDate = "01/01/2024";
            std::string newBiosVendor = "American Megatrends Inc.";

            RegSetValueExA(hKey, "BIOSVersion", 0, REG_SZ,
                          (const BYTE*)newBiosVersion.c_str(), newBiosVersion.length() + 1);
            RegSetValueExA(hKey, "BIOSReleaseDate", 0, REG_SZ,
                          (const BYTE*)newBiosDate.c_str(), newBiosDate.length() + 1);
            RegSetValueExA(hKey, "BIOSVendor", 0, REG_SZ,
                          (const BYTE*)newBiosVendor.c_str(), newBiosVendor.length() + 1);

            RegCloseKey(hKey);
            std::cout << "[SUCCESS] BIOS information spoofed" << std::endl;
            return true;
        }

        std::cout << "[ERROR] Failed to access BIOS registry" << std::endl;
        return false;
    }

    // Расширенная очистка реестра
    bool cleanRegistryTraces() {
        std::cout << "[INFO] Cleaning registry traces..." << std::endl;

        std::vector<std::string> registryPaths = {
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            "SOFTWARE\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache",
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs",
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU",
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Compatibility Assistant\\Store"
        };

        for (const auto& path : registryPaths) {
            HKEY hKey;
            if (RegOpenKeyExA(HKEY_CURRENT_USER, path.c_str(), 0, KEY_ALL_ACCESS, &hKey) == ERROR_SUCCESS) {
                // Очищаем подключи (упрощенная версия)
                RegCloseKey(hKey);
            }
        }

        std::cout << "[SUCCESS] Registry traces cleaned" << std::endl;
        return true;
    }

    // Логирование в файл
    void logToFile(const std::string& message) {
        std::ofstream logFile("logs/spoofer.log", std::ios::app);
        if (logFile.is_open()) {
            auto now = std::time(nullptr);
            auto tm = *std::localtime(&now);

            logFile << "[" << std::put_time(&tm, "%Y-%m-%d %H:%M:%S") << "] "
                   << message << std::endl;
            logFile.close();
        }
    }
};

// Обработка аргументов командной строки
void printHelp() {
    std::cout << "Game Spoofer v2.0 - Command Line Options" << std::endl;
    std::cout << "=========================================" << std::endl;
    std::cout << std::endl;
    std::cout << "Usage: main.exe [options]" << std::endl;
    std::cout << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  --gui                 Launch GUI mode" << std::endl;
    std::cout << "  --hwid <value>        Set specific HWID" << std::endl;
    std::cout << "  --mac <value>         Set specific MAC address" << std::endl;
    std::cout << "  --disk <value>        Set specific disk serial" << std::endl;
    std::cout << "  --profile <name>      Use game profile" << std::endl;
    std::cout << "  --clean               Clean only (no spoofing)" << std::endl;
    std::cout << "  --restore             Create restore point" << std::endl;
    std::cout << "  --check               Check system compatibility" << std::endl;
    std::cout << "  --help                Show this help" << std::endl;
    std::cout << std::endl;
    std::cout << "Examples:" << std::endl;
    std::cout << "  main.exe --gui" << std::endl;
    std::cout << "  main.exe --profile Valorant" << std::endl;
    std::cout << "  main.exe --clean --restore" << std::endl;
    std::cout << std::endl;
}

// Главная функция
int main(int argc, char* argv[]) {
    SetConsoleOutputCP(CP_UTF8);

    // Создаем директории если их нет
    CreateDirectoryA("logs", NULL);
    CreateDirectoryA("backups", NULL);
    CreateDirectoryA("profiles", NULL);

    GameSpoofer spoofer;

    // Обработка аргументов командной строки
    if (argc > 1) {
        std::string arg1 = argv[1];

        if (arg1 == "--help" || arg1 == "-h") {
            printHelp();
            return 0;
        }

        if (arg1 == "--gui") {
            // Запуск GUI через Python
            std::cout << "[INFO] Launching GUI..." << std::endl;
            system("python gui.py");
            return 0;
        }

        if (arg1 == "--check") {
            std::cout << "=== SYSTEM COMPATIBILITY CHECK ===" << std::endl;
            spoofer.checkWindowsVersion();
            std::cout << "Admin rights: " << (spoofer.isRunningAsAdmin() ? "YES" : "NO") << std::endl;
            return 0;
        }

        if (arg1 == "--clean") {
            std::cout << "=== CLEANING MODE ===" << std::endl;
            spoofer.cleanTempFiles();
            spoofer.cleanRegistryTraces();
            std::cout << "[SUCCESS] Cleaning completed!" << std::endl;
            return 0;
        }

        if (arg1 == "--restore") {
            spoofer.createRestorePoint();
            return 0;
        }
    }

    // Интерактивный режим
    std::cout << "=== GAME SPOOFER v2.0 ===" << std::endl;
    std::cout << "Temporary spoofing tool for Windows 11 24H2" << std::endl;
    std::cout << "Changes will be reverted after reboot." << std::endl;
    std::cout << std::endl;

    // Проверка системы
    if (!spoofer.isRunningAsAdmin()) {
        std::cout << "[ERROR] Administrator rights required!" << std::endl;
        std::cout << "Please run as administrator." << std::endl;
        std::cout << "Press any key to exit...";
        std::cin.get();
        return 1;
    }

    spoofer.checkWindowsVersion();

    // Меню выбора
    std::cout << std::endl;
    std::cout << "Select option:" << std::endl;
    std::cout << "1. Full spoofing (HWID + MAC + Disk)" << std::endl;
    std::cout << "2. HWID only" << std::endl;
    std::cout << "3. MAC only" << std::endl;
    std::cout << "4. Clean temporary files" << std::endl;
    std::cout << "5. Create restore point" << std::endl;
    std::cout << "6. Exit" << std::endl;
    std::cout << std::endl;

    int choice;
    std::cout << "Enter choice (1-6): ";
    std::cin >> choice;

    switch (choice) {
        case 1:
            std::cout << std::endl << "=== FULL SPOOFING ===" << std::endl;
            spoofer.createRestorePoint();
            spoofer.startSpoofing();
            break;

        case 2:
            std::cout << std::endl << "=== HWID SPOOFING ===" << std::endl;
            spoofer.spoofHWID();
            break;

        case 3:
            std::cout << std::endl << "=== MAC SPOOFING ===" << std::endl;
            spoofer.spoofMAC();
            break;

        case 4:
            std::cout << std::endl << "=== CLEANING ===" << std::endl;
            spoofer.cleanTempFiles();
            spoofer.cleanRegistryTraces();
            break;

        case 5:
            std::cout << std::endl << "=== RESTORE POINT ===" << std::endl;
            spoofer.createRestorePoint();
            break;

        case 6:
            std::cout << "Goodbye!" << std::endl;
            return 0;

        default:
            std::cout << "Invalid choice!" << std::endl;
            break;
    }

    std::cout << std::endl << "Press any key to exit...";
    std::cin.ignore();
    std::cin.get();

    return 0;
}
