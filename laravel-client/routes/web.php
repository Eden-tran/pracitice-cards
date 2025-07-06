<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', 'BusinessCardController@index');
Route::post('/upload', 'BusinessCardController@upload');
Route::get('/results/{id}', 'BusinessCardController@results');
Route::get('/api/history', 'BusinessCardController@history');
