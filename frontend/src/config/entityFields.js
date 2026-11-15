export const fields = {
  students: [['first_name', 'Prénom'], ['last_name', 'Nom'], ['registration_number', 'Matricule'], ['school_class_id', 'Classe', 'classes'], ['email', 'Adresse e-mail', 'email', true], ['phone', 'Téléphone', 'text', true], ['birth_date', 'Date de naissance', 'date', true], ['status', 'Statut', 'status']],
  programs: [['name', 'Nom de la filière'], ['code', 'Code'], ['description', 'Description', 'text', true]],
  classes: [['name', 'Nom de la classe'], ['program_id', 'Filière', 'programs'], ['academic_year', 'Année académique (2026-2027)']],
  subjects: [['name', 'Nom de la matière'], ['code', 'Code'], ['school_class_id', 'Classe', 'classes'], ['coefficient', 'Coefficient', 'number']],
  grades: [['student_id', 'Étudiant', 'students'], ['subject_id', 'Matière', 'subjects'], ['assessment', 'Évaluation'], ['score', 'Note sur 20', 'number'], ['weight', 'Poids de l’évaluation', 'number']],
};
