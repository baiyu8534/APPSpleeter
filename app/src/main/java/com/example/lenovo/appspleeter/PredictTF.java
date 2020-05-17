package com.example.lenovo.appspleeter;


import android.content.res.AssetManager;
import android.util.Log;

import org.tensorflow.contrib.android.TensorFlowInferenceInterface;

/**
 * @author BaiYu
 * @description:
 * @date :2020/5/17 10:16
 */
public class PredictTF {
    private static final String TAG = "PredictionTF";
    //模型中输入变量的名称
    private static final String inputName = "'mix_stft:0";
    //模型中输出变量的名称
    private static final String outputName_1 = "mul_2:0";
    private static final String outputName_2 = "mul_3:0";



    TensorFlowInferenceInterface inferenceInterface;
    static {
        //加载libtensorflow_inference.so库文件
        System.loadLibrary("tensorflow_inference");
        Log.e("","libtensorflow_inference.so库加载成功");
    }

    PredictTF(AssetManager assetManager, String modePath) {
        //初始化TensorFlowInferenceInterface对象
        inferenceInterface = new TensorFlowInferenceInterface(assetManager,modePath);
        Log.e(TAG,"TensoFlow模型文件加载成功");
    }

    public void predict(String music_path){
//        inferenceInterface.feed();
    }


}
