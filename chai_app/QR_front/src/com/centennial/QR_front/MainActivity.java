package com.centennial.QR_front;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.RelativeLayout;
import android.widget.TextView;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;


public class MainActivity extends Activity {

    TextView scanText;
    WebView webView;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        init();
    }

    public void init() {
        scanText = (TextView) findViewById(R.id.scanText);
        // webview hidden by default
        webView = (WebView) findViewById(R.id.webView);
        webView.setVisibility(View.GONE);
        // enable javascript
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);

    }

    public void scanNow(View v) {
        // scan intent
        (new IntentIntegrator(this)).initiateScan();
    }

    public void webViewOn(String url) {
        webView.setVisibility(View.VISIBLE);
        webView.setWebViewClient(new WebViewClient()); //prevents open in browser
        webView.loadUrl(url);
        // modify position of text
        RelativeLayout.LayoutParams scanTextParams =
                new RelativeLayout.LayoutParams(scanText.getLayoutParams());
        scanTextParams.addRule(RelativeLayout.ABOVE, R.id.button); // set to above button
        scanTextParams.addRule(RelativeLayout.CENTER_VERTICAL, 0); // remove center screen location
        scanText.setLayoutParams(scanTextParams);
    }

    public void webViewOff() {
        webView.setVisibility(View.GONE);
        // modify position of text
        RelativeLayout.LayoutParams scanTextParams =
                new RelativeLayout.LayoutParams(scanText.getLayoutParams());
        scanTextParams.addRule(RelativeLayout.ABOVE, 0); // remove above button layout
        scanTextParams.addRule(RelativeLayout.CENTER_VERTICAL); // move text to center of screen
        scanText.setLayoutParams(scanTextParams);
    }

    public String getUrl(String content) {
        // gets url from string that includes more than just URL
        // assumes " " in string and "http://" in string.
        String[] items = content.split("\\s+");
        int urlID = 0;
        for (int i = 0; i < items.length; i++) {
            if (items[i].contains("http://")) {
                urlID = i; // capture index of url
            }
        }
        return items[urlID];
    }
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        // capture result return
        IntentResult scan = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        if (scan!=null) {
            String content = scan.getContents();
            String format = scan.getFormatName();
            scanText.setText("Content: " + content + "\n\nFormat: " + format);
            if (content.toLowerCase().contains("http://")) {
                // URL found, send to webview.
                if (content.contains(" ")) {
                    // handle multiple-item QR
                    webViewOn(getUrl(content));

                } else {
                    webViewOn(content);
                }
            } else {
                webView.setVisibility(View.GONE);
            }
        }
    }

}
