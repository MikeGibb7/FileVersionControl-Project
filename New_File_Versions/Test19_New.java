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

    public void activate() { // moved
        active = true;
    }

    public void deactivate() { // moved
        active = false;
    }

    public boolean hasSetting(String s) { // moved
        return settings.contains(s);
    }

    public void printSettings() { // moved
        System.out.println("Settings (" + settings.size() + "):");
        for (String s : settings) {
            System.out.println("  " + s);
        }
    }

    public int getVersion() { // moved
        return version;
    }

    public void clearSettings() { // moved
        settings.clear();
    }

    public String getSetting(int index) { // moved
        if (index >= 0 && index < settings.size()) {
            return settings.get(index);
        }
        return null;
    }

    public void reorderSettings() { // removed
        // Placeholder
    }

    public void logSettings() { // removed
        for (String s : settings) {
            System.out.println("LOG: " + s);
        }
    }

    public void legacyMethod() { // removed
        System.out.println("Legacy method, will be removed soon.");
    }

    public void bulkAdd(ArrayList<String> newSettings) { // added
        settings.addAll(newSettings);
    }

    public void removeMatchingPrefix(String prefix) { // added
        settings.removeIf(s -> s.startsWith(prefix));
    }

    public void deactivateIfEmpty() { // added
        if (settings.isEmpty()) {
            deactivate();
        }
    }

    public static void main(String[] args) {
        SettingsManager sm = new SettingsManager();
        sm.addSetting("configA");
        sm.addSetting("configB");
        sm.addSetting("configC");
        sm.printSettings();
    }
}