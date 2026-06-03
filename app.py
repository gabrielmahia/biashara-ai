import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Biashara AI — Rasimisha Biashara Yako", page_icon="🏪", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0a12;color:#ede7f6}
.b-card{background:#1a0a2e;border:1px solid #4a148c;border-radius:10px;padding:14px 18px;margin:8px 0}
.step{background:#0d0d1a;border-left:3px solid #7b1fa2;padding:8px 14px;margin:5px 0;border-radius:0 8px 8px 0}
.stButton>button{background:#6a1b9a;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")

SYSTEM = """Wewe ni mshauri wa biashara Kenya. Msaada watu kurasimisha biashara zao.
Eleza hatua kwa Kiswahili rahisi. Toa:
- Hatua halisi na mfuatano wake
- Gharama za makadirio (KES)
- Muda unaohitajika
- Ofisi au tovuti inayohusika
- Tahadhari na makosa ya kawaida
Kama hujui jibu kamili, sema hivyo na umpeleke kwa chanzo rasmi."""

def ask_biashara(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.2,"maxOutputTokens":800}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),
                                     headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🏪 Biashara AI")
st.markdown("**Rasimisha Biashara Yako Kenya**")
st.caption("Mwongozo wa hatua kwa hatua: KRA PIN, vibali, usajili, na uzingatifu")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Anza Biashara", "🔑 KRA & Kodi", "📜 Vibali vya Kaunti", "✅ Orodha ya Ukaguzi"])

with tab1:
    biz_type = st.selectbox("Aina ya biashara:", ["Biashara peke yangu (Sole Proprietor)","Ushirika (Partnership)",
                             "Kampuni (Limited Company)","NGO/CBO","Chama/SACCO","Biashara ya dijiti/online"])
    county = st.selectbox("Kaunti:", ["Nairobi","Kiambu","Mombasa","Kisumu","Nakuru","Machakos","Nyeri","Kakamega"])
    sector = st.selectbox("Sekta:", ["Biashara ya rejareja","Chakula na vinywaji","Teknolojia","Kilimo","Usafirishaji","Afya","Elimu"])
    if st.button("📋 Pata Mwongozo", key="start_btn"):
        q = f"Ninataka kuanzisha {biz_type} ya {sector} katika Kaunti ya {county}. Niambie hatua zote za kurasimisha biashara hii."
        with st.spinner("Ninachambua..."):
            result = ask_biashara(q)
        st.markdown(f'<div class="b-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    tax_q = st.selectbox("Swali la kodi:", ["Jinsi ya kupata KRA PIN","Jinsi ya kusajili VAT","Jinsi ya kulipa kodi ya biashara",
                          "Ninaweza kupata exemption?","Jinsi ya kutumia eTims","Faida za kujisajili na KRA"])
    if st.button("🔑 Niambie", key="kra_btn"):
        with st.spinner("..."):
            result = ask_biashara(tax_q)
        st.markdown(f'<div class="b-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    county2 = st.selectbox("Kaunti yako:", ["Nairobi","Kiambu","Mombasa","Kisumu","Nakuru"], key="c2")
    permit_type = st.selectbox("Kibali:", ["Single Business Permit","Food Handler Certificate","Liquor Licence",
                                "Health Inspection Certificate","Building Permit","Fire Safety Certificate"])
    if st.button("📜 Hatua za Kibali", key="permit_btn"):
        q2 = f"Jinsi ya kupata {permit_type} katika Kaunti ya {county2}? Gharama, muda, na mahitaji?"
        with st.spinner("..."):
            result = ask_biashara(q2)
        st.markdown(f'<div class="b-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### Orodha ya Ukaguzi — Rasimisha Biashara Yako")
    checks = [
        ("KRA PIN Number", "Bure — kra.go.ke", "Masaa 2-24"),
        ("Business Name Registration", "KES 950 — eCitizen", "Siku 1-3"),
        ("Single Business Permit", "KES 5,000-50,000 (inategemea kaunti)", "Siku 5-14"),
        ("VAT Registration (kama mapato >KES 5M/yr)", "Bure — kra.go.ke", "Siku 3-7"),
        ("NHIF Registration", "Bure — nhif.or.ke", "Siku 1-3"),
        ("NSSF Registration", "Bure — nssf.or.ke", "Siku 1-3"),
        ("Leseni ya Biashara ya Kaunti", "Inategemea aina ya biashara", "Wiki 1-4"),
    ]
    for name, cost, time in checks:
        st.markdown(f'<div class="step">✅ <b>{name}</b><br>💰 {cost} | ⏱ {time}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🏪 Biashara AI v1.0 | Habari kwa madhumuni ya elimu | Thibitisha na KRA/eCitizen | CC BY-NC-ND 4.0")
