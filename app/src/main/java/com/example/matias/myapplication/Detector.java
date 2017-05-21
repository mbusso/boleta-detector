package com.example.matias.myapplication;

import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.util.Log;

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
import java.util.List;


/**
 * Created by matias on 06/05/17.
 */

public class Detector {

    public static final int        JAVA_DETECTOR       = 0;
    private static int count = 0;
    private static Rect[] resultsAux = new Rect[]{};


    public static CascadeClassifier create(Resources resources, File directory, String TAG, int raw_banana_classifier, String filename) {
        try {
            // load cascade file from application resources
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

    public static void detect(String TAG, List<CascadeClassifier> classifiers, Mat mGray, Mat mRgba, int mAbsoluteFaceSize, Bitmap bMap) {
        MatOfRect faces1 = new MatOfRect();
        MatOfRect faces2 = new MatOfRect();

            if (classifiers != null) {
                double scaleFactor = 1.1;
                int minNeighbors = 2;
                int flag = 0;

                classifiers.get(0).detectMultiScale(mGray, faces1, scaleFactor, minNeighbors, flag, new Size(mAbsoluteFaceSize, mAbsoluteFaceSize), new Size());
                classifiers.get(1).detectMultiScale(mGray, faces2, scaleFactor, minNeighbors, flag, new Size(mAbsoluteFaceSize, mAbsoluteFaceSize), new Size());
            }

        bla(faces1, "zamora", new Point(100,100), mRgba, bMap);
        bla(faces2, "lilita", new Point(50, 50),mRgba, bMap);
    }

    private static void bla(MatOfRect faces, String label, Point point, Mat mRgba, Bitmap bMap) {
        final Scalar FACE_RECT_COLOR     = new Scalar(0, 255, 0, 255);
        Rect[] facesArray = faces.toArray();
        if(facesArray.length >0) {
            resultsAux = facesArray.clone();
            drawResults(facesArray, label, point, mRgba, bMap, FACE_RECT_COLOR);
            count = 0;
        }
        else {
            if (count <= 30 ) {
                drawResults(resultsAux, label, point, mRgba, bMap, FACE_RECT_COLOR);
                count ++;
            } else {
                resultsAux = new Rect[]{};
                count = 0;
            }
        }
    }

    private static void drawResults(Rect[] results, String label, Point point, Mat mRgba, Bitmap bMap, Scalar FACE_RECT_COLOR) {
        for (int i = 0; i < results.length; i++) {
            //Imgproc.rectangle(mRgba, rect.tl(), rect.br(), FACE_RECT_COLOR, 3);
            Imgproc.putText(mRgba, label, point, Core.FONT_ITALIC, 1.0, FACE_RECT_COLOR);
            displayImage(mRgba, bMap);
        }
    }

    private static void displayImage(Mat mRgba, Bitmap bMap) {
        Mat bitmapMat = new Mat();
        Utils.bitmapToMat(bMap, bitmapMat);
        bitmapMat.copyTo(mRgba.submat(0, bMap.getHeight(), 0, bMap.getWidth()));
    }

    public static void deliverTouchEvent(Mat mRgba, float x, float y) {
        Imgproc.putText(mRgba, "Touched", new Point(130, 130), Core.FONT_ITALIC, 1.0, new Scalar(0, 255, 0, 255));
    }
}
