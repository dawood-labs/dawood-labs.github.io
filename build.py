"""Build the portfolio site from data/content.json.

Usage:  python3 build.py
Writes index.html and projects/<slug>.html. Edit data/content.json, rebuild, push.
"""
import json, html, os

ROOT = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(ROOT, "data", "content.json"), encoding="utf-8"))
P = C["person"]
e = html.escape

ICONS = {
    "radar": '<path d="M12 12l7-7"/><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "wave": '<path d="M3 17c3 0 3-10 6-10s3 10 6 10 3-6 6-6"/>',
    "brain": '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/><circle cx="12" cy="12" r="2"/><path d="M8 7l3 3M16 7l-3 3M8 17l3-3M16 17l-3-3"/>',
    "grid": '<path d="M3 3h7v7H3zM14 3h7v5h-7zM14 12h7v9h-7zM3 14h7v7H3z"/>',
    "flow": '<rect x="2" y="9" width="5" height="6" rx="1"/><rect x="10" y="9" width="5" height="6" rx="1"/><rect x="18" y="9" width="4" height="6" rx="1"/><path d="M7 12h3M15 12h3"/>',
    "map": '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
}
def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, "")}</svg>'

CSS = """
:root{--bg:#07111c;--bg2:#0b1a29;--card:#0f2234;--card2:#132a40;--line:#1d3a55;--text:#e9f0f6;--muted:#8fa6bb;--acc:#34d399;--acc2:#38bdf8;--warm:#fbbf24}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,system-ui,sans-serif;line-height:1.65;font-size:16px;-webkit-font-smoothing:antialiased}
a{color:var(--acc);text-decoration:none}a:hover{color:#6ee7b7}
img{max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
nav{position:fixed;top:0;left:0;right:0;z-index:50;transition:.3s;border-bottom:1px solid transparent}
nav.solid{background:rgba(7,17,28,.88);backdrop-filter:blur(12px);border-bottom-color:var(--line)}
nav .wrap{display:flex;align-items:center;justify-content:space-between;height:66px}
.logo{font-weight:800;color:var(--text);letter-spacing:.06em;font-size:15px;display:flex;align-items:center;gap:10px}
.logo i{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,var(--acc),var(--acc2));display:grid;place-items:center;font-style:normal;color:#04131f;font-size:13px}
.navlinks a{color:var(--muted);margin-left:26px;font-size:14px;font-weight:500}.navlinks a:hover{color:var(--text)}
.navcv{border:1px solid var(--line);padding:7px 14px;border-radius:8px;color:var(--text)!important}
.hero{position:relative;min-height:100vh;display:flex;align-items:center;overflow:hidden;padding:110px 0 60px}
.hero:before{content:"";position:absolute;inset:-5%;background:url(assets/img/hero_contours.webp) center/cover no-repeat;opacity:.16;-webkit-mask-image:radial-gradient(ellipse at 70% 45%,#000 30%,transparent 75%);mask-image:radial-gradient(ellipse at 70% 45%,#000 30%,transparent 75%);animation:drift 40s ease-in-out infinite alternate}@keyframes drift{to{transform:translate(-2%,1.5%) scale(1.04)}}@media(prefers-reduced-motion:reduce){.hero:before{animation:none}}
.hero:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 75% 30%,rgba(52,211,153,.18),transparent 55%),radial-gradient(ellipse at 15% 85%,rgba(56,189,248,.14),transparent 55%);pointer-events:none}
.gridbg{position:absolute;inset:0;background-image:linear-gradient(rgba(56,189,248,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(56,189,248,.06) 1px,transparent 1px);background-size:48px 48px;mask-image:radial-gradient(ellipse at center,#000 30%,transparent 75%)}
.hero .wrap{position:relative;z-index:2;display:grid;grid-template-columns:1.5fr 1fr;gap:60px;align-items:center}
.badge{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);background:rgba(15,34,52,.7);padding:6px 14px;border-radius:30px;font-size:13px;color:var(--muted)}
.badge b{width:8px;height:8px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 4px rgba(52,211,153,.2);animation:pulse 2s infinite}
@keyframes pulse{50%{box-shadow:0 0 0 8px rgba(52,211,153,0)}}
h1{font-size:clamp(38px,5.6vw,68px);line-height:1.04;margin:20px 0;font-weight:800;letter-spacing:-.02em}
.grad{background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{font-size:19px;color:var(--muted);max-width:640px}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:13px 22px;border-radius:11px;font-weight:600;font-size:15px;transition:.2s}
.btn.p{background:linear-gradient(135deg,var(--acc),#10b981);color:#04131f}.btn.p:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(52,211,153,.3);color:#04131f}
.btn.g{border:1px solid var(--line);color:var(--text);background:rgba(15,34,52,.6)}.btn.g:hover{border-color:var(--acc);color:var(--text)}
.portrait{position:relative;justify-self:center}
.portrait img{width:330px;height:330px;border-radius:50%;object-fit:cover;border:4px solid var(--card2);position:relative;z-index:2}
.portrait:before{content:"";position:absolute;inset:-14px;border-radius:50%;background:conic-gradient(var(--acc),var(--acc2),transparent 60%,var(--acc));animation:spin 8s linear infinite;z-index:1}
@keyframes spin{to{transform:rotate(360deg)}}
.chip{position:absolute;z-index:3;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 12px;font-size:12.5px;box-shadow:0 10px 30px rgba(0,0,0,.4)}
.chip b{color:var(--acc);display:block;font-size:16px}
.c1{top:10px;left:-50px}.c2{bottom:30px;right:-40px}.c3{bottom:-10px;left:-20px}
.impact{display:grid;grid-template-columns:repeat(6,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:18px;overflow:hidden;margin-top:-20px;position:relative;z-index:3}
.impact div{background:var(--bg2);padding:24px 18px}
.impact b{font-size:30px;font-weight:800;display:block;background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:-.02em}
.impact span{font-size:13.5px;color:var(--text);display:block;font-weight:500}.impact small{color:var(--muted);font-size:12px}
section{padding:100px 0}
.kicker{color:var(--acc);font-size:13px;font-weight:700;letter-spacing:.18em;text-transform:uppercase}
h2{font-size:clamp(30px,3.6vw,44px);margin:10px 0 12px;letter-spacing:-.02em;line-height:1.15}
.sub{color:var(--muted);max-width:720px;margin:0 0 46px;font-size:17px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:linear-gradient(180deg,var(--card),var(--bg2));border:1px solid var(--line);border-radius:18px;padding:26px;transition:.25s;position:relative}
.card:hover{transform:translateY(-4px);border-color:rgba(52,211,153,.45)}
.card .ic{width:46px;height:46px;border-radius:12px;background:rgba(52,211,153,.1);color:var(--acc);display:grid;place-items:center;margin-bottom:16px}
.card .ic svg{width:24px;height:24px}
.card h3{margin:0 0 8px;font-size:18.5px}.card p{margin:0;color:var(--muted);font-size:15px}
.themes{display:flex;flex-wrap:wrap;gap:10px;margin-top:34px}
.themes span{border:1px solid var(--line);background:var(--card);padding:8px 16px;border-radius:30px;font-size:14px}
.proj{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}
.pc{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:20px;overflow:hidden;transition:.25s;color:var(--text)}
.pc:hover{transform:translateY(-5px);border-color:rgba(52,211,153,.5);box-shadow:0 20px 50px rgba(0,0,0,.35);color:var(--text)}
.pc .top{height:150px;position:relative;background:linear-gradient(135deg,#0d3b3a,#0b2440 60%,#13294a);overflow:hidden}
.pc .top img{width:100%;height:100%;object-fit:cover;opacity:.9}
.pc .top .no{position:absolute;inset:0;background-image:linear-gradient(rgba(56,189,248,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(56,189,248,.09) 1px,transparent 1px);background-size:22px 22px}
.pc .top .big{position:absolute;left:22px;bottom:16px;font-size:34px;font-weight:800;color:#fff;letter-spacing:-.02em;text-shadow:0 2px 12px rgba(0,0,0,.5)}
.pc .top .big small{display:block;font-size:12px;font-weight:500;color:#cfe;letter-spacing:0}
.pc .place{position:absolute;right:16px;top:14px;background:rgba(7,17,28,.75);border:1px solid var(--line);font-size:12px;padding:4px 10px;border-radius:20px;color:var(--muted)}
.pc .body{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1}
.pc h3{margin:0 0 8px;font-size:20px;line-height:1.3}.pc p{color:var(--muted);margin:0 0 14px;font-size:15px;flex:1}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tag{font-size:12px;background:rgba(56,189,248,.1);color:var(--acc2);padding:3px 10px;border-radius:20px}
.more{margin-top:16px;font-weight:600;color:var(--acc);font-size:14px}
.tl{position:relative;padding-left:34px}
.tl:before{content:"";position:absolute;left:8px;top:6px;bottom:6px;width:2px;background:linear-gradient(var(--acc),var(--acc2),transparent)}
.job{position:relative;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px 28px;margin-bottom:22px}
.job:before{content:"";position:absolute;left:-33px;top:30px;width:14px;height:14px;border-radius:50%;background:var(--bg);border:3px solid var(--acc)}
.job .h{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
.job h3{margin:0;font-size:20px}.job .org{color:var(--acc2);font-weight:600}.job .org small{color:var(--muted);font-weight:400}
.job .when{color:var(--muted);font-size:14px;background:var(--bg2);border:1px solid var(--line);padding:3px 12px;border-radius:20px;height:fit-content}
.job ul{margin:14px 0 0;padding-left:20px;color:#c4d3e0}.job li{margin:7px 0}
.pub{display:grid;grid-template-columns:90px 1fr;gap:22px;padding:24px 0;border-bottom:1px solid var(--line)}
.pub .yr{font-size:26px;font-weight:800;color:var(--acc)}.pub .st{font-size:12px;color:var(--muted)}
.pub .t{font-weight:600;font-size:17px}.pub .a{color:var(--muted);font-size:14.5px;margin-top:4px}.pub .a b{color:var(--text)}
.repos{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.repo{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;color:var(--text);transition:.2s;display:block}
.repo:hover{border-color:var(--acc2);color:var(--text);transform:translateY(-3px)}
.repo .n{font-family:ui-monospace,Menlo,monospace;color:var(--acc2);font-weight:600;font-size:14.5px}
.repo .g{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em}
.repo p{margin:8px 0 0;color:var(--muted);font-size:14px}
.skills{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.sk h3{margin:0 0 12px;font-size:16px;color:var(--acc)}
.sk .tags span{font-size:13px;border:1px solid var(--line);background:var(--bg2);padding:5px 12px;border-radius:8px}
.edu{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.updates{border-left:2px solid var(--line);margin-left:6px}
.up{display:grid;grid-template-columns:110px 1fr;gap:16px;padding:12px 0 12px 22px;position:relative}
.up:before{content:"";position:absolute;left:-7px;top:19px;width:12px;height:12px;border-radius:50%;background:var(--acc2)}
.up .d{color:var(--acc2);font-weight:600;font-size:14px}
.cta{text-align:center;background:radial-gradient(ellipse at center,rgba(52,211,153,.14),transparent 70%);border:1px solid var(--line);border-radius:26px;padding:70px 30px}
.cta .btns{justify-content:center}
footer{border-top:1px solid var(--line);padding:30px 0;color:var(--muted);font-size:13.5px}
footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.rv{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}.rv.in{opacity:1;transform:none}
/* case page */
.ch{padding:130px 0 50px;position:relative;overflow:hidden}
.ch:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 80% 20%,rgba(52,211,153,.14),transparent 55%);pointer-events:none}
.back{color:var(--muted);font-size:14px}
.mstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-top:34px}
.mstrip div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
.mstrip b{font-size:26px;display:block;background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}
.mstrip span{color:var(--muted);font-size:13.5px}
.cbody{display:grid;grid-template-columns:1fr 300px;gap:50px;padding-bottom:60px}
.cbody h2{font-size:26px;margin:40px 0 12px}.cbody h2:first-child{margin-top:0}
.cbody p,.cbody li{color:#c4d3e0}
.steps{counter-reset:s;list-style:none;padding:0}
.steps li{counter-increment:s;position:relative;padding:14px 18px 14px 62px;background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:10px}
.steps li:before{content:counter(s);position:absolute;left:16px;top:12px;width:32px;height:32px;border-radius:9px;background:rgba(52,211,153,.12);color:var(--acc);font-weight:800;display:grid;place-items:center}
.res li{margin:8px 0}
.lesson{border-left:4px solid var(--acc);background:var(--card);padding:18px 22px;border-radius:0 12px 12px 0;font-style:italic;color:var(--text)}
.side{position:sticky;top:90px;height:fit-content;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
.side h4{margin:0 0 10px;color:var(--muted);font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.gal{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:10px}
.gal img{width:100%;border-radius:12px;background:#fff;border:1px solid var(--line);cursor:zoom-in}
.nextp{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--line);padding:30px 0}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;place-items:center;z-index:99;cursor:zoom-out}.lb img{max-width:94vw;max-height:92vh;background:#fff;border-radius:8px}.lb.on{display:grid}
@media(max-width:980px){.hero .wrap,.cbody{grid-template-columns:1fr}.portrait{order:-1}.portrait img{width:220px;height:220px}.chip{display:none}.impact{grid-template-columns:repeat(3,1fr)}.cards,.repos{grid-template-columns:1fr 1fr}.navlinks a:not(.navcv){display:none}.side{position:static}}
@media(max-width:640px){.impact,.cards,.repos,.proj,.skills,.edu,.gal{grid-template-columns:1fr}.impact{grid-template-columns:1fr 1fr}.pub{grid-template-columns:1fr;gap:4px}.up{grid-template-columns:1fr;gap:2px}section{padding:70px 0}.job{padding:20px}}
"""

JS = """
const n=document.querySelector('nav');const f=()=>n.classList.toggle('solid',scrollY>30);addEventListener('scroll',f);f();
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
const lb=document.querySelector('.lb');if(lb){document.querySelectorAll('.gal img').forEach(i=>i.onclick=()=>{lb.querySelector('img').src=i.src;lb.classList.add('on')});lb.onclick=()=>lb.classList.remove('on')}
"""

def head(title, desc, prefix=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://dawood-labs.github.io/assets/img/ndvi_map.jpg">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%2334d399'/><text x='16' y='22' font-size='16' font-family='Arial' font-weight='bold' text-anchor='middle' fill='%2304131f'>DA</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<nav><div class="wrap"><a class="logo" href="{prefix}index.html"><i>DA</i>DAWOOD AHMAD</a><div class="navlinks">
<a href="{prefix}index.html#work">Work</a><a href="{prefix}index.html#experience">Experience</a><a href="{prefix}index.html#research">Research</a><a href="{prefix}index.html#code">Code</a><a href="{prefix}index.html#updates">Updates</a><a href="{prefix}index.html#contact">Contact</a>
{f'<a class="navcv" href="{prefix}{P["cv"]}" target="_blank">Download CV</a>' if P.get("cv") else ''}</div></div></nav>"""

def foot():
    return f"""<footer><div class="wrap"><span>© 2026 {e(P['name'])} · {e(P['location'])}</span><span><a href="{P['github']}" target="_blank" rel="noopener">GitHub</a> · <a href="{P['linkedin']}" target="_blank" rel="noopener">LinkedIn</a> · <a href="mailto:{P['email']}">Email</a></span></div></footer>
<div class="lb"><img alt=""></div><script>{JS}</script></body></html>"""

def proj_card(p, prefix=""):
    img = p["images"][0] if p.get("images") else ""
    top = f'<img src="{prefix}{img}" alt="" loading="lazy">' if img else '<div class="no"></div>'
    m = p["metrics"][0]
    return f"""<a class="pc rv" href="{prefix}projects/{p['slug']}.html"><div class="top">{top}<span class="place">{e(p['place'])}</span><div class="big">{e(m[0])}<small>{e(m[1])}</small></div></div>
<div class="body"><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p><div class="tags">{''.join(f'<span class="tag">{e(t)}</span>' for t in p['tags'][:5])}</div><span class="more">Read case study →</span></div></a>"""

RESEARCH = {"snowmelt-prediction", "glacial-lake-segmentation", "optical-vs-radar-thesis"}

def index():
    s = [head(f"{P['name']} | {P['title']}", P["intro"])]
    s.append(f"""<header class="hero"><div class="gridbg"></div><div class="wrap"><div>
<span class="badge"><b></b>{e(P['location'])}</span>
<h1>I turn <span class="grad">satellite data</span> into maps, models and decisions.</h1>
<p class="lead">{e(P['intro'])}</p>
<div class="btns"><a class="btn p" href="#work">Explore my work →</a>{f'<a class="btn g" href="{P["cv"]}" target="_blank">Download CV</a>' if P.get('cv') else ''}<a class="btn g" href="{P['github']}" target="_blank" rel="noopener">GitHub</a><a class="btn g" href="{P['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></div></div>
<div class="portrait"><img src="{P['photo']}" alt="{e(P['name'])}"><div class="chip c1"><b>Team Lead</b>ML and remote sensing</div><div class="chip c2"><b>Gold Medal</b>M.Phil. Space Science</div><div class="chip c3"><b>6 countries</b>mapped from space</div></div>
</div></header>""")
    s.append('<div class="wrap"><div class="impact rv">' + "".join(f'<div><b>{e(i["value"])}</b><span>{e(i["label"])}</span><small>{e(i["note"])}</small></div>' for i in C["impact"]) + "</div></div>")
    s.append('<section id="expertise"><div class="wrap"><div class="kicker">What I do</div><h2>End-to-end geospatial AI</h2><p class="sub">From raw radar and optical imagery to validated maps, field polygons and dashboards that clients use to make decisions.</p><div class="cards">')
    s += [f'<div class="card rv"><div class="ic">{icon(x["icon"])}</div><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></div>' for x in C["expertise"]]
    s.append('</div><div class="themes rv">' + "".join(f"<span>{e(t)}</span>" for t in C["themes"]) + "</div></div></section>")
    work = [p for p in C["projects"] if p["slug"] not in RESEARCH]
    research = [p for p in C["projects"] if p["slug"] in RESEARCH]
    s.append('<section id="work" style="background:var(--bg2)"><div class="wrap"><div class="kicker">Case studies</div><h2>Selected industry work</h2><p class="sub">Production projects in radar and optical crop mapping, validation and geospatial engineering. Each case study covers the problem, data, method and measured results.</p><div class="proj">')
    s += [proj_card(p) for p in work]
    s.append("</div></div></section>")
    s.append('<section id="experience"><div class="wrap"><div class="kicker">Career</div><h2>Experience</h2><p class="sub">Industry roles in Earth observation, GIS and machine learning.</p><div class="tl">')
    for j in C["experience"]:
        s.append(f'<div class="job rv"><div class="h"><div><h3>{e(j["role"])}</h3><div class="org">{e(j["org"])} <small>· {e(j["orgnote"])}</small></div></div><span class="when">{e(j["when"])}</span></div><ul>' + "".join(f"<li>{e(x)}</li>" for x in j["points"]) + "</ul></div>")
    s.append("</div></div></section>")
    s.append('<section id="research" style="background:var(--bg2)"><div class="wrap"><div class="kicker">Research</div><h2>Research and publications</h2><p class="sub">Peer-reviewed work in machine learning for hydrology, glaciers, air quality and crop mapping.</p><div class="proj" style="margin-bottom:50px">')
    s += [proj_card(p) for p in research]
    s.append("</div>")
    for p in C["publications"]:
        link = f' · <a href="{p["link"]}" target="_blank" rel="noopener">DOI ↗</a>' if p["link"] else ""
        s.append(f'<div class="pub rv"><div><div class="yr">{e(p["year"]) or "—"}</div><div class="st">{e(p["status"])}</div></div><div><div class="t">{e(p["title"])}</div><div class="a">{p["authors"]}{" · " if p["authors"] else ""}<i>{e(p["venue"])}</i>{link}</div></div></div>')
    s.append("</div></section>")
    s.append('<section id="code"><div class="wrap"><div class="kicker">Open source</div><h2>Code on GitHub</h2><p class="sub">Public repositories with full documentation, from radar preprocessing to geometry tools.</p><div class="repos">')
    s += [f'<a class="repo rv" href="https://github.com/dawood-labs/{r["name"]}" target="_blank" rel="noopener"><div class="g">{e(r["group"])}</div><div class="n">{e(r["name"])}</div><p>{e(r["text"])}</p></a>' for r in C["repos"]]
    s.append("</div></div></section>")
    s.append('<section id="skills" style="background:var(--bg2)"><div class="wrap"><div class="kicker">Toolbox</div><h2>Skills and education</h2><p class="sub">The tools I use every day, and where I learned the science behind them.</p><div class="skills">')
    s += [f'<div class="card sk rv"><h3>{e(k)}</h3><div class="tags">' + "".join(f"<span>{e(x)}</span>" for x in v) + "</div></div>" for k, v in C["skills"].items()]
    s.append('</div><div class="edu" style="margin-top:20px">')
    s += [f'<div class="card rv"><div class="kicker" style="font-size:12px">{e(d["when"])}</div><h3 style="margin-top:6px">{e(d["degree"])}</h3><p>{e(d["place"])}</p><p style="margin-top:8px;color:var(--text)">{e(d["note"])}</p></div>' for d in C["education"]]
    s.append("</div></div></section>")
    s.append('<section id="updates"><div class="wrap"><div class="kicker">Log</div><h2>Achievements and updates</h2><p class="sub">A running record of milestones.</p><div class="updates">')
    s += [f'<div class="up rv"><div class="d">{e(u["date"])}</div><div>{e(u["text"])}</div></div>' for u in C["updates"]]
    s.append("</div></div></section>")
    s.append(f'<section id="contact"><div class="wrap"><div class="cta rv"><div class="kicker">Contact</div><h2>Have satellite or GIS data that needs answers?</h2><p class="sub" style="margin:0 auto 10px">I am open to remote projects, collaborations and full-time roles.</p><div class="btns"><a class="btn p" href="mailto:{P["email"]}">{e(P["email"])}</a><a class="btn g" href="{P["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><a class="btn g" href="{P["github"]}" target="_blank" rel="noopener">GitHub</a></div></div></div></section>')
    s.append(foot())
    return "\n".join(s)

def case(p, prev, nxt):
    pre = "../"
    s = [head(f"{p['title']} | {P['name']}", p["summary"], pre)]
    s.append(f"""<header class="ch"><div class="wrap" style="position:relative;z-index:2"><a class="back" href="../index.html#work">← All work</a>
<div class="kicker" style="margin-top:26px">{e(p['place'])}</div><h1 style="font-size:clamp(32px,4.6vw,54px)">{e(p['title'])}</h1><p class="lead">{e(p['summary'])}</p>
<div class="tags" style="margin-top:18px">{''.join(f'<span class="tag">{e(t)}</span>' for t in p['tags'])}</div>
<div class="mstrip">{''.join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in p['metrics'])}</div></div></header>""")
    s.append('<div class="wrap cbody"><div>')
    s.append(f"<h2>The problem</h2><p>{e(p['problem'])}</p>")
    s.append("<h2>Data</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in p["data"]) + "</ul>")
    s.append('<h2>Method</h2><ol class="steps">' + "".join(f"<li>{e(x)}</li>" for x in p["method"]) + "</ol>")
    s.append('<h2>Results</h2><ul class="res">' + "".join(f"<li>{e(x)}</li>" for x in p["results"]) + "</ul>")
    if p.get("images"):
        s.append('<h2>Gallery</h2><div class="gal">' + "".join(f'<img src="../{x}" alt="" loading="lazy">' for x in p["images"]) + "</div>")
    if p.get("lesson"):
        s.append(f'<h2>What I learned</h2><div class="lesson">{e(p["lesson"])}</div>')
    s.append("</div><aside class=\"side\"><h4>Role</h4><p style=\"margin:0 0 18px\">Design, data, modelling, validation and delivery</p><h4>Stack</h4><div class=\"tags\" style=\"margin-bottom:18px\">" + "".join(f'<span class="tag">{e(t)}</span>' for t in p["tags"]) + "</div>")
    if p.get("repo"):
        s.append(f'<a class="btn p" style="width:100%;justify-content:center" href="{p["repo"]}" target="_blank" rel="noopener">View code on GitHub</a>')
    if p.get("paper"):
        s.append(f'<a class="btn g" style="width:100%;justify-content:center;margin-top:10px" href="{p["paper"]}" target="_blank" rel="noopener">Read the paper</a>')
    s.append(f'<a class="btn g" style="width:100%;justify-content:center;margin-top:10px" href="mailto:{P["email"]}">Discuss a similar project</a></aside></div>')
    s.append(f'<div class="wrap nextp"><a href="{prev["slug"]}.html">← {e(prev["title"])}</a><a href="{nxt["slug"]}.html" style="text-align:right">{e(nxt["title"])} →</a></div>')
    s.append(foot())
    return "\n".join(s)

open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(index())
os.makedirs(os.path.join(ROOT, "projects"), exist_ok=True)
pr = C["projects"]
for i, p in enumerate(pr):
    open(os.path.join(ROOT, "projects", p["slug"] + ".html"), "w", encoding="utf-8").write(case(p, pr[i - 1], pr[(i + 1) % len(pr)]))
print(f"built index + {len(pr)} case pages")
