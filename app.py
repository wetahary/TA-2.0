import streamlit as st
import pandas as pd
st.set_page_config(page_title="Company Game | HE Pilot",page_icon="🎮",layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.block-container{padding-top:1.2rem;max-width:1450px}
[data-testid="stSidebar"]{background:#12243c}[data-testid="stSidebar"] *{color:#edf3fa!important}
.hero{background:linear-gradient(120deg,#12243c,#1f4a68);padding:1.4rem 1.6rem;border-radius:18px;color:white;margin-bottom:1rem}
.hero h1{color:white;font-family:'Space Grotesk';margin:0}.hero p{color:#cbd9e8;margin:.4rem 0 0}
.kpi{background:#f3f6fa;border:1px solid #e4eaf1;padding:1rem;border-radius:14px;min-height:95px}
.kpi small{color:#687b91;font-weight:700;text-transform:uppercase}.kpi strong{display:block;color:#14263d;font-size:1.8rem;font-family:'Space Grotesk'}
.task{border:1px solid #e3eaf2;border-radius:14px;padding:1rem;background:white;margin:.4rem 0}
</style>""",unsafe_allow_html=True)
DEPTS=["Processing HE","Service HE","SCM","Finance","Accounting","HC","GS","Branding & Media","QMS","SHE"]
ROLES={"Game Master":"Top Management","Game Controller":"Operational Leader","Processing HE Player":"Processing HE","Service HE Player":"Service HE","SCM Player":"SCM","Finance Player":"Finance","Accounting Player":"Accounting","HC Player":"HC","GS Player":"GS","Branding & Media Player":"Branding & Media","QMS Guardian":"QMS","SHE Guardian":"SHE"}
SEED=[
("T01","HE-DEMO-026","Validasi permintaan survey","Processing HE","PIC Processing","In Progress","High","4 jam",["Validasi customer dan pemberi instruksi","Cocokkan unit dan lokasi","Tetapkan surveyor","Kirim konfirmasi jadwal"],"Survey request dan konfirmasi jadwal","Membuka proses survey dan estimasi."),
("T02","HE-DEMO-026","Rencana manpower awal","Service HE","Service Planner","Ready","High","1 hari",["Identifikasi skill","Cek ketersediaan teknisi","Cek bay dan tools","Submit rencana manpower"],"Manpower readiness","Menentukan kesiapan kapasitas workshop."),
("T03","HE-DEMO-026","Cek ketersediaan material","SCM","SCM Planner","Ready","High","1 hari",["Identifikasi material indikatif","Cek stok","Tandai item indent","Berikan estimasi lead time"],"Material availability","Mengurangi risiko parts delay."),
("T04","HE-DEMO-026","Survey dan dokumentasi","Processing HE","Surveyor","Blocked","High","1 hari",["Konfirmasi akses unit","Dokumentasi foto","Catat kerusakan","Submit survey report"],"Survey report dan foto","Dasar estimasi dan scope."),
("T05","HE-DEMO-024","Lengkapi quotation","Processing HE","Estimator","At Risk","High","8 jam",["Validasi scope","Review labor dan material","Lampirkan foto","Review internal","Submit quotation"],"Quotation package","Mempengaruhi approval dan kepastian scope."),
("T06","HE-DEMO-023","Konfirmasi ETA material kritis","SCM","Buyer","Blocked","Critical","2 hari",["Konfirmasi vendor","Validasi ETA","Cari alternatif supply","Update Service"],"Vendor confirmation / revised ETA","Berpotensi menggeser target repair."),
("T07","HE-DEMO-022","Review final inspection","QMS","QC Inspector","Ready","Medium","4 jam",["Periksa scope","Periksa fungsi","Catat defect","Terbitkan hasil inspeksi"],"QC checklist","Quality release sebelum handover."),
("T08","HE-DEMO-026","Review kebutuhan safety","SHE","Safety Officer","Ready","High","Sebelum mulai",["Identifikasi hazard","Tentukan kontrol risiko","Validasi JSA / permit","Berikan safety clearance"],"Risk assessment / JSA","Mencegah pekerjaan tanpa kontrol."),
("T09","HE-DEMO-025","Validasi biaya aktual JO","Accounting","Cost Controller","In Progress","Medium","2 hari",["Tarik transaksi material","Validasi labor actual","Cocokkan biaya eksternal","Update JO costing"],"JO cost sheet","Menjaga visibilitas HPP dan margin."),
("T10","HE-DEMO-026","Review kebutuhan pendanaan","Finance","Finance Officer","Ready","Medium","1 hari",["Review payment requirement","Cek budget","Validasi approval","Catat keputusan"],"Payment / budget review","Mendukung kelancaran pengadaan."),
("T11","HE-DEMO-026","Cek fasilitas dan tools","GS","GS Coordinator","Ready","Low","1 hari",["Cek bay","Cek tools dan equipment","Cek utilities","Laporkan gap"],"Facility readiness","Mencegah gangguan unit masuk."),
("T12","HE-DEMO-026","Siapkan komunikasi pelanggan","Branding & Media","Customer Communication","Ready","Low","Milestone",["Validasi informasi dengan PIC","Siapkan update","Minta persetujuan","Catat komunikasi"],"Communication log","Menjaga konsistensi komunikasi.")]
if "tasks" not in st.session_state:
 st.session_state.tasks=[dict(id=x[0],jo=x[1],title=x[2],dept=x[3],owner=x[4],status=x[5],priority=x[6],sla=x[7],check=x[8],evidence=x[9],impact=x[10],step="Selesaikan aktivitas sesuai instruksi, koordinasikan dependency, dan serahkan hasil dengan bukti.") for x in SEED]
if "events" not in st.session_state: st.session_state.events=["09:05 · HE-DEMO-026 · Permintaan survey diterima","09:18 · Processing HE · PIC ditetapkan","09:32 · System · Mission awal dibentuk"]
if "page" not in st.session_state: st.session_state.page="My Mission"
if "gate" not in st.session_state: st.session_state.gate=False
def head(t,s): st.markdown(f'<div class="hero"><h1>{t}</h1><p>{s}</p></div>',unsafe_allow_html=True)
def metric(label,value,hint): st.markdown(f'<div class="kpi"><small>{label}</small><strong>{value}</strong><span style="color:#718198;font-size:.8rem">{hint}</span></div>',unsafe_allow_html=True)
def card(t):
 st.markdown(f'<div class="task"><b>{t["title"]}</b> &nbsp; <span style="color:#55708c">[{t["status"]}]</span><div style="color:#718198;font-size:.82rem">{t["jo"]} · {t["dept"]} · PIC {t["owner"]}</div><div style="font-size:.85rem">Priority: {t["priority"]} · SLA: {t["sla"]}</div></div>',unsafe_allow_html=True)
 if st.button("Open mission →",key="open"+t["id"],use_container_width=True):
  st.session_state.sel=t["id"];st.session_state.page="Mission Detail";st.rerun()
with st.sidebar:
 st.markdown("## 🎮 COMPANY GAME")
 st.caption("TRINITY AUTO · HE PILOT 1.0")
 role=st.selectbox("Simulate player role",list(ROLES))
 dept=ROLES[role]
 st.caption("Role selector hanya simulasi, bukan autentikasi.")
 st.divider()
 pages=["Command Center","My Mission","Mission Board","Team Arena","Live Operations","Performance & Rank","Challenge Lab","Mission Detail","Bug & Feedback"]
 st.session_state.page=st.radio("NAVIGATION",pages,index=pages.index(st.session_state.page))
 st.divider();st.success("Synthetic data only");st.caption("Local prototype · No Odoo connection")
tasks=st.session_state.tasks
open_tasks=[t for t in tasks if t["status"] not in ("Verified","Completed")]
blocked=[t for t in open_tasks if t["status"]=="Blocked"]
atrisk=[t for t in open_tasks if t["status"]=="At Risk"]
mine=tasks if dept in ("Top Management","Operational Leader") else [t for t in tasks if t["dept"]==dept]
p=st.session_state.page
if p=="Command Center":
 head("Command Center","Company-wide operational picture · Synthetic HE portfolio")
 c=st.columns(4)
 for col,args in zip(c,[("Active Missions","08","Across pilot departments"),("Open Tasks",len(open_tasks),f"{len(blocked)} blocked · {len(atrisk)} at risk"),("JO Value at Risk","Rp 1.08 B","Illustrative only"),("On-time Completion","87%","Synthetic baseline")]):
  with col: metric(*args)
 l,r=st.columns([1.3,1])
 with l:
  st.subheader("Cross-department watchlist")
  for t in blocked+atrisk: card(t)
 with r:
  st.subheader("Department pulse")
  st.dataframe(pd.DataFrame({"Department":DEPTS,"Open tasks":[sum(x["dept"]==d and x["status"] not in ("Verified","Completed") for x in tasks) for d in DEPTS]}),hide_index=True,use_container_width=True)
  st.subheader("Recent events")
  for e in st.session_state.events[-6:]: st.write("• "+e)
elif p=="My Mission":
 head("My Mission",f"Your mission space · {role} · {dept}")
 c=st.columns(4)
 for col,args in zip(c,[("My tasks",len(mine),"Assigned to your team"),("Priority",sum(t["priority"] in ("High","Critical") for t in mine),"High / Critical"),("Blocked",sum(t["status"]=="Blocked" for t in mine),"Needs action"),("Completed",sum(t["status"]=="Verified" for t in mine),"Verified tasks")]):
  with col: metric(*args)
 st.write("Fokus: selesaikan prioritas, buka blocker, dan jaga handover tetap jelas.")
 if not mine: st.info("Belum ada task pada role ini. Game Controller dapat melakukan assignment.")
 for t in sorted(mine,key=lambda x:{"Critical":0,"High":1,"Medium":2,"Low":3}[x["priority"]]): card(t)
elif p=="Mission Board":
 head("Mission Board","One job order · Multiple workstreams · Shared outcome")
 stages=[("01 · Assessment & Commercial","Processing HE","Survey · Estimate · Quotation · Approval · JO"),("02 · Operational Readiness","Service HE · SCM · HC · GS · Finance · SHE","Manpower · Material · Facility · Budget · Risk"),("03 · Repair Execution","Service HE · SCM · QMS · SHE · Accounting","Repair · Material issue · Quality checkpoints · Safety"),("04 · Completion & Handover","Processing HE · Service HE · QMS · Finance · Accounting · Branding & Media","Final QC · Joint inspection · BAST · Invoice readiness")]
 for title,owners,desc in stages:
  with st.expander(f"{title} — {owners}",expanded=title.startswith("02")):
   st.write(desc)
   for t in tasks:
    if t["dept"] in owners.split(" · "): card(t)
 st.caption("Mission templates konseptual; setiap JO mengaktifkan workstream sesuai kebutuhan.")
elif p=="Team Arena":
 head("Team Arena","Department capacity, contribution and shared performance")
 df=pd.DataFrame({"Department":DEPTS,"Open tasks":[sum(t["dept"]==d and t["status"] not in ("Verified","Completed") for t in tasks) for d in DEPTS],"Verified":[sum(t["dept"]==d and t["status"]=="Verified" for t in tasks) for d in DEPTS]})
 st.dataframe(df,use_container_width=True,hide_index=True)
 for d in DEPTS:
  with st.expander(d):
   for t in [x for x in tasks if x["dept"]==d]: st.write(f'**{t["title"]}** — {t["status"]} · {t["jo"]}')
elif p=="Live Operations":
 head("Live Operations","Alerts, dependencies and event stream")
 if blocked: st.error(f"{len(blocked)} blocked task(s) need recovery.")
 if atrisk: st.warning(f"{len(atrisk)} task(s) at risk.")
 for t in blocked+atrisk: card(t)
 st.subheader("Event stream")
 for e in reversed(st.session_state.events): st.write("• "+e)
elif p=="Performance & Rank":
 head("Performance & Rank","Balanced performance · Individual and team outcome")
 parts={"Company Result":88,"Department Performance":82,"Process Integration":76,"Governance & Safety":94}
 score=sum(v*w for v,w in zip(parts.values(),[.4,.3,.2,.1]));score=min(score,59) if st.session_state.gate else score
 c=st.columns(4)
 for col,args in zip(c,[("Game score",f"{score:.1f}","Synthetic score"),("Experience","420 XP","Illustrative"),("Team level","Level 04","Collaborator"),("Verified tasks",sum(t["status"]=="Verified" for t in tasks),"Evidence accepted")]):
  with col: metric(*args)
 st.bar_chart(pd.DataFrame({"Score":parts}).T)
 st.latex(r"S=0.4C+0.3D+0.2I+0.1G")
 st.checkbox("Activate critical safety / compliance gate (demo)",key="gate")
 if st.session_state.gate: st.error("Hard gate active: illustrative score capped at 59.")
 st.caption("Bobot dan angka adalah konfigurasi dummy, bukan KPI resmi.")
elif p=="Challenge Lab":
 head("Challenge Lab","Test decisions, consequences and recovery paths")
 sc=st.selectbox("Choose scenario",["Normal Operation","Material Shortage","Insurance Supplement Not Approved","QC Failure / Rework","Critical Safety Hazard"])
 desc={"Normal Operation":"Approval, material, manpower and safety controls ready.","Material Shortage":"Critical component unavailable at planned start.","Insurance Supplement Not Approved":"Additional damage identified but payer approval pending.","QC Failure / Rework":"Final inspection finds defect requiring correction.","Critical Safety Hazard":"Unsafe condition identified during execution."}
 st.info(desc[sc])
 opts={"Normal Operation":["Confirm readiness","Start approved work"],"Material Shortage":["Expedite vendor","Check approved alternative","Resequence unaffected work"],"Insurance Supplement Not Approved":["Hold only unapproved additional scope","Seek written approval","Continue unrelated approved scope only if authorized and safe"],"QC Failure / Rework":["Record NCR","Assign corrective action","Re-inspect before release"],"Critical Safety Hazard":["Stop affected work","Secure area and report hazard","Resume only after authorized clearance"]}
 for x in opts[sc]: st.checkbox(x,key=sc+x)
 if st.button("Apply scenario to simulation",type="primary"):
  if sc=="Material Shortage":
   next(t for t in tasks if t["id"]=="T06")["status"]="Blocked"
  elif sc=="QC Failure / Rework": next(t for t in tasks if t["id"]=="T07")["status"]="At Risk"
  elif sc=="Critical Safety Hazard": st.session_state.gate=True
  st.session_state.events.append(f"Now · Challenge · {sc} applied");st.success("Scenario applied. Check Live Operations and Performance.")
 st.caption("Scenario ini adalah latihan keputusan, bukan otorisasi operasional.")
elif p=="Mission Detail":
 head("Mission Detail","Understand the task · Execute steps · Submit evidence")
 ids=[t["id"] for t in tasks];sel=st.selectbox("Select mission",ids,format_func=lambda i:next(t["title"]+" · "+t["jo"] for t in tasks if t["id"]==i))
 t=next(t for t in tasks if t["id"]==sel)
 a,b=st.columns([1.3,1])
 with a:
  st.subheader(t["title"]);st.caption(f'{t["id"]} · {t["jo"]} · {t["dept"]} · {t["owner"]}');st.write(t["step"])
  checks=[st.checkbox(x,key=sel+str(i)) for i,x in enumerate(t["check"])]
  st.markdown("**Evidence required**");st.info(t["evidence"])
  evidence=st.text_input("Evidence reference / note",placeholder="Synthetic document reference")
 with b:
  st.metric("SLA",t["sla"]);st.metric("Priority",t["priority"]);st.write("**Expected impact**");st.write(t["impact"])
  status=st.selectbox("Update status",["Ready","In Progress","Blocked","At Risk","Submitted for Review","Verified"],index=["Ready","In Progress","Blocked","At Risk","Submitted for Review","Verified"].index(t["status"]) if t["status"] in ["Ready","In Progress","Blocked","At Risk","Submitted for Review","Verified"] else 0)
  if st.button("Save mission update",type="primary"):
   t["status"]=status;st.session_state.events.append(f"Now · {t['dept']} · {t['id']} → {status}");st.rerun()
  if st.button("Submit for verification"):
   if not all(checks): st.error("Complete seluruh checklist.")
   elif not evidence.strip(): st.error("Tambahkan evidence reference.")
   else: t["status"]="Verified";st.session_state.events.append(f"Now · {t['dept']} · {t['id']} verified in demo");st.success("Verified in demo.");st.rerun()
 st.caption("Verifikasi pada prototype masih simulasi; produksi wajib memakai verifier terpisah.")
elif p=="Bug & Feedback":
 head("Bug & Feedback","Capture usability issues and simulation defects")
 with st.form("bug"):
  title=st.text_input("Bug / feedback title");area=st.selectbox("Area",["Navigation","My Mission","Mission Detail","Workflow","Scoring","Scenario","Visual / UI","Other"]);sev=st.selectbox("Severity",["Low","Medium","High","Critical"]);detail=st.text_area("Steps to reproduce / expected vs actual");ok=st.form_submit_button("Record feedback")
 if ok: st.session_state.events.append(f"Feedback · {sev} · {area} · {title} · {detail}");st.success("Feedback recorded in this session.")
 st.download_button("Download event log CSV",pd.DataFrame({"Event":st.session_state.events}).to_csv(index=False).encode(),file_name="company_game_event_log.csv",mime="text/csv")
 st.subheader("Known limitations")
 for x in ["No authentication or secure RBAC","No persistent shared database","No Odoo connection","No multi-user sync","SLA values are illustrative, not live timers","Synthetic data only"]: st.write("• "+x)
st.divider();st.caption("COMPANY GAME MASTER · HE PILOT 1.0 · SYNTHETIC DATA ONLY · LOCAL DESIGN PROTOTYPE")
