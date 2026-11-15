import { useEffect, useState } from 'react';
import api, { clearToken, getToken } from '../services/api';

export default function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (getToken()) {
      api('me')
        .then(setUser)
        .catch(() => clearToken())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }

    const expire = () => {
      clearToken();
      setUser(null);
    };
    window.addEventListener('campus-expired', expire);
    return () => window.removeEventListener('campus-expired', expire);
  }, []);

  async function logout() {
    try {
      await api('logout', { method: 'POST' });
      clearToken();
      setUser(null);
    } catch (e) {
      setError(e.message);
    }
  }

  return { user, loading, login: setUser, logout, error, clearError: () => setError('') };
}
