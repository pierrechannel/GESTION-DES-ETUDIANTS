"""Create a 16:9 PowerPoint with editable text/shapes and speaker notes.
Requires python-pptx (install into .tools/pptx). Existing project diagrams are embedded.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime, timezone
import struct
import xml.etree.ElementTree as ET
import posixpath
import sys
import io
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUTPUT = DOCS / 'Soutenance_Groupe_1_Gestion_Etudiants.pptx'
W,H = 13.333333,7.5
EMU=914400
GREEN='215749'; DARK='173F35'; INK='263831'; MUTED='6D8175'; LIGHT='F2F6F3'; GOLD='D6AC62'; WHITE='FFFFFF'
NS='xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
BASE='http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
slides=[]
media={}


def e(value): return escape(str(value), {'"':'&quot;'})
def n(value): return str(round(value*EMU))
def group():
    return '<p:nvGrpSpPr><p:cNvPr id="1" name="Groupe"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'


class Slide:
    def __init__(self, title, section, notes, duration=45, dark=False):
        self.title,self.section,self.notes,self.duration,self.dark=title,section,notes,duration,dark
        self.shapes=[]; self.relationships=[]; self.index=len(slides)+1; self.sid=2
        slides.append(self)
        self.rect(0,0,W,H,DARK if dark else WHITE)
        self.rect(0,0,.13,H,GOLD if dark else GREEN)
        self.text(.55,.30,11.8,.25,'CAMPUS  /  GROUPE 1     ·     '+section.upper(),11,'B7CCBE' if dark else MUTED,True)
        self.text(.55,.83,12.1,.68,title,29,WHITE if dark else GREEN,True)
        self.line(.55,7.02,12.24,7.02,'47715E' if dark else 'DDE7E0',1)
        self.text(.55,7.1,10.8,.2,'Programmation côté serveur  ·  Laravel + React + MUI',10,'B7CCBE' if dark else MUTED)
        self.text(12.0,7.06,.7,.28,f'{self.index:02}',12,'B7CCBE' if dark else MUTED,True,align='r')
    def shape(self,x,y,w,h,geometry,fill,line=None,body=''):
        sid=self.sid; self.sid+=1
        self.shapes.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Forme {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{n(x)}" y="{n(y)}"/><a:ext cx="{n(w)}" cy="{n(h)}"/></a:xfrm><a:prstGeom prst="{geometry}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln w="9525">'+(f'<a:solidFill><a:srgbClr val="{line}"/></a:solidFill>' if line else '<a:noFill/>')+'</a:ln></p:spPr>'+body+'</p:sp>')
    def rect(self,x,y,w,h,fill,line=None): self.shape(x,y,w,h,'rect',fill,line)
    def line(self,x1,y1,x2,y2,color=GREEN,width=2,arrow=False):
        sid=self.sid; self.sid+=1
        x,y=min(x1,x2),min(y1,y2); w,h=abs(x2-x1),abs(y2-y1)
        flip=(' flipH="1"' if x2<x1 else '')+(' flipV="1"' if y2<y1 else '')
        self.shapes.append(f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid}" name="Lien {sid}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr><a:xfrm{flip}><a:off x="{n(x)}" y="{n(y)}"/><a:ext cx="{n(w)}" cy="{n(h)}"/></a:xfrm><a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="{int(width*12700)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'+('<a:tailEnd type="triangle"/>' if arrow else '')+'</a:ln></p:spPr></p:cxnSp>')
    def text(self,x,y,w,h,value,size=20,color=INK,bold=False,align='l'):
        sid=self.sid; self.sid+=1
        paragraphs=[]
        for line in value.split('\n'):
            paragraphs.append(f'<a:p><a:pPr algn="{align}"><a:lnSpc><a:spcPct val="110000"/></a:lnSpc><a:spaceAfter><a:spcPts val="500"/></a:spaceAfter></a:pPr><a:r><a:rPr lang="fr-FR" sz="{int(size*100)}" b="{int(bold)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{e(line)}</a:t></a:r><a:endParaRPr lang="fr-FR" sz="{int(size*100)}"/></a:p>')
        self.shapes.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Texte {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{n(x)}" y="{n(y)}"/><a:ext cx="{n(w)}" cy="{n(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/>'+''.join(paragraphs)+'</p:txBody></p:sp>')
    def bullets(self,x,y,w,items,size=21,gap=.76,color=INK):
        for i,item in enumerate(items):
            self.text(x,y+i*gap,.22,.5,'•',size,GOLD if self.dark else GREEN,True)
            self.text(x+.30,y+i*gap,w-.3,gap-.08,item,size,color)
    def card(self,x,y,w,h,label,content,number=None):
        self.rect(x,y,w,h,LIGHT)
        self.rect(x,y,.045,h,GREEN)
        offset=.2
        if number:
            self.text(x+.23,y+.19,w-.46,.65,number,34,GREEN,True)
            offset=.95
        self.text(x+.23,y+offset,w-.46,.55,label,19,GREEN,True)
        self.text(x+.23,y+offset+.64,w-.46,h-offset-.74,content,17,INK)
    def picture(self,name):
        data=(DOCS/'diagrammes'/(name+'.png')).read_bytes(); media[name+'.png']=data
        iw,ih=struct.unpack('>II',data[16:24])
        w=min(12.1,5.20*iw/ih); h=w*ih/iw
        x=(W-w)/2; y=1.62
        rid='rIdImage'+str(len(self.relationships)+1)
        self.relationships.append((rid,'image','../media/'+name+'.png'))
        sid=self.sid; self.sid+=1
        self.shapes.append(f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="{name}" descr="{e(self.title)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="{n(x)}" y="{n(y)}"/><a:ext cx="{n(w)}" cy="{n(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    def xml(self):
        return f'<p:sld {NS}><p:cSld><p:spTree>{group()}{"".join(self.shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'


s=Slide('Système de gestion des étudiants','Soutenance',
'40 s — Présenter le groupe et le sujet. Remplacer le champ des membres avant la soutenance. Annoncer le fil conducteur : besoin métier, conception, réalisation et démonstration.',40,True)
s.text(.6,2.05,8.4,1.55,'Accompagner chaque\nparcours étudiant.',37,WHITE,True)
s.text(.63,3.9,8.2,1.1,'Une application de scolarité\nconstruite avec Laravel, React et Material UI.',23,'D1E0D5')
s.rect(10.0,2.12,2.5,2.6,'315D4B')
s.text(10.2,2.35,2.1,1.3,'01',68,GOLD,True,'ctr')
s.text(10.2,3.85,2.1,.4,'GROUPE',18,WHITE,True,'ctr')
s.text(.63,5.55,11.7,.7,'Membres du groupe : à compléter\nTravaux pratiques · Programmation côté serveur · 15 novembre 2026',16,'B7CCBE')

s=Slide('Du fichier Excel à une gestion centralisée','Contexte',
'45 s — Expliquer le contexte du sujet : l’établissement souhaite remplacer ses fichiers Excel. Présenter les risques comme des difficultés possibles de ce mode de gestion, sans inventer une enquête de terrain. Relier chaque objectif à une fonctionnalité.',45)
s.card(.6,1.95,3.85,3.65,'Centraliser','Regrouper les étudiants,\nles formations et les résultats\ndans une même application.','01')
s.card(4.75,1.95,3.85,3.65,'Fiabiliser','Contrôler les matricules,\nles relations entre classes\net matières, et les notes.','02')
s.card(8.9,1.95,3.85,3.65,'Faciliter le suivi','Rechercher un dossier,\nconsulter les statistiques\net imprimer un relevé.','03')
s.text(.65,6.0,11.9,.95,'Objectif : disposer de données cohérentes et de résultats calculés automatiquement.',21,GREEN,True)

s=Slide('Deux rôles pour la scolarité','Acteurs et périmètre',
'45 s — Distinguer l’étudiant, qui est une fiche métier, des comptes de connexion. Les utilisateurs de consultation sont des membres du personnel et voient tous les dossiers. Un visiteur peut s’inscrire ; le serveur impose le rôle user.',45)
s.card(.65,1.95,5.85,3.8,'Utilisateur de scolarité','Consulter, rechercher et filtrer\nConsulter le tableau de bord\nExporter les étudiants en CSV\nConsulter et imprimer les relevés')
s.card(6.8,1.95,5.85,3.8,'Administrateur','Tous les droits de consultation\nGérer étudiants, filières et classes\nGérer les matières et coefficients\nSaisir et corriger les notes')
s.text(.7,6.05,11.8,.55,'Inscription publique → rôle utilisateur uniquement. L’étudiant n’a pas de portail individuel.',19,MUTED)

s=Slide('Une interface séparée de l’API Laravel','Architecture',
'50 s — Suivre le chemin d’une requête depuis React jusqu’à la base. Expliquer le proxy /api en développement et le rôle de Sanctum pour les requêtes authentifiées. MySQL est la cible du TP ; SQLite sert à la démonstration et aux tests.',50)
for x,title,content in [(.65,'React + MUI','Pages, formulaires,\ntables et graphiques'),(4.75,'Laravel + Eloquent','API REST JSON, validation,\nrègles métier et relations'),(8.85,'Base relationnelle','MySQL pour le TP\nSQLite en démonstration')]:
    s.card(x,2.3,3.8,2.2,title,content)
s.line(4.45,3.35,4.73,3.35,GREEN,3,True); s.line(8.55,3.35,8.83,3.35,GREEN,3,True)
s.text(.85,1.83,11.5,.4,'Navigateur                        HTTP /api/v1                         ORM / requêtes préparées',17,MUTED)
s.rect(.65,5.2,12.0,.85,LIGHT)
s.text(.9,5.42,11.5,.5,'Laravel Sanctum : jetons révocables · autorisations admin · mots de passe hachés',20,GREEN,True)

s=Slide('MCD : les entités et leurs cardinalités','Conception des données',
'55 s — Lire les associations principales : une filière contient des classes ; une classe inscrit des étudiants et propose des matières. Une note concerne exactement un étudiant et une matière. Expliquer 0,N et 1,1. Le compte utilisateur est indépendant.',55)
s.picture('mcd')

s=Slide('MLD : six tables métier reliées','Conception des données',
'50 s — Montrer les clés étrangères issues des associations 1,N. Citer les unicités du matricule et des codes, puis les deux unicités composées : classe/filière/année et étudiant/matière/évaluation. Les tables techniques Laravel/Sanctum sont documentées dans le Word.',50)
s.picture('mld')

s=Slide('Les cas d’utilisation du système','Conception fonctionnelle',
'55 s — Distinguer visiteur, utilisateur de scolarité et administrateur. Le triangle représente la généralisation : l’administrateur dispose des droits de consultation en plus des écritures. L’authentification est une précondition des opérations de scolarité.',55)
s.picture('cas-utilisation')

s=Slide('Des contrôles avant chaque enregistrement','Règles métier',
'45 s — Donner un exemple concret de refus : une note de 21/20 ou une matière extérieure à la classe. Expliquer qu’un changement de classe est bloqué si des notes existent. Les validations sont effectuées côté Laravel, même si le formulaire guide aussi la saisie.',45)
s.card(.65,1.95,5.85,1.85,'Identité fiable','Matricule obligatoire et unique.\nCodes des filières et matières uniques.')
s.card(6.8,1.95,5.85,1.85,'Évaluations cohérentes','Note de 0 à 20 ; poids et coefficient positifs.\nUne seule note par étudiant/matière/évaluation.')
s.card(.65,4.1,5.85,1.85,'Classe respectée','La matière évaluée appartient à la classe\nde l’étudiant concerné.')
s.card(6.8,4.1,5.85,1.85,'Relations protégées','Les références bloquent les suppressions.\nSupprimer un étudiant supprime ses notes.')

s=Slide('Des moyennes pondérées, calculées côté serveur','Résultats scolaires',
'55 s — Détailler le premier calcul : (10×1 + 18×3)/4 = 16. Puis pondérer les matières : (16×3 + 12×1)/4 = 15. Insister sur les matières sans note : elles sont exclues et le relevé reste provisoire. L’arrondi final porte sur la moyenne générale.',55)
s.card(.65,1.95,5.85,4.0,'Moyenne par matière','Contrôle : 10/20, poids 1\nExamen : 18/20, poids 3\n\n(10 × 1 + 18 × 3) ÷ 4')
s.text(1.0,5.0,5.1,.8,'16 / 20',36,GREEN,True)
s.card(6.8,1.95,5.85,4.0,'Moyenne générale','Matière A : 16/20, coefficient 3\nMatière B : 12/20, coefficient 1\n\n(16 × 3 + 12 × 1) ÷ 4')
s.text(7.15,5.0,5.1,.8,'15 / 20',36,GREEN,True)
s.text(.7,6.2,11.9,.4,'Sans note : moyenne absente et relevé provisoire. Les moyennes ne sont pas stockées.',18,MUTED)

s=Slide('Un tableau de bord pour suivre les effectifs','Pilotage',
'45 s — Décrire les graphiques réellement présents : courbe des nouveaux dossiers sur six mois, camembert par filière et camembert actif/inactif. Les mois sans inscription sont conservés à zéro. Les dates sont regroupées selon le fuseau Africa/Bujumbura.',45)
s.card(.65,1.95,3.8,3.75,'Inscriptions mensuelles','Courbe sur les six derniers mois\nMois sans inscription à zéro\nComptage à partir de created_at','06')
s.card(4.75,1.95,3.8,3.75,'Répartition par filière','Camembert des effectifs\nNombre et pourcentage\nLégende par formation','%')
s.card(8.85,1.95,3.8,3.75,'Actifs / inactifs','Camembert des statuts\nInfobulles accessibles\nAffichage adapté au mobile','2')
s.text(.7,6.12,11.8,.45,'Compléments : effectifs par classe, totaux et dernières inscriptions.',21,GREEN,True)

s=Slide('Un frontend organisé par responsabilité','Organisation du code',
'40 s — Montrer que main.jsx se limite au démarrage. Chaque page porte ses colonnes et son affichage. EntityList mutualise la recherche, la pagination et les actions CRUD ; les formulaires, graphiques et relevés sont des composants séparés.',40)
s.rect(.65,1.95,5.5,4.65,LIGHT)
s.text(.9,2.15,5.0,4.2,'src/\n  main.jsx       démarrage React\n  App.jsx        sélection de la page\n  pages/         7 pages\n  layouts/       structure commune\n  components/    éléments partagés\n  hooks/         authentification\n  services/      client API\n  config/        rubriques et champs\n  utils/         formatage et CSV',18,INK)
s.bullets(6.6,2.25,5.8,['Un fichier par page métier','Un tableau CRUD réutilisable','Un client HTTP centralisé','Un service Laravel pour les moyennes'],21,.90)

s=Slide('Vérifier les règles, les droits et les calculs','Validation',
'45 s — Présenter les résultats déjà obtenus pendant le développement : 14 tests Laravel et 81 assertions, build React réussi et contrôles de rendu statique après découpage. Les tests utilisent SQLite en mémoire. Ne pas les présenter comme une validation complète dans un navigateur ni comme un test MySQL.',45)
s.card(.65,1.95,3.8,2.75,'Tests Laravel','Permissions, CRUD, filtres,\nunicité, cohérence et moyennes.','14')
s.card(4.75,1.95,3.8,2.75,'Assertions','Dont les mois sans inscription\net les limites de fuseau horaire.','81')
s.card(8.85,1.95,3.8,2.75,'Build React','Compilation de production\net imports vérifiés.','OK')
s.text(.85,4.75,11.5,.55,'Autres contrôles : proxy HTTP, connexion, listes, relevé et révocation du jeton.',20,GREEN,True)
s.text(.85,5.65,11.5,.65,'À compléter sur la cible : vérification MySQL et inspection visuelle dans un navigateur.',20,MUTED)

s=Slide('Démonstration : suivre un dossier de bout en bout','Parcours proposé',
'70 s — Préparer la démonstration avant la soutenance. Ouvrir http://127.0.0.1:5173 après node dev.mjs. Utiliser le compte admin indiqué dans le README. Créer un matricule inédit, choisir une classe puis une de ses matières. Utiliser des notes faciles à recalculer. Terminer avec un compte de consultation pour montrer le contrôle des droits.',70)
steps=[('01','Se connecter','Compte administrateur'),('02','Retrouver un étudiant','Recherche et filtre par filière'),('03','Ajouter un dossier','Matricule unique et classe'),('04','Saisir une note','Matière de la classe et poids'),('05','Ouvrir le relevé','Moyennes et impression'),('06','Vérifier les accès','Compte de consultation')]
for i,(num,label,content) in enumerate(steps):
    x=.65+(i%3)*4.1; y=1.95+(i//3)*2.15
    s.rect(x,y,3.8,1.85,LIGHT)
    s.text(x+.2,y+.16,.6,.45,num,24,GREEN,True)
    s.text(x+.95,y+.18,2.65,.75,label,19,GREEN,True)
    s.text(x+.22,y+1.12,3.35,.5,content,16,INK)
s.text(.7,6.5,11.9,.32,'Jeu d’exemple : 12 étudiants · 3 filières · 6 classes · 18 matières · 36 notes',17,MUTED)

s=Slide('Reproduire et exécuter le projet','Livraison',
'35 s — Présenter la commande de lancement sur le poste déjà préparé. Pour une nouvelle installation, suivre le README : Composer, configuration .env, clé, migrations/seeders et npm ci. Ne pas afficher les mots de passe à l’écran ; ils figurent dans la documentation de démonstration.',35)
s.card(.65,1.95,5.85,3.8,'Démarrage local','Depuis la racine du projet :\n\nnode dev.mjs\n\nInterface : http://127.0.0.1:5173')
s.card(6.8,1.95,5.85,3.8,'Livrables disponibles','Code Laravel et React\nMigrations, seeders et tests\nREADME et collection Postman\nDossier Word : MCD, MLD et cas UML')
s.text(.7,6.07,11.9,.55,'Hébergement cible : serveur PHP + MySQL, frontend compilé et HTTPS.',20,GREEN,True)

s=Slide('Un périmètre clair, des pistes d’évolution','Limites et perspectives',
'40 s — Séparer clairement ce qui existe des évolutions proposées. Le modèle actuel rattache chaque étudiant à une classe courante et ne garde pas d’historique annuel distinct. Les fonctionnalités suivantes restent des perspectives.',40)
s.bullets(.85,2.02,11.7,[
'Historiser les inscriptions et les changements de classe.',
'Introduire les semestres et les périodes d’évaluation.',
'Créer un portail étudiant limité à son propre dossier.',
'Journaliser l’auteur et la date des modifications.',
'Valider MySQL et le rendu navigateur avant le déploiement cible.',
],23,.84)

s=Slide('Des dossiers fiables, des résultats lisibles','Conclusion',
'35 s — Rappeler les trois apports : centralisation, cohérence et consultation. Inviter aux questions. Les détails du modèle et les règles sont disponibles dans le document Word. Renseigner les noms du groupe avant la présentation.',35,True)
s.text(.7,2.0,11.9,1.5,'Centraliser. Contrôler.\nAccompagner les parcours.',36,WHITE,True)
s.text(.75,3.85,11.4,1.5,'Une conception relationnelle expliquée\nUne API Laravel sécurisée par rôles\nUne interface React structurée et accessible',23,'D1E0D5')
s.text(.75,5.65,11.8,1.1,'Merci pour votre attention.\nQuestions et échanges',27,GOLD,True)


# Build the actual package with python-pptx's standard Office template. The
# slide descriptions above are converted to native shapes, not injected XML.
sys.path.insert(0, str(ROOT / '.tools' / 'pptx'))
try:
    from pptx import Presentation
    from pptx.util import Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
    from pptx.oxml.xmlchemy import OxmlElement
except ImportError as error:
    raise SystemExit('Install python-pptx with: python -m pip install --target .tools/pptx python-pptx') from error

namespaces = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

def geometry(element):
    transform = element.find('p:spPr/a:xfrm', namespaces)
    offset = transform.find('a:off', namespaces)
    extent = transform.find('a:ext', namespaces)
    return transform, tuple(int(v) for v in [offset.get('x'), offset.get('y'), extent.get('cx'), extent.get('cy')])


def rgb(value):
    return RGBColor.from_string(value)


def source_shape(source):
    return ET.fromstring('<root '+NS+'>'+source+'</root>')[0]


presentation = Presentation()
presentation.slide_width = 12192000
presentation.slide_height = 6858000
# The explicit dimensions define 16:9 without requiring a size preset.
presentation._element.sldSz.attrib.pop('type', None)
presentation.core_properties.title = 'Groupe 1 - Gestion des etudiants'
presentation.core_properties.subject = 'Soutenance : conception et realisation de Campus'
presentation.core_properties.author = 'Groupe 1'
presentation.core_properties.keywords = 'Laravel, React, MUI, MCD, MLD, scolarite'

for source_slide in slides:
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    for description in source_slide.shapes:
        element = source_shape(description)
        tag = element.tag.rsplit('}', 1)[-1]
        transform, (left, top, width, height) = geometry(element)
        if tag == 'pic':
            name = element.find('p:nvPicPr/p:cNvPr', namespaces).get('name')
            picture = slide.shapes.add_picture(str(DOCS/'diagrammes'/(name+'.png')), left, top, width, height)
            picture.name = name
            picture._element.nvPicPr.cNvPr.set('descr', source_slide.title)
        elif tag == 'cxnSp':
            x1, y1, x2, y2 = left, top, left+width, top+height
            if transform.get('flipH') == '1': x1, x2 = x2, x1
            if transform.get('flipV') == '1': y1, y2 = y2, y1
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
            line = element.find('p:spPr/a:ln', namespaces)
            color = line.find('a:solidFill/a:srgbClr', namespaces)
            if color is not None: connector.line.color.rgb = rgb(color.get('val'))
            connector.line.width = int(line.get('w', '12700'))
            if line.find('a:tailEnd', namespaces) is not None:
                arrow = OxmlElement('a:tailEnd')
                arrow.set('type', 'triangle')
                connector._element.spPr.get_or_add_ln().append(arrow)
        elif tag == 'sp':
            body = element.find('p:txBody', namespaces)
            if body is not None:
                shape = slide.shapes.add_textbox(left, top, width, height)
                frame = shape.text_frame
                frame.clear()
                frame.word_wrap = True
                frame.auto_size = MSO_AUTO_SIZE.NONE
                frame.vertical_anchor = MSO_ANCHOR.TOP
                frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
                for index, paragraph_xml in enumerate(body.findall('a:p', namespaces)):
                    paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
                    props = paragraph_xml.find('a:pPr', namespaces)
                    align = props.get('algn', 'l') if props is not None else 'l'
                    paragraph.alignment = {'l': PP_ALIGN.LEFT, 'ctr': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
                    paragraph.line_spacing = 1.1
                    paragraph.space_after = Pt(5)
                    for run_xml in paragraph_xml.findall('a:r', namespaces):
                        item = paragraph.add_run()
                        item.text = run_xml.find('a:t', namespaces).text or ''
                        formatting = run_xml.find('a:rPr', namespaces)
                        item.font.name = 'Arial'
                        item.font.size = Pt(int(formatting.get('sz'))/100)
                        item.font.bold = formatting.get('b') == '1'
                        color = formatting.find('a:solidFill/a:srgbClr', namespaces)
                        if color is not None: item.font.color.rgb = rgb(color.get('val'))
            else:
                shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
                fill = element.find('p:spPr/a:solidFill/a:srgbClr', namespaces)
                shape.fill.solid()
                shape.fill.fore_color.rgb = rgb(fill.get('val'))
                border = element.find('p:spPr/a:ln/a:solidFill/a:srgbClr', namespaces)
                if border is None:
                    shape.line.fill.background()
                else:
                    shape.line.color.rgb = rgb(border.get('val'))
                    shape.line.width = Pt(.75)
        else:
            raise ValueError('Unsupported shape: '+tag)
    slide.notes_slide.notes_text_frame.text = source_slide.title+'\n\n'+source_slide.notes+'\n\nSources : README.md, migrations et code du projet.'

# Preserve the previous file locally for diagnosis, outside the deliverables.
backup = ROOT/'.tools'/'repair'/'presentation_previous.pptx'
if OUTPUT.exists() and not backup.exists():
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT, backup)
corrected = OUTPUT.with_stem(OUTPUT.stem+'_CORRIGE')
presentation.save(corrected)
# Reopen the output using the presentation library and inspect all content.
reopened = Presentation(corrected)
assert len(reopened.slides) == 16
assert sum(1 for slide in reopened.slides for shape in slide.shapes if shape.shape_type == 13) == 3
for expected, actual in zip(slides, reopened.slides):
    assert len(actual.shapes) == len(expected.shapes)
    assert expected.notes in actual.notes_slide.notes_text_frame.text
    for shape in actual.shapes:
        if shape.has_text_frame:
            assert shape.text_frame is not None
with ZipFile(corrected) as archive:
    assert archive.testzip() is None
    for name in archive.namelist():
        if name.endswith('.xml') or name.endswith('.rels'): ET.fromstring(archive.read(name))
shutil.copy2(corrected, OUTPUT)
notes=['# Guide de soutenance ? Groupe 1','',f'{len(slides)} diapositives ? dur?e indicative : {sum(s.duration for s in slides)//60} min {sum(s.duration for s in slides)%60} s.','', 'Compl?ter les membres du groupe sur la premi?re diapositive avant la pr?sentation.','']
for s in slides: notes += [f'## {s.index:02}. {s.title}', '', s.notes, '']
(DOCS/'Guide_Soutenance_Groupe_1.md').write_text('\n'.join(notes),encoding='utf-8')
print(f'Rebuilt {corrected.name}: {len(reopened.slides)} slides, 16 notes, 3 diagrams.')
print('Saved with python-pptx, reopened and inspected successfully; original link updated.')
