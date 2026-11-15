export const studentName = s => `${s.first_name} ${s.last_name}`;
export const className = c => c ? `${c.name} · ${c.program?.code || ''} · ${c.academic_year}` : '—';
export const number = n => n == null ? '—' : Number(n).toLocaleString('fr-FR', { maximumFractionDigits: 2 });
