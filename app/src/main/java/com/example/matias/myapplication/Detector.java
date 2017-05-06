package com.example.matias.myapplication;

import android.content.Context;
import android.content.res.Resources;
import android.util.Log;

import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

/**
 * Created by matias on 06/05/17.
 */

public class Detector {

    public static final int        JAVA_DETECTOR       = 0;

    public static CascadeClassifier create(Resources resources, File directory, String TAG) {
        try {
            // load cascade file from application resources
            InputStream is = resources.openRawResource(R.raw.banana_classifier);
            File cascadeDir = directory;
            File mCascadeFile = new File(cascadeDir, "banana_classifier.xml");
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

    public static void detect(String TAG, CascadeClassifier mJavaDetector, Mat mGray, Mat mRgba, int mAbsoluteFaceSize) {
        int mDetectorType       = JAVA_DETECTOR;
        final Scalar FACE_RECT_COLOR     = new Scalar(0, 255, 0, 255);
        MatOfRect faces = new MatOfRect();

        if (mDetectorType == JAVA_DETECTOR) {
            if (mJavaDetector != null) {
                double scaleFactor = 1.1;
                int minNeighbors = 2;
                int flag = 0;
                mJavaDetector.detectMultiScale(mGray, faces, scaleFactor, minNeighbors, flag, new Size(mAbsoluteFaceSize, mAbsoluteFaceSize), new Size());
            }
        }
        else {
            Log.e(TAG, "Detection method is not selected!");
        }

        Rect[] facesArray = faces.toArray();
        for (int i = 0; i < facesArray.length; i++)
        {	Imgproc.rectangle(mRgba, facesArray[i].tl(), facesArray[i].br(),
                FACE_RECT_COLOR, 3);
            Rect r = facesArray[i];
        }
    }

}
