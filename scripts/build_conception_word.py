"""Build an editable OOXML Word document using the project model and embedded diagrams.
Uses only the Python standard library; diagrams must be rendered first.
"""
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUTPUT = DOCS / 'Conception_Groupe_1_MCD_MLD_Cas_Utilisation.docx'
GREEN = '215749'


def text(value):
    return escape(str(value))


def run(value, bold=False, color=None, size=None):
    props = ('<w:b/>' if bold else '')
    if color: props += f'<w:color w:val="{color}"/>'
    if size: props += f'<w:sz w:val="{size}"/>'
    lines = str(value).split('\n')
    content = '<w:br/>'.join(f'<w:t xml:space="preserve">{text(line)}</w:t>' for line in lines)
    return f'<w:r><w:rPr>{props}</w:rPr>{content}</w:r>'


def para(value='', style=None, bold=False, color=None, size=None, center=False):
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else '')
    if center: ppr += '<w:jc w:val="center"/>'
    return f'<w:p><w:pPr>{ppr}</w:pPr>{run(value,bold,color,size)}</w:p>'


def title(value): return para(value, 'Heading1')
def subtitle(value): return para(value, 'Heading2')
def pagebreak(): return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def table(headers, rows, widths=None):
    widths = widths or [int(9600/len(headers))] * len(headers)
    xml = '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
    for border in ['top','left','bottom','right','insideH','insideV']:
        xml += f'<w:{border} w:val="single" w:sz="4" w:color="DCE5DF"/>'
    xml += '</w:tblBorders><w:tblCellMar><w:top w:w="65" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="65" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    xml += '<w:tblGrid>'+''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)+'</w:tblGrid>'
    for i,row in enumerate([headers]+rows):
        xml += '<w:tr><w:trPr><w:cantSplit/>'+('<w:tblHeader/>' if i==0 else '')+'</w:trPr>'
        for j,cell in enumerate(row):
            fill=GREEN if i==0 else ('F3F7F4' if i%2==0 else 'FFFFFF')
            xml+=f'<w:tc><w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/><w:shd w:fill="{fill}"/><w:vAlign w:val="center"/></w:tcPr>'
            xml+='<w:p><w:pPr><w:spacing w:after="0" w:line="230" w:lineRule="auto"/></w:pPr>'+run(cell,i==0,'FFFFFF' if i==0 else '263831',18)+'</w:p></w:tc>'
        xml+='</w:tr>'
    return xml+'</w:tbl>'+para('','Spacer')


def section(landscape=False, final=False):
    size='<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>' if landscape else '<w:pgSz w:w="11906" w:h="16838"/>'
    margin=720 if landscape else 1000
    result='<w:sectPr><w:headerReference w:type="default" r:id="rIdHeader"/><w:footerReference w:type="default" r:id="rIdFooter"/><w:type w:val="nextPage"/>'+size+f'<w:pgMar w:top="{margin}" w:right="{margin}" w:bottom="{margin}" w:left="{margin}" w:header="350" w:footer="350"/><w:cols w:space="708"/></w:sectPr>'
    return result if final else '<w:p><w:pPr>'+result+'</w:pPr></w:p>'


images=[]
def picture(name, alt, width=9.8):
    image=DOCS/'diagrammes'/(name+'.png')
    b=image.read_bytes()
    if b[:8] != b'\x89PNG\r\n\x1a\n': raise ValueError(f'Invalid PNG: {image}')
    w,h=struct.unpack('>II',b[16:24])
    cx=int(width*914400); cy=int(cx*h/w)
    index=len(images)+1; rid=f'rIdImage{index}'
    images.append((rid,name+'.png',b))
    return f'''<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="80"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{index}" name="{text(name)}" descr="{text(alt)}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="{index}" name="{name}.png"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''


body=[]
add=body.append
# Cover, portrait.
add(para('CAMPUS  /  GROUPE 1', 'Kicker'))
add(para('DOSSIER DE CONCEPTION', 'Subtitle'))
add(para('Système de gestion\ndes étudiants', 'Title'))
add(para('MCD • MLD • Diagramme de cas d’utilisation', 'Subtitle'))
add(para('Travaux pratiques — Programmation côté serveur', size=24))
add(para('Laravel · Eloquent · Sanctum · React · Material UI', color=GREEN, size=24))
add(para(''))
add(table(['Repère','Description'],[
    ['Sujet','Groupe 1 — Système de gestion des étudiants'],
    ['Finalité','Remplacer les fichiers Excel par une gestion centralisée des dossiers et résultats.'],
    ['Base cible','MySQL ; SQLite pour la démonstration locale et les tests.'],
    ['Version','1.0 — 15 novembre 2026'],
    ['Membres du groupe','À compléter par le groupe'],
],[2400,7400]))
add(para('Document établi à partir des migrations, modèles Eloquent, routes et règles de calcul présents dans le projet. Les diagrammes décrivent la version implémentée.', 'Note'))
add(pagebreak())
# Scope and rules, portrait.
add(title('1. Périmètre et règles de gestion'))
add(para('Le système couvre l’inscription administrative des étudiants, l’organisation des filières et classes, les matières et leurs coefficients, les évaluations et l’édition des relevés. Une classe représente un groupe pour une année académique.'))
add(subtitle('1.1 Acteurs et responsabilités'))
add(table(['Acteur','Responsabilité'],[
    ['Visiteur','Créer un compte de consultation et se connecter.'],
    ['Utilisateur de scolarité','Consulter les dossiers, rechercher et filtrer, consulter les statistiques, exporter la liste des étudiants et imprimer les relevés.'],
    ['Administrateur','Posséder les droits de consultation et gérer les étudiants, filières, classes, matières et notes.'],
],[2600,7200]))
add(para('L’étudiant est une donnée métier. Il n’est pas un acteur connecté de cette version : aucun lien entre users et students n’est imposé. Le rôle est un attribut du compte ; il ne nécessite pas de table roles.', 'Note'))
add(subtitle('1.2 Règles structurantes'))
for v in [
    'RG01 — Chaque classe appartient à une seule filière ; une filière peut ne contenir aucune classe ou en contenir plusieurs.',
    'RG02 — Chaque étudiant appartient à une seule classe ; une classe peut accueillir zéro à plusieurs étudiants.',
    'RG03 — Chaque matière appartient à une seule classe ; une classe propose zéro à plusieurs matières.',
    'RG04 — Une note correspond à un étudiant, une matière et un libellé d’évaluation. Ce triplet est unique.',
    'RG05 — Une note est comprise entre 0 et 20. Son poids et le coefficient d’une matière sont compris entre 0,01 et 100.',
    'RG06 — La matière évaluée doit appartenir à la classe de l’étudiant. Matricule, codes de filière et de matière sont uniques.',
    'RG07 — Le couple de comptes admin/user limite les écritures aux administrateurs. L’inscription publique ne donne jamais le rôle administrateur.',
]: add(para(v))
add(section(False))
# Diagram pages, landscape.
add(title('2. Modèle conceptuel des données — MCD'))
add(para('Notation Merise : les cardinalités sont placées près des entités ; les associations n’introduisent pas de clé étrangère dans le modèle conceptuel.'))
add(picture('mcd','MCD Merise : filière contient classe ; classe inscrit étudiant et propose matière ; étudiant obtient note ; matière évalue note. Utilisateur indépendant.'))
add(para('Lecture : 0,N = aucune à plusieurs occurrences ; 1,1 = exactement une occurrence. Une note a exactement un étudiant et une matière. Le symbole # repère l’identifiant.', 'Caption'))
add(pagebreak())
add(title('3. Modèle logique des données — MLD'))
add(para('Passage au relationnel : chaque association 1,N se traduit par une clé étrangère du côté de l’entité portant la cardinalité 1,1. Les noms correspondent aux tables Laravel.'))
add(picture('mld','MLD relationnel des six tables principales et flèches des clés étrangères vers leurs clés primaires référencées.'))
add(para('Unicités composées : school_classes(program_id, name, academic_year) ; grades(student_id, subject_id, assessment). Les colonnes techniques et les types sont détaillés aux pages suivantes.', 'Caption'))
add(pagebreak())
add(title('4. Diagramme UML des cas d’utilisation'))
add(para('La frontière encadre les fonctionnalités de Campus. Les traits relient un acteur à ses cas d’utilisation ; le triangle ouvert indique que l’administrateur hérite des droits de l’utilisateur.'))
add(picture('cas-utilisation','Diagramme UML : visiteur, utilisateur de scolarité et administrateur ; consultation partagée et gestion réservée aux administrateurs.'))
add(para('Les opérations de scolarité exigent une authentification préalable. Les ellipses ocre correspondent aux droits d’écriture supplémentaires de l’administrateur.', 'Caption'))
add(section(True))
# Dictionary 1, portrait.
add(title('5. Dictionnaire des données'))
add(para('Les types ci-dessous représentent la cible MySQL des migrations. PK = clé primaire ; FK = clé étrangère ; UQ = unique ; NULL = valeur facultative. Les identifiants sont des BIGINT UNSIGNED auto-incrémentés.'))
headers=['Attribut','Type MySQL','NULL','Règle / référence']
widths=[2800,2150,650,4300]
add(subtitle('5.1 users — comptes du personnel'))
add(table(headers,[
    ['id','BIGINT UNSIGNED','Non','PK'],['name','VARCHAR(255)','Non','Nom du compte'],
    ['email','VARCHAR(255)','Non','UQ ; adresse e-mail valide'],['password','VARCHAR(255)','Non','Mot de passe haché par Laravel'],
    ['role','VARCHAR(255)','Non','Défaut user ; valeurs applicatives user/admin'],
    ['email_verified_at','TIMESTAMP','Oui','Colonne technique Laravel, sans parcours de vérification activé'],
    ['remember_token','VARCHAR(100)','Oui','Colonne technique Laravel ; connexion par jeton Sanctum'],
],widths))
add(subtitle('5.2 programs — filières'))
add(table(headers,[
    ['id','BIGINT UNSIGNED','Non','PK'],['name','VARCHAR(255)','Non','Nom de la filière'],
    ['code','VARCHAR(255)','Non','UQ'],['description','TEXT','Oui','Description facultative'],
],widths))
add(subtitle('5.3 school_classes — classes'))
add(table(headers,[
    ['id','BIGINT UNSIGNED','Non','PK'],['program_id','BIGINT UNSIGNED','Non','FK → programs.id ; suppression restreinte'],
    ['name','VARCHAR(255)','Non','Nom de la classe'],['academic_year','VARCHAR(255)','Non','Format applicatif AAAA-AAAA'],
],widths))
add(para('Contrainte UQ composite : program_id + name + academic_year. Les limites de saisie peuvent être plus strictes que la capacité des colonnes SQL (par exemple name : 150 caractères pour une filière).', 'Note'))
add(pagebreak())
# Dictionary 2.
add(title('5. Dictionnaire des données — suite'))
add(subtitle('5.4 students — dossiers étudiants'))
add(table(headers,[
    ['id','BIGINT UNSIGNED','Non','PK'],['school_class_id','BIGINT UNSIGNED','Non','FK → school_classes.id ; suppression restreinte'],
    ['registration_number','VARCHAR(255)','Non','UQ ; matricule obligatoire'],
    ['first_name / last_name','VARCHAR(255) chacun','Non','Prénom et nom'],
    ['email','VARCHAR(255)','Oui','UQ si renseigné ; adresse valide'],
    ['phone','VARCHAR(255)','Oui','Téléphone'],['birth_date','DATE','Oui','Date non postérieure à aujourd’hui'],
    ['status','VARCHAR(255)','Non','Défaut active ; active/inactive'],
],widths))
add(subtitle('5.5 subjects — matières'))
add(table(headers,[
    ['id','BIGINT UNSIGNED','Non','PK'],['school_class_id','BIGINT UNSIGNED','Non','FK → school_classes.id ; suppression restreinte'],
    ['name / code','VARCHAR(255) chacun','Non','Code UQ'],['coefficient','DECIMAL(6,2)','Non','Défaut 1 ; validation 0,01..100'],
],widths))
add(subtitle('5.6 grades — notes d’évaluation'))
add(table(headers,[
    ['id','BIGINT UNSIGNED','Non','PK'],['student_id','BIGINT UNSIGNED','Non','FK → students.id ; suppression en cascade'],
    ['subject_id','BIGINT UNSIGNED','Non','FK → subjects.id ; suppression restreinte'],
    ['assessment','VARCHAR(255)','Non','Libellé de l’évaluation'],['score','DECIMAL(5,2)','Non','Validation 0..20'],
    ['weight','DECIMAL(6,2)','Non','Défaut 1 ; validation 0,01..100'],
],widths))
add(para('UQ composite : student_id + subject_id + assessment. Toutes les tables métier ont created_at et updated_at (TIMESTAMP, facultatifs dans les migrations). Les bornes numériques et la cohérence de classe sont vérifiées côté Laravel.', 'Note'))
add(pagebreak())
# Scenarios.
add(title('6. Description des cas d’utilisation'))
add(table(['Cas','Acteur','Résultat / condition'],[
    ['UC01 — S’inscrire','Visiteur','Compte user créé après validation et hachage du mot de passe.'],
    ['UC02 — Se connecter','Visiteur','Identifiants contrôlés ; jeton Sanctum valable 8 heures.'],
    ['UC03 — Se déconnecter','Utilisateur / admin','Jeton courant révoqué.'],
    ['UC04 — Consulter et rechercher','Utilisateur / admin','Listes filtrées et paginées ; accès aux fiches.'],
    ['UC05 — Consulter le relevé','Utilisateur / admin','Notes, moyennes pondérées et relevé imprimable.'],
    ['UC06 — Exporter en CSV','Utilisateur / admin','Tous les étudiants correspondant aux filtres, sur toutes les pages.'],
    ['UC07 — Consulter les statistiques','Utilisateur / admin','Effectifs, inscriptions mensuelles et répartitions par filière/statut.'],
    ['UC08 — Gérer les dossiers et référentiels','Administrateur','Créer, lire, modifier et supprimer étudiants, filières, classes et matières.'],
    ['UC09 — Gérer les notes','Administrateur','Créer, modifier et supprimer les évaluations après contrôles métier.'],
],[2750,1800,5350]))
add(subtitle('Scénario A — Enregistrer un étudiant'))
add(para('L’administrateur ouvre la page Étudiants, clique sur Ajouter, remplit l’identité, le matricule et la classe puis valide. Laravel vérifie les champs et l’unicité ; le dossier est créé et la liste est actualisée. En cas de doublon, le formulaire affiche une erreur sur le matricule.'))
add(subtitle('Scénario B — Saisir une note'))
add(para('L’administrateur choisit l’étudiant puis une matière de sa classe, indique l’évaluation, la note sur 20 et le poids. Le serveur vérifie les bornes, la classe et l’unicité du triplet. Une note invalide est refusée sans enregistrement.'))
add(subtitle('Scénario C — Imprimer un relevé'))
add(para('Un utilisateur authentifié ouvre la fiche d’un étudiant. Le serveur calcule les moyennes ; l’interface affiche les évaluations et indique si le relevé est provisoire. L’utilisateur imprime ou enregistre le document en PDF avec le navigateur.'))
add(pagebreak())
# Details and sources.
add(title('7. Calculs, intégrité et limites'))
add(subtitle('7.1 Moyennes calculées, sans stockage redondant'))
add(para('Moyenne d’une matière = Σ(note × poids d’évaluation) / Σ(poids d’évaluation).', bold=True, color=GREEN))
add(para('Moyenne générale = Σ(moyenne matière × coefficient matière) / Σ(coefficients des matières notées).', bold=True, color=GREEN))
add(para('Exemple : une matière avec 10/20 de poids 1 et 18/20 de poids 3 a une moyenne de 16/20. Avec une autre matière à 12/20, les coefficients 3 et 1 donnent une moyenne générale de (16 × 3 + 12 × 1) / 4 = 15/20.'))
add(para('Une matière sans note reste sans moyenne et est exclue du calcul général. Le relevé est provisoire tant que toutes les matières de la classe ne sont pas notées. Sans matière notée, la moyenne générale est absente ; elle ne vaut pas zéro. La moyenne générale finale est arrondie à deux décimales.'))
add(subtitle('7.2 Intégrité et suppression'))
add(para('Un étudiant ou une matière ayant des notes ne peut pas changer de classe avant retrait de ses notes. Une filière, classe ou matière encore référencée ne peut pas être supprimée. La suppression confirmée d’un étudiant entraîne celle de ses notes. Les droits sont contrôlés par les middlewares auth:sanctum et admin.'))
add(subtitle('7.3 Tables techniques et limites du modèle'))
add(para('Sanctum ajoute personal_access_tokens : id, tokenable_type, tokenable_id, name, token unique haché, abilities, last_used_at, expires_at et horodatages. Le lien au compte est polymorphe, avec index ; ce n’est pas une FK SQL classique. Un compte peut posséder zéro à plusieurs jetons.'))
add(para('Laravel crée aussi sessions, password_reset_tokens et des tables de cache/file de tâches. Leur présence technique ne signifie pas que les parcours de vérification d’e-mail ou de réinitialisation du mot de passe sont implémentés. Elles ne constituent pas des entités métier du MCD.'))
add(para('Cette version gère une classe courante par étudiant, sans historique des changements de classe, sans inscription annuelle distincte et sans semestre. Les utilisateurs de consultation voient tous les dossiers ; aucun portail étudiant individuel ni journal d’auteur des modifications n’est prévu.'))
add(subtitle('7.4 Traçabilité de la conception'))
add(para('Sources internes : migrations create_school_tables et create_users_table ; migration personal_access_tokens ; modèles dans backend/app/Models ; SchoolController, AuthController et AdminOnly ; TranscriptService ; backend/routes/api.php ; pages React et DashboardCharts.'))
add(para('Les diagrammes PNG sont intégrés au fichier Word. Leurs versions SVG et leurs descriptions de dessin restent disponibles dans docs/diagrammes pour adaptation. La conception doit être mise à jour si les règles ou les migrations évoluent.', 'Note'))
add(section(False,final=True))

NS='''xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'''
document='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '+NS+'><w:body>'+''.join(body)+'</w:body></w:document>'
styles=f'''<?xml version="1.0" encoding="UTF-8"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="263831"/><w:sz w:val="21"/><w:lang w:val="fr-FR"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="130" w:line="270" w:lineRule="auto"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="700" w:after="320"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:color w:val="{GREEN}"/><w:sz w:val="60"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:rPr><w:color w:val="658372"/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Kicker"><w:name w:val="Kicker"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:color w:val="{GREEN}"/><w:sz w:val="22"/><w:spacing w:val="35"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="120" w:after="180"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="{GREEN}"/><w:sz w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="180" w:after="90"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="{GREEN}"/><w:sz w:val="25"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="60" w:after="100"/></w:pPr><w:rPr><w:color w:val="607368"/><w:sz w:val="19"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="90"/></w:pPr><w:rPr><w:i/><w:color w:val="607368"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Spacer"><w:name w:val="Spacer"/><w:pPr><w:spacing w:after="20" w:line="80" w:lineRule="exact"/></w:pPr><w:rPr><w:sz w:val="2"/></w:rPr></w:style></w:styles>'''
rels=[('rIdStyles','styles','styles.xml'),('rIdSettings','settings','settings.xml'),('rIdHeader','header','header1.xml'),('rIdFooter','footer','footer1.xml')]
rels += [(rid,'image','media/'+name) for rid,name,b in images]
relationship_xml='<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{typ}" Target="{target}"/>' for rid,typ,target in rels)+'</Relationships>'
content_types='''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'''
for part,typ in [('document','document.main'),('styles','styles'),('settings','settings'),('header1','header'),('footer1','footer')]:
    content_types+=f'<Override PartName="/word/{part}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.{typ}+xml"/>'
content_types+='<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'
header=f'<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">{para("CAMPUS  /  GROUPE 1                                                DOSSIER DE CONCEPTION",color=GREEN,size=16)}</w:hdr>'
footer='<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="right"/></w:pPr>'+run('MCD · MLD · Cas d’utilisation     |     ',color='607368',size=16)+'<w:fldSimple w:instr="PAGE"><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>'
core='''<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Groupe 1 — Conception du système de gestion des étudiants</dc:title><dc:creator>Groupe 1</dc:creator><dc:language>fr-FR</dc:language><dc:description>MCD, MLD, dictionnaire des données et cas d’utilisation de Campus.</dc:description></cp:coreProperties>'''
parts={
    '[Content_Types].xml':content_types,
    '_rels/.rels':'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>',
    'word/document.xml':document, 'word/styles.xml':styles, 'word/_rels/document.xml.rels':relationship_xml,
    'word/header1.xml':header,'word/footer1.xml':footer,'docProps/core.xml':core,
    'word/settings.xml':'<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:updateFields w:val="true"/><w:defaultTabStop w:val="720"/></w:settings>',
}
for name,xml in parts.items(): ET.fromstring(xml)
with ZipFile(OUTPUT,'w',ZIP_DEFLATED) as archive:
    for name,xml in parts.items(): archive.writestr(name,xml.encode('utf-8'))
    for rid,name,b in images: archive.writestr('word/media/'+name,b)
with ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    assert len([p for p in archive.namelist() if p.startswith('word/media/')])==3
print(f'Created {OUTPUT.name}: {OUTPUT.stat().st_size:,} bytes, 3 embedded diagrams, XML and ZIP verified.')
