<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\{AuthController, SchoolController};
Route::prefix('v1')->group(function () {
    Route::post('login', [AuthController::class, 'login'])->middleware('throttle:5,1');
    Route::post('register', [AuthController::class, 'register'])->middleware('throttle:5,1');
    Route::middleware('auth:sanctum')->group(function () {
        Route::get('me', fn (\Illuminate\Http\Request $request) => $request->user());
        Route::post('logout', [AuthController::class, 'logout']);
        Route::get('dashboard', [SchoolController::class, 'dashboard']);
        Route::get('options', [SchoolController::class, 'options']);
        Route::get('students/{student}/transcript', [SchoolController::class, 'transcript']);
        Route::get('{entity}', [SchoolController::class, 'index'])->where('entity', 'students|programs|classes|subjects|grades');
        Route::get('{entity}/{id}', [SchoolController::class, 'show'])->where('entity', 'students|programs|classes|subjects|grades')->whereNumber('id');
        Route::middleware('admin')->group(function () {
            Route::post('{entity}', [SchoolController::class, 'store'])->where('entity', 'students|programs|classes|subjects|grades');
            Route::put('{entity}/{id}', [SchoolController::class, 'update'])->where('entity', 'students|programs|classes|subjects|grades')->whereNumber('id');
            Route::delete('{entity}/{id}', [SchoolController::class, 'destroy'])->where('entity', 'students|programs|classes|subjects|grades')->whereNumber('id');
        });
    });
});
