package com.example.matias.myapplication;

import android.app.Activity;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.widget.TextView;

public class CandidateDetailActivity extends Activity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        Bundle bundle = getIntent().getBundleExtra("candidateBundle");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.candidate_info);
        ((TextView) findViewById(R.id.candidateName)).setText((CharSequence) bundle.get("name"));
    }
}
