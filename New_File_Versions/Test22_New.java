package org.example.config;

import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

public class ConfigManager {

    private Map<String, String> settings;
    private List<String> logs;

    public ConfigManager() {
        settings = new HashMap<>();
        logs = new ArrayList<>();
    }

    public void addSetting(String key, String value) {
        settings.put(key, value);
        logs.add("Added setting: " + key);
    }

    public String getSetting(String key) {
        return settings.get(key);
    }

    public void removeSetting(String key) {
        settings.remove(key);
        logs.add("Removed setting: " + key);
    }

    public void printAllSettings() {
        for (String key : settings.keySet()) {
            System.out.println(key + ": " + settings.get(key));
        }
    }

    public void clearSettings() {
        settings.clear();
        logs.add("Cleared all settings");
    }

    public void addLog(String message) {
        logs.add(message);
    }

    public void backupSettings() {
        System.out.println("Backup started");
        for (String key : settings.keySet()) {
            System.out.println("Backing up: " + key);
        }
    }

    public void importSettings(List<String> externalSettings) {
        for (String s : externalSettings) {
            String[] kv = s.split("=");
            if (kv.length == 2) {
                settings.put(kv[0], kv[1]);
            }
        }
    }

    public void restoreSettings() {
        System.out.println("Restore started");
    }

    public static void main(String[] args) {
        ConfigManager cm = new ConfigManager();
        cm.printAllSettings();
        cm.backupSettings();
    }
}