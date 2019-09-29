package com.example.cosmonews.activities;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Paint;
import android.net.Uri;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.example.cosmonews.R;
import com.example.cosmonews.core.Post;

import java.util.List;

import static androidx.core.content.ContextCompat.startActivity;

public class PostCellAdapter extends ArrayAdapter<Post>  {
    private Context context;
    private List<Post> items;

    public PostCellAdapter(List<Post> data, Context context) {
        super(context, R.layout.row_item, data);
        items = data;
        this.context = context;
    }

    public void openUrl(String url) {
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setData(Uri.parse(url));
        startActivity(context, intent, null);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View listItem = convertView;
        if (listItem == null) {
            listItem = LayoutInflater
                    .from(context)
                    .inflate(R.layout.row_item, parent, false);
        }

        final Post post = items.get(position);

        ImageView image = listItem.findViewById(R.id.itemCelebPic);
        String imageUrl = post.getPath2Avatar();
        //Log.d("DEBUGGGG", imageUrl);
        Glide.with(context).load(imageUrl).into(image);

        TextView name = listItem.findViewById(R.id.itemCelebName);
        name.setText(post.getCelebName());
        name.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openUrl(post.getUrl2Profile());
            }
        });
        name.setTextColor(Color.BLUE);
        name.setPaintFlags(name.getPaintFlags() | Paint.UNDERLINE_TEXT_FLAG);

        TextView link = listItem.findViewById(R.id.itemLink);
        link.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openUrl(post.getUrl2Post());
            }
        });
        link.setTextColor(Color.BLUE);
        link.setPaintFlags(link.getPaintFlags() | Paint.UNDERLINE_TEXT_FLAG);

        TextView date = listItem.findViewById(R.id.itemDate);
        date.setText(post.getPostedTime());

        ImageView sourcePic = listItem.findViewById(R.id.itemSourcePic);
        post.setSourceImage(sourcePic);

        return listItem;
    }
}
