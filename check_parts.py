import json,glob,os,re
have={}
for f in sorted(glob.glob('data/parts-*.json')):
    try: d=json.load(open(f))
    except Exception as e: print('BAD',f,e); continue
    for m in d: have[m['id']]=(f,[(p['k'],p['kind'],p['name']) for p in m['parts']])
svgs=sorted(os.path.basename(x) for x in glob.glob('parts/[0-9]*.svg'))
pngs=sorted(os.path.basename(x) for x in glob.glob('parts/[0-9]*.png'))
allmods=[l.split()[1] for l in open('AREAS.md') if l.startswith('- 0')]
print('json modules:',len(have),'/',len(allmods),' svg files:',len(svgs),' hw png:',len(pngs))
nojson=[m for m in allmods if m not in have]; print('NO JSON:',nojson)
missing={}
for mid,(f,parts) in sorted(have.items()):
    for k,kind,name in parts:
        if kind=='hw':
            miss=[] if (f'{mid}-{k}.png' in pngs or f'{mid}-{k}.svg' in svgs) else [f'{mid}-{k}.png']
        else:
            need=[f'{mid}-{k}.svg', f'{mid}-{k}-poster.svg']
            miss=[n for n in need if n not in svgs]
        if miss: missing.setdefault(mid,[]).extend(miss)
for k,v in missing.items(): print('MISSING',k,len(v),v)
done=[m for m in have if m not in missing]; print('COMPLETE:',done)
