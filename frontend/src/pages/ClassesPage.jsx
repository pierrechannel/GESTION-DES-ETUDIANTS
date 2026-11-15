import React from 'react';
import EntityList from '../components/entities/EntityList';

const columns = ['Classe', 'Filière', 'Année académique', 'Effectif'];

function renderCells(schoolClass) {
  return [
    <strong>{schoolClass.name}</strong>,
    schoolClass.program.name,
    schoolClass.academic_year,
    `${schoolClass.students_count} étudiants`,
  ];
}

export default function ClassesPage({ admin }) {
  return <EntityList entity="classes" admin={admin} columns={columns} renderCells={renderCells} />;
}
