package com.example.cosmonews.core;

import java.util.ArrayList;
import java.util.List;

// Singleton
public class Filters {
    private String time = null;
    private final List<String> celebrities;
    private final List<String> events;

    private static Filters instance = null;

    private Filters() {
        time = null;
        celebrities = new ArrayList();
        events = new ArrayList();
    }

    public static Filters getInstance() {
        if (instance == null)
            instance = new Filters();

        return instance;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public void addCelebrity(String celebrity) {
        this.celebrities.add(celebrity);
    }

    public void delCelebrity(String celebrity) {
        this.celebrities.remove(celebrity);
    }

    public void addEvent(String event) {
        this.events.add(event);
    }

    public void delEvent(String event) {
        this.events.remove(event);
    }

    public String getTime() {
        return time;
    }

    public List<String> getCelebrities() {
        return celebrities;
    }

    public List<String> getEvents() {
        return events;
    }
}
