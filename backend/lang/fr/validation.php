<?php
return [
    'required' => 'Le champ :attribute est obligatoire.',
    'string' => 'Le champ :attribute doit être un texte.',
    'email' => 'Le champ :attribute doit être une adresse e-mail valide.',
    'unique' => 'Cette valeur du champ :attribute est déjà utilisée.',
    'exists' => 'La valeur sélectionnée pour :attribute est invalide.',
    'numeric' => 'Le champ :attribute doit être un nombre.',
    'min' => ['numeric' => 'Le champ :attribute doit être au moins :min.', 'string' => 'Le champ :attribute doit contenir au moins :min caractères.'],
    'max' => ['numeric' => 'Le champ :attribute ne doit pas dépasser :max.', 'string' => 'Le champ :attribute ne doit pas dépasser :max caractères.'],
    'confirmed' => 'La confirmation du champ :attribute ne correspond pas.',
    'date' => 'Le champ :attribute doit être une date valide.',
    'before_or_equal' => 'Le champ :attribute doit être une date antérieure ou égale à :date.',
    'in' => 'La valeur du champ :attribute est invalide.',
    'regex' => 'Le format du champ :attribute est invalide.',
    'attributes' => ['name' => 'nom', 'email' => 'e-mail', 'password' => 'mot de passe', 'first_name' => 'prénom', 'last_name' => 'nom', 'registration_number' => 'matricule', 'school_class_id' => 'classe', 'program_id' => 'filière', 'subject_id' => 'matière', 'student_id' => 'étudiant', 'academic_year' => 'année académique', 'score' => 'note', 'weight' => 'poids', 'coefficient' => 'coefficient', 'assessment' => 'évaluation', 'birth_date' => 'date de naissance', 'status' => 'statut'],
];
