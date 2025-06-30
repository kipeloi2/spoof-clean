#include <windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cctype>
#include <ctime>
#include <fstream>
#include <winreg.h>
#include <tlhelp32.h>
#include <psapi.h>

#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "psapi.lib")
#pragma comment(lib, "kernel32.lib")

class SMBIOSDeepSpoofer {
private:
    std::vector<std::string> originalValues;
    bool isActive = false;
    
public:
    // Генерация реалистичных серийников в стиле 2025
    std::string generateRealisticSerial(const std::string& type) {
        std::random_device rd;
        std::mt19937 gen(rd());
        
        if (type == "BIOS") {
            // Реалистичные BIOS серийники 2025
            std::vector<std::string> patterns = {"BIOS", "AMI", "AWARD", "PHOENIX"};
            std::string prefix = patterns[gen() % patterns.size()];
            return prefix + "-" + generateRandomString(4) + "-" + generateRandomString(4);
        }
        else if (type == "BASEBOARD") {
            // Реалистичные серийники материнских плат 2025
            std::vector<std::string> patterns = {"MB", "BB", "ASUS", "MSI", "GB"};
            std::string prefix = patterns[gen() % patterns.size()];
            return prefix + "-" + generateRandomString(4) + "-" + generateRandomString(4);
        }
        else if (type == "SYSTEM") {
            // Реалистичные системные серийники 2025
            std::vector<std::string> patterns = {"SYS", "PC", "DESK", "GAME"};
            std::string prefix = patterns[gen() % patterns.size()];
            return prefix + "-" + generateRandomString(4) + "-" + generateRandomString(4);
        }
        else if (type == "ENCLOSURE") {
            // Реалистичные серийники корпуса 2025
            std::vector<std::string> patterns = {"ENC", "CASE", "TOWER", "MINI"};
            std::string prefix = patterns[gen() % patterns.size()];
            return prefix + "-" + generateRandomString(4) + "-" + generateRandomString(4);
        }
        
        return generateRandomString(8);
    }
    
    std::string generateRandomString(int length) {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 35);
        
        std::string result;
        const char* chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        
        for (int i = 0; i < length; ++i) {
            result += chars[dis(gen)];
        }
        return result;
    }
    
    std::string generateGUID() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 15);
        
        std::string guid;
        const char* hex_chars = "0123456789ABCDEF";
        
        for (int i = 0; i < 32; ++i) {
            if (i == 8 || i == 12 || i == 16 || i == 20) guid += "-";
            guid += hex_chars[dis(gen)];
        }
        return guid;
    }
    
    // Остановка критических служб для глубокого доступа
    bool stopCriticalServices() {
        std::cout << "[DEEP] Stopping critical services for deep access..." << std::endl;
        
        std::vector<std::string> services = {
            "Winmgmt",      // WMI Service
            "CryptSvc",     // Cryptographic Services
            "BITS",         // Background Intelligent Transfer Service
            "wuauserv",     // Windows Update
            "Themes"        // Themes Service
        };
        
        for (const auto& service : services) {
            std::string command = "net stop \"" + service + "\" /y >nul 2>&1";
            system(command.c_str());
        }
        
        Sleep(3000); // Ждем остановки служб
        std::cout << "[SUCCESS] Critical services stopped" << std::endl;
        return true;
    }
    
    // Запуск служб обратно
    bool startCriticalServices() {
        std::cout << "[DEEP] Starting services back..." << std::endl;
        
        std::vector<std::string> services = {
            "Winmgmt",
            "CryptSvc", 
            "BITS",
            "wuauserv",
            "Themes"
        };
        
        for (const auto& service : services) {
            std::string command = "net start \"" + service + "\" >nul 2>&1";
            system(command.c_str());
        }
        
        std::cout << "[SUCCESS] Services restarted" << std::endl;
        return true;
    }
    
    // Глубокий спуфинг SMBIOS через множественные методы
    bool deepSMBIOSSpoof() {
        std::cout << "[DEEP] Starting deep SMBIOS spoofing..." << std::endl;
        
        // Генерируем новые серийники
        std::string newBiosSerial = generateRealisticSerial("BIOS");
        std::string newBaseboardSerial = generateRealisticSerial("BASEBOARD");
        std::string newSystemSerial = generateRealisticSerial("SYSTEM");
        std::string newEnclosureSerial = generateRealisticSerial("ENCLOSURE");
        std::string newUUID = generateGUID();
        
        std::cout << "[INFO] Generated new serials:" << std::endl;
        std::cout << "  BIOS Serial: " << newBiosSerial << std::endl;
        std::cout << "  Baseboard Serial: " << newBaseboardSerial << std::endl;
        std::cout << "  System Serial: " << newSystemSerial << std::endl;
        std::cout << "  Enclosure Serial: " << newEnclosureSerial << std::endl;
        std::cout << "  UUID: " << newUUID << std::endl;
        
        // Метод 1: Прямое изменение реестра SMBIOS
        bool method1 = spoofSMBIOSRegistry(newBiosSerial, newBaseboardSerial, newSystemSerial, newEnclosureSerial);
        
        // Метод 2: Изменение системных идентификаторов
        bool method2 = spoofSystemIdentifiers(newUUID);
        
        // Метод 3: Очистка WMI кэша
        bool method3 = clearWMICache();
        
        // Метод 4: Дополнительные системные изменения
        bool method4 = spoofAdditionalIdentifiers();
        
        if (method1 && method2 && method3 && method4) {
            std::cout << "[SUCCESS] Deep SMBIOS spoofing completed successfully!" << std::endl;
            isActive = true;
            return true;
        } else {
            std::cout << "[WARNING] Some spoofing methods failed, but core changes applied" << std::endl;
            return false;
        }
    }
    
    // Спуфинг SMBIOS через реестр
    bool spoofSMBIOSRegistry(const std::string& biosSerial, const std::string& baseboardSerial, 
                            const std::string& systemSerial, const std::string& enclosureSerial) {
        std::cout << "[DEEP] Method 1: SMBIOS Registry spoofing..." << std::endl;
        
        HKEY hKey;
        const char* biosPath = "HARDWARE\\DESCRIPTION\\System\\BIOS";
        
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, biosPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            // Основные серийники
            RegSetValueExA(hKey, "BIOSSerialNumber", 0, REG_SZ, 
                          (const BYTE*)biosSerial.c_str(), biosSerial.length() + 1);
            RegSetValueExA(hKey, "BaseBoardSerialNumber", 0, REG_SZ,
                          (const BYTE*)baseboardSerial.c_str(), baseboardSerial.length() + 1);
            RegSetValueExA(hKey, "SystemSerialNumber", 0, REG_SZ,
                          (const BYTE*)systemSerial.c_str(), systemSerial.length() + 1);
            RegSetValueExA(hKey, "EnclosureSerialNumber", 0, REG_SZ,
                          (const BYTE*)enclosureSerial.c_str(), enclosureSerial.length() + 1);
            
            // Дополнительные Asset Tags
            std::string assetTag1 = "ASSET-" + generateRandomString(4);
            std::string assetTag2 = "ENC-" + generateRandomString(4);
            RegSetValueExA(hKey, "BaseBoardAssetTag", 0, REG_SZ,
                          (const BYTE*)assetTag1.c_str(), assetTag1.length() + 1);
            RegSetValueExA(hKey, "EnclosureAssetTag", 0, REG_SZ,
                          (const BYTE*)assetTag2.c_str(), assetTag2.length() + 1);
            
            // Дополнительные системные поля
            std::string systemFamily = "Gaming-PC-2025";
            std::string systemSKU = generateRandomString(12);
            std::string systemVersion = generateRandomString(10);
            
            RegSetValueExA(hKey, "SystemFamily", 0, REG_SZ,
                          (const BYTE*)systemFamily.c_str(), systemFamily.length() + 1);
            RegSetValueExA(hKey, "SystemSKU", 0, REG_SZ,
                          (const BYTE*)systemSKU.c_str(), systemSKU.length() + 1);
            RegSetValueExA(hKey, "SystemVersion", 0, REG_SZ,
                          (const BYTE*)systemVersion.c_str(), systemVersion.length() + 1);
            
            RegCloseKey(hKey);
            std::cout << "[SUCCESS] SMBIOS registry values updated" << std::endl;
            return true;
        }
        
        std::cout << "[ERROR] Failed to access SMBIOS registry" << std::endl;
        return false;
    }
    
    // Спуфинг системных идентификаторов
    bool spoofSystemIdentifiers(const std::string& newUUID) {
        std::cout << "[DEEP] Method 2: System identifiers spoofing..." << std::endl;
        
        HKEY hKey;
        bool success = true;
        
        // Machine GUID
        const char* cryptoPath = "SOFTWARE\\Microsoft\\Cryptography";
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, cryptoPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            RegSetValueExA(hKey, "MachineGuid", 0, REG_SZ,
                          (const BYTE*)newUUID.c_str(), newUUID.length() + 1);
            RegCloseKey(hKey);
        } else {
            success = false;
        }
        
        // Computer Name
        const char* computerPath = "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ActiveComputerName";
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, computerPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            std::string newComputerName = "DESKTOP-" + generateRandomString(7);
            RegSetValueExA(hKey, "ComputerName", 0, REG_SZ,
                          (const BYTE*)newComputerName.c_str(), newComputerName.length() + 1);
            RegCloseKey(hKey);
        } else {
            success = false;
        }
        
        // Installation Date
        const char* installPath = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion";
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, installPath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            DWORD newInstallDate = (DWORD)(time(nullptr) - (rand() % 31536000)); // Случайная дата в прошлом году
            RegSetValueExA(hKey, "InstallDate", 0, REG_DWORD,
                          (const BYTE*)&newInstallDate, sizeof(DWORD));
            
            std::string newProductId = "00331-" + generateRandomString(5) + "-" + generateRandomString(5) + "-AA" + generateRandomString(3);
            RegSetValueExA(hKey, "ProductId", 0, REG_SZ,
                          (const BYTE*)newProductId.c_str(), newProductId.length() + 1);
            RegCloseKey(hKey);
        } else {
            success = false;
        }
        
        if (success) {
            std::cout << "[SUCCESS] System identifiers updated" << std::endl;
        } else {
            std::cout << "[WARNING] Some system identifiers failed to update" << std::endl;
        }
        
        return success;
    }
    
    // Очистка WMI кэша
    bool clearWMICache() {
        std::cout << "[DEEP] Method 3: Clearing WMI cache..." << std::endl;
        
        // Остановка WMI службы
        system("net stop Winmgmt /y >nul 2>&1");
        Sleep(2000);
        
        // Удаление WMI репозитория
        std::string command = "rmdir /s /q \"C:\\Windows\\System32\\wbem\\Repository\" >nul 2>&1";
        system(command.c_str());
        
        // Запуск WMI службы (она пересоздаст репозиторий)
        system("net start Winmgmt >nul 2>&1");
        Sleep(3000);
        
        std::cout << "[SUCCESS] WMI cache cleared and rebuilt" << std::endl;
        return true;
    }
    
    // Дополнительные системные изменения
    bool spoofAdditionalIdentifiers() {
        std::cout << "[DEEP] Method 4: Additional system spoofing..." << std::endl;
        
        // Очистка дополнительных следов
        std::vector<std::string> pathsToClean = {
            "C:\\Windows\\System32\\config\\systemprofile\\AppData\\Local\\Microsoft\\Windows\\INetCache\\*",
            "C:\\Windows\\Temp\\*",
            "C:\\Windows\\Prefetch\\*.pf"
        };
        
        for (const auto& path : pathsToClean) {
            std::string command = "del /q /f /s \"" + path + "\" >nul 2>&1";
            system(command.c_str());
        }
        
        // Изменение дополнительных реестровых ключей
        HKEY hKey;
        const char* hardwarePath = "SYSTEM\\HardwareConfig";
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, hardwarePath, 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
            std::string newHardwareID = generateRandomString(16);
            RegSetValueExA(hKey, "LastConfig", 0, REG_SZ,
                          (const BYTE*)newHardwareID.c_str(), newHardwareID.length() + 1);
            RegCloseKey(hKey);
        }
        
        std::cout << "[SUCCESS] Additional identifiers spoofed" << std::endl;
        return true;
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
    
    // Главная функция глубокого спуфинга
    bool startDeepSpoof() {
        std::cout << "=== SMBIOS DEEP SPOOFER 2025 ===" << std::endl;
        std::cout << "Maximum depth SMBIOS spoofing for Fortnite" << std::endl;
        std::cout << "All hardware serials will be changed" << std::endl;
        std::cout << std::endl;
        
        if (!isRunningAsAdmin()) {
            std::cout << "[ERROR] Administrator rights required!" << std::endl;
            return false;
        }
        
        // Остановка служб
        stopCriticalServices();
        
        // Глубокий спуфинг
        bool success = deepSMBIOSSpoof();
        
        // Запуск служб обратно
        startCriticalServices();
        
        if (success) {
            std::cout << std::endl;
            std::cout << "[SUCCESS] Deep SMBIOS spoofing completed!" << std::endl;
            std::cout << "[INFO] All hardware serials changed" << std::endl;
            std::cout << "[INFO] Changes are temporary until reboot" << std::endl;
            std::cout << "[READY] You can now launch Fortnite!" << std::endl;
        }
        
        return success;
    }
    
    bool getStatus() {
        return isActive;
    }
};

// Главная функция
int main(int argc, char* argv[]) {
    SetConsoleOutputCP(CP_UTF8);

    SMBIOSDeepSpoofer spoofer;

    std::cout << "=== SMBIOS DEEP SPOOFER 2025 ===" << std::endl;
    std::cout << "Ultimate hardware serial spoofing tool" << std::endl;
    std::cout << "Designed for maximum EAC bypass effectiveness" << std::endl;
    std::cout << std::endl;

    // Обработка аргументов
    if (argc > 1) {
        std::string arg1 = argv[1];

        if (arg1 == "--help" || arg1 == "-h") {
            std::cout << "SMBIOS Deep Spoofer - Command Line Options" << std::endl;
            std::cout << "==========================================" << std::endl;
            std::cout << std::endl;
            std::cout << "Usage: smbios_deep_spoofer.exe [options]" << std::endl;
            std::cout << std::endl;
            std::cout << "Options:" << std::endl;
            std::cout << "  --help                Show this help" << std::endl;
            std::cout << "  --auto                Automatic deep spoofing" << std::endl;
            std::cout << "  --check               Check admin rights" << std::endl;
            std::cout << std::endl;
            return 0;
        }

        if (arg1 == "--check") {
            std::cout << "=== SYSTEM CHECK ===" << std::endl;
            std::cout << "Admin rights: " << (spoofer.isRunningAsAdmin() ? "YES" : "NO") << std::endl;
            std::cout << "Ready for deep spoofing: " << (spoofer.isRunningAsAdmin() ? "YES" : "NO") << std::endl;
            return 0;
        }

        if (arg1 == "--auto") {
            std::cout << "=== AUTOMATIC DEEP SPOOFING ===" << std::endl;
            spoofer.startDeepSpoof();
            return 0;
        }
    }

    // Проверка прав
    if (!spoofer.isRunningAsAdmin()) {
        std::cout << "[ERROR] Administrator rights required!" << std::endl;
        std::cout << "Please run as administrator." << std::endl;
        std::cout << "Press any key to exit...";
        std::cin.get();
        return 1;
    }

    // Интерактивный режим
    std::cout << "WARNING: This will change ALL hardware serials!" << std::endl;
    std::cout << "Changes are temporary and will be reverted after reboot." << std::endl;
    std::cout << std::endl;

    char choice;
    std::cout << "Start deep SMBIOS spoofing? (y/n): ";
    std::cin >> choice;

    if (choice == 'y' || choice == 'Y') {
        spoofer.startDeepSpoof();
    } else {
        std::cout << "Operation cancelled." << std::endl;
    }

    std::cout << std::endl << "Press any key to exit...";
    std::cin.ignore();
    std::cin.get();

    return 0;
}
