# Guide de soutenance ? Groupe 1

16 diapositives ? dur?e indicative : 12 min 30 s.

Compl?ter les membres du groupe sur la premi?re diapositive avant la pr?sentation.

## 01. Système de gestion des étudiants

40 s — Présenter le groupe et le sujet. Remplacer le champ des membres avant la soutenance. Annoncer le fil conducteur : besoin métier, conception, réalisation et démonstration.

## 02. Du fichier Excel à une gestion centralisée

45 s — Expliquer le contexte du sujet : l’établissement souhaite remplacer ses fichiers Excel. Présenter les risques comme des difficultés possibles de ce mode de gestion, sans inventer une enquête de terrain. Relier chaque objectif à une fonctionnalité.

## 03. Deux rôles pour la scolarité

45 s — Distinguer l’étudiant, qui est une fiche métier, des comptes de connexion. Les utilisateurs de consultation sont des membres du personnel et voient tous les dossiers. Un visiteur peut s’inscrire ; le serveur impose le rôle user.

## 04. Une interface séparée de l’API Laravel

50 s — Suivre le chemin d’une requête depuis React jusqu’à la base. Expliquer le proxy /api en développement et le rôle de Sanctum pour les requêtes authentifiées. MySQL est la cible du TP ; SQLite sert à la démonstration et aux tests.

## 05. MCD : les entités et leurs cardinalités

55 s — Lire les associations principales : une filière contient des classes ; une classe inscrit des étudiants et propose des matières. Une note concerne exactement un étudiant et une matière. Expliquer 0,N et 1,1. Le compte utilisateur est indépendant.

## 06. MLD : six tables métier reliées

50 s — Montrer les clés étrangères issues des associations 1,N. Citer les unicités du matricule et des codes, puis les deux unicités composées : classe/filière/année et étudiant/matière/évaluation. Les tables techniques Laravel/Sanctum sont documentées dans le Word.

## 07. Les cas d’utilisation du système

55 s — Distinguer visiteur, utilisateur de scolarité et administrateur. Le triangle représente la généralisation : l’administrateur dispose des droits de consultation en plus des écritures. L’authentification est une précondition des opérations de scolarité.

## 08. Des contrôles avant chaque enregistrement

45 s — Donner un exemple concret de refus : une note de 21/20 ou une matière extérieure à la classe. Expliquer qu’un changement de classe est bloqué si des notes existent. Les validations sont effectuées côté Laravel, même si le formulaire guide aussi la saisie.

## 09. Des moyennes pondérées, calculées côté serveur

55 s — Détailler le premier calcul : (10×1 + 18×3)/4 = 16. Puis pondérer les matières : (16×3 + 12×1)/4 = 15. Insister sur les matières sans note : elles sont exclues et le relevé reste provisoire. L’arrondi final porte sur la moyenne générale.

## 10. Un tableau de bord pour suivre les effectifs

45 s — Décrire les graphiques réellement présents : courbe des nouveaux dossiers sur six mois, camembert par filière et camembert actif/inactif. Les mois sans inscription sont conservés à zéro. Les dates sont regroupées selon le fuseau Africa/Bujumbura.

## 11. Un frontend organisé par responsabilité

40 s — Montrer que main.jsx se limite au démarrage. Chaque page porte ses colonnes et son affichage. EntityList mutualise la recherche, la pagination et les actions CRUD ; les formulaires, graphiques et relevés sont des composants séparés.

## 12. Vérifier les règles, les droits et les calculs

45 s — Présenter les résultats déjà obtenus pendant le développement : 14 tests Laravel et 81 assertions, build React réussi et contrôles de rendu statique après découpage. Les tests utilisent SQLite en mémoire. Ne pas les présenter comme une validation complète dans un navigateur ni comme un test MySQL.

## 13. Démonstration : suivre un dossier de bout en bout

70 s — Préparer la démonstration avant la soutenance. Ouvrir http://127.0.0.1:5173 après node dev.mjs. Utiliser le compte admin indiqué dans le README. Créer un matricule inédit, choisir une classe puis une de ses matières. Utiliser des notes faciles à recalculer. Terminer avec un compte de consultation pour montrer le contrôle des droits.

## 14. Reproduire et exécuter le projet

35 s — Présenter la commande de lancement sur le poste déjà préparé. Pour une nouvelle installation, suivre le README : Composer, configuration .env, clé, migrations/seeders et npm ci. Ne pas afficher les mots de passe à l’écran ; ils figurent dans la documentation de démonstration.

## 15. Un périmètre clair, des pistes d’évolution

40 s — Séparer clairement ce qui existe des évolutions proposées. Le modèle actuel rattache chaque étudiant à une classe courante et ne garde pas d’historique annuel distinct. Les fonctionnalités suivantes restent des perspectives.

## 16. Des dossiers fiables, des résultats lisibles

35 s — Rappeler les trois apports : centralisation, cohérence et consultation. Inviter aux questions. Les détails du modèle et les règles sont disponibles dans le document Word. Renseigner les noms du groupe avant la présentation.
