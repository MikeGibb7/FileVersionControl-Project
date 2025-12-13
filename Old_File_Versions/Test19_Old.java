package org.example.config;

import java.util.ArrayList;

public class SettingsManager {

    private ArrayList<String> settings;
    private int version;
    private boolean active;

    public SettingsManager() {
        settings = new ArrayList<>();
        version = 1;
        active = true;
    }

    public void addSetting(String s) {
        settings.add(s);
    }

    public void removeSetting(String s) {
        settings.remove(s);
    }

    public boolean hasSetting(String s) {
        return settings.contains(s);
    }

    public void activate() {
        active = true;
    }

    public void deactivate() {
        active = false;
    }

    public int getVersion() {
        return version;
    }

    public void printSettings() {
        System.out.println("Settings (" + settings.size() + "):");
        for (String s : settings) {
            System.out.println("  " + s);
        }
    }

    public void clearSettings() {
        settings.clear();
    }

    public String getSetting(int index) {
        if (index >= 0 && index < settings.size()) {
            return settings.get(index);
        }
        return null;
    }

    public void reorderSettings() {
        // Placeholder
    }

    public void logSettings() {
        for (String s : settings) {
            System.out.println("LOG: " + s);
        }
    }

    public void legacyMethod() {
        System.out.println("Legacy method, will be removed soon.");
    }

    public static void main(String[] args) {
        SettingsManager sm = new SettingsManager();
        sm.addSetting("configA");
        sm.addSetting("configB");
        sm.addSetting("configC");
        sm.printSettings();
    }
}