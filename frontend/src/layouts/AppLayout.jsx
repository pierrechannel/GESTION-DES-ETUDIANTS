import React, { useState } from 'react';
import { Alert, Avatar, IconButton } from '@mui/material';
import SchoolOutlined from '@mui/icons-material/SchoolOutlined';
import Logout from '@mui/icons-material/Logout';
import MenuIcon from '@mui/icons-material/Menu';
import Brand from '../components/common/Brand';
import { sections } from '../config/sections';

export default function AppLayout({ user, page, onNavigate, onLogout, error, onClearError, children }) {
  const [mobile, setMobile] = useState(false);

  function navigate(key) {
    onNavigate(key);
    setMobile(false);
  }

  return (
    <div className="app-shell">
      <aside className={mobile ? 'sidebar visible' : 'sidebar'}>
        <Brand />
        <span className="nav-heading">ESPACE DE GESTION</span>
        <nav aria-label="Navigation principale">
          {Object.entries(sections).map(([key, { label, icon: Icon }]) => (
            <button key={key} className={page === key ? 'nav-item selected' : 'nav-item'}
              aria-current={page === key ? 'page' : undefined} onClick={() => navigate(key)}>
              <Icon fontSize="small" />
              {label}
              {page === key && <span className="nav-dot" />}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="school-badge">
            <SchoolOutlined />
            <div>Votre établissement<span>Année académique 2026–2027</span></div>
          </div>
          <button className="nav-item" onClick={onLogout}>
            <Logout fontSize="small" />Se déconnecter
          </button>
        </div>
      </aside>
      {mobile && <div className="scrim" onClick={() => setMobile(false)} />}
      <div className="workspace">
        <header className="topbar">
          <div className="breadcrumb">
            <IconButton className="mobile-toggle" aria-label="Afficher le menu" onClick={() => setMobile(true)}>
              <MenuIcon />
            </IconButton>
            Scolarité <span>/</span> <strong>{sections[page].label}</strong>
          </div>
          <div className="profile">
            <div><strong>{user.name}</strong><span>{user.role === 'admin' ? 'Administrateur' : 'Consultation'}</span></div>
            <Avatar sx={{ bgcolor: '#e9f1ed', color: '#215749', width: 38, height: 38 }}>{user.name[0]}</Avatar>
          </div>
        </header>
        <main className="main-content">
          {error && <Alert severity="error" onClose={onClearError}>{error}</Alert>}
          {children}
          <footer>Campus <span>Un regard clair sur chaque parcours.</span><small>Groupe 1 · Laravel + React</small></footer>
        </main>
      </div>
    </div>
  );
}
