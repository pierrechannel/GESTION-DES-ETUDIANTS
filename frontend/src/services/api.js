let token = sessionStorage.getItem('campus_token');
export default async function api(path, options = {}) {
  const response = await fetch(`/api/v1/${path}`, { ...options, headers: { Accept: 'application/json', ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers } });
  if (response.status === 204) return null;
  const data = await response.json().catch(() => ({ message: 'Le serveur ne répond pas correctement. Vérifiez que Laravel est démarré.' }));
  if (!response.ok) { if (response.status === 401 && token) window.dispatchEvent(new Event('campus-expired')); throw Object.assign(new Error(data.message || 'Une erreur est survenue.'), { errors: data.errors, status: response.status }); }
  return data;
}

export function getToken() { return token; }
export function setToken(value) {
  token = value;
  if (value) sessionStorage.setItem('campus_token', value);
  else sessionStorage.removeItem('campus_token');
}
export function clearToken() { setToken(null); }

