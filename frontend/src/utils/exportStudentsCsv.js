import { getStudentsForExport } from '../services/students';

function csvCell(value) {
  const text = String(value ?? '');
  // Prevent a spreadsheet from interpreting user-entered text as a formula.
  const prefix = /^[=+@\-\t\r]/.test(text) ? "'" : '';
  return `"${prefix}${text.replaceAll('"', '""')}"`;
}

export async function exportStudentsCsv(filters) {
  const students = await getStudentsForExport(filters);
  const rows = [
    ['Matricule', 'Prénom', 'Nom', 'Filière', 'Classe', 'Email', 'Statut'],
    ...students.map(student => [
      student.registration_number,
      student.first_name,
      student.last_name,
      student.school_class.program.name,
      student.school_class.name,
      student.email,
      student.status === 'active' ? 'Actif' : 'Inactif',
    ]),
  ];
  const csv = rows.map(row => row.map(csvCell).join(';')).join('\r\n');
  const url = URL.createObjectURL(new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'etudiants.csv';
  link.click();
  URL.revokeObjectURL(url);
}
