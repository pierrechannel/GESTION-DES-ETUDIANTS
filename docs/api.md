# API Campus

Base : `http://127.0.0.1:8000/api/v1`. Envoyer `Accept: application/json`, `Content-Type: application/json` pour les écritures et `Authorization: Bearer <token>` après connexion.

| Méthode | Route | Accès | Résultat |
| --- | --- | --- | --- |
| POST | /register | Public, 5/minute | name, email, password, password_confirmation ; crée un utilisateur, 201 |
| POST | /login | Public, 5/minute | email, password ; retourne user et token, 200 |
| GET | /me | Connecté | Profil courant |
| POST | /logout | Connecté | Révoque le jeton courant, 204 |
| GET | /dashboard | Connecté | Totaux, effectifs par classe et derniers inscrits |
| GET | /options | Connecté | Filières/classes/matières/étudiants pour les sélecteurs |
| GET | /students/{id}/transcript | Connecté | Étudiant, matières, évaluations, moyennes et indicateur complete |
| GET | /{entité} | Connecté | Liste paginée |
| GET | /{entité}/{id} | Connecté | Détail |
| POST | /{entité} | Admin | Création, 201 |
| PUT | /{entité}/{id} | Admin | Mise à jour complète des champs obligatoires, 200 |
| DELETE | /{entité}/{id} | Admin | Suppression, 204 |

Entités : `students`, `programs`, `classes`, `subjects`, `grades`.

## Corps des requêtes

- programs : `name`, `code`, `description` (facultatif).
- classes : `name`, `program_id`, `academic_year` (format `2026-2027`).
- subjects : `name`, `code`, `school_class_id`, `coefficient` (0.01 à 100).
- students : `first_name`, `last_name`, `registration_number`, `school_class_id`, `status` (`active`/`inactive`), `email`, `phone`, `birth_date` (les trois derniers facultatifs).
- grades : `student_id`, `subject_id`, `assessment`, `score` (0 à 20), `weight` (0.01 à 100).

Les IDs de relation doivent exister. Matricules et codes sont uniques. Une évaluation portant le même nom ne peut pas être répétée pour le même étudiant et la même matière.

## Listes

Paramètres communs : `search`, `page` (1 par défaut), `per_page` (10 par défaut, maximum 100).

- students : recherche nom/prénom/matricule, filtres `program_id`, `class_id`, `status`.
- classes : recherche nom/année, filtre `program_id`.
- subjects : recherche nom/code, filtre `class_id`.
- grades : recherche évaluation ou nom/matricule étudiant, filtres `subject_id`, `student_id`.
- programs : recherche nom/code.

Les réponses paginées comprennent `data`, `total`, `current_page`, `per_page`, `last_page` et les liens de pagination Laravel. Les résultats sont triés par ID décroissant.

## Erreurs

- 401 : authentification absente, expirée ou invalide.
- 403 : rôle insuffisant.
- 404 : ressource ou route inconnue.
- 409 : suppression bloquée par une dépendance.
- 422 : validation ; `errors` associe chaque champ à une liste de messages.
- 429 : trop de tentatives de connexion/inscription.
- 500 : erreur inattendue ; voir les journaux Laravel.

## Postman

Importer `campus.postman_collection.json`. Exécuter « Connexion » : le script enregistre automatiquement le jeton dans la variable de collection `token`. Les dossiers suivants utilisent ce jeton. Les IDs d’exemple 1 correspondent aux données initiales ; adapter les corps avant création et modifier les IDs avant suppression. Les requêtes de suppression modifient réellement les données.

Le CSV est produit dans React après récupération de toutes les pages filtrées. Le PDF utilise l’impression du navigateur ; il n’existe pas d’endpoint CSV/PDF côté serveur.
