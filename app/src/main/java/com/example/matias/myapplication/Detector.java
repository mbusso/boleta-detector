package com.example.matias.myapplication;

import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;


/**
 * Created by matias on 06/05/17.
 */

public class Detector {

    public static final int        JAVA_DETECTOR       = 0;
    private static int count = 0;
    private static Rect[] resultsAux = new Rect[]{};
    private static JSONArray source;
    private final MainActivity activity;
    private List <CascadeClassifier> classifiers;
    private static final String    TAG                 = "Detector";

    public Detector(MainActivity mainActivity) {
        this.activity = mainActivity;
        this.classifiers =  new ArrayList<CascadeClassifier>();
    }


    public void loadClassifiers() {
        this.classifiers.add(this.create(activity.getResources(), activity.getCascadeDirectory(), TAG, R.raw.autodeterminacion_classifier, "autodeterminacion_classifier_classifier.xml" ));
        this.classifiers.add(this.create(activity.getResources(), activity.getCascadeDirectory(), TAG, R.raw.ari_classifier, "ari_classifier.xml"));
    }


    private CascadeClassifier create(Resources resources, File directory, String TAG, int raw_banana_classifier, String filename) {
        try {
            // load cascade file from application resources
            source = loadDataSource(resources);
            InputStream is = resources.openRawResource(raw_banana_classifier);
            File cascadeDir = directory;
            File mCascadeFile = new File(cascadeDir, filename);
            FileOutputStream os = new FileOutputStream(mCascadeFile);

            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            is.close();
            os.close();
            CascadeClassifier mJavaDetector = new CascadeClassifier(mCascadeFile.getAbsolutePath());
            if (mJavaDetector.empty()) {
                Log.e(TAG, "Failed to load cascade classifier");
                mJavaDetector = null;
            } else
                Log.i(TAG, "Loaded cascade classifier from " + mCascadeFile.getAbsolutePath());
            cascadeDir.delete();
            return mJavaDetector;
        } catch (IOException e) {
            e.printStackTrace();
            Log.e(TAG, "Failed to load cascade. Exception thrown: " + e);
        }
        return null;
    }

    private static JSONArray loadDataSource(Resources resources) {
        InputStream is = resources.openRawResource(R.raw.boleta_source);
        int size = 0;
        try {
            size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            return new JSONArray(new String(buffer, "UTF-8"));
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void detectBoletas(final Mat mGray, Mat mRgba, final int mAbsoluteFaceSize) {
            if (classifiers != null) {
                for (CascadeClassifier classifier : classifiers) {
                    displayResults(detect(classifier, mGray, mAbsoluteFaceSize));
                }
            }
    }

    private MatOfRect detect(CascadeClassifier classifier, Mat mGray, int mAbsoluteFaceSize) {
        MatOfRect results = new MatOfRect();
        double scaleFactor = 1.1;
        int minNeighbors = 2;
        int flag = 0;
        classifier.detectMultiScale(mGray, results, scaleFactor, minNeighbors, flag, new Size(mAbsoluteFaceSize, mAbsoluteFaceSize), new Size());
        return results;
    }

    private void displayResults(MatOfRect faces) {
        final Scalar FACE_RECT_COLOR     = new Scalar(0, 255, 0, 255);
        Rect[] facesArray = faces.toArray();
        if(facesArray.length >0) {
            try {
                this.activity.displayList(source.getJSONObject(0).getJSONArray("candidatos"));
            } catch (JSONException e) {
                e.printStackTrace();
            }
            resultsAux = facesArray.clone();
            count = 0;
        }
        else {
            if (count <= 30 ) {
                count ++;
            } else {
                resultsAux = new Rect[]{};
                count = 0;
                //mainActivity.hideList();
            }
        }
    }


}
