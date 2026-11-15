<?php
namespace App\Http\Middleware;
use Closure;
use Illuminate\Http\Request;
class AdminOnly {
    public function handle(Request $request, Closure $next) {
        abort_unless($request->user()?->role === 'admin', 403, 'Action réservée aux administrateurs.');
        return $next($request);
    }
}
