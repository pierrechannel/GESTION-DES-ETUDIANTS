import React from 'react';
import { Chip } from '@mui/material';
import EntityList from '../components/entities/EntityList';
import { studentName, number } from '../utils/formatters';

const columns = ['Étudiant', 'Matière', 'Évaluation', 'Note / 20', 'Poids'];

function renderCells(grade) {
  return [
    <div className="two-lines"><strong>{studentName(grade.student)}</strong><span>{grade.student.registration_number}</span></div>,
    grade.subject.name,
    grade.assessment,
    <Chip size="small" label={number(grade.score)} color={Number(grade.score) >= 10 ? 'success' : 'warning'} variant="outlined" />,
    number(grade.weight),
  ];
}

export default function GradesPage({ admin }) {
  return <EntityList entity="grades" admin={admin} columns={columns} renderCells={renderCells} />;
}
