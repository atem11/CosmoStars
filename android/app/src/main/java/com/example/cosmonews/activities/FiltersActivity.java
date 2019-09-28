package com.example.cosmonews.activities;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.InputType;
import android.text.TextWatcher;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import com.example.cosmonews.R;
import com.example.cosmonews.core.CachedPosts;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class FiltersActivity extends AppCompatActivity {
    private enum TimeBorder {
        oneDay, threeDays, week, month
    }
    private TimeBorder currentTime;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_filters);

        currentTime = TimeBorder.oneDay;


        Button addCeleb = findViewById(R.id.addCeleb);
        final Context thisActivity = this;

        addCeleb.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final AlertDialog.Builder builder;
                builder = new AlertDialog.Builder(thisActivity);
                builder.setTitle("Введите имя знаменитости");
                final Map<String, String> uniques = CachedPosts.getInstance().getAllCelebNames();
                List<String> celebNames = new ArrayList<>(uniques.keySet());
                String[] allCelebs = new String[celebNames.size()];
                for (int i = 0; i < allCelebs.length; i++) {
                    allCelebs[i] = celebNames.get(i);
                }

                // Set up the input
                final AutoCompleteTextView input = new AutoCompleteTextView(thisActivity);
                ArrayAdapter<String> adapter = new ArrayAdapter<>
                        (thisActivity, android.R.layout.select_dialog_item, allCelebs);
                input.setAdapter(adapter);

                // Specify the type of input expected; this, for example, sets the input as a password, and will mask the text
                input.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
                builder.setView(input);

                // Set up the buttons
                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String enteredText = input.getText().toString();
                        if (uniques.containsKey(enteredText)) {
                            // добавить в флекс layout
                        }
                    }
                });
                builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });

                final AlertDialog dialog = builder.create();
                dialog.show();
                dialog.getButton(AlertDialog.BUTTON_POSITIVE).setEnabled(false);
                input.addTextChangedListener(new TextWatcher() {

                    @Override
                    public void beforeTextChanged(CharSequence s, int start, int count, int after) {

                    }

                    @Override
                    public void onTextChanged(CharSequence s, int start, int before, int count) {

                    }

                    @Override
                    public void afterTextChanged(Editable s) {
                        if (uniques.containsKey(s.toString())) {
                            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setEnabled(true);
                        }
                    }
                });
            }
        });
    }

    public void openFavList(View view) {
        Intent intent = new Intent(this, ListActivity.class);
        startActivity(intent);
    }
}
