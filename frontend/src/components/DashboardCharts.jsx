import React, { useState } from 'react';
import { Chip, Tooltip } from '@mui/material';

const palette = ['#215749', '#699c82', '#d6ac62', '#7895b1', '#a183ad', '#c57e6c'];
const colorAt = index => palette[index] || `hsl(${(index * 137.5) % 360} 38% 48%)`;
const formatCount = value => value.toLocaleString('fr-FR');
const monthDate = month => {
  const [year, number] = month.split('-').map(Number);
  return new Date(year, number - 1, 1);
};
const monthLabel = (month, long = false) => new Intl.DateTimeFormat('fr-FR', {
  month: long ? 'long' : 'short', year: long ? 'numeric' : '2-digit',
}).format(monthDate(month));

function RegistrationChart({ months }) {
  const [selected, setSelected] = useState(null);
  if (!months.length) return <p className="chart-empty">Aucune période disponible.</p>;

  const width = 640, height = 240;
  const left = 42, right = 28, top = 22, bottom = 42;
  const step = Math.max(1, Math.ceil(Math.max(...months.map(m => m.count)) / 4));
  const maximum = step * 4;
  const x = index => left + index * (width - left - right) / Math.max(1, months.length - 1);
  const y = count => height - bottom - count / maximum * (height - top - bottom);
  const points = months.map((month, index) => `${x(index)},${y(month.count)}`).join(' ');
  const current = months[selected ?? months.length - 1];
  const total = months.reduce((sum, month) => sum + month.count, 0);

  return <>
    <div className="chart-summary">
      <strong>{formatCount(total)} <span>inscriptions sur la période</span></strong>
      <span className="chart-key"><i/>Inscriptions mensuelles</span>
    </div>
    <svg className="line-chart" viewBox={`0 0 ${width} ${height}`} role="group" aria-label="Inscriptions mensuelles sur les six derniers mois">
      {Array.from({ length: 5 }, (_, index) => {
        const value = index * step;
        return <g key={value} aria-hidden="true">
          <line x1={left} x2={width - right} y1={y(value)} y2={y(value)} className="chart-gridline"/>
          <text x={left - 12} y={y(value) + 4} textAnchor="end" className="chart-axis">{formatCount(value)}</text>
        </g>;
      })}
      <polygon points={`${left},${y(0)} ${points} ${x(months.length - 1)},${y(0)}`} fill="#eaf2ec" aria-hidden="true"/>
      <polyline points={points} fill="none" stroke="#215749" strokeWidth="3" strokeLinejoin="round" aria-hidden="true"/>
      {months.map((month, index) => {
        const label = `${monthLabel(month.month, true)} : ${formatCount(month.count)} inscription${month.count === 1 ? '' : 's'}`;
        return <g key={month.month}>
          <text x={x(index)} y={height - 12} textAnchor="middle" className="chart-axis" aria-hidden="true">{monthLabel(month.month)}</text>
          <Tooltip title={label} arrow>
            <circle cx={x(index)} cy={y(month.count)} r={selected === index ? 7 : 5} fill="#fff" stroke="#215749" strokeWidth="3"
              tabIndex={0} role="img" aria-label={label} className="chart-point"
              onMouseEnter={() => setSelected(index)} onMouseLeave={() => setSelected(null)}
              onFocus={() => setSelected(index)} onBlur={() => setSelected(null)}/>
          </Tooltip>
        </g>;
      })}
    </svg>
    <p className="chart-detail" aria-live="polite">{monthLabel(current.month, true)} <strong>{formatCount(current.count)} inscription{current.count === 1 ? '' : 's'}</strong></p>
    {total === 0 && <p className="chart-empty">Aucune inscription pendant ces six mois.</p>}
  </>;
}

function PieChart({ items, label }) {
  const [active, setActive] = useState(null);
  const total = items.reduce((sum, item) => sum + item.value, 0);
  if (!total) return <p className="chart-empty">Aucun étudiant à représenter pour le moment.</p>;

  let angle = -Math.PI / 2;
  const segments = items.map((item, index) => {
    const start = angle;
    angle += item.value / total * Math.PI * 2;
    const radius = 94, center = 110;
    const point = value => `${center + radius * Math.cos(value)} ${center + radius * Math.sin(value)}`;
    return { ...item, index, color: colorAt(index), full: item.value === total,
      path: `M ${center} ${center} L ${point(start)} A ${radius} ${radius} 0 ${angle - start > Math.PI ? 1 : 0} 1 ${point(angle)} Z` };
  });
  const percentage = value => (value / total * 100).toLocaleString('fr-FR', { maximumFractionDigits: 1 }) + ' %';
  const description = item => `${item.label} : ${formatCount(item.value)} étudiant${item.value === 1 ? '' : 's'} (${percentage(item.value)})`;

  return <div className="pie-layout">
    <svg viewBox="0 0 220 220" className="pie-chart" role="group" aria-label={label}>
      {segments.filter(item => item.value > 0).map(item => {
        const props = {
          fill: item.color, stroke: '#fff', strokeWidth: 3, tabIndex: 0, role: 'img',
          'aria-label': description(item), className: 'pie-slice',
          opacity: active === null || active === item.index ? 1 : 0.4,
          onMouseEnter: () => setActive(item.index), onMouseLeave: () => setActive(null),
          onFocus: () => setActive(item.index), onBlur: () => setActive(null),
        };
        return <Tooltip key={item.index} title={description(item)} arrow>
          {item.full ? <circle cx="110" cy="110" r="94" {...props}/> : <path d={item.path} {...props}/>}
        </Tooltip>;
      })}
    </svg>
    <ul className="chart-legend">
      {segments.map(item => <li key={item.id}>
        <button type="button" aria-pressed={active === item.index} aria-label={description(item)}
          onClick={() => setActive(active === item.index ? null : item.index)}>
          <i style={{ background: item.color }}/><span>{item.label}</span>
          <strong>{formatCount(item.value)}<small>{percentage(item.value)}</small></strong>
        </button>
      </li>)}
    </ul>
    <p className="pie-total">{formatCount(total)} étudiant{total === 1 ? '' : 's'} au total</p>
  </div>;
}

export default function DashboardCharts({ data }) {
  // Sum class counts by program; these are full dashboard counts, not paginated lists.
  const programs = new Map();
  for (const schoolClass of data.by_class) {
    const program = schoolClass.program;
    if (!program) continue;
    if (!programs.has(program.id)) programs.set(program.id, { id: program.id, label: program.name, value: 0 });
    programs.get(program.id).value += schoolClass.students_count;
  }
  const byProgram = [...programs.values()].sort((a, b) => b.value - a.value || a.label.localeCompare(b.label, 'fr'));
  const statuses = [
    { id: 'active', label: 'Actifs', value: data.active_students },
    { id: 'inactive', label: 'Inactifs', value: data.students - data.active_students },
  ];
  return <div className="dashboard-charts">
    <section className="panel registration-panel">
      <div className="panel-heading"><div><h3>Évolution des inscriptions</h3><p className="muted">Nouveaux dossiers étudiants par mois · heure de Bujumbura</p></div><Chip size="small" label="6 derniers mois" variant="outlined"/></div>
      <div className="line-chart-body"><RegistrationChart months={data.registrations_by_month || []}/></div>
    </section>
    <section className="panel">
      <div className="panel-heading"><div><h3>Étudiants par filière</h3><p className="muted">Répartition des effectifs de l’établissement</p></div></div>
      <PieChart items={byProgram} label="Répartition des étudiants par filière"/>
    </section>
    <section className="panel">
      <div className="panel-heading"><div><h3>Statut des étudiants</h3><p className="muted">Part des dossiers actifs et inactifs</p></div></div>
      <PieChart items={statuses} label="Répartition des étudiants par statut"/>
    </section>
  </div>;
}
