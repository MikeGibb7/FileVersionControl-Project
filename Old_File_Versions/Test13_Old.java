package com.example.data;

import java.util.ArrayList;
import java.util.List;

public class UserCache {

    private List<String> users;
    private boolean active;

    public UserCache() {
        users = new ArrayList<>();
        active = true;
    }

    public void add(String name) {
        if (active) {
            users.add(name);
        }
    }

    public boolean remove(String name) {
        return users.remove(name);
    }

    public boolean contains(String name) {
        return users.contains(name);
    }

    public List<String> getAll() {
        return users;
    }

    public int count() {
        return users.size();
    }

    public void deactivate() {
        active = false;
    }

    public void activate() {
        active = true;
    }

    public boolean isActive() {
        return active;
    }

    public void replaceAll(List<String> list) {
        users.clear();
        users.addAll(list);
    }

    public String findLongest() {
        String longest = "";
        for (String s : users) {
            if (s.length() > longest.length()) {
                longest = s;
            }
        }
        return longest;
    }
}
