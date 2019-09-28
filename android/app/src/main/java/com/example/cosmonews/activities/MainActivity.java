package com.example.cosmonews.activities;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.bumptech.glide.Glide;
import com.example.cosmonews.R;
import com.example.cosmonews.core.Backend;
import com.example.cosmonews.core.CachedPosts;
import com.example.cosmonews.core.Post;

public class MainActivity extends AppCompatActivity {
    private final String listPrefix = "Просмотр списка: ";
    private CachedPosts cache;
    private Backend server;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        server = Backend.getInstance();
        cache = CachedPosts.getInstance();
        updatePost();
    }


    private void updatePost() {
        final Post currentPost = cache.getCurrentPost();
        TextView celebName = findViewById(R.id.celebName);
        celebName.setText(currentPost.getCelebName());

        String imageUrl = currentPost.getPath2Avatar();
        ImageView celebAvatar = findViewById(R.id.celebrityAvatar);
        Glide.with(this).load(imageUrl).into(celebAvatar);

        TextView date = findViewById(R.id.date);
        date.setText(currentPost.getPostedTime());

        TextView mainText = findViewById(R.id.mainText);
        mainText.setText(currentPost.getText());

        ImageView sourcePic = findViewById(R.id.sourcePic);
        currentPost.setSourceImage(sourcePic);

        int newSize = cache.getLikedPosts().size();
        Button listLen = findViewById(R.id.favListView);
        listLen.setText(listPrefix + newSize);
    }

    public void openFavList(View view) {
        Intent intent = new Intent(this, ListActivity.class);
        startActivity(intent);
    }

    public void openFilters(View view) {
        Intent intent = new Intent(this, FiltersActivity.class);
        startActivity(intent);
    }

    public void openUrl(View view) {
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setData(Uri.parse(cache.getUrl2Profile()));
        startActivity(intent);
    }

    public void likePost(View view) {
        //Log.d("DEBUGGGGGGGGG", "Post liked");
        cache.like();
        updatePost();
    }

    public void dislikePost(View view) {
        cache.dislike();
        updatePost();
    }
}
