package com.example.cosmonews.core;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;

public class CachedPosts {
    private Post currentPost;
    private Queue<Post> cachedPosts;
    // make static?
    private final List<Post> likedPosts; // for list view
    private final List<Post> dislikedPosts; // history

    private static CachedPosts instance = null;

    public Post getCurrentPost() {
        return currentPost;
    }

    public Map<String, String> getAllCelebNames() {
        Map<String, String> uniques = new HashMap<>();
        for (Post post : cachedPosts) {
            uniques.put(post.getCelebName(), "");
        }

        return uniques;
    }

    private CachedPosts() {
        cachedPosts = new LinkedList<>();
        likedPosts = new LinkedList<>();
        dislikedPosts = new LinkedList<>();

        updatePosts();
    }

    public List<Post> getLikedPosts() {
        return likedPosts;
    }

    public static CachedPosts getInstance() {
        if (instance == null)
            instance = new CachedPosts();

        return instance;
    }

    public void updatePosts() {
        if (cachedPosts.size() == 0) {
            cachedPosts = Backend.getInstance().getNewPosts();
        }

        currentPost = cachedPosts.poll();
    }

    public void like() {
        likedPosts.add(currentPost);
        updatePosts();
    }

    public void dislike() {
        dislikedPosts.add(currentPost);
        updatePosts();
    }

    public String getUrl2Profile() {
        return currentPost.getUrl2Profile();
    }
}
