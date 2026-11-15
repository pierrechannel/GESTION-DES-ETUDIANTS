import React from 'react';
import { Avatar, Chip } from '@mui/material';
import EntityList from '../components/entities/EntityList';
import { studentName } from '../utils/formatters';

const columns = ['Étudiant', 'Matricule', 'Filière / Classe', 'Statut'];

function renderCells(student) {
  return [
    <div className="person-cell">
      <Avatar sx={{ width: 36, height: 36, bgcolor: '#edf2ef', color: '#54796b', fontSize: 13 }}>
        {student.first_name[0]}{student.last_name[0]}
      </Avatar>
      <div><strong>{studentName(student)}</strong><span>{student.email || 'E-mail non renseigné'}</span></div>
    </div>,
    <span className="mono">{student.registration_number}</span>,
    <div className="two-lines"><strong>{student.school_class.program.name}</strong><span>{student.school_class.name}</span></div>,
    <Chip size="small" label={student.status === 'active' ? 'Actif' : 'Inactif'}
      sx={{ bgcolor: student.status === 'active' ? '#edf5ef' : '#f1f2f3', color: student.status === 'active' ? '#2f7a4d' : '#6b7280' }} />,
  ];
}

export default function StudentsPage({ admin }) {
  return <EntityList entity="students" admin={admin} columns={columns} renderCells={renderCells} />;
}
