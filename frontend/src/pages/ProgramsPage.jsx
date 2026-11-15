import React from 'react';
import { Chip } from '@mui/material';
import EntityList from '../components/entities/EntityList';

const columns = ['Filière', 'Code', 'Description', 'Classes'];

function renderCells(program) {
  return [
    <strong>{program.name}</strong>,
    <Chip size="small" variant="outlined" label={program.code} />,
    program.description || '—',
    program.classes_count,
  ];
}

export default function ProgramsPage({ admin }) {
  return <EntityList entity="programs" admin={admin} columns={columns} renderCells={renderCells} />;
}
