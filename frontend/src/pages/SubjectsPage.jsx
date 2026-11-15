import React from 'react';
import EntityList from '../components/entities/EntityList';
import { className, number } from '../utils/formatters';

const columns = ['Matière', 'Code', 'Classe', 'Coefficient'];

function renderCells(subject) {
  return [
    <strong>{subject.name}</strong>,
    subject.code,
    className(subject.school_class),
    number(subject.coefficient),
  ];
}

export default function SubjectsPage({ admin }) {
  return <EntityList entity="subjects" admin={admin} columns={columns} renderCells={renderCells} />;
}
