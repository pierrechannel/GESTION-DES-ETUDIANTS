import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { createServer } from 'node:net';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = path.dirname(fileURLToPath(import.meta.url));
for (const required of ['backend/vendor/autoload.php', 'backend/.env', 'frontend/node_modules/vite/bin/vite.js']) {
  if (!existsSync(path.join(root, required))) { console.error(`Missing ${required}. Follow README.md installation first.`); process.exit(1); }
}
async function checkPort(port) {
  await new Promise((resolve, reject) => { const server = createServer(); server.once('error', () => reject(new Error(`Port ${port} is already in use.`))); server.listen(port, '127.0.0.1', () => server.close(resolve)); });
}
try { await checkPort(8000); await checkPort(5173); } catch (e) { console.error(e.message); process.exit(1); }
const children = [
  spawn('php', ['-S', '127.0.0.1:8000', path.join(root, 'backend/vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php')], { cwd: path.join(root, 'backend/public'), stdio: 'inherit', windowsHide: true }),
  spawn(process.execPath, [path.join(root, 'frontend/node_modules/vite/bin/vite.js'), '--host', '127.0.0.1', '--port', '5173', '--strictPort'], { cwd: path.join(root, 'frontend'), stdio: 'inherit', windowsHide: true }),
];
let stopping = false;
function stop(code = 0) { if (stopping) return; stopping = true; for (const child of children) child.kill(); process.exitCode = code; }
for (const child of children) { child.on('error', error => { console.error(error.message); stop(1); }); child.on('exit', code => { if (!stopping) stop(code || 0); }); }
process.on('SIGINT', () => stop()); process.on('SIGTERM', () => stop());
console.log('Campus: http://127.0.0.1:5173 | API: http://127.0.0.1:8000/api/v1 | Ctrl+C to stop');
