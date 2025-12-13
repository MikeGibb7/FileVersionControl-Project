package com.example.config;

import java.util.ArrayList;
import java.util.List;
import java.util.Collections;

public class SettingsManager {

    private List<String> settings;
    private boolean initialized;

    public SettingsManager() {
        initialized = false;
        settings = new ArrayList<>();
    }

    public void initialize() {
        settings.add("theme:light");
        settings.add("language:en");
        settings.add("autosave:true");
        settings.add("notifications:on"); // new setting added
        initialized = true;
    }

    public boolean isInitialized() {
        return initialized;
    }

    public void addSetting(String setting) {
        if (!settings.contains(setting)) { // avoid duplicates
            settings.add(setting);
        }
    }

    public void removeSetting(String setting) {
        settings.remove(setting);
    }

    public String getSetting(int index) {
        if (index < settings.size()) {
            return settings.get(index);
        }
        return null;
    }

    public int count() {
        return settings.size();
    }

    public void reset() {
        settings.clear();
        initialized = false;
    }

    public void displaySettings() {
        for (String s : settings) {
            System.out.println(s);
        }
    }

    public void updateSetting(int index, String newSetting) {
        if (index < settings.size()) {
            settings.set(index, newSetting);
        }
    }

    public boolean containsSetting(String setting) {
        return settings.contains(setting);
    }

    public void duplicateSettings() {
        List<String> copy = new ArrayList<>(settings);
        settings.addAll(copy);
    }

    public void removeDuplicates() {
        List<String> unique = new ArrayList<>();
        for (String s : settings) {
            if (!unique.contains(s)) {
                unique.add(s);
            }
        }
        settings = unique;
    }
}
