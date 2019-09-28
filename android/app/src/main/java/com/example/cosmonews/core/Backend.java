package com.example.cosmonews.core;

import java.util.Collections;
import java.util.LinkedList;
import java.util.Queue;

public class Backend {

    private static Backend instance = null;

    private Backend() {}

    public static Backend getInstance() {
        if (instance == null)
            instance = new Backend();

        return instance;
    }

    // server communication
    public Queue<Post> getNewPosts() {
        Post mockPost = Post.getMockPost();
        LinkedList<Post> list = new LinkedList<>();
        list.add(mockPost);
        list.add(mockPost);
        list.add(mockPost);
        return list;
    }
}
