package com.example.cosmonews.core;

import android.widget.ImageView;

import com.example.cosmonews.R;

import java.util.Date;

public class Post {
    private final String path2Avatar;
    private final String celebName;
    private final String url2Profile;
    private final String postedTime;
    private final String url2Post;
    private final Source postSource = Source.VK;
    private final String text;

    // TODO: init from server data
    private Post(String avatarUrl, String celebName, String profileUrl, String postUrl, String time, String text) {
        path2Avatar = avatarUrl;
        this.celebName = celebName;
        url2Profile = profileUrl;
        postedTime = time;
        this.url2Post = postUrl;
        this.text = text;
    }

    public String getUrl2Post() {
        return url2Post;
    }

    public static Post getMockPost() {
        String longText = "Москва! 14 Ноября \"Известия Холл\".Последний концерт Ольги Бузовой \"Под звуки поцелуев\" \uD83D\uDC8B\n" +
                "Билеты: https://www.concert.ru/Event?ActionID=89082\n" +
                "Официальная встреча ВКонтакте: vk.com/lastpzp ❤\n" +
                "\n" +
                "Санкт-Петербург! 20 Ноября. Клуб \"А2\".Последний концерт Ольги Бузовой \"Под звуки поцелуев\" \uD83D\uDC8B\n" +
                "Билеты: https://spb.kassir.ru/koncert/klub-a2-green-concert/p..\n" +
                "Официальная встреча ВКонтакте: https://vk.com/lastpzp_piter ❤";

        return new Post(
                "https://s9.stc.all.kpcdn.net/share/i/12/10274416/inx960x640.jpg",
                "Ольга Бузова",
                "https://vk.com/buzovaofficial",
                "https://vk.com/wall-4887563_331976",
                "18 сен в 16:33",
                longText
        );
    }

    public String getUrl2Profile() {
        return url2Profile;
    }

    public String getPath2Avatar() {
        return path2Avatar;
    }

    public String getCelebName() {
        return celebName;
    }

    public String getPostedTime() {
        return postedTime;
    }

    public void setSourceImage(ImageView view) {
        switch (postSource) {
            case VK:
                view.setImageResource(R.drawable.vk_logo);

            // case FB
            // case Instagram
        }
    }

    public String getText() {
        return text;
    }
}
