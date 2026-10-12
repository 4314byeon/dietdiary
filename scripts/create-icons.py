from PIL import Image, ImageDraw
from pathlib import Path
import json
root=Path('dietdiary')
shapes=[]
def rect(x,y,w,h,c,r=0):shapes.append(dict(kind='rect',x=x,y=y,w=w,h=h,color=c,r=r))
def ellipse(x,y,w,h,c):shapes.append(dict(kind='ellipse',x=x,y=y,w=w,h=h,color=c))
def poly(points,c):shapes.append(dict(kind='poly',points=points,color=c))
rect(0,0,64,64,'#f5efe5')
ellipse(9,53,46,5,'#d7c5a9')
rect(13,22,38,32,'#79573b',3)
rect(16,25,32,26,'#dfc09a',2)
rect(10,20,44,5,'#97714c',2)
rect(12,20,40,2,'#b99a71',1)
for y in [28,35,42]:
    for x in [20,33]:
        rect(x,y,10,5,'#79573b',1)
        rect(x+1,y+1,8,3,'#9bab83',1)
        rect(x+2,y+1,1,3,'#d7e0b5')
rect(28,48,8,6,'#79573b',1)
rect(30,49,4,5,'#ead6b6')
rect(9,54,46,3,'#9a7653',1)
rect(31,12,2,9,'#7a875a',1)
poly([(31,16),(24,15),(21,9),(27,9),(32,13)],'#8f9e70')
poly([(33,13),(36,7),(43,6),(42,12),(36,16),(33,16)],'#6e845b')
rect(44,16,3,3,'#cda96b',1)
rect(48,13,2,2,'#d8bc8c')
def draw(size):
    scale=size/64;im=Image.new('RGB',(size,size),'#f5efe5');d=ImageDraw.Draw(im)
    for s in shapes:
        c=s['color']
        if s['kind']=='poly':d.polygon([(round(x*scale),round(y*scale)) for x,y in s['points']],fill=c)
        else:
            box=[round(s['x']*scale),round(s['y']*scale),round((s['x']+s['w'])*scale)-1,round((s['y']+s['h'])*scale)-1]
            if s['kind']=='ellipse':d.ellipse(box,fill=c)
            elif s['r']:d.rounded_rectangle(box,radius=s['r']*scale,fill=c)
            else:d.rectangle(box,fill=c)
    return im
for size in [192,512]:draw(size).save(root/f'web/icon-{size}.png')
for folder,size in [('mipmap-mdpi',48),('mipmap-hdpi',72),('mipmap-xhdpi',96),('mipmap-xxhdpi',144),('mipmap-xxxhdpi',192)]:
    path=root/'android/app/src/main/res'/folder;path.mkdir(parents=True,exist_ok=True);draw(size).save(path/'ic_launcher.png')
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">']
paths=[]
for i,s in enumerate(shapes):
    color=s['color']
    if s['kind']=='rect':
        x,y,w,h,r=[s[k] for k in ['x','y','w','h','r']]
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}"/>')
        p=f'M{x+r},{y} H{x+w-r} Q{x+w},{y} {x+w},{y+r} V{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} H{x+r} Q{x},{y+h} {x},{y+h-r} V{y+r} Q{x},{y} {x+r},{y} Z'
    elif s['kind']=='ellipse':
        x,y,w,h=[s[k] for k in ['x','y','w','h']];svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{color}"/>');p=f'M{x},{y+h/2} a{w/2},{h/2} 0,1 0,{w},0 a{w/2},{h/2} 0,1 0,{-w},0'
    else:
        points=s['points'];svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{color}"/>');p='M'+' L'.join(f'{x},{y}' for x,y in points)+' Z'
    if i>0:paths.append(f'<path android:fillColor="{color}" android:pathData="{p}"/>')
svg.append('</svg>');(root/'web/icon.svg').write_text(''.join(svg),encoding='utf8')
vector='<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108"><group android:scaleX="1.05" android:scaleY="1.05" android:translateX="20.4" android:translateY="20.4">'+''.join(paths)+'</group></vector>'
(root/'android/app/src/main/res/drawable/ic_office.xml').write_text(vector,encoding='utf8')
(root/'android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml').write_text('<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/cream"/><foreground android:drawable="@drawable/ic_office"/></adaptive-icon>',encoding='utf8')
