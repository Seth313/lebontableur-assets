import sys, re, json
from html.parser import HTMLParser
src=open(sys.argv[1],encoding="utf-8").read()
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.cadres=[]; s.cur=None; s.grade=None; s.stack=[]; s.cap=None; s.buf=""; s.row=None; s.cell=None
    def handle_starttag(s,t,a):
        a=dict(a); c=a.get("class","") or ""
        if t=="section" and "gi-cadre" in c.split():
            s.cur={"id":a.get("id"),"filiere":a.get("data-filiere"),"cat":"","nom":"","intro":"","textes":[],"grades":[]}; s.cadres.append(s.cur)
        if not s.cur: return
        if t=="span" and "gi-cat" in c: s.cap="cat"; s.buf=""
        elif t=="h2" and not s.grade: s.cap="nom"; s.buf=""
        elif t=="p" and not s.grade and not s.cur["intro"]: s.cap="intro"; s.buf=""
        elif t=="div" and c.split()[:1]==["gi-grade"]:
            s.grade={"id":a.get("id"),"nom":"","rows":[]}; s.cur["grades"].append(s.grade)
        elif t=="h3" and s.grade: s.cap="gnom"; s.buf=""
        elif t=="small" and s.cap=="gnom": s.cap="gsmall"; s.gsmall=""
        elif t=="tr" and s.grade and "data-im" in a: s.row={"ib":a.get("data-ib"),"im":a.get("data-im"),"cells":[]}; s.grade["rows"].append(s.row)
        elif t=="td" and s.row is not None: s.cell=""
        elif t=="a" and s.cur and not s.grade and "legifrance" in (a.get("href") or ""): s.cur["textes"].append({"url":a["href"],"titre":""}); s.cap="texte"; s.buf=""
    def handle_endtag(s,t):
        if t=="span" and s.cap=="cat": s.cur["cat"]=s.buf.strip(); s.cap=None
        elif t=="h2" and s.cap=="nom": s.cur["nom"]=s.buf.strip(); s.cap=None
        elif t=="p" and s.cap=="intro": s.cur["intro"]=re.sub(r"\s+"," ",s.buf).strip(); s.cap=None
        elif t=="small" and s.cap=="gsmall": s.cap="gnom"; s.grade["echelle"]=s.gsmall.strip(" ()")
        elif t=="h3" and s.cap=="gnom": s.grade["nom"]=re.sub(r"\s+"," ",s.buf).strip(); s.cap=None
        elif t=="a" and s.cap=="texte": s.cur["textes"][-1]["titre"]=s.buf.strip(); s.cap=None
        elif t=="td" and s.cell is not None: s.row["cells"].append(re.sub(r"\s+"," ",s.cell).strip()); s.cell=None
        elif t=="tr": s.row=None
        elif t=="table" and s.grade: s.grade=None if False else s.grade
        elif t=="section": s.cur=None; s.grade=None
    def handle_data(s,d):
        if s.cell is not None: s.cell+=d
        if s.cap=="gsmall": s.gsmall+=d; return
        if s.cap: s.buf+=d
p=P(); p.feed(src)
json.dump(p.cadres,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
print(len(p.cadres),"cadres",sum(len(c["grades"]) for c in p.cadres),"grades")
from collections import Counter
print(Counter(c["filiere"] for c in p.cadres))
durs=Counter(r["cells"][3] if len(r["cells"])>3 else "?" for c in p.cadres for g in c["grades"] for r in g["rows"]); print(durs)
ims=[r["im"] for c in p.cadres for g in c["grades"] for r in g["rows"] if not (r["im"] or "").isdigit()]; print("IM non num:",Counter(ims))
