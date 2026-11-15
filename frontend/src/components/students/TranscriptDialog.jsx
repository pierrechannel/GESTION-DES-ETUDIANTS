import React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, IconButton, Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
import Close from '@mui/icons-material/Close';
import PrintOutlined from '@mui/icons-material/PrintOutlined';
import Brand from '../common/Brand';
import { studentName, number } from '../../utils/formatters';

export default function TranscriptDialog({ data, onClose }) {
  const student = data.student;
  return (
    <Dialog open fullWidth maxWidth="md" onClose={onClose} className="transcript-dialog">
      <DialogTitle className="no-print">
        Fiche étudiante et relevé
        <IconButton aria-label="Fermer" onClick={onClose} sx={{ float: 'right' }}><Close /></IconButton>
      </DialogTitle>
      <DialogContent>
        <article className="transcript">
          <div className="transcript-heading">
            <Brand />
            <span>SCOLARITÉ<br />{student.school_class.academic_year}</span>
          </div>
          <h1>Relevé de notes</h1>
          <h2>{studentName(student)}</h2>
          <p>{student.registration_number} · {student.school_class.program.name} · {student.school_class.name}</p>
          <p className="muted">
            E-mail : {student.email || '—'} · Téléphone : {student.phone || '—'}<br />
            Date de naissance : {student.birth_date || '—'} · Statut : {student.status === 'active' ? 'Actif' : 'Inactif'}
          </p>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Matière / Évaluations</TableCell>
                <TableCell>Coefficient</TableCell>
                <TableCell align="right">Moyenne / 20</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.subjects.map(row => (
                <TableRow key={row.subject.id}>
                  <TableCell>
                    <strong>{row.subject.name}</strong>
                    <div className="muted grade-details">
                      {row.grades.map(grade => `${grade.assessment} : ${number(grade.score)}/20 (poids ${number(grade.weight)})`).join(' · ') || 'Aucune note saisie'}
                    </div>
                  </TableCell>
                  <TableCell>{number(row.subject.coefficient)}</TableCell>
                  <TableCell align="right">{number(row.average)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="average">
            <span>Moyenne générale {data.complete ? '' : '(provisoire)'}</span>
            <strong>{number(data.general_average)} <small>/ 20</small></strong>
          </div>
          <p className="muted">
            Moyennes pondérées par le poids des évaluations, puis par les coefficients des matières.
            {' '}Les matières sans note sont exclues de la moyenne provisoire.
          </p>
        </article>
      </DialogContent>
      <DialogActions className="no-print">
        <Button onClick={onClose}>Fermer</Button>
        <Button variant="contained" startIcon={<PrintOutlined />} onClick={() => window.print()}>
          Imprimer / Enregistrer en PDF
        </Button>
      </DialogActions>
    </Dialog>
  );
}
