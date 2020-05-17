package com.example.lenovo.appspleeter;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;


public class MainActivity extends AppCompatActivity {

    private PredictTF mPredictTF;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mPredictTF = new PredictTF(this.getResources().getAssets(), "file:///android_asset/spleeter_freeze_v1.pb");
//        initPython();
//
//        callPython();


    }

    private void callPython() {
        Python py = Python.getInstance();
        // 调用hello.py模块中的greet函数，并传一个参数
        // 等价用法：py.getModule("hello").get("greet").call("Android");
        py.getModule("transfromData").callAttr("get_transfrom_data", "/storage/emulated/0/banhusha.mp3");
    }

    // 初始化Python环境
    void initPython(){
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
    }
}
