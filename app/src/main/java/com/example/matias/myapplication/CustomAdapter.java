package com.example.matias.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

/**
 * Created by matias on 01/06/17.
 */

public class CustomAdapter extends BaseAdapter {

    private final String[] values;
    private final MainActivity activity;
    private final LayoutInflater inflater;

    public CustomAdapter(MainActivity mainActivity, String[] values) {
        super();
        this.activity = mainActivity;
        this.values = values;
        this.inflater = (LayoutInflater)this.activity.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }


    @Override
    public int getCount() {
        return values.length;
    }

    @Override
    public Object getItem(int position) {
        return values[position];
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View rowView;
        rowView = inflater.inflate(R.layout.row_list, null);
        ImageView image = (ImageView)rowView.findViewById(R.id.imageView1);
        TextView textView = (TextView) rowView.findViewById(R.id.textView1);
        textView.setText(values[position]);
        image.setImageBitmap(BitmapFactory.decodeResource(this.activity.getResources(),R.drawable.minionsmall));
        return rowView;
    }
}


