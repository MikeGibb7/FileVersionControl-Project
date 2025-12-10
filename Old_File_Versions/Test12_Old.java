package com.example.editor;

import java.util.ArrayList;
import java.util.List;

public class TextBuffer {

    private List<String> buffer;
    private boolean locked;

    public TextBuffer() {
        buffer = new ArrayList<>();
        locked = false;
    }

    public void add(String s) {
        if (!locked) {
            buffer.add(s);
        }
    }

    public void remove(String s) {
        buffer.remove(s);
    }

    public void clear() {
        buffer.clear();
    }

    public int size() {
        return buffer.size();
    }

    public boolean contains(String s) {
        return buffer.contains(s);
    }

    public boolean isLocked() {
        return locked;
    }

    public void lock() {
        locked = true;
    }

    public void unlock() {
        locked = false;
    }

    public boolean validate(String s) {                     
        if (s == null) {                                   
            return false;                                  
        }                                                 
        if (s.length() == 0) {                             
            return false;                                  
        }                                                 
        if (s.length() > 50) {                           
            return false;                                 
        }                                                  
        for (char c : s.toCharArray()) {                  
            if (!Character.isLetterOrDigit(c)) {          
                return false;                             
            }                                             
        }                                                  
        return true;                                       
    }                                                      

    public void print() {
        System.out.println("Lines = " + buffer.size());    
    }                                                      
}                                                          
