"""Render the simple native slides to a portable PDF fallback without Office."""
from pathlib import Path
import sys, io, math
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'.tools'/'pptx'))
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image, ImageDraw, ImageFont

SOURCE = ROOT/'docs'/'Soutenance_Groupe_1_Gestion_Etudiants_CORRIGE.pptx'
DESTINATION = ROOT/'docs'/'Soutenance_Groupe_1_Gestion_Etudiants.pdf'
PREVIEWS = ROOT/'.tools'/'repair'/'previews'
PREVIEWS.mkdir(parents=True, exist_ok=True)
SCALE = 2
POINT_EMU = 12700

def px(value): return round(int(value)/POINT_EMU*SCALE)
def color(value, default='#263831'):
    try: return '#'+str(value.rgb)
    except (AttributeError, TypeError, ValueError): return default

def wrapped(draw, text, font, maximum):
    if not text: return ['']
    result=[]; line=''
    for word in text.split(' '):
        candidate=(line+' '+word).strip()
        if line and draw.textlength(candidate,font=font)>maximum:
            result.append(line); line=word
        else: line=candidate
    result.append(line)
    return result

presentation=Presentation(SOURCE)
pages=[]
for index,slide in enumerate(presentation.slides,1):
    image=Image.new('RGB',(px(presentation.slide_width),px(presentation.slide_height)),'white')
    draw=ImageDraw.Draw(image)
    for shape in slide.shapes:
        x,y,w,h=px(shape.left),px(shape.top),px(shape.width),px(shape.height)
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            picture=Image.open(io.BytesIO(shape.image.blob)).convert('RGB')
            image.paste(picture.resize((w,h),Image.Resampling.LANCZOS),(x,y))
            continue
        if shape.shape_type == MSO_SHAPE_TYPE.LINE:
            start=(px(shape.begin_x),px(shape.begin_y)); end=(px(shape.end_x),px(shape.end_y))
            stroke=color(shape.line.color); thickness=max(1,px(shape.line.width or POINT_EMU))
            draw.line([start,end],fill=stroke,width=thickness)
            if shape._element.spPr.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd') is not None:
                angle=math.atan2(end[1]-start[1],end[0]-start[0]); length=18
                draw.polygon([end,(end[0]-length*math.cos(angle)+length*.45*math.sin(angle),end[1]-length*math.sin(angle)-length*.45*math.cos(angle)),(end[0]-length*math.cos(angle)-length*.45*math.sin(angle),end[1]-length*math.sin(angle)+length*.45*math.cos(angle))],fill=stroke)
            continue
        if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            fill=color(shape.fill.fore_color,'white')
            draw.rectangle((x,y,x+w,y+h),fill=fill)
        if not shape.has_text_frame or not shape.text.strip(): continue
        current_y=y+px(shape.text_frame.margin_top)
        content_x=x+px(shape.text_frame.margin_left)
        content_w=w-px(shape.text_frame.margin_left)-px(shape.text_frame.margin_right)
        for paragraph in shape.text_frame.paragraphs:
            if not paragraph.runs: continue
            first=paragraph.runs[0]
            size=first.font.size.pt if first.font.size else 18
            font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if first.font.bold else 'arial.ttf'),round(size*SCALE))
            fill=color(first.font.color)
            line_spacing=paragraph.line_spacing if isinstance(paragraph.line_spacing,float) else 1.1
            for explicit_line in paragraph.text.split('\n'):
                for line in wrapped(draw,explicit_line,font,content_w):
                    width=draw.textlength(line,font=font)
                    alignment=str(paragraph.alignment)
                    line_x=content_x+(content_w-width)/2 if 'CENTER' in alignment else content_x+content_w-width if 'RIGHT' in alignment else content_x
                    draw.text((round(line_x),round(current_y)),line,font=font,fill=fill,anchor='lt')
                    current_y+=size*SCALE*line_spacing
            current_y+=(paragraph.space_after.pt if paragraph.space_after else 0)*SCALE
    if index in (1,5,9,12): image.save(PREVIEWS/f'slide-{index:02}.png')
    pages.append(image)
pages[0].save(DESTINATION,'PDF',save_all=True,append_images=pages[1:],resolution=144.0,quality=92,title='Groupe 1 - Gestion des etudiants',author='Groupe 1')
assert DESTINATION.read_bytes().startswith(b'%PDF')
print(f'PDF fallback created: {len(pages)} pages; {DESTINATION.stat().st_size:,} bytes.')
