#ifndef SPOOFER_H
#define SPOOFER_H

#include <windows.h>
#include <string>
#include <vector>

// Константы для спуфинга
#define SPOOFER_VERSION "2.0"
#define MAX_HWID_LENGTH 64
#define MAX_MAC_LENGTH 18

// Структуры данных
struct SpoofProfile {
    std::string name;
    std::string hwid;
    std::string mac;
    std::string diskSerial;
    bool enabled;
};

struct SystemInfo {
    std::string originalHWID;
    std::string originalMAC;
    std::string originalDiskSerial;
    std::string currentHWID;
    std::string currentMAC;
    std::string currentDiskSerial;
};

// Класс для работы с реестром
class RegistryManager {
public:
    static bool setRegistryValue(HKEY hKey, const std::string& subKey, 
                                const std::string& valueName, const std::string& value);
    static std::string getRegistryValue(HKEY hKey, const std::string& subKey, 
                                       const std::string& valueName);
    static bool deleteRegistryValue(HKEY hKey, const std::string& subKey, 
                                   const std::string& valueName);
};

// Класс для работы с сетевыми адаптерами
class NetworkManager {
public:
    static std::vector<std::string> getNetworkAdapters();
    static bool changeAdapterMAC(const std::string& adapterName, const std::string& newMAC);
    static std::string getCurrentMAC(const std::string& adapterName);
};

// Класс для работы с дисками
class DiskManager {
public:
    static std::vector<std::string> getDiskList();
    static bool changeDiskSerial(const std::string& diskName, const std::string& newSerial);
    static std::string getCurrentDiskSerial(const std::string& diskName);
};

// Утилиты
class Utils {
public:
    static std::string generateRandomString(int length);
    static std::string generateRandomHex(int length);
    static bool isValidMAC(const std::string& mac);
    static bool isValidHWID(const std::string& hwid);
    static std::string formatMAC(const std::string& mac);
    static void logMessage(const std::string& message);
    static bool isWindows11();
    static std::string getCurrentTimestamp();
};

// Класс для управления профилями
class ProfileManager {
public:
    static bool saveProfile(const SpoofProfile& profile);
    static SpoofProfile loadProfile(const std::string& name);
    static std::vector<std::string> getProfileList();
    static bool deleteProfile(const std::string& name);
};

// Основные функции спуфинга
namespace Spoof {
    bool spoofHardwareID(const std::string& newHWID = "");
    bool spoofMACAddress(const std::string& newMAC = "");
    bool spoofDiskSerial(const std::string& newSerial = "");
    bool spoofBIOSInfo();
    bool spoofSystemInfo();
    bool cleanRegistryTraces();
    bool cleanTempFiles();
    bool restoreOriginalValues();
    SystemInfo getCurrentSystemInfo();
}

// Функции безопасности
namespace Security {
    bool checkAdminRights();
    bool checkWindowsVersion();
    bool checkAntivirusStatus();
    bool createBackup();
    bool restoreBackup();
}

// Константы реестра
namespace Registry {
    const char* MACHINE_GUID_PATH = "SOFTWARE\\Microsoft\\Cryptography";
    const char* INSTALL_DATE_PATH = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion";
    const char* NETWORK_ADAPTERS_PATH = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}";
    const char* DISK_INFO_PATH = "HARDWARE\\DEVICEMAP\\Scsi";
    const char* BIOS_INFO_PATH = "HARDWARE\\DESCRIPTION\\System\\BIOS";
}

// Игровые профили
namespace GameProfiles {
    const SpoofProfile VALORANT_PROFILE = {
        "Valorant",
        "",
        "",
        "",
        true
    };
    
    const SpoofProfile FORTNITE_PROFILE = {
        "Fortnite",
        "",
        "",
        "",
        true
    };
    
    const SpoofProfile APEX_PROFILE = {
        "Apex Legends",
        "",
        "",
        "",
        true
    };
    
    const SpoofProfile WARZONE_PROFILE = {
        "Call of Duty Warzone",
        "",
        "",
        "",
        true
    };
}

#endif // SPOOFER_H
