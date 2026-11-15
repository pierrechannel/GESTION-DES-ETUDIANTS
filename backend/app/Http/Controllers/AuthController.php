<?php
namespace App\Http\Controllers;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;
use Illuminate\Validation\Rules\Password;
class AuthController extends Controller {
    public function register(Request $request) {
        $data = $request->validate(['name' => 'required|string|max:100', 'email' => 'required|email|max:255|unique:users', 'password' => ['required', 'confirmed', Password::min(8)]]);
        $user = User::create([...$data, 'role' => 'user']);
        return response()->json(['user' => $user, 'token' => $user->createToken('campus', ['*'], now()->addHours(8))->plainTextToken], 201);
    }
    public function login(Request $request) {
        $data = $request->validate(['email' => 'required|email', 'password' => 'required|string']);
        $user = User::where('email', $data['email'])->first();
        if (!$user || !Hash::check($data['password'], $user->password)) throw ValidationException::withMessages(['email' => ['Identifiants incorrects.']]);
        return ['user' => $user, 'token' => $user->createToken('campus', ['*'], now()->addHours(8))->plainTextToken];
    }
    public function logout(Request $request) {
        $request->user()->currentAccessToken()->delete();
        return response()->noContent();
    }
}
