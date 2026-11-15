import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'diagrammes'
GREEN = '#215749'
INK = '#263831'

class Diagram:
    def __init__(self, name, height=820):
        self.name, self.width, self.height, self.shapes = name, 1500, height, []
    def rect(self, x, y, w, h, fill='#ffffff', stroke='#cad7cf'):
        self.shapes.append(dict(type='rect', x=x, y=y, w=w, h=h, fill=fill, stroke=stroke))
    def ellipse(self, x, y, w, h, fill='#edf4ef', stroke=GREEN):
        self.shapes.append(dict(type='ellipse', x=x, y=y, w=w, h=h, fill=fill, stroke=stroke))
    def text(self, x, y, w, h, text, size=22, color=INK, bold=False, align='left'):
        self.shapes.append(dict(type='text', x=x, y=y, w=w, h=h, text=text, size=size, color=color, bold=bold, align=align))
    def line(self, points, color=GREEN, arrow=False, hollow=False, dash=False):
        self.shapes.append(dict(type='line', points=points, color=color, arrow=arrow, hollow=hollow, dash=dash))
    def box(self, x, y, w, h, title, rows):
        self.rect(x, y, w, h, '#f7faf8')
        self.rect(x, y, w, 48, GREEN, GREEN)
        self.text(x+8, y+4, w-16, 38, title, 25, '#ffffff', True, 'center')
        for i, row in enumerate(rows):
            self.text(x+15, y+57+i*29, w-30, 28, row, 22)
    def association(self, x, y, title):
        self.ellipse(x, y, 170, 70)
        self.text(x+4, y+5, 162, 60, title, 21, GREEN, True, 'center')
    def cardinal(self, x, y, text):
        self.text(x, y, 58, 30, text, 22, GREEN, True, 'center')
    def actor(self, x, y, name):
        self.ellipse(x-17, y, 34, 34, '#ffffff', INK)
        self.line([(x, y+34), (x, y+85)], INK)
        self.line([(x-32, y+52), (x+32, y+52)], INK)
        self.line([(x, y+85), (x-27, y+118)], INK)
        self.line([(x, y+85), (x+27, y+118)], INK)
        self.text(x-104, y+122, 208, 65, name, 21, INK, True, 'center')
    def usecase(self, cx, cy, label, admin=False):
        self.ellipse(cx-140, cy-40, 280, 80, '#fbf4e8' if admin else '#edf4ef', '#a47c35' if admin else GREEN)
        self.text(cx-130, cy-34, 260, 68, label, 21, INK, False, 'center')
    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / (self.name+'.json')).write_text(json.dumps(dict(width=self.width, height=self.height, shapes=self.shapes), ensure_ascii=False), encoding='utf-8')
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">', '<rect width="100%" height="100%" fill="white"/>']
        for s in self.shapes:
            t = s['type']
            if t == 'rect':
                svg.append(f'<rect x="{s["x"]}" y="{s["y"]}" width="{s["w"]}" height="{s["h"]}" fill="{s["fill"]}" stroke="{s["stroke"]}" stroke-width="2"/>')
            elif t == 'ellipse':
                svg.append(f'<ellipse cx="{s["x"]+s["w"]/2}" cy="{s["y"]+s["h"]/2}" rx="{s["w"]/2}" ry="{s["h"]/2}" fill="{s["fill"]}" stroke="{s["stroke"]}" stroke-width="2"/>')
            elif t == 'line':
                pts = s['points']
                svg.append(f'<polyline points="{" ".join(str(x)+","+str(y) for x,y in pts)}" fill="none" stroke="{s["color"]}" stroke-width="2"'+(' stroke-dasharray="8 5"' if s['dash'] else '')+'/>')
                if s['arrow'] or s['hollow']:
                    import math
                    (ax,ay),(bx,by)=pts[-2:]
                    a=math.atan2(by-ay,bx-ax)
                    length=20 if s['hollow'] else 13
                    points=[(bx,by),(bx-length*math.cos(a)+length*.45*math.sin(a),by-length*math.sin(a)-length*.45*math.cos(a)),(bx-length*math.cos(a)-length*.45*math.sin(a),by-length*math.sin(a)+length*.45*math.cos(a))]
                    svg.append(f'<polygon points="{" ".join(str(x)+","+str(y) for x,y in points)}" fill="{"white" if s["hollow"] else s["color"]}" stroke="{s["color"]}" stroke-width="2"/>')
            elif t == 'text':
                lines=s['text'].split('\n')
                anchor='middle' if s['align']=='center' else 'start'
                x=s['x']+s['w']/2 if anchor=='middle' else s['x']
                base=s['y']+(s['h']-len(lines)*s['size']*1.2)/2+s['size']
                for i,line in enumerate(lines):
                    svg.append(f'<text x="{x}" y="{base+i*s["size"]*1.2}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{s["size"]}" fill="{s["color"]}" font-weight="{"bold" if s["bold"] else "normal"}">{escape(line)}</text>')
        (OUT/(self.name+'.svg')).write_text('\n'.join(svg+['</svg>']), encoding='utf-8')

def prepare_diagrams():
    d=Diagram('mcd')
    d.line([(325,190),(590,190)])
    d.line([(900,190),(1180,190)])
    d.line([(745,300),(745,510)])
    d.line([(900,635),(1180,635)])
    d.line([(1325,300),(1325,530)])
    d.box(35,100,290,190,'FILIÈRE',['# id_filière','nom','code','description'])
    d.box(590,100,310,200,'CLASSE',['# id_classe','nom','année_académique'])
    d.box(1180,100,290,200,'MATIÈRE',['# id_matière','nom','code','coefficient'])
    d.box(590,510,310,280,'ÉTUDIANT',['# id_étudiant','matricule','prénom, nom','e-mail, téléphone','date_naissance','statut'])
    d.box(1180,530,290,215,'NOTE',['# id_note','libellé_évaluation','valeur_sur_20','poids_évaluation'])
    d.box(35,530,290,215,'UTILISATEUR',['# id_utilisateur','nom','e-mail','mot_de_passe_haché','rôle'])
    d.association(365,155,'Contenir')
    d.association(960,155,'Proposer')
    d.association(660,370,'Inscrire')
    d.association(960,600,'Obtenir')
    d.association(1240,385,'Évaluer')
    for x,y,t in [(325,145,'0,N'),(535,145,'1,1'),(900,145,'0,N'),(1125,145,'1,1'),(757,320,'0,N'),(757,465,'1,1'),(900,590,'0,N'),(1125,590,'1,1'),(1336,335,'0,N'),(1336,477,'1,1')]: d.cardinal(x,y,t)
    d.text(35,340,420,110,'# : identifiant de l’entité\nLes clés étrangères apparaissent au MLD.\nLe compte utilisateur reste indépendant\nde la fiche étudiant.',21)
    d.save()

    d=Diagram('mld',850)
    d.line([(535,130),(415,130)],arrow=True)
    d.line([(1065,130),(965,130)],arrow=True)
    d.line([(750,470),(750,285)],arrow=True)
    d.line([(1065,650),(965,650)],arrow=True)
    d.line([(1265,470),(1265,325)],arrow=True)
    d.box(35,60,380,210,'programs',['PK id','name','UQ code','description [NULL]'])
    d.box(535,60,430,225,'school_classes',['PK id','FK program_id → programs.id','name','academic_year'])
    d.box(1065,60,400,265,'subjects',['PK id','FK school_class_id','name, UQ code','coefficient'])
    d.box(35,470,380,240,'users',['PK id','name','UQ email','password (haché)','role'])
    d.box(535,470,430,300,'students',['PK id','FK school_class_id','UQ registration_number','first_name, last_name','UQ email [NULL], phone [NULL]','birth_date [NULL], status'])
    d.box(1065,470,400,270,'grades',['PK id','FK student_id → students.id','FK subject_id → subjects.id','assessment','score, weight'])
    d.text(35,350,420,75,'PK : clé primaire · FK : clé étrangère\nUQ : unicité · [NULL] : valeur facultative',21)
    d.text(35,785,1430,40,'Flèches : FK → PK. Toutes les tables métier possèdent created_at et updated_at. Contraintes composites détaillées dans le dictionnaire.',20)
    d.save()

    d=Diagram('cas-utilisation',850)
    d.rect(300,25,1175,785,'#ffffff','#a8beb0')
    d.text(580,30,620,35,'SYSTÈME DE GESTION DES ÉTUDIANTS — CAMPUS',23,GREEN,True,'center')
    # Associations are undirected; the hollow triangle denotes actor generalization.
    for points in [ [(150,130),(360,130)], [(150,110),(245,80),(710,80),(710,130)],
                    [(150,392),(360,340)], [(150,410),(260,410),(850,410),(850,380)],
                    [(150,430),(260,440),(1200,440),(1200,380)], [(150,445),(360,510)],
                    [(150,375),(270,275),(1040,275),(1040,130),(1060,130)],
                    [(150,670),(710,690)], [(150,690),(265,780),(1040,780),(1040,690),(1060,690)] ]:
        d.line(points,'#7b8f82')
    d.line([(115,620),(115,494)],INK,hollow=True)
    d.text(132,540,140,45,'héritage\ndes droits',18)
    d.actor(115,75,'Visiteur')
    d.actor(115,305,'Utilisateur\nde scolarité')
    d.actor(115,620,'Administrateur')
    d.usecase(500,130,'S’inscrire')
    d.usecase(850,130,'Se connecter')
    d.usecase(1200,130,'Se déconnecter')
    d.usecase(500,340,'Consulter, rechercher\net filtrer les données')
    d.usecase(850,340,'Consulter et imprimer\nun relevé de notes')
    d.usecase(1200,340,'Consulter le tableau\nde bord et les graphiques')
    d.usecase(500,510,'Exporter les étudiants\nen CSV')
    d.usecase(850,690,'Gérer les étudiants\net les référentiels',True)
    d.usecase(1200,690,'Saisir, modifier et\nsupprimer les notes',True)
    d.text(710,455,710,105,'Précondition des opérations de scolarité : session authentifiée.\nL’administrateur possède tous les droits de consultation.\nL’inscription publique crée uniquement le rôle utilisateur.',21)
    d.save()

if __name__ == '__main__':
    prepare_diagrams()
    print('Diagram sources prepared in docs/diagrammes.')
