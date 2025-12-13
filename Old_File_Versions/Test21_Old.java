package com.example.config;

import java.util.ArrayList;
import java.util.List;

/**
 * Manages application settings and configurations.
 */
public class SettingsManager {

    private List<String> settings;
    private boolean isLoaded;

    public SettingsManager() {
        settings = new ArrayList<>();
        isLoaded = false;
    }

    public void loadDefaults() {
        settings.clear();
        settings.add("theme=light");
        settings.add("notifications=enabled");
        settings.add("autosave=on");
        isLoaded = true;
    }

    public void printSettings() {
        for (String s : settings) {
            System.out.println(s);
        }
    }

    public void reloadSettings() {
        clearSettings();
        loadDefaults();
    }

    public boolean isLoaded() {
        return isLoaded;
    }

    public void markLoaded(boolean loaded) {
        this.isLoaded = loaded;
    }

    // Additional utility methods
    public int countSettings() {
        return settings.size();
    }

    public String getSettingAt(int index) {
        if (index < 0 || index >= settings.size()) return null;
        return settings.get(index);
    }

      public boolean addSetting(String setting) {
        if (!settings.contains(setting)) {
            settings.add(setting);
            return true;
        }
        return false;
    }

    public boolean removeSetting(String setting) {
        return settings.remove(setting);
    }

    public boolean containsSetting(String setting) {
        return settings.contains(setting);
    }

    public void clearSettings() {
        settings.clear();
    }

    public List<String> getSettings() {
        return new ArrayList<>(settings);
    }

}
