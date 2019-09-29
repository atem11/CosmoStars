package com.example.cosmonews.activities;

import android.os.Bundle;
import android.widget.ListAdapter;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.cosmonews.R;
import com.example.cosmonews.core.CachedPosts;
import com.example.cosmonews.core.Post;

import java.util.List;

public class ListActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list);

        ListView favList = findViewById(R.id.list_view);
        List<Post> liked = CachedPosts.getInstance().getLikedPosts();
        ListAdapter customAdapter = new PostCellAdapter(liked, this);
        favList.setAdapter(customAdapter);

    }

}
