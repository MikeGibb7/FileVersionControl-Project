package com.example.tools;

import java.util.ArrayList;
import java.util.List;

public class LineManager {

    private List<String> lines;
    private boolean enabled;

    public LineManager() {
        lines = new ArrayList<>();
        enabled = true;
    }

    public void addLine(String s) {
        if (enabled) {
            lines.add(s);
        }
    }

    public void removeLine(String s) {
        lines.remove(s);
    }

    public List<String> getAll() {
        return lines;
    }

    public boolean contains(String s) {
        return lines.contains(s);
    }

    public int size() {
        return lines.size();
    }

    public void clear() {
        lines.clear();
    }

    public void disable() {
        enabled = false;
    }

    public void enable() {
        enabled = true;
    }

    public boolean isValid(String s) {                    
        if (s == null || s.isEmpty()) {                  
            return false;                                
        }                                                

        if (s.length() < 5) {
            return false;
        }

        if (s.contains("!")) {                           // NEW inserted check
            return false;
        }

        for (char c : s.toCharArray()) {
            if (!Character.isLetter(c)) {
                return false;
            }
        }

        return true;                                     // shifted down
    }

    public void printInfo() {
        System.out.println("Count = " + size());
    }
}
