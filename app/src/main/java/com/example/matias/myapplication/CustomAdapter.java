package com.example.matias.myapplication;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by matias on 01/06/17.
 */

public class CustomAdapter extends BaseAdapter {

    private final JSONArray values;
    private final MainActivity activity;
    private final LayoutInflater inflater;

    public CustomAdapter(MainActivity mainActivity, JSONArray values) {
        super();
        this.activity = mainActivity;
        this.values = values;
        this.inflater = (LayoutInflater)this.activity.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }


    @Override
    public int getCount() {
        return values.length();
    }

    @Override
    public Object getItem(int position) {
        try {
            return values.getJSONObject(position);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, final View convertView, ViewGroup parent) {
        JSONObject jsonObject = null;
        try {
            jsonObject = values.getJSONObject(position);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        View rowView;
        rowView = inflater.inflate(R.layout.row_list, null);
        ImageView image = (ImageView)rowView.findViewById(R.id.imageView1);
        final TextView textView = (TextView) rowView.findViewById(R.id.textView1);
        image.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent mainIntent = new Intent(v.getContext(), CandidateDetailActivity.class);
                Bundle bundle = new Bundle();
                bundle.putString("name", textView.getText().toString());
                mainIntent.putExtra("candidateBundle", bundle);
                activity.startActivity(mainIntent);

            }
        });
        try {
            textView.setText(jsonObject.getString("nombre"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        try {
            byte[] imgAsb64s = Base64.decode(jsonObject.getString("imgAsb64"), Base64.DEFAULT);
            image.setImageBitmap(BitmapFactory.decodeByteArray(imgAsb64s, 0, imgAsb64s.length));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return rowView;
    }
}


