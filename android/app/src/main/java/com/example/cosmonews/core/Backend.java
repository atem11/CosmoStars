package com.example.cosmonews.core;

import android.os.AsyncTask;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Collections;
import java.util.Date;
import java.util.LinkedList;
import java.util.Queue;

import javax.net.ssl.HttpsURLConnection;

public class Backend {

    private static Backend instance = null;
    private static URL backendEndpoint;
    HttpsURLConnection myConnection;

    private Backend() {
        try {
            backendEndpoint = new URL("http://95.213.39.9:5000");
            myConnection = (HttpsURLConnection)backendEndpoint.openConnection();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

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

        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                myConnection.setRequestProperty("time_start", Long.toString(0));
                myConnection.setRequestProperty("time_end", Long.toString(new Date().getTime()));
            }
        });

        return list;
    }
}
