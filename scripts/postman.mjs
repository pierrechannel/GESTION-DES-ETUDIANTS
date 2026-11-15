import fs from 'node:fs';
const request = (name, method, route, body, extra = {}) => ({ name, request: { method, header: [{ key: 'Accept', value: 'application/json' }, ...(body ? [{ key: 'Content-Type', value: 'application/json' }] : [])], url: '{{base_url}}' + route, ...(body ? { body: { mode: 'raw', raw: JSON.stringify(body, null, 2), options: { raw: { language: 'json' } } } } : {}), ...extra } });
const login = request('Connexion', 'POST', '/login', { email: 'admin@campus.test', password: 'Campus2026!' }, { auth: { type: 'noauth' } });
login.event = [{ listen: 'test', script: { type: 'text/javascript', exec: ['if (pm.response.code === 200) pm.collectionVariables.set("token", pm.response.json().token);'] } }];
const examples = {
  programs: { name: 'Sciences', code: 'SCI', description: 'Formation scientifique' },
  classes: { name: 'Master 1', program_id: 1, academic_year: '2026-2027' },
  subjects: { name: 'Base de donnees', code: 'BDD-NEW', school_class_id: 1, coefficient: 3 },
  students: { first_name: 'Test', last_name: 'Etudiant', registration_number: 'ETU-NEW-001', school_class_id: 1, status: 'active', email: 'new@example.test' },
  grades: { student_id: 1, subject_id: 1, assessment: 'Examen final', score: 16, weight: 2 },
};
const collection = {
  info: { name: 'Campus - Groupe 1', schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json', description: 'API Laravel Sanctum. Executer Connexion pour enregistrer le jeton. Adapter les IDs et valeurs uniques avant ecriture.' },
  variable: [{ key: 'base_url', value: 'http://127.0.0.1:8000/api/v1' }, { key: 'token', value: '' }, ...Object.keys(examples).map(e => ({ key: e + '_id', value: '1' }))],
  auth: { type: 'bearer', bearer: [{ key: 'token', value: '{{token}}', type: 'string' }] },
  item: [login, request('Inscription', 'POST', '/register', { name: 'Lecteur test', email: 'nouveau@example.test', password: 'TestPass123!', password_confirmation: 'TestPass123!' }, { auth: { type: 'noauth' } }), request('Profil', 'GET', '/me'), request('Tableau de bord', 'GET', '/dashboard'), request('Options', 'GET', '/options'), request('Releve', 'GET', '/students/{{students_id}}/transcript'), ...Object.entries(examples).map(([entity, body]) => ({ name: entity, item: [request('Liste et recherche', 'GET', '/' + entity + '?page=1&per_page=10&search='), request('Detail', 'GET', '/' + entity + '/{{' + entity + '_id}}'), request('Creer', 'POST', '/' + entity, body), request('Modifier', 'PUT', '/' + entity + '/{{' + entity + '_id}}', body), request('Supprimer', 'DELETE', '/' + entity + '/{{' + entity + '_id}}')] })), request('Deconnexion', 'POST', '/logout')],
};
fs.writeFileSync(new URL('../docs/campus.postman_collection.json', import.meta.url), JSON.stringify(collection, null, 2) + '\n');
