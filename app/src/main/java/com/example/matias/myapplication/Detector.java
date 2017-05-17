package com.example.matias.myapplication;

import android.content.res.Resources;
import android.util.Log;

import org.opencv.core.Core;
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

    public static void detect(String TAG, List<CascadeClassifier> classifiers, Mat mGray, Mat mRgba, int mAbsoluteFaceSize) {
        int mDetectorType = JAVA_DETECTOR;

        MatOfRect faces1 = new MatOfRect();
        MatOfRect faces2 = new MatOfRect();

        if (mDetectorType == JAVA_DETECTOR) {
            if (classifiers != null) {
                double scaleFactor = 1.1;
                int minNeighbors = 2;
                int flag = 0;

                classifiers.get(0).detectMultiScale(mGray, faces1, scaleFactor, minNeighbors, flag, new Size(mAbsoluteFaceSize, mAbsoluteFaceSize), new Size());
                classifiers.get(1).detectMultiScale(mGray, faces2, scaleFactor, minNeighbors, flag, new Size(mAbsoluteFaceSize, mAbsoluteFaceSize), new Size());

            }
        }
        else {
            Log.e(TAG, "Detection method is not selected!");
        }

        bla(faces1, "zamora", new Point(100,100), mRgba);
        bla(faces2, "lilita", new Point(50, 50),mRgba);
    }

    private static void bla(MatOfRect faces, String label, Point point, Mat mRgba) {
        final Scalar FACE_RECT_COLOR     = new Scalar(0, 255, 0, 255);
        Rect[] facesArray = faces.toArray();
        for (int i = 0; i < facesArray.length; i++) {
            Imgproc.rectangle(mRgba, facesArray[i].tl(), facesArray[i].br(),
                    FACE_RECT_COLOR, 3);
            Imgproc.putText(mRgba, label, point, Core.FONT_ITALIC, 1.0,FACE_RECT_COLOR);
            Rect r = facesArray[i];


        }
    }
}
