import sys,json,re,unicodedata,hashlib
d=json.load(open(sys.argv[1],encoding="utf-8"))
FIL={"administrative":"Administrative","technique":"Technique","culturelle":"Culturelle","sportive":"Sportive","animation":"Animation","police":"Police municipale","medico-sociale":"Médico-sociale","sociale":"Sociale","pompiers":"Sapeurs-pompiers professionnels"}
MOIS={"janvier":1,"février":2,"mars":3,"avril":4,"mai":5,"juin":6,"juillet":7,"août":8,"septembre":9,"octobre":10,"novembre":11,"décembre":12}
def effet(txt):
    m=re.findall(r"(?:depuis le|à compter du) (\d+)(?:er)? (\w+) (\d{4})",txt)
    if not m: return None
    j,mo,a=m[-1]; return f"{a}-{MOIS[mo]:02d}-{int(j):02d}" if mo in MOIS else None
def duree(t):
    if t in ("—","-",""): return None
    a=re.search(r"(\d+) ans?",t); m=re.search(r"(\d+) mois",t)
    return (int(a.group(1))*12 if a else 0)+(int(m.group(1)) if m else 0)
def slug(s):
    s=unicodedata.normalize("NFD",s).encode("ascii","ignore").decode().lower(); return re.sub(r"[^a-z0-9]+","-",s).strip("-")
fils={}; grilles={}; sig2id={}
for c in d:
    eff=effet(c["intro"]) or "2022-01-01"
    cat=c["cat"].replace("Catégorie ","")
    cad={"nom":c["nom"],"cat":cat,"grades":[],"textes":[t["titre"] for t in c["textes"]]}
    for g in c["grades"]:
        ech=[]
        for r in g["rows"]:
            ims=[int(x) for x in (r["im"] or "").split() if x.isdigit()]
            e={"d":duree(r["cells"][3]),"im":ims[0] if ims else None}
            if len(ims)>1: e["chevrons"]=ims
            if not re.match(r"^\d+(er|e) échelon$",r["cells"][0]): e["lib"]=r["cells"][0]
            ech.append(e)
        base=g["nom"].strip(); small=re.match(r"échelle (C\d)$",g.get("echelle",""))
        sig=json.dumps(ech,sort_keys=True)
        if sig in sig2id: gid=sig2id[sig]
        else:
            gid=("ech-"+small.group(1).lower()) if small else slug(c["id"]+"-"+base)
            while gid in grilles: gid+="-b"
            sig2id[sig]=gid
            grilles[gid]={"nom":("Échelle "+small.group(1)) if small else base,"versions":[{"effet":eff,"echelons":ech}]}
        cad["grades"].append({"nom":base,"grille":gid})
    fils.setdefault(c["filiere"],[]).append(cad)
order=["administrative","technique","culturelle","sportive","animation","police","medico-sociale","sociale","pompiers"]
out={"maj":sys.argv[3],"point":[{"effet":"2023-07-01","valeur":4.92278}],
 "source":"fpt-pratique.fr, grilles indiciaires relevées sur Légifrance (https://www.fpt-pratique.fr/grilles-indiciaires.html)",
 "filieres":[{"nom":FIL[f],"cadres":sorted(fils[f],key=lambda x:"C B A A+".split().index(x["cat"]) if x["cat"] in "C B A A+".split() else 9)} for f in order if f in fils],
 "grilles":grilles}
json.dump(out,open(sys.argv[2],"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(sum(len(c["grades"]) for f in out["filieres"] for c in f["cadres"]),"grades,",len(grilles),"grilles distinctes")
