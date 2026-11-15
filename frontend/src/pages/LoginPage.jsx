import React, { useState } from 'react';
import { Button, TextField, Alert, CircularProgress } from '@mui/material';
import SchoolOutlined from '@mui/icons-material/SchoolOutlined';
import ArrowForward from '@mui/icons-material/ArrowForward';
import api, { setToken } from '../services/api';
import Brand from '../components/common/Brand';

export default function LoginPage({ onLogin }) {
  const [register, setRegister] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError('');
    try {
      const data = await api(register ? 'register' : 'login', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))),
      });
      setToken(data.token);
      onLogin(data.user);
    } catch (e) {
      setError(Object.values(e.errors || {}).flat().join(' ') || e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-layout">
      <div className="login-story">
        <Brand />
        <div>
          <span className="eyebrow">VOTRE CAMPUS, CONNECTÉ</span>
          <h1>Accompagner<br />chaque parcours.</h1>
          <p>Étudiants, formations et résultats.<br />Un espace pour faire avancer votre établissement.</p>
          <div className="story-art">
            <SchoolOutlined sx={{ fontSize: 140 }} />
            <span>Apprendre. Progresser. Réussir.</span>
          </div>
        </div>
        <small>Projet de programmation côté serveur · Groupe 1</small>
      </div>
      <main className="login-form">
        <form onSubmit={submit}>
          <span className="eyebrow">ESPACE SCOLARITÉ</span>
          <h2>{register ? 'Créer un compte' : 'Bienvenue sur Campus'}</h2>
          <p className="muted">
            {register ? 'Votre compte permet de consulter les données scolaires.' : 'Connectez-vous pour retrouver votre établissement.'}
          </p>
          {error && <Alert severity="error">{error}</Alert>}
          {register && <TextField required fullWidth name="name" label="Nom complet" autoComplete="name" />}
          <TextField required fullWidth type="email" name="email" label="Adresse e-mail" autoComplete="username" />
          <TextField required fullWidth type="password" name="password" label="Mot de passe"
            inputProps={{ minLength: 8 }} autoComplete={register ? 'new-password' : 'current-password'} />
          {register && (
            <TextField required fullWidth type="password" name="password_confirmation"
              label="Confirmer le mot de passe" autoComplete="new-password" />
          )}
          <Button disabled={busy} fullWidth variant="contained" size="large" type="submit"
            endIcon={busy ? <CircularProgress size={18} /> : <ArrowForward />}>
            {register ? 'Créer mon compte' : 'Se connecter'}
          </Button>
          <Button fullWidth onClick={() => { setRegister(!register); setError(''); }}>
            {register ? 'J’ai déjà un compte' : 'Créer un compte de consultation'}
          </Button>
        </form>
        <small className="muted">Campus · Gestion des étudiants</small>
      </main>
    </div>
  );
}
