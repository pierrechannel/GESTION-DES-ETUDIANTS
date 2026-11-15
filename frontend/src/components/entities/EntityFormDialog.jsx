import React, { useState } from 'react';
import { Button, TextField, MenuItem, Alert, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import api from '../../services/api';
import { fields } from '../../config/entityFields';
import { sections } from '../../config/sections';
import { studentName, className } from '../../utils/formatters';

export default function EntityFormDialog({ entity, record, options, onClose, onSaved }) {
  const [form, setForm] = useState({ status: 'active', coefficient: 1, weight: 1, academic_year: '2026-2027', ...record });
  const [errors, setErrors] = useState({});
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function save(event) {
    event.preventDefault();
    setBusy(true);
    setError('');
    setErrors({});
    try {
      const payload = Object.fromEntries(fields[entity].map(([key]) => [key, form[key] === '' ? null : form[key]]));
      await api(`${entity}${record.id ? '/' + record.id : ''}`, {
        method: record.id ? 'PUT' : 'POST',
        body: JSON.stringify(payload),
      });
      onSaved();
    } catch (e) {
      setErrors(e.errors || {});
      setError(e.errors ? 'Vérifiez les champs indiqués.' : e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Dialog open fullWidth maxWidth="sm" onClose={() => !busy && onClose()}>
      <form onSubmit={save}>
        <DialogTitle>{record.id ? 'Modifier' : 'Ajouter'} {sections[entity].singular}</DialogTitle>
        <DialogContent>
          <div className="form-fields">
            {error && <Alert severity="error">{error}</Alert>}
            {fields[entity].map(([key, label, type = 'text', optional]) => {
              let choices = options[type];
              if (entity === 'grades' && key === 'subject_id') {
                const student = options.students.find(item => item.id === Number(form.student_id));
                choices = options.subjects.filter(subject => subject.school_class_id === student?.school_class_id);
              }
              const select = Boolean(choices) || type === 'status';
              return (
                <TextField key={key} fullWidth required={!optional} label={label} select={select}
                  type={select ? undefined : type} value={form[key] ?? ''}
                  error={!!errors[key]} helperText={errors[key]?.join(' ')}
                  onChange={event => setForm({
                    ...form,
                    [key]: event.target.value,
                    ...(entity === 'grades' && key === 'student_id' ? { subject_id: '' } : {}),
                  })}
                  slotProps={{
                    inputLabel: { shrink: type === 'date' ? true : undefined },
                    htmlInput: type === 'number'
                      ? { step: '0.01', min: key === 'score' ? 0 : 0.01, max: key === 'score' ? 20 : 100 }
                      : {},
                  }}>
                  {select && (type === 'status'
                    ? [<MenuItem key="active" value="active">Actif</MenuItem>, <MenuItem key="inactive" value="inactive">Inactif</MenuItem>]
                    : choices.map(option => (
                      <MenuItem key={option.id} value={option.id}>
                        {type === 'students' ? `${studentName(option)} · ${option.registration_number}`
                          : type === 'classes' ? className(option)
                          : type === 'subjects' ? `${option.name} · ${option.code}` : option.name}
                      </MenuItem>
                    )))}
                </TextField>
              );
            })}
          </div>
        </DialogContent>
        <DialogActions>
          <Button disabled={busy} onClick={onClose}>Annuler</Button>
          <Button type="submit" disabled={busy} variant="contained">{busy ? 'Enregistrement…' : 'Enregistrer'}</Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
