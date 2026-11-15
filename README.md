# Campus — Gestion des étudiants (Groupe 1)

Application du sujet « Système de gestion des étudiants » du PDF fourni. Backend Laravel 12 / Eloquent / Sanctum, interface React 19 avec Material UI 7 et Vite. Interface en français, adaptée au mobile.

## Fonctionnalités

- Inscription, connexion, déconnexion et expiration des jetons après 8 heures.
- Deux rôles : administrateur (gestion) et utilisateur (consultation de toutes les données scolaires). L'inscription publique crée uniquement un utilisateur de consultation.
- CRUD des étudiants, filières, classes, matières et notes.
- Matricule unique, fiche détaillée, recherche par nom/prénom/matricule et filtre par filière.
- Recherche, filtrage et pagination sur les étudiants, classes, matières et notes ; recherche et pagination sur les filières.
- Notes sur 20, poids des évaluations et coefficients des matières ; calcul des moyennes côté serveur.
- Relevé imprimable : ouvrir l’icône œil d’un étudiant, puis « Imprimer / Enregistrer en PDF ».
- Export CSV de tous les étudiants correspondant aux filtres, y compris au-delà de la page affichée.
- Tableau de bord avec courbe des inscriptions sur six mois, camemberts par filière et par statut, statistiques par classe et inscriptions récentes. Les graphiques utilisent les données réelles, avec infobulles et légendes accessibles au clavier.

## Démarrer sur ce poste

Les dépendances sont installées et une base SQLite de démonstration est préparée. Depuis le dossier racine :

```powershell
node dev.mjs
```

Ouvrir http://127.0.0.1:5173. Garder le terminal ouvert ; Ctrl+C arrête les deux serveurs. PHP et Node doivent être dans le PATH.

| Rôle | E-mail | Mot de passe de démonstration |
| --- | --- | --- |
| Administrateur | admin@campus.test | Campus2026! |
| Consultation | lecteur@campus.test | Campus2026! |

Le jeu d’exemple contient 12 étudiants, 3 filières, 6 classes, 18 matières et 36 notes. Les seeders sont réservés à la démonstration : ils réappliquent les exemples portant les mêmes codes/matricules. Les comptes existants ne sont pas réinitialisés.

## Installation sur un autre poste — MySQL (pile du TP)

Prérequis : PHP 8.2+ avec PDO MySQL, Composer, Node.js 20.19+ et MySQL/MariaDB (XAMPP convient).

1. Démarrer MySQL dans XAMPP et créer une base `campus_groupe1` dans phpMyAdmin (encodage `utf8mb4`).
2. Installer et configurer Laravel :

```powershell
cd backend
composer install
Copy-Item .env.example .env
# Adapter DB_USERNAME et DB_PASSWORD dans .env.
php artisan key:generate
php artisan migrate --seed
cd ..\frontend
npm ci
cd ..
node dev.mjs
```

Sur ce poste, ne pas écraser le `.env` SQLite si vous souhaitez conserver la démonstration. Pour passer à MySQL, modifier les variables `DB_*` selon `.env.example`, supprimer une éventuelle valeur `DB_DATABASE` pointant vers SQLite et exécuter `php artisan config:clear`, puis `php artisan migrate --seed`.

SQLite sert uniquement à la démonstration immédiate et aux tests isolés. Le fichier `.env.example` fournit la configuration MySQL pour le rendu. Pour recréer la démonstration ailleurs, copier `.env.example`, mettre `DB_CONNECTION=sqlite`, retirer `DB_DATABASE=campus_groupe1`, créer le fichier vide `backend/database/database.sqlite`, puis lancer les migrations et seeders.

Deux terminaux peuvent remplacer le lanceur : `php artisan serve --host=127.0.0.1 --port=8000` dans `backend` et `npm run dev` dans `frontend`.

## Vérifications

```powershell
cd backend
php artisan test
cd ..\frontend
npm run build
```

Les tests utilisent SQLite **en mémoire**, sans modifier la base de travail. Ils couvrent les rôles, l’inscription sans élévation de privilèges, la révocation des jetons, les CRUD, l’unicité, les filtres, les dépendances et les calculs pondérés. La vérification MySQL et l’inspection visuelle dans un navigateur restent à effectuer sur votre configuration cible.

## Organisation et documentation

- `backend/app/Models` : entités et relations Eloquent.
- `backend/app/Http/Controllers` : authentification et API scolaire.
- `backend/app/Http/Middleware/AdminOnly.php` : restriction des écritures.
- `backend/app/Services/TranscriptService.php` : calcul du relevé.
- `backend/database` : migrations et seeders.
- `frontend/src/main.jsx` : point d’entrée React et application du thème MUI.
- `frontend/src/App.jsx` : sélection de la page et protection par authentification.
- `frontend/src/pages` : pages de connexion, tableau de bord, étudiants, filières, classes, matières et notes ; chaque page de gestion définit ses colonnes et l’affichage de ses données.
- `frontend/src/layouts/AppLayout.jsx` : navigation latérale, en-tête et structure commune des pages.
- `frontend/src/components` : graphiques, tableau CRUD partagé, formulaires, confirmation de suppression, relevé imprimable et logo.
- `frontend/src/hooks/useAuth.js` : restauration de session, profil et déconnexion.
- `frontend/src/services` : client HTTP, gestion du jeton et récupération des étudiants pour l’export.
- `frontend/src/config` : rubriques de navigation et définition des champs des formulaires.
- `frontend/src/utils` : formatage des valeurs et export CSV.
- `frontend/src/theme.js` et `style.css` : thème MUI et styles communs.
- [Conception : MCD/MLD et cas d’utilisation](docs/conception.md).
- [Document Word : MCD, MLD et diagramme UML des cas d’utilisation](docs/Conception_Groupe_1_MCD_MLD_Cas_Utilisation.docx), avec dictionnaire des données, cardinalités et règles de gestion. Les diagrammes PNG/SVG sont dans `docs/diagrammes`.
- [Présentation PowerPoint reconstruite](docs/Soutenance_Groupe_1_Gestion_Etudiants_CORRIGE.pptx) : 16 diapositives avec notes du présentateur et les trois diagrammes. Le fichier est généré avec `python-pptx` et son modèle Office standard ; l’ancien lien pointe également vers cette version. [PDF de secours](docs/Soutenance_Groupe_1_Gestion_Etudiants.pdf) et [guide de présentation](docs/Guide_Soutenance_Groupe_1.md), pour environ 13 minutes d’exposé. Compléter les membres du groupe sur la première diapositive. La vérification automatique dans l’application PowerPoint locale n’a pas abouti : son serveur COM a refusé l’appel.
- [Documentation des routes et règles](docs/api.md).
- [Collection Postman importable](docs/campus.postman_collection.json).

## Règles de calcul et cohérence

Moyenne matière = somme(note × poids) / somme(poids). Moyenne générale = somme(moyenne matière × coefficient) / somme(coefficients des matières notées). On arrondit uniquement la moyenne générale finale à deux décimales. Une matière sans note reste « — » ; son absence rend le relevé provisoire. Il n’y a pas de découpage par semestre dans cette version : la classe est rattachée à une année académique.

Une note doit porter sur une matière de la classe de l’étudiant. Un étudiant ou une matière ayant des notes ne peut pas changer de classe avant suppression de ses notes. Une filière/classe/matière référencée ne peut pas être supprimée. Supprimer un étudiant supprime ses notes après confirmation explicite.

## Déploiement

La version actuelle s’exécute localement. Laravel nécessite un hébergement PHP avec racine web `backend/public`, une base MySQL et `APP_DEBUG=false`. Construire React avec `npm ci` puis `npm run build`, servir `frontend/dist` et faire suivre `/api` vers Laravel sur le même domaine, comme le proxy de développement Vite. Le jeton est conservé dans le stockage de session de l’onglet et envoyé en Bearer ; utiliser HTTPS et une politique CSP adaptée en production.

Les mots de passe de démonstration doivent être remplacés avant un déploiement réel. Les utilisateurs de consultation peuvent lire tous les dossiers : ce rôle correspond au personnel de scolarité, pas à un portail étudiant personnel.

## Livrables pédagogiques à compléter par le groupe

Le code, les migrations, les exemples et la documentation technique sont présents. Le rapport de 8 à 12 pages, les captures d’écran, la soutenance et le dépôt distant doivent être préparés par le groupe à partir du travail réellement compris et vérifié. Le sujet est utilisé comme cahier des charges ; aucune publication ni aucun envoi à l’enseignant n’a été effectué.
