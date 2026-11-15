import React, { useState } from 'react';
import { CircularProgress } from '@mui/material';
import useAuth from './hooks/useAuth';
import AppLayout from './layouts/AppLayout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import StudentsPage from './pages/StudentsPage';
import ProgramsPage from './pages/ProgramsPage';
import ClassesPage from './pages/ClassesPage';
import SubjectsPage from './pages/SubjectsPage';
import GradesPage from './pages/GradesPage';

const pages = {
  dashboard: DashboardPage,
  students: StudentsPage,
  programs: ProgramsPage,
  classes: ClassesPage,
  subjects: SubjectsPage,
  grades: GradesPage,
};

export default function App() {
  const { user, loading, login, logout, error, clearError } = useAuth();
  const [page, setPage] = useState('dashboard');

  if (loading) return <div className="loading"><CircularProgress /></div>;
  if (!user) return <LoginPage onLogin={login} />;

  const Page = pages[page];
  return (
    <AppLayout user={user} page={page} onNavigate={setPage} onLogout={logout} error={error} onClearError={clearError}>
      <Page key={page} admin={user.role === 'admin'} navigate={setPage} />
    </AppLayout>
  );
}
