"""Convierte el JSON de OpenStreetMap (Overpass, 'out geom') en map-data.js para el juego.
Uso: python bake_map.py osm.json   ->  map-data.js
Datos (c) colaboradores de OpenStreetMap, licencia ODbL."""
import json, math, sys
LAT0, LON0, SC = 3.45405, -76.5344, 1.8      # centro del CAM, pixeles por metro
W, H = 1600, 960
d = json.load(open(sys.argv[1], encoding='utf-8'))

def P(la, lo):
    return (round((lo-LON0)*111320*math.cos(math.radians(LAT0))*SC+W/2, 1),
            round(-(la-LAT0)*110574*SC+H/2, 1))

def simp(pts):
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0]-out[-1][0]) + abs(p[1]-out[-1][1]) >= 1.2: out.append(p)
    if len(out) < len(pts) and out[-1] != pts[-1]: out.append(pts[-1])
    return out

def flat(pts): return [v for p in pts for v in p]
def inside(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return max(xs) > -40 and min(xs) < W+40 and max(ys) > -40 and min(ys) < H+40

def raw(geom): return [(g['lat'], g['lon']) for g in geom]

def join(segs):
    segs = [list(s) for s in segs if len(s) > 1]; rings = []
    while segs:
        cur = segs.pop()
        while cur[0] != cur[-1]:
            for i, s in enumerate(segs):
                if s[0] == cur[-1]: cur += s[1:]; segs.pop(i); break
                if s[-1] == cur[-1]: cur += s[::-1][1:]; segs.pop(i); break
                if s[-1] == cur[0]: cur = s[:-1] + cur; segs.pop(i); break
                if s[0] == cur[0]: cur = s[::-1][:-1] + cur; segs.pop(i); break
            else: break
        rings.append(cur)
    return rings

def rings_of(e):
    if e['type'] == 'way': return [raw(e['geometry'])]
    segs = [raw(m['geometry']) for m in e.get('members', []) if m['type'] == 'way' and 'geometry' in m]
    return join(segs)

SKIP_HW = {'steps', 'platform', 'construction', 'proposed', 'elevator'}
GRASS_L = {'park', 'garden', 'common', 'pitch', 'playground', 'recreation_ground', 'dog_park'}
GRASS_U = {'grass', 'recreation_ground', 'village_green', 'forest', 'meadow', 'cemetery'}
GRASS_N = {'grassland', 'wood', 'scrub', 'tree_row'}
out = dict(roads=[], plaza=[], grass=[], bld=[], water=[], rivers=[])
for e in d['elements']:
    t = e.get('tags', {})
    if 'highway' in t:
        hw = t['highway']
        if hw in SKIP_HW or t.get('tunnel') in ('yes', 'building_passage'): continue
        if e['type'] == 'relation' or t.get('area') == 'yes':
            for r in rings_of(e):
                pp = simp([P(*q) for q in r])
                if len(pp) > 2 and inside(pp): out['plaza'].append(flat(pp))
        elif e['type'] == 'way':
            pp = simp([P(*q) for q in raw(e['geometry'])])
            if len(pp) > 1 and inside(pp):
                out['roads'].append(dict(k=hw, b=1 if t.get('bridge') in ('yes', 'viaduct') else 0, p=flat(pp)))
    elif 'building' in t:
        for r in rings_of(e):
            pp = simp([P(*q) for q in r])
            if len(pp) > 2 and inside(pp):
                out['bld'].append(dict(cam=1 if t.get('short_name') == 'CAM' else 0, p=flat(pp)))
    elif t.get('natural') == 'water' or t.get('water'):
        rs = [flat(simp([P(*q) for q in r])) for r in rings_of(e)]
        if rs: out['water'].append(rs)
    elif 'waterway' in t:
        if e['type'] == 'way':
            pp = simp([P(*q) for q in raw(e['geometry'])])
            if len(pp) > 1 and inside(pp): out['rivers'].append(dict(w=18 if t['waterway'] == 'river' else 4, p=flat(pp)))
    elif t.get('leisure') in GRASS_L or t.get('landuse') in GRASS_U or t.get('natural') in GRASS_N:
        rs = [flat(simp([P(*q) for q in r])) for r in rings_of(e)]
        rs = [r for r in rs if len(r) >= 6]
        if rs: out['grass'].append(rs)
s = json.dumps(out, separators=(',', ':'))
open('map-data.js', 'w', encoding='utf-8').write('/* (c) colaboradores de OpenStreetMap, ODbL. Centro: CAM Cali 3.45405,-76.5344 · 1.8 px/m */\nwindow.MAPDATA=' + s + ';\n')
print({k: len(v) for k, v in out.items()}, len(s)//1024, 'KB')
