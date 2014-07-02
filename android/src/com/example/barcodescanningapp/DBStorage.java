/*
 * DBStorage.java
 * 
 * Copyright 2014 mikee <mikee@thinky.saxicola>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * Store into librarian DB if available, else temporary store on device
 * until we can connect to the librarian DB.
 */
package com.example.barcodescanningapp;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.widget.Toast;
import android.util.Log;
import android.content.Context;

import android.content.ContentValues;
import android.database.sqlite.SQLiteCursor;

import com.example.barcodescanningapp.MySQLiteHelper;
import android.database.sqlite.SQLiteDatabase;
import android.database.Cursor;

public class DBStorage {
    public static final int DATABASE_VERSION = 2;
    public static final String DATABASE_NAME = "librarian.db";
    private MySQLiteHelper dbHelper; 
    private SQLiteDatabase database;
    
    // Example code CHANGE ME
    public final static String BOOK_TABLE="books"; // name of table 
  
     
     /** 
         * 
         * @param context 
         */  
        public DBStorage(Context context){
            Log.d("DBStorage","Here we are!");  
            dbHelper = new MySQLiteHelper(context);  
            database = dbHelper.getWritableDatabase();  
        }
        
        // TODO
        public long createRecords(String author, String title, String description, String date, String rating){  
           ContentValues values = new ContentValues();  
           values.put("author", author);  
           values.put("title", title);
           Log.d(DBStorage.class.getName(),author);  
           return database.insert(BOOK_TABLE, null, values);  
}    
    // TODO
    /*
    public Cursor selectRecords() {
       String[] cols = new String[] {EMP_ID, EMP_NAME};  
       Cursor mCursor = database.query(true, BOOK_TABLE,cols,null  
                , null, null, null, null, null);  
       if (mCursor != null) {  
         mCursor.moveToFirst();  
       }  
       return mCursor; // iterate to get each value.
    }*/
}
