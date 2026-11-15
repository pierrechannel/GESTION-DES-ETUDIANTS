import React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';

export default function ConfirmDeleteDialog({ open, busy, entity, onClose, onConfirm }) {
  return (
    <Dialog open={open} onClose={() => !busy && onClose()}>
      <DialogTitle>Confirmer la suppression</DialogTitle>
      <DialogContent>
        <p>
          Supprimer cet élément ? Cette opération est définitive.
          {entity === 'students' ? ' Les notes de cet étudiant seront également supprimées.' : ''}
        </p>
      </DialogContent>
      <DialogActions>
        <Button disabled={busy} onClick={onClose}>Annuler</Button>
        <Button disabled={busy} color="error" variant="contained" onClick={onConfirm}>Supprimer</Button>
      </DialogActions>
    </Dialog>
  );
}
