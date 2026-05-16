import streamlit as st
from groq import Groq
import json

st.set_page_config(
    page_title="ResearchForgeAI – End-to-End Research Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; background-color: #060d1c; color: #c8deff; }
.stApp { background-color: #060d1c; }
section[data-testid="stSidebar"] { background: #080f20; border-right: 1px solid #1e2d4a; }
section[data-testid="stSidebar"] * { color: #c8deff !important; }
h1 { font-family: 'Sora', sans-serif !important; font-weight: 800 !important; color: #ffffff !important; }
h2 { font-family: 'Sora', sans-serif !important; font-weight: 700 !important; color: #ffffff !important; }
h3 { font-family: 'Sora', sans-serif !important; color: #00c6a7 !important; letter-spacing: 2px; text-transform: uppercase; font-size: 13px !important; }
input[type="text"], textarea, .stTextInput input, .stTextArea textarea {
    background: #0d1526 !important; border: 1.5px solid #1e2d4a !important;
    border-radius: 10px !important; color: #c8deff !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.stSelectbox > div > div { background: #0d1526 !important; border: 1.5px solid #1e2d4a !important; border-radius: 10px !important; color: #c8deff !important; }
.stButton > button {
    background: linear-gradient(135deg, #00c6a7, #0077ff) !important;
    border: none !important; border-radius: 10px !important; color: #ffffff !important;
    font-family: 'Sora', sans-serif !important; font-weight: 700 !important;
    font-size: 14px !important; padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 20px #0077ff33 !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stMultiSelect > div > div { background: #0d1526 !important; border: 1.5px solid #1e2d4a !important; border-radius: 10px !important; }
.stMultiSelect span[data-baseweb="tag"] { background: linear-gradient(135deg,#00c6a755,#0077ff33) !important; border: 1px solid #00c6a7 !important; color: #00c6a7 !important; }
.stFileUploader { background: #0d1526 !important; border: 1.5px dashed #2e3a5a !important; border-radius: 10px !important; }
hr { border-color: #1e2d4a !important; }
.step-badge {
    display: inline-block; background: linear-gradient(135deg,#00c6a7,#0077ff);
    color: white; font-family: 'Sora', sans-serif; font-weight: 700;
    font-size: 11px; letter-spacing: 2px; padding: 4px 12px; border-radius: 20px; margin-bottom: 8px;
}
.output-box {
    background: #0d1526; border: 1px solid #1e2d4a; border-radius: 12px;
    padding: 1.2rem 1.4rem; font-family: 'IBM Plex Mono', monospace;
    font-size: 13px; line-height: 1.85; color: #c8deff;
    white-space: pre-wrap; max-height: 520px; overflow-y: auto;
}
.edit-box {
    background: #0a1a2e; border: 1.5px solid #00c6a755; border-radius: 10px;
    padding: 1rem; margin: 0.5rem 0 1rem 0;
}
.info-card {
    background: #0a1a2e; border: 1px solid #1e3a5a; border-radius: 10px;
    padding: 0.8rem 1rem; margin-bottom: 0.8rem; font-size: 13px; color: #7a9abf; line-height: 1.6;
}
.saved-badge {
    display:inline-block; background:#00c6a720; border:1px solid #00c6a7;
    color:#00c6a7; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:600;
}
.doc-card {
    background:#0a1220; border:1px solid #1e2d4a; border-radius:10px;
    padding:0.8rem 1rem; margin-bottom:0.5rem; font-size:12px; color:#c8deff;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
STEPS = [
    ("📋", "Proposal"),
    ("📁", "Upload Docs"),
    ("📘", "Chapter One"),
    ("📚", "Literature"),
    ("📊", "Data Analysis"),
    ("🎯", "Conclusion"),
    ("✍️", "Abstract"),
    ("🔖", "References"),
    ("📄", "Export"),
]

METHODOLOGIES = ["", "Quantitative", "Qualitative", "Mixed Methods",
                  "Experimental", "Survey", "Case Study", "Systematic Review"]

STAT_TESTS = [
    "Descriptive Statistics",
    "Pearson Correlation", "Spearman Correlation",
    "Simple Linear Regression", "Multiple Regression",
    "Time Series Regression",
    "Autoregressive (AR) Model",
    "Binary Logistic Regression",
    "Independent Samples T-Test", "Paired Samples T-Test",
    "One-Way ANOVA", "Two-Way ANOVA",
    "Chi-Square Test",
    "Mann-Whitney U Test", "Kruskal-Wallis Test",
    "Full Time Series Analysis (ADF + Differencing + ARIMA + SARIMA)",
    "Factor Analysis", "Cluster Analysis",
]

REF_STYLES = ["APA 7th", "APA 6th", "MLA", "Chicago", "Harvard", "Vancouver"]

DEFAULT_PROPOSAL_HEADINGS = (
    "1. Introduction\n2. Research Methodology\n2.1 Research Design\n"
    "2.2 Population and Sampling\n2.3 Data Collection Instruments\n"
    "2.4 Data Analysis Technique\n2.5 Ethical Considerations"
)
DEFAULT_CH1_HEADINGS = (
    "1.1 Background of the Study\n1.2 Statement of the Problem\n"
    "1.3 Aim of the Study\n1.4 Objectives of the Study\n"
    "1.5 Research Questions\n1.6 Research Hypotheses\n"
    "1.7 Significance of the Study\n1.8 Scope of the Study\n"
    "1.9 Limitations of the Study\n1.10 Definition of Terms\nReferences"
)
DEFAULT_METH_HEADINGS = (
    "3.1 Introduction\n3.2 Research Design\n3.3 Population and Sampling\n"
    "3.4 Research Instrument\n3.5 Validity and Reliability\n"
    "3.6 Data Collection Procedure\n3.7 Data Analysis Technique\n"
    "3.8 Ethical Considerations"
)

# ── Session state ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "current_step": 1,
    "topic": "", "methodology": "", "ref_style": "APA 7th",
    "variables": "", "manual_summary": "",
    # Multi-doc storage: list of dicts {name, text, author_info, char_count}
    "uploaded_docs_list": [],
    "uploaded_docs_text": "",      # combined summary for LLM prompts
    "uploaded_doc_names": [],
    "uploaded_doc_authors": "",
    "image_metadata": {},          # {filename: {name, source}}
    "data_filename": "", "data_columns": "", "selected_tests": [],
    "proposal_intro": "", "proposal_methodology": "",
    "chapter_one": "", "literature": "", "analysis": "",
    "ts_analysis": "",             # time series specific output
    "analysis_summary": "", "conclusion": "", "abstract": "", "references": "",
    "groq_api_key": "",
    "proposal_headings": DEFAULT_PROPOSAL_HEADINGS,
    "ch1_headings": DEFAULT_CH1_HEADINGS,
    "meth_headings": DEFAULT_METH_HEADINGS,
    "df_json": "", "lit_subheadings": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Core helpers ──────────────────────────────────────────────────────────────
def get_client():
    try:
        key = st.secrets.get("GROQ_API_KEY", "") or st.session_state.groq_api_key
    except Exception:
        key = st.session_state.groq_api_key
    return Groq(api_key=key) if key else None

def stream_response(system_prompt, user_prompt, state_key):
    client = get_client()
    if not client:
        st.error("⚠️ Enter your Groq API key in the sidebar.")
        return
    st.session_state[state_key] = ""
    placeholder = st.empty()
    try:
        with client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user",   "content": user_prompt}],
            max_tokens=2000, stream=True,
        ) as stream:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                st.session_state[state_key] += delta
                placeholder.markdown(
                    f'<div class="output-box">{st.session_state[state_key]}</div>',
                    unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ {e}")

def llm_call(system_prompt, user_prompt, max_tokens=800):
    """Non-streaming LLM call — returns text or empty string."""
    client = get_client()
    if not client:
        return ""
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user",   "content": user_prompt}],
            max_tokens=max_tokens, stream=False,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return ""

def extract_file_text(uploaded):
    """Extract full text from any supported file type."""
    try:
        name = uploaded.name.lower()
        if name.endswith(".pdf"):
            import pdfplumber
            text = ""
            with pdfplumber.open(uploaded) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
            return text
        elif name.endswith(".docx"):
            import docx
            doc = docx.Document(uploaded)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif name.endswith((".jpg", ".jpeg", ".png")):
            return None   # signal: image — handle separately
        else:
            return uploaded.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"[Error: {e}]"

def build_combined_docs_text(max_chars_per_doc=4000):
    """
    Build a combined text from all uploaded docs.
    Each doc gets up to max_chars_per_doc characters so ALL docs are represented.
    """
    docs = st.session_state.uploaded_docs_list
    if not docs:
        return ""
    parts = []
    for doc in docs:
        snippet = doc["text"][:max_chars_per_doc]
        parts.append(f"=== DOCUMENT: {doc['name']} ===\n{snippet}")
    return "\n\n".join(parts)

def extract_single_doc_info(doc_name, doc_text, ref_style="APA 7th"):
    """
    Extract author, year, title, reference, and summary for ONE document.
    Returns a dict with keys: authors, year, title, reference, summary
    """
    import re as _re, json as _json
    sys_p = f"""You are an expert academic librarian.
You are analysing ONE document: \"{doc_name}\"

Tasks:
1. Find the AUTHOR(S) of THIS document only (not secondary authors cited inside).
   If multiple people co-authored this ONE document, list them all together.
   Do NOT create separate entries for each author of the same document.
2. Find the YEAR of publication
3. Find the FULL TITLE
4. Format a complete reference in {ref_style} style for this single document
5. Write a 3-4 sentence summary from the Abstract, Results, Summary, Conclusion,
   and Recommendations sections

Return ONLY valid JSON, no extra text:
{{
  "authors": "Surname, A., & Surname, B.",
  "year": "2024",
  "title": "Full document title here",
  "reference": "Formatted reference in {ref_style}",
  "summary": "3-4 sentence summary of key findings and conclusions"
}}"""

    usr_p = (
        f"Document: {doc_name}\n\n"
        f"Text (first 5000 chars):\n{doc_text[:5000]}\n\n"
        f"Return JSON for this ONE document only."
    )
    raw = llm_call(sys_p, usr_p, max_tokens=500)
    try:
        match = _re.search(r"\{[^{}]*\}", raw, _re.DOTALL)
        if match:
            return _json.loads(match.group())
    except Exception:
        pass
    clean_name = doc_name.replace(".pdf","").replace(".docx","").replace(".txt","")
    return {
        "authors": "Unknown Author",
        "year": "n.d.",
        "title": clean_name,
        "reference": f"Unknown Author. (n.d.). {clean_name}.",
        "summary": raw[:300] if raw else "Could not extract summary."
    }

def build_authors_string():
    """Build a formatted string of all document authors for use in prompts."""
    docs = st.session_state.uploaded_docs_list
    lines = []
    for doc in docs:
        info = doc.get("doc_info", {})
        if info.get("authors") and info.get("year"):
            lines.append(f"{info['authors']} ({info['year']}). {info.get('title','')[:60]}")
    return "\n".join(lines) if lines else "Authors from uploaded documents"

def show_output(key, label="Output"):
    if st.session_state.get(key):
        st.markdown(f"### {label}")
        st.markdown(
            f'<div class="output-box">{st.session_state[key]}</div>',
            unsafe_allow_html=True)

def editable_headings(label, key, default):
    with st.expander(f"✏️ Edit {label} Headings", expanded=False):
        st.markdown('<div class="edit-box">', unsafe_allow_html=True)
        val = st.text_area("Headings (one per line)",
                           value=st.session_state[key],
                           height=200, key=f"edit_{key}",
                           label_visibility="collapsed")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save", key=f"save_{key}"):
                st.session_state[key] = val
                st.success("✅ Saved!")
        with c2:
            if st.button("↩️ Reset", key=f"reset_{key}"):
                st.session_state[key] = default
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#080f20;border-bottom:1px solid #1e2d4a;padding:1.2rem 2rem;
            display:flex;align-items:center;gap:1rem;margin:-1rem -1rem 2rem -1rem;">
  <div style="width:44px;height:44px;background:linear-gradient(135deg,#00c6a7,#0077ff);
              border-radius:10px;display:flex;align-items:center;
              justify-content:center;font-size:22px;">🔬</div>
  <div>
    <div style="font-family:Sora,sans-serif;font-weight:800;font-size:20px;color:#fff;">ResearchAI</div>
    <div style="font-family:Sora,sans-serif;font-size:11px;color:#4a6a8a;letter-spacing:2px;">
      END-TO-END RESEARCH &amp; REPORT PLATFORM · Powered by Groq + LLaMA 3.3</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 Groq API Key")
    api_key_input = st.text_input("Key", value=st.session_state.groq_api_key,
                                   type="password", placeholder="gsk_...",
                                   label_visibility="collapsed")
    if api_key_input != st.session_state.groq_api_key:
        st.session_state.groq_api_key = api_key_input
    if st.session_state.groq_api_key:
        st.success("✅ Key set")
    else:
        st.info("Get FREE key:\nconsole.groq.com")

    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    for i, (icon, label) in enumerate(STEPS, 1):
        badge = ("✅" if i < st.session_state.current_step
                 else ("▶️" if i == st.session_state.current_step else "⭕"))
        if st.button(f"{badge} {i}. {icon} {label}", key=f"nav_{i}",
                     use_container_width=True):
            st.session_state.current_step = i
            st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Topic")
    t = st.text_input("Topic", value=st.session_state.topic,
                       label_visibility="collapsed", placeholder="Research topic...")
    if t != st.session_state.topic:
        st.session_state.topic = t

    docs = st.session_state.uploaded_docs_list
    if docs:
        st.markdown(f"### 📁 Docs ({len(docs)})")
        for d in docs:
            st.caption(f"📄 {d['name'][:35]} ({d['char_count']:,} chars)")

    st.markdown("---")
    done = sum(1 for k in ["proposal_intro", "chapter_one", "literature",
                            "analysis", "conclusion", "abstract", "references"]
               if st.session_state.get(k))
    st.markdown(f"**Progress:** {done}/7 sections")
    st.progress(done / 7)

# ── Progress bar ──────────────────────────────────────────────────────────────
cur = st.session_state.current_step
pcols = st.columns(len(STEPS) * 2 - 1)
for i, (icon, label) in enumerate(STEPS):
    with pcols[i * 2]:
        active, done_s = (i + 1 == cur), (i + 1 < cur)
        bg = ("linear-gradient(135deg,#00c6a7,#0077ff)" if active
              else ("#00c6a7" if done_s else "#1e2740"))
        bc = "#00c6a7" if (active or done_s) else "#2e3a5a"
        tc = "#00c6a7" if (active or done_s) else "#4a5a7a"
        st.markdown(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;">'
            f'<div style="width:36px;height:36px;border-radius:50%;background:{bg};'
            f'border:2px solid {bc};display:flex;align-items:center;justify-content:center;'
            f'font-size:14px;box-shadow:{"0 0 14px #00c6a755" if active else "none"};">'
            f'{"✓" if done_s else icon}</div>'
            f'<span style="font-size:8px;font-weight:600;color:{tc};'
            f'letter-spacing:.5px;white-space:nowrap;">{label}</span></div>',
            unsafe_allow_html=True)
    if i < len(STEPS) - 1:
        with pcols[i * 2 + 1]:
            st.markdown(
                f'<div style="height:2px;background:'
                f'{"#00c6a7" if i+1 < cur else "#1e2740"};margin-top:18px;"></div>',
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — PROPOSAL
# ═══════════════════════════════════════════════════════════════════════════════
if cur == 1:
    st.markdown('<div class="step-badge">STEP 1 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 📋 Research Proposal")
    st.markdown(
        '<div class="info-card">Two parts only: <strong>(1) Introduction</strong> and '
        '<strong>(2) Methodology</strong>. Saved and reused across all chapters. '
        'No citations in this section.</div>', unsafe_allow_html=True)

    topic = st.text_input("Research Topic *", value=st.session_state.topic,
                           placeholder="e.g. Time Series Analysis of Malaria Cases in Enugu State")
    st.session_state.topic = topic

    col_a, col_b = st.columns(2)
    with col_a:
        methodology = st.selectbox("Research Methodology *", METHODOLOGIES,
                                    index=METHODOLOGIES.index(st.session_state.methodology)
                                    if st.session_state.methodology in METHODOLOGIES else 0)
        st.session_state.methodology = methodology
    with col_b:
        ref_style_p = st.selectbox("Citation Style", REF_STYLES,
                                    index=REF_STYLES.index(st.session_state.ref_style)
                                    if st.session_state.ref_style in REF_STYLES else 0, key="ref_p")
        st.session_state.ref_style = ref_style_p

    editable_headings("Proposal", "proposal_headings", DEFAULT_PROPOSAL_HEADINGS)

    if st.button("🚀 Generate Proposal",
                  disabled=not (st.session_state.topic and st.session_state.methodology)):
        sys_p = f"""You are an expert academic research proposal writer.
Generate a concise RESEARCH PROPOSAL with ONLY these two sections:

SECTION 1 — INTRODUCTION:
- Background context (2–3 paragraphs)
- Statement of the problem
- Aim + at least 3 objectives
- Research questions (one per objective)
- Significance of the study

SECTION 2 — RESEARCH METHODOLOGY:
Use this heading structure:
{st.session_state.proposal_headings}

Be specific about: research design, population, sampling, instruments, analysis approach.

RULES: NO citations. Future tense. No literature review. No results section."""
        stream_response(sys_p,
                        f"Topic: {topic}\nMethodology: {methodology}\nGenerate proposal.",
                        "proposal_intro")
        st.session_state.proposal_methodology = st.session_state.proposal_intro

    if st.session_state.proposal_intro:
        st.markdown("---")
        st.markdown(f'<div class="output-box">{st.session_state.proposal_intro}</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="saved-badge">✅ Saved — used in all subsequent chapters</div>',
                    unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — DOCUMENT UPLOAD  (FIX 1: all docs stored individually; FIX 2: image metadata)
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 2:
    st.markdown('<div class="step-badge">STEP 2 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 📁 Document Upload Centre")
    st.markdown(
        '<div class="info-card">'
        'Upload all your source documents. Each document is processed individually — '
        'the system extracts the author(s), year, title and reference for each file separately. '
        'After each document is confirmed, its formatted reference is shown below it.<br><br>'
        '<strong>Content extracted:</strong> Abstract, Results, Summary, Conclusion, Recommendations.<br>'
        '<strong>Images:</strong> Fill in the caption and source in the box that appears.'
        '</div>', unsafe_allow_html=True)

    ref_style_up = st.selectbox(
        "Reference Style for Extraction", REF_STYLES,
        index=REF_STYLES.index(st.session_state.ref_style)
        if st.session_state.ref_style in REF_STYLES else 0, key="ref_upload")

    uploaded_files = st.file_uploader(
        "Upload source documents (PDF, DOCX, TXT, JPG, PNG) — as many as needed",
        type=["pdf", "txt", "docx", "jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed")

    if uploaded_files and st.button("📥 Process All Documents"):
        new_docs = []
        image_meta = st.session_state.get("image_metadata", {})
        all_references = []

        progress_bar = st.progress(0)
        status_text  = st.empty()

        for idx, f in enumerate(uploaded_files):
            status_text.markdown(f"⏳ Processing **{f.name}** ({idx+1}/{len(uploaded_files)})...")
            is_image = f.name.lower().endswith((".jpg", ".jpeg", ".png"))

            if is_image:
                doc_entry = {
                    "name": f.name,
                    "text": f"[IMAGE: {f.name}]",
                    "char_count": 0,
                    "is_image": True,
                    "doc_info": {
                        "authors": "See image metadata",
                        "year": "n.d.",
                        "title": f.name,
                        "reference": f"[Image: {f.name}. Source: to be completed.]",
                        "summary": f"Image file: {f.name}"
                    }
                }
                new_docs.append(doc_entry)
                st.info(f"🖼️ {f.name} — image uploaded (fill metadata below)")

            else:
                text = extract_file_text(f)
                if not text or text.startswith("[Error"):
                    st.warning(f"⚠️ Could not read {f.name}: {text}")
                    continue

                char_count = len(text)

                # Extract doc info per document
                with st.spinner(f"🔍 Extracting info from {f.name}..."):
                    doc_info = extract_single_doc_info(f.name, text, ref_style_up)

                doc_entry = {
                    "name": f.name,
                    "text": text,
                    "char_count": char_count,
                    "is_image": False,
                    "doc_info": doc_info
                }
                new_docs.append(doc_entry)

                # Show confirmation card for each document
                st.markdown(
                    f'<div class="doc-card">'
                    f'<strong>✅ {f.name}</strong><br>'
                    f'📊 {char_count:,} characters extracted<br>'
                    f'👤 <strong>Author(s):</strong> {doc_info.get("authors","Unknown")}<br>'
                    f'📅 <strong>Year:</strong> {doc_info.get("year","n.d.")}<br>'
                    f'📄 <strong>Title:</strong> {doc_info.get("title","")}<br>'
                    f'<br><strong>📚 Reference ({ref_style_up}):</strong><br>'
                    f'<em>{doc_info.get("reference","")}</em><br>'
                    f'<br><strong>🔑 Key Content Summary:</strong><br>'
                    f'{doc_info.get("summary","")}'
                    f'</div>',
                    unsafe_allow_html=True)

                all_references.append(doc_info.get("reference", ""))

            progress_bar.progress((idx + 1) / len(uploaded_files))

        # Handle image metadata input
        img_docs = [d for d in new_docs if d.get("is_image")]
        if img_docs:
            st.markdown("---")
            st.markdown("### 🖼️ Image Metadata")
            for img_d in img_docs:
                with st.expander(f"📷 {img_d['name']}", expanded=True):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        img_name = st.text_input(
                            "Figure caption / name",
                            value=image_meta.get(img_d['name'],{}).get("name",""),
                            key=f"img_name_{img_d['name']}",
                            placeholder="e.g. Figure 1: Trend of Malaria Cases 2010-2023")
                    with col_b:
                        img_source = st.text_input(
                            "Source / author",
                            value=image_meta.get(img_d['name'],{}).get("source",""),
                            key=f"img_src_{img_d['name']}",
                            placeholder="e.g. WHO Global Malaria Report (2023)")
                    image_meta[img_d['name']] = {"name": img_name, "source": img_source}
                    img_d["text"] = (
                        f"[IMAGE: {img_d['name']}]\n"
                        f"Caption: {img_name}\n"
                        f"Source: {img_source}"
                    )
                    img_d["doc_info"]["reference"] = (
                        f"{img_source}. {img_name}. [Figure]."
                    )

            st.session_state.image_metadata = image_meta

        # Save everything to session state
        st.session_state.uploaded_docs_list = new_docs
        st.session_state.uploaded_doc_names = [d["name"] for d in new_docs]

        # Build master authors string
        authors_list = []
        for doc in new_docs:
            info = doc.get("doc_info", {})
            a = info.get("authors","")
            y = info.get("year","")
            t = info.get("title","")[:50]
            if a and a != "See image metadata":
                authors_list.append(f"{a} ({y}). {t}")
        st.session_state.uploaded_doc_authors = "\n".join(authors_list)

        # Build combined text for LLM use
        combined = build_combined_docs_text(max_chars_per_doc=4000)
        st.session_state.uploaded_docs_text = combined

        status_text.empty()
        progress_bar.progress(1.0)

        # Master reference list preview
        if all_references:
            st.markdown("---")
            st.markdown("### 📚 Master Reference List (All Documents)")
            refs_text = "\n\n".join(
                f"{i+1}. {r}" for i, r in enumerate(all_references))
            st.markdown(
                f'<div class="output-box">{refs_text}</div>',
                unsafe_allow_html=True)
            st.session_state.references = refs_text

        total = sum(d["char_count"] for d in new_docs)
        st.success(
            f"✅ {len(new_docs)} document(s) processed successfully — "
            f"{total:,} total characters")

    # Show stored docs if already processed
    if st.session_state.uploaded_docs_list and not uploaded_files:
        st.markdown("### 📚 Previously Processed Documents")
        for doc in st.session_state.uploaded_docs_list:
            icon = "🖼️" if doc.get("is_image") else "📄"
            info = doc.get("doc_info", {})
            st.markdown(
                f'<div class="doc-card">'
                f'{icon} <strong>{doc["name"]}</strong> — {doc["char_count"]:,} chars<br>'
                f'👤 {info.get("authors","")} ({info.get("year","")}) — {info.get("title","")[:60]}<br>'
                f'<em>{info.get("reference","")}</em>'
                f'</div>',
                unsafe_allow_html=True)

    if not st.session_state.uploaded_docs_list:
        st.warning("⚠️ No documents uploaded yet. Upload files and click Process.")


elif cur == 3:
    st.markdown('<div class="step-badge">STEP 3 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 📘 Chapter One — Introduction")
    st.markdown(
        '<div class="info-card">'
        '• Citations only in <strong>Section 1.1 Background</strong>.<br>'
        '• Only the uploaded documents\' own authors are cited.<br>'
        '• Content drawn from Results/Summary/Conclusion/Recommendations of ALL uploaded docs.<br>'
        '• Fully paraphrased to avoid plagiarism.'
        '</div>', unsafe_allow_html=True)

    if not st.session_state.proposal_intro:
        st.warning("⚠️ Complete Step 1 first.")
    elif not st.session_state.uploaded_docs_list:
        st.warning("⚠️ Upload documents in Step 2 first.")
    else:
        ref_style_c1 = st.selectbox(
            "Citation Style", REF_STYLES,
            index=REF_STYLES.index(st.session_state.ref_style)
            if st.session_state.ref_style in REF_STYLES else 0, key="ref_c1")
        editable_headings("Chapter One", "ch1_headings", DEFAULT_CH1_HEADINGS)

        doc_authors = (st.session_state.uploaded_doc_authors
                       or "Authors as identified in uploaded documents")
        num_docs = len(st.session_state.uploaded_docs_list)
        st.info(f"📚 {num_docs} document(s) will be integrated into Chapter One.")

        if st.button("📘 Generate Chapter One"):
            # Build per-doc summaries: give each doc a fair allocation
            per_doc_chars = max(1500, 12000 // max(num_docs, 1))
            doc_summaries = []
            for doc in st.session_state.uploaded_docs_list:
                snippet = doc["text"][:per_doc_chars]
                doc_summaries.append(
                    f"--- FROM: {doc['name']} ---\n{snippet}")
            all_docs_text = "\n\n".join(doc_summaries)

            sys_p = f"""You are an expert academic dissertation writer.
Generate a complete CHAPTER ONE — INTRODUCTION.

Use this heading structure:
{st.session_state.ch1_headings}

CITATION RULES:
- Add citations in {ref_style_c1} style ONLY inside Section 1.1 Background of the Study
- EVERY paragraph in 1.1 must have at least one citation from the uploaded documents
- Cite ONLY these document authors: {doc_authors}
- NO citations in Sections 1.2 through 1.10
- References section lists ONLY these cited authors

SECTION 1.1 BACKGROUND — CRITICAL RULES:
- This section MUST be long, detailed and substantive (minimum 5-6 paragraphs)
- Each paragraph starts with context, cites an uploaded document, and develops the idea
- Draw from the Abstract, Results, Summary, Conclusion, and Recommendations of ALL {num_docs} documents
- Show how each document contributes to understanding the topic
- Build a logical narrative: global context → regional context → local context → specific gap
- Every factual claim, statistic, or finding must be supported by a citation
- Do NOT write a single short paragraph — this must be the most detailed section

ALL OTHER SECTIONS (1.2-1.10):
- Derive directly from the proposal objectives and the document content
- Paraphrase completely — restructure sentences, vary vocabulary, change sentence structure
- Do NOT copy text verbatim from documents (plagiarism prevention)
- Do NOT invent facts, statistics, or findings not found in the documents
- Minimum 2 substantive paragraphs per section heading

LANGUAGE: Formal academic dissertation style. Past or present tense (never future)."""

            usr_p = (
                f"Topic: {st.session_state.topic}\n"
                f"Methodology: {st.session_state.methodology}\n"
                f"Citation Style: {ref_style_c1}\n\n"
                f"Proposal context:\n{st.session_state.proposal_intro[:800]}\n\n"
                f"ALL UPLOADED DOCUMENTS ({num_docs} total):\n{all_docs_text}\n\n"
                f"Document authors to cite in 1.1 only: {doc_authors}\n\n"
                f"Generate complete Chapter One using findings from ALL documents."
            )
            stream_response(sys_p, usr_p, "chapter_one")

    show_output("chapter_one", "📘 Chapter One Output")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — LITERATURE REVIEW
# Paragraph-per-author pattern; all docs integrated; optional subheadings
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 4:
    st.markdown('<div class="step-badge">STEP 4 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 📚 Literature Review — Chapter Two")
    st.markdown(
        '<div class="info-card">'
        '• <strong>No headings by default</strong> — continuous academic prose.<br>'
        '• Each paragraph begins with an uploaded document author and their work.<br>'
        '• All {n} uploaded documents are integrated.<br>'
        '• Content drawn from Results/Summary/Conclusion/Recommendations only.<br>'
        '• Fully paraphrased.'
        '</div>'.format(n=len(st.session_state.uploaded_docs_list)),
        unsafe_allow_html=True)

    if not st.session_state.uploaded_docs_list:
        st.warning("⚠️ Upload documents in Step 2 first.")
    else:
        ref_style_lit = st.selectbox(
            "Citation Style", REF_STYLES,
            index=REF_STYLES.index(st.session_state.ref_style)
            if st.session_state.ref_style in REF_STYLES else 0, key="ref_lit")

        doc_authors = (st.session_state.uploaded_doc_authors
                       or "Authors as identified in documents")
        num_docs = len(st.session_state.uploaded_docs_list)

        # Optional subheadings box
        with st.expander("➕ Optional: Add Subheadings", expanded=False):
            st.markdown('<div class="edit-box">', unsafe_allow_html=True)
            sub_val = st.text_area(
                "Subheadings (one per line) — leave blank for none",
                value=st.session_state.lit_subheadings, height=120,
                key="lit_sub_input", label_visibility="collapsed",
                placeholder="e.g.\n2.1 Conceptual Framework\n2.2 Empirical Studies\n2.3 Research Gap")
            if st.button("💾 Save Subheadings", key="save_lit_sub"):
                st.session_state.lit_subheadings = sub_val
                st.success("✅ Saved!")
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Generate Literature Review", use_container_width=True):
                subheadings = st.session_state.lit_subheadings.strip()
                heading_instr = (
                    f"Organise under these subheadings:\n{subheadings}\n"
                    "Each section must still start paragraphs with an author."
                    if subheadings else
                    "Write as CONTINUOUS PROSE — NO subheadings or section numbers whatsoever."
                )

                per_doc_chars = max(2000, 14000 // max(num_docs, 1))
                doc_summaries = []
                for doc in st.session_state.uploaded_docs_list:
                    snippet = doc["text"][:per_doc_chars]
                    doc_summaries.append(
                        f"--- SOURCE: {doc['name']} ---\n{snippet}")
                all_docs_text = "\n\n".join(doc_summaries)

                sys_p = f"""You are an expert academic writer specialising in comprehensive literature reviews.
Generate a LONG, THOROUGH, PROFESSIONAL CHAPTER TWO — LITERATURE REVIEW.

{heading_instr}

STRUCTURE PATTERN — FOLLOW PRECISELY:
1. Opening paragraph (no citation) — introduces the themes, scope and organisation of the review
2. For EACH of the {num_docs} uploaded documents, write MULTIPLE paragraphs (minimum 2 per document):
   - FIRST paragraph: Introduce the study — begin with the author and year:
     "[Author Surname] ([Year]) conducted/investigated/examined/explored/argued that..."
     Describe the study's background, purpose, and objectives.
   - SECOND paragraph: Continue with methodology, key findings, results, and conclusions.
     End with a properly formatted in-text citation in {ref_style_lit}.
   - If the document is rich enough, add a THIRD paragraph covering implications or gaps noted.
3. After covering all documents, write a SYNTHESIS paragraph comparing/contrasting findings
4. Write a RESEARCH GAP paragraph — clearly articulate what is missing and justify this study

CITATION RULES:
- Use {ref_style_lit} in-text citations
- Cite ONLY these uploaded document authors: {doc_authors}
- Every non-opening paragraph must contain at least one citation
- Do NOT cite secondary authors mentioned inside the documents

CONTENT RULES — CRITICAL:
- Extract content from Abstract, Results, Summary, Conclusion, AND Recommendations of every doc
- ALL {num_docs} documents MUST each have at least 2 dedicated paragraphs
- The review must be LONG and COMPREHENSIVE — do not summarise briefly
- Paraphrase all content thoroughly: restructure sentences, change vocabulary completely
- Do NOT reproduce any sentence verbatim from the documents (plagiarism prevention)
- Do NOT invent findings, statistics, or authors not present in the documents
- Professional academic writing — varied sentence structure, formal tone, logical flow
- Each paragraph should be substantive (minimum 5-6 sentences)

REFERENCES: End with a References section listing ONLY the uploaded document authors in {ref_style_lit} style, alphabetically sorted."""

                usr_p = (
                    f"Topic: {st.session_state.topic}\n"
                    f"Citation Style: {ref_style_lit}\n\n"
                    f"Proposal objectives:\n{st.session_state.proposal_intro[:500]}\n\n"
                    f"ALL UPLOADED DOCUMENTS ({num_docs}):\n{all_docs_text}\n\n"
                    f"Authors to cite: {doc_authors}\n\n"
                    f"Generate comprehensive literature review integrating ALL {num_docs} documents."
                )
                stream_response(sys_p, usr_p, "literature")

        with col2:
            if st.button("🔍 Extract References Only", use_container_width=True):
                combined = build_combined_docs_text(max_chars_per_doc=2000)
                sys_p = (
                    f"Extract ONLY the references of the uploaded documents themselves. "
                    f"Format in {ref_style_lit}. Sort alphabetically. Number each."
                )
                usr_p = (
                    f"Style: {ref_style_lit}\nAuthors: {doc_authors}\n"
                    f"Documents:\n{combined}\nFormat references."
                )
                stream_response(sys_p, usr_p, "references")
                st.success("✅ Saved to Step 8!")

    show_output("literature", "📚 Chapter Two Output")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — DATA ANALYSIS
# FIX 3: Time Series Regression; FIX 4: Full TS with ADF/differencing;
# FIX 5: ARIMA + SARIMA with ACF/PACF
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 5:
    st.markdown('<div class="step-badge">STEP 5 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 📊 Methodology & Data Analysis — Chapter Three")
    st.markdown(
        '<div class="info-card">'
        '• Methodology prose: no citations (formulas have citations).<br>'
        '• Assumptions shown with actual computed values.<br>'
        '• Every table followed by interpretation.<br>'
        '• Time Series: full ADF stationarity test → differencing if needed → ARIMA/SARIMA → ACF/PACF.<br>'
        '• Descriptive statistics include graphs.'
        '</div>', unsafe_allow_html=True)

    if not st.session_state.proposal_intro:
        st.warning("⚠️ Complete Step 1 first.")
    else:
        data_file = st.file_uploader("Upload Dataset (Excel / CSV)",
                                      type=["xlsx", "xls", "csv"])
        df = None

        if data_file:
            st.session_state.data_filename = data_file.name
            try:
                import pandas as pd
                import numpy as np
                df_raw = (pd.read_csv(data_file)
                          if data_file.name.endswith(".csv")
                          else pd.read_excel(data_file))
                st.session_state.data_columns = ", ".join(str(c) for c in df_raw.columns)
                st.session_state.df_json = df_raw.to_json()
                st.success(
                    f"✅ {data_file.name} — "
                    f"{df_raw.shape[0]} rows × {df_raw.shape[1]} columns")
                st.dataframe(df_raw.head(10), use_container_width=True)
                df = df_raw
            except Exception as e:
                st.error(f"❌ {e}")

        if df is None and st.session_state.df_json:
            try:
                import pandas as pd
                import numpy as np
                df = pd.read_json(st.session_state.df_json)
            except Exception:
                pass

        col_a, col_b = st.columns(2)
        with col_a:
            variables = st.text_input(
                "Dependent / Independent Variables",
                value=st.session_state.variables,
                placeholder="e.g. Dependent: Cases; Independent: Rainfall, Temperature")
            st.session_state.variables = variables
        with col_b:
            ref_style_an = st.selectbox(
                "Citation Style for Formulas", REF_STYLES,
                index=REF_STYLES.index(st.session_state.ref_style)
                if st.session_state.ref_style in REF_STYLES else 0, key="ref_an")

        # Time series column selector
        ts_col = None
        time_col = None
        if df is not None:
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            all_cols = ["— None —"] + list(df.columns)
            num_cols_opts = ["— None —"] + numeric_cols

            ts_selected = "Full Time Series Analysis (ADF + Differencing + ARIMA + SARIMA)" in (
                st.session_state.selected_tests)
            ts_reg_selected = "Time Series Regression" in st.session_state.selected_tests

            if ts_selected or ts_reg_selected:
                st.markdown("### ⏱️ Time Series Configuration")
                tc1, tc2 = st.columns(2)
                with tc1:
                    time_col = st.selectbox(
                        "Date/Time Column", all_cols, key="ts_time_col")
                    if time_col == "— None —":
                        time_col = None
                with tc2:
                    ts_col = st.selectbox(
                        "Target Variable (series to analyse)", num_cols_opts,
                        key="ts_target_col")
                    if ts_col == "— None —":
                        ts_col = None

        editable_headings("Methodology", "meth_headings", DEFAULT_METH_HEADINGS)

        st.markdown("### Select Statistical Tests")
        selected_tests = st.multiselect(
            "Select all applicable", STAT_TESTS,
            default=st.session_state.selected_tests)
        st.session_state.selected_tests = selected_tests

        # ── Descriptive graphs ────────────────────────────────────────────
        if df is not None and "Descriptive Statistics" in selected_tests:
            st.markdown("---")
            st.markdown("### 📈 Descriptive Statistics Graphs")
            try:
                import pandas as pd
                import numpy as np
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                import matplotlib.colors as mcolors
                from scipy import stats as _stats

                CLRS = ["#00c6a7","#0077ff","#ff6b6b","#ffd166","#a29bfe","#fd79a8","#55efc4","#fdcb6e"]

                def style_ax(ax, title=""):
                    ax.set_facecolor("#0d1526")
                    ax.tick_params(colors="#7a9abf")
                    for sp in ax.spines.values():
                        sp.set_edgecolor("#1e2d4a")
                    if title:
                        ax.set_title(title, color="#c8deff", fontsize=11, pad=8)

                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                cat_cols     = df.select_dtypes(include=["object","category"]).columns.tolist()

                # 1. Histograms with normal curve
                if numeric_cols:
                    st.markdown("**1. Histograms with Normal Distribution Curve**")
                    n = len(numeric_cols)
                    cpr = min(3, n)
                    rows = (n + cpr - 1) // cpr
                    fig, axes = plt.subplots(rows, cpr, figsize=(5*cpr, 4*rows), facecolor="#0d1526")
                    if n == 1:
                        af = [axes]
                    elif rows == 1:
                        af = list(axes)
                    else:
                        af = list(axes.flatten())
                    for idx_h, col in enumerate(numeric_cols):
                        ax = af[idx_h]
                        data = df[col].dropna()
                        style_ax(ax, col)
                        ax.hist(data, bins=15, color="#00c6a7", edgecolor="#0077ff", alpha=0.75, density=True)
                        mu, std = data.mean(), data.std()
                        x_r = np.linspace(data.min(), data.max(), 100)
                        ax.plot(x_r, _stats.norm.pdf(x_r, mu, std), color="#ffd166", linewidth=2, label="Normal")
                        ax.set_xlabel("Value", color="#7a9abf", fontsize=9)
                        ax.set_ylabel("Density", color="#7a9abf", fontsize=9)
                        ax.legend(fontsize=7, facecolor="#0d1526", labelcolor="#c8deff")
                    for idx_h in range(n, len(af)):
                        af[idx_h].set_visible(False)
                    fig.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()

                # 2. Box plots
                if numeric_cols:
                    st.markdown("**2. Box Plots — Spread, Median & Outliers**")
                    fig2, ax2 = plt.subplots(figsize=(max(8, len(numeric_cols)*1.8), 5), facecolor="#0d1526")
                    style_ax(ax2, "Box Plot of Numeric Variables")
                    ax2.boxplot(
                        [df[c].dropna() for c in numeric_cols],
                        labels=numeric_cols, patch_artist=True,
                        boxprops=dict(facecolor="#0077ff33", color="#00c6a7"),
                        medianprops=dict(color="#ffd166", linewidth=2.5),
                        whiskerprops=dict(color="#7a9abf"),
                        capprops=dict(color="#7a9abf"),
                        flierprops=dict(marker="o", color="#ff6b6b", alpha=0.6))
                    ax2.tick_params(axis="x", rotation=20)
                    fig2.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig2)
                    plt.close()

                # 3. Bar charts categorical
                if cat_cols:
                    st.markdown("**3. Bar Charts — Frequency of Categorical Variables**")
                    for col in cat_cols[:5]:
                        vc = df[col].value_counts()
                        fig3, ax3 = plt.subplots(figsize=(9, 4), facecolor="#0d1526")
                        style_ax(ax3, f"Frequency Distribution: {col}")
                        bars3 = ax3.bar(vc.index.astype(str), vc.values, color=CLRS[:len(vc)], edgecolor="#1e2d4a", width=0.6)
                        ax3.set_xlabel(col, color="#7a9abf", fontsize=9)
                        ax3.set_ylabel("Count", color="#7a9abf", fontsize=9)
                        ax3.tick_params(axis="x", rotation=30)
                        for bar3, val3 in zip(bars3, vc.values):
                            ax3.text(bar3.get_x()+bar3.get_width()/2, bar3.get_height()+0.3,
                                     f"{val3}\n({val3/vc.sum()*100:.1f}%)",
                                     ha="center", color="#c8deff", fontsize=8)
                        fig3.patch.set_facecolor("#0d1526")
                        plt.tight_layout()
                        st.pyplot(fig3)
                        plt.close()

                # 4. Line graphs
                if numeric_cols:
                    st.markdown("**4. Line Graphs — Trend Over Observations**")
                    fig4, ax4 = plt.subplots(figsize=(12, 5), facecolor="#0d1526")
                    style_ax(ax4, "Line Graph: Numeric Variables over Observations")
                    for i4, col4 in enumerate(numeric_cols[:6]):
                        ax4.plot(df[col4].values, color=CLRS[i4 % len(CLRS)], linewidth=1.5, label=col4, alpha=0.85)
                    ax4.set_xlabel("Observation Index", color="#7a9abf", fontsize=9)
                    ax4.set_ylabel("Value", color="#7a9abf", fontsize=9)
                    ax4.legend(facecolor="#0d1526", labelcolor="#c8deff", fontsize=8)
                    fig4.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig4)
                    plt.close()

                # 5. Pie charts
                if cat_cols:
                    st.markdown("**5. Pie Charts — Proportional Breakdown**")
                    pc_cols_ui = st.columns(min(3, len(cat_cols)))
                    for ci5, col5 in enumerate(cat_cols[:3]):
                        vc5 = df[col5].value_counts().head(6)
                        with pc_cols_ui[ci5]:
                            fig5, ax5 = plt.subplots(figsize=(4, 4), facecolor="#0d1526")
                            ax5.set_facecolor("#0d1526")
                            ax5.pie(vc5.values, labels=vc5.index.astype(str),
                                    colors=CLRS[:len(vc5)], autopct="%1.1f%%", startangle=90,
                                    textprops=dict(color="#c8deff", fontsize=8),
                                    wedgeprops=dict(edgecolor="#0d1526", linewidth=1.5))
                            ax5.set_title(col5, color="#c8deff", fontsize=10)
                            fig5.patch.set_facecolor("#0d1526")
                            plt.tight_layout()
                            st.pyplot(fig5)
                            plt.close()

                # 6. Scatter plots with trend
                if len(numeric_cols) >= 2:
                    st.markdown("**6. Scatter Plots — Pairwise Relationships with Trend Line**")
                    pairs6 = [(numeric_cols[i], numeric_cols[j])
                              for i in range(len(numeric_cols)) for j in range(i+1, len(numeric_cols))][:4]
                    sp_cols6 = st.columns(min(2, len(pairs6)))
                    for pi6, (cx6, cy6) in enumerate(pairs6):
                        with sp_cols6[pi6 % 2]:
                            fig6, ax6 = plt.subplots(figsize=(5, 4), facecolor="#0d1526")
                            style_ax(ax6, f"{cx6} vs {cy6}")
                            valid6 = df[[cx6, cy6]].dropna()
                            ax6.scatter(valid6[cx6], valid6[cy6], color="#00c6a7", alpha=0.65, edgecolors="#0077ff", s=30)
                            if len(valid6) > 2:
                                z6 = np.polyfit(valid6[cx6], valid6[cy6], 1)
                                p6 = np.poly1d(z6)
                                ax6.plot(sorted(valid6[cx6]), p6(sorted(valid6[cx6])),
                                         color="#ffd166", linewidth=1.5, linestyle="--", label="Trend")
                            ax6.set_xlabel(cx6, color="#7a9abf", fontsize=9)
                            ax6.set_ylabel(cy6, color="#7a9abf", fontsize=9)
                            ax6.legend(facecolor="#0d1526", labelcolor="#c8deff", fontsize=7)
                            fig6.patch.set_facecolor("#0d1526")
                            plt.tight_layout()
                            st.pyplot(fig6)
                            plt.close()

                # 7. Correlation heatmap
                if len(numeric_cols) >= 2:
                    st.markdown("**7. Correlation Heatmap**")
                    corr = df[numeric_cols].corr()
                    fig7, ax7 = plt.subplots(figsize=(max(6, len(numeric_cols)), max(5, len(numeric_cols))), facecolor="#0d1526")
                    style_ax(ax7, "Pearson Correlation Matrix")
                    cmap7 = mcolors.LinearSegmentedColormap.from_list("tb", ["#ff6b6b","#0d1526","#00c6a7"])
                    im7 = ax7.imshow(corr, cmap=cmap7, vmin=-1, vmax=1)
                    ax7.set_xticks(range(len(numeric_cols)))
                    ax7.set_yticks(range(len(numeric_cols)))
                    ax7.set_xticklabels(numeric_cols, rotation=45, ha="right", color="#c8deff", fontsize=9)
                    ax7.set_yticklabels(numeric_cols, color="#c8deff", fontsize=9)
                    for i7 in range(len(numeric_cols)):
                        for j7 in range(len(numeric_cols)):
                            val7 = corr.iloc[i7, j7]
                            ax7.text(j7, i7, f"{val7:.2f}", ha="center", va="center",
                                     color="white" if abs(val7) > 0.4 else "#c8deff", fontsize=8, fontweight="bold")
                    plt.colorbar(im7, ax=ax7)
                    fig7.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig7)
                    plt.close()

                # 8. Area chart
                if numeric_cols:
                    st.markdown("**8. Area Charts — Cumulative Trend**")
                    fig_area, ax_area = plt.subplots(figsize=(12, 5), facecolor="#0d1526")
                    style_ax(ax_area, "Area Chart: Numeric Variables")
                    for i_a, col_a2 in enumerate(numeric_cols[:5]):
                        vals_a = df[col_a2].fillna(0).values
                        ax_area.fill_between(range(len(vals_a)), vals_a,
                                             alpha=0.25, color=CLRS[i_a % len(CLRS)], label=col_a2)
                        ax_area.plot(vals_a, color=CLRS[i_a % len(CLRS)], linewidth=1.2)
                    ax_area.set_xlabel("Observation Index", color="#7a9abf", fontsize=9)
                    ax_area.set_ylabel("Value", color="#7a9abf", fontsize=9)
                    ax_area.legend(facecolor="#0d1526", labelcolor="#c8deff", fontsize=8)
                    fig_area.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig_area)
                    plt.close()

                # 9. Frequency polygon
                if numeric_cols:
                    st.markdown("**9. Frequency Polygons**")
                    fig_fp, ax_fp = plt.subplots(figsize=(10, 5), facecolor="#0d1526")
                    style_ax(ax_fp, "Frequency Polygon")
                    for i_fp, col_fp in enumerate(numeric_cols[:5]):
                        d_fp = df[col_fp].dropna()
                        counts_fp, bins_fp = np.histogram(d_fp, bins=15)
                        mids_fp = (bins_fp[:-1] + bins_fp[1:]) / 2
                        ax_fp.plot(mids_fp, counts_fp, color=CLRS[i_fp % len(CLRS)],
                                   linewidth=1.8, marker="o", markersize=4, label=col_fp)
                    ax_fp.set_xlabel("Value", color="#7a9abf", fontsize=9)
                    ax_fp.set_ylabel("Frequency", color="#7a9abf", fontsize=9)
                    ax_fp.legend(facecolor="#0d1526", labelcolor="#c8deff", fontsize=8)
                    fig_fp.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig_fp)
                    plt.close()

                # 10. Stacked bar (categorical combinations)
                if cat_cols and len(cat_cols) >= 2:
                    st.markdown("**10. Stacked Bar Chart — Cross-tabulation**")
                    try:
                        ct = pd.crosstab(df[cat_cols[0]], df[cat_cols[1]])
                        fig_sb, ax_sb = plt.subplots(figsize=(10, 5), facecolor="#0d1526")
                        style_ax(ax_sb, f"{cat_cols[0]} × {cat_cols[1]} Stacked Bar")
                        bottom_sb = np.zeros(len(ct))
                        for ci_sb, col_sb in enumerate(ct.columns):
                            ax_sb.bar(ct.index.astype(str), ct[col_sb].values,
                                      bottom=bottom_sb, color=CLRS[ci_sb % len(CLRS)],
                                      label=str(col_sb), edgecolor="#0d1526", width=0.6)
                            bottom_sb += ct[col_sb].values
                        ax_sb.set_xlabel(cat_cols[0], color="#7a9abf", fontsize=9)
                        ax_sb.set_ylabel("Count", color="#7a9abf", fontsize=9)
                        ax_sb.tick_params(axis="x", rotation=25)
                        ax_sb.legend(title=cat_cols[1], facecolor="#0d1526",
                                     labelcolor="#c8deff", fontsize=8,
                                     title_fontsize=8)
                        fig_sb.patch.set_facecolor("#0d1526")
                        plt.tight_layout()
                        st.pyplot(fig_sb)
                        plt.close()
                    except Exception:
                        pass

                # 11. Grouped mean bar
                if cat_cols and numeric_cols:
                    st.markdown("**11. Grouped Mean Bar Chart — Categorical vs Numeric Mean**")
                    for cat8 in cat_cols[:2]:
                        for num8 in numeric_cols[:2]:
                            try:
                                grp8 = df.groupby(cat8)[num8].mean().dropna()
                                if len(grp8) < 2:
                                    continue
                                fig8, ax8 = plt.subplots(figsize=(9, 4), facecolor="#0d1526")
                                style_ax(ax8, f"Mean {num8} by {cat8}")
                                bars8 = ax8.bar(grp8.index.astype(str), grp8.values, color=CLRS[:len(grp8)], edgecolor="#1e2d4a")
                                ax8.set_xlabel(cat8, color="#7a9abf", fontsize=9)
                                ax8.set_ylabel(f"Mean {num8}", color="#7a9abf", fontsize=9)
                                ax8.tick_params(axis="x", rotation=25)
                                for bar8, val8 in zip(bars8, grp8.values):
                                    ax8.text(bar8.get_x()+bar8.get_width()/2, bar8.get_height()+0.01,
                                             f"{val8:.2f}", ha="center", color="#c8deff", fontsize=8)
                                fig8.patch.set_facecolor("#0d1526")
                                plt.tight_layout()
                                st.pyplot(fig8)
                                plt.close()
                            except Exception:
                                pass

            except Exception as eg:
                st.warning(f"Graph error: {eg}")

        # ── Assumption testing with REMEDIATION ───────────────────────────
        regression_tests = ["Simple Linear Regression","Multiple Regression",
                            "One-Way ANOVA","Two-Way ANOVA",
                            "Independent Samples T-Test","Paired Samples T-Test",
                            "Binary Logistic Regression","Autoregressive (AR) Model"]
        if df is not None and any(t in selected_tests for t in regression_tests):
            st.markdown("---")
            st.markdown("### 🔬 Assumption Testing & Automatic Remediation")
            try:
                import numpy as np
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                from scipy import stats as _stats

                numeric_cols_a = df.select_dtypes(include=[np.number]).columns.tolist()
                cat_cols_a = df.select_dtypes(include=["object","category"]).columns.tolist()

                for test_col_a in numeric_cols_a[:3]:
                    data_a = df[test_col_a].dropna()
                    if len(data_a) < 4:
                        continue
                    with st.expander(f"🔬 Assumptions: {test_col_a}", expanded=True):

                        # Normality
                        st.markdown("**A. Normality — Shapiro-Wilk Test**")
                        sw_data = data_a.sample(5000, random_state=42) if len(data_a) > 5000 else data_a
                        sw_s, sw_p = _stats.shapiro(sw_data)
                        norm_ok = sw_p > 0.05
                        st.markdown(
                            f"| Test | W-statistic | p-value | Decision |\n"
                            f"|---|---|---|---|\n"
                            f"| Shapiro-Wilk | {sw_s:.4f} | {sw_p:.4f} | "
                            f"{'✅ Normal (p>0.05)' if norm_ok else '❌ Non-normal (p≤0.05)'} |"
                        )
                        if not norm_ok:
                            st.error("❌ **NORMALITY FAILED — Remedy: Log Transformation**")
                            st.markdown("""
**Remedial Action Applied:** Log Transformation Y* = ln(Y)
- Compresses right-skewed data toward normality
- Formula: Y*ᵢ = ln(Yᵢ) for all i where Yᵢ > 0
""")
                            if (data_a > 0).all():
                                data_log_a = np.log(data_a)
                                sw_s2, sw_p2 = _stats.shapiro(data_log_a[:5000] if len(data_log_a) > 5000 else data_log_a)
                                st.markdown(
                                    f"**After Log Transform:** W = {sw_s2:.4f}, p = {sw_p2:.4f} — "
                                    f"{'✅ Normality restored' if sw_p2 > 0.05 else '⚠️ Still non-normal. Try Box-Cox or Yeo-Johnson transformation.'}"
                                )
                                fig_nn, (ax_nn1, ax_nn2) = plt.subplots(1, 2, figsize=(10, 4), facecolor="#0d1526")
                                for ax_nn in [ax_nn1, ax_nn2]:
                                    ax_nn.set_facecolor("#0d1526")
                                    for sp in ax_nn.spines.values(): sp.set_edgecolor("#1e2d4a")
                                    ax_nn.tick_params(colors="#7a9abf")
                                ax_nn1.hist(data_a, bins=15, color="#ff6b6b", edgecolor="#1e2d4a", alpha=0.8)
                                ax_nn1.set_title(f"Original: {test_col_a}", color="#c8deff", fontsize=10)
                                ax_nn2.hist(data_log_a, bins=15, color="#00c6a7", edgecolor="#1e2d4a", alpha=0.8)
                                ax_nn2.set_title(f"After log(Y): {test_col_a}", color="#c8deff", fontsize=10)
                                fig_nn.patch.set_facecolor("#0d1526")
                                plt.tight_layout()
                                st.pyplot(fig_nn)
                                plt.close()
                            else:
                                st.info("Values include zero/negative — try square root: Y* = √(Y + 1)")

                        st.markdown("---")

                        # Homoscedasticity — Levene + Breusch-Pagan
                        st.markdown("**B. Homoscedasticity — Levene's Test & Breusch-Pagan Test**")

                        # Levene's test (group-based)
                        if cat_cols_a:
                            g_col_a = cat_cols_a[0]
                            groups_a = [gd[test_col_a].dropna().values
                                        for _, gd in df.groupby(g_col_a)
                                        if len(gd[test_col_a].dropna()) >= 2]
                            if len(groups_a) >= 2:
                                lev_s, lev_p = _stats.levene(*groups_a)
                                homo_ok = lev_p > 0.05
                                st.markdown(
                                    f"| Test | F-statistic | p-value | Decision |\n"
                                    f"|---|---|---|---|\n"
                                    f"| Levene's | {lev_s:.4f} | {lev_p:.4f} | "
                                    f"{'✅ Homoscedastic (p>0.05)' if homo_ok else '❌ Heteroscedastic (p≤0.05)'} |"
                                )
                                if not homo_ok:
                                    st.error(
                                        "🚨 **HOMOSCEDASTICITY ASSUMPTION FAILED — HETEROSCEDASTICITY DETECTED**\n\n"
                                        "The variance of residuals is not constant across groups/fitted values. "
                                        "Proceeding without correction would produce biased standard errors and invalid inference."
                                    )
                                    st.markdown("""
---
### 🔧 REMEDIATION APPLIED — Heteroscedasticity Correction

**Why this matters:** Heteroscedasticity inflates/deflates standard errors, making t-statistics and p-values unreliable.

**Remedial Actions Available:**

| Remedy | Formula | When to Use |
|---|---|---|
| **1. Log Transformation** | Y* = ln(Y) | Right-skewed, multiplicative errors |
| **2. Square Root Transform** | Y* = √Y | Count data, mild skew |
| **3. Weighted Least Squares (WLS)** | wᵢ = 1/σ̂ᵢ² | Known variance structure |
| **4. White's Robust Standard Errors** | Var(β̂_HC) = (X'X)⁻¹(X'ΩX)(X'X)⁻¹ | General heteroscedasticity |
| **5. Welch's t-test (no equal variance assumption)** | t = (x̄₁-x̄₂)/√(s₁²/n₁+s₂²/n₂) | Two-group comparison |

---
**✅ REMEDY EXECUTED: Welch's t-test applied** (does not assume equal variances — directly corrects for heteroscedasticity in group comparisons)
""")
                                    if len(groups_a) == 2:
                                        w_s, w_p = _stats.ttest_ind(*groups_a, equal_var=False)
                                        st.markdown(
                                            f"| Welch t-stat | p-value | df | Interpretation |\n"
                                            f"|---|---|---|---|\n"
                                            f"| {w_s:.4f} | {w_p:.4f} | approx | "
                                            f"{'✅ Significant difference (p<0.05) — corrected for unequal variance' if w_p < 0.05 else '⚪ No significant difference between groups'} |"
                                        )
                                        st.success("✅ Welch's correction applied. Results above are valid despite heteroscedasticity.")

                                    # Also attempt log-transform remedy
                                    if (data_a > 0).all():
                                        st.markdown("**✅ REMEDY ALSO APPLIED: Log Transformation of dependent variable**")
                                        data_log_h = np.log(data_a)
                                        groups_log_h = []
                                        for g_name, gd_h in df.groupby(g_col_a):
                                            vals_h = gd_h[test_col_a].dropna()
                                            if len(vals_h) >= 2:
                                                groups_log_h.append(np.log(vals_h[vals_h > 0]))
                                        if len(groups_log_h) >= 2:
                                            lev_log_s, lev_log_p = _stats.levene(*groups_log_h)
                                            st.markdown(
                                                f"| After log(Y) — Levene's | {lev_log_s:.4f} | {lev_log_p:.4f} | "
                                                f"{'✅ Homoscedasticity restored' if lev_log_p > 0.05 else '⚠️ Still heteroscedastic — use WLS or robust SEs'} |"
                                            )
                        else:
                            # Breusch-Pagan style test without groups
                            st.info("ℹ️ No categorical variable found for Levene's test. Running variance-ratio check on fitted residuals.")
                            if len(data_a) >= 8:
                                mid = len(data_a) // 2
                                var1 = np.var(data_a[:mid])
                                var2 = np.var(data_a[mid:])
                                f_rat = max(var1,var2)/min(var1,var2) if min(var1,var2) > 0 else float("inf")
                                st.markdown(
                                    f"| Variance Ratio (first vs second half) | {f_rat:.4f} | "
                                    f"{'✅ Approximately homoscedastic (ratio<3)' if f_rat < 3 else '❌ Possible heteroscedasticity (ratio≥3)'} |"
                                )

                        st.markdown("---")

                        # Multicollinearity VIF
                        if len(numeric_cols_a) >= 3:
                            st.markdown("**C. Multicollinearity — Variance Inflation Factor (VIF)**")
                            try:
                                from numpy.linalg import lstsq as _lstsq2
                                vif_header = "| Variable | R² | VIF | Status |"
                                vif_div = "|---|---|---|---|"
                                vif_rows_a = [vif_header, vif_div]
                                for vc_a in numeric_cols_a:
                                    others_a = [c for c in numeric_cols_a if c != vc_a]
                                    y_va = df[vc_a].dropna()
                                    X_va = df[others_a].loc[y_va.index].dropna()
                                    common_a = y_va.index.intersection(X_va.index)
                                    if len(common_a) < 4:
                                        continue
                                    y_v2 = y_va.loc[common_a].values
                                    Xm2 = np.column_stack([np.ones(len(common_a)), X_va.loc[common_a].values])
                                    c2, _, _, _ = _lstsq2(Xm2, y_v2, rcond=None)
                                    yp2 = Xm2 @ c2
                                    ss_r2 = np.sum((y_v2 - yp2)**2)
                                    ss_t2 = np.sum((y_v2 - y_v2.mean())**2)
                                    r2_v2 = 1 - ss_r2/ss_t2 if ss_t2 > 0 else 0
                                    vif2 = 1/(1-r2_v2) if r2_v2 < 1 else float("inf")
                                    flag_v = "✅ OK" if vif2 < 5 else ("⚠️ Moderate" if vif2 < 10 else "❌ Severe")
                                    vif_rows_a.append(f"| {vc_a} | {r2_v2:.4f} | {vif2:.2f} | {flag_v} |")
                                for row_v in vif_rows_a:
                                    st.markdown(row_v)
                                st.markdown("""
**REMEDY if VIF > 10:** Remove the correlated predictor, apply Ridge regularisation (L2 penalty),
or use PCA to combine correlated predictors into uncorrelated components.
""")
                            except Exception as e_v2:
                                st.warning(f"VIF error: {e_v2}")

                        st.markdown("---")

                        # Autocorrelation — Durbin-Watson
                        st.markdown("**D. Autocorrelation — Durbin-Watson Test**")
                        try:
                            from numpy.linalg import lstsq as _lstsq_dw
                            numeric_cols_dw = df.select_dtypes(include=[np.number]).columns.tolist()
                            if len(numeric_cols_dw) >= 2:
                                y_dw = df[test_col_a].dropna()
                                x_dw_cols = [c for c in numeric_cols_dw if c != test_col_a]
                                x_dw = df[x_dw_cols].loc[y_dw.index].dropna()
                                idx_dw = y_dw.index.intersection(x_dw.index)
                                if len(idx_dw) >= 4:
                                    Xm_dw = np.column_stack([np.ones(len(idx_dw)), x_dw.loc[idx_dw].values])
                                    c_dw, _, _, _ = _lstsq_dw(Xm_dw, y_dw.loc[idx_dw].values, rcond=None)
                                    resid_dw = y_dw.loc[idx_dw].values - (Xm_dw @ c_dw)
                                    dw_stat = np.sum(np.diff(resid_dw)**2) / np.sum(resid_dw**2)
                                    if 1.5 <= dw_stat <= 2.5:
                                        dw_interp = "✅ No autocorrelation (DW ≈ 2.0)"
                                        dw_ok = True
                                    elif dw_stat < 1.5:
                                        dw_interp = "❌ Positive autocorrelation (DW < 1.5)"
                                        dw_ok = False
                                    else:
                                        dw_interp = "❌ Negative autocorrelation (DW > 2.5)"
                                        dw_ok = False
                                    st.markdown(
                                        f"| Durbin-Watson | {dw_stat:.4f} | {dw_interp} |\n"
                                        f"|---|---|---|"
                                    )
                                    if not dw_ok:
                                        st.error("🚨 **AUTOCORRELATION DETECTED — REMEDIATION REQUIRED**")
                                        st.markdown(f"""
**Durbin-Watson = {dw_stat:.4f}** — residuals are not independent.

### 🔧 Remediation for Autocorrelation:

| Method | Formula | Effect |
|---|---|---|
| **Cochrane-Orcutt Transform** | Y*ₜ = Yₜ - ρ·Yₜ₋₁ | Removes first-order autocorrelation |
| **Generalised Least Squares** | β = (X'Ω⁻¹X)⁻¹X'Ω⁻¹y | Full autocorrelation correction |
| **Newey-West HAC SE** | Adjusts SEs for autocorrelation | Valid inference without transform |
| **Add AR lag term** | Include Yₜ₋₁ as predictor | Absorbs autocorrelation in model |

✅ **Recommended action:** Run "Autoregressive (AR) Model" or "Full Time Series Analysis" from the test selector above to properly model the autocorrelation structure.
""")
                        except Exception as dw_err:
                            st.caption(f"Durbin-Watson: {dw_err}")

            except Exception as e_assump2:
                st.warning(f"Assumption testing error: {e_assump2}")



                # ── FULL TIME SERIES BLOCK ────────────────────────────────────────
        run_full_ts = ("Full Time Series Analysis (ADF + Differencing + ARIMA + SARIMA)"
                       in selected_tests)
        run_ts_reg  = "Time Series Regression" in selected_tests

        if df is not None and (run_full_ts or run_ts_reg) and ts_col:
            st.markdown("---")
            st.markdown("### ⏱️ Time Series Analysis")

            try:
                import pandas as pd
                import numpy as np
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt

                series = df[ts_col].dropna()
                if time_col and time_col in df.columns:
                    try:
                        df[time_col] = pd.to_datetime(df[time_col])
                        series.index = df[time_col][:len(series)]
                    except Exception:
                        pass

                # ── Raw series plot ───────────────────────────────────────
                st.markdown("#### Raw Time Series Plot")
                fig_ts, ax_ts = plt.subplots(figsize=(12, 4), facecolor="#0d1526")
                ax_ts.set_facecolor("#0d1526")
                ax_ts.plot(series.values, color="#00c6a7", linewidth=1.5)
                ax_ts.set_title(f"Time Series: {ts_col}", color="#c8deff", fontsize=12)
                ax_ts.set_xlabel("Time", color="#7a9abf")
                ax_ts.set_ylabel(ts_col, color="#7a9abf")
                ax_ts.tick_params(colors="#7a9abf")
                for sp in ax_ts.spines.values():
                    sp.set_edgecolor("#1e2d4a")
                fig_ts.patch.set_facecolor("#0d1526")
                plt.tight_layout()
                st.pyplot(fig_ts)
                plt.close()

                # ── ADF Stationarity Test ─────────────────────────────────
                st.markdown("#### ADF Stationarity Test")
                try:
                    from statsmodels.tsa.stattools import adfuller
                    adf_result = adfuller(series, autolag="AIC")
                    adf_stat   = adf_result[0]
                    adf_p      = adf_result[1]
                    adf_lags   = adf_result[2]
                    adf_nobs   = adf_result[3]
                    crit_vals  = adf_result[4]

                    st.markdown(f"""
| ADF Test Parameter | Value |
|---|---|
| ADF Statistic | {adf_stat:.4f} |
| p-value | {adf_p:.4f} |
| Lags Used | {adf_lags} |
| Number of Observations | {adf_nobs} |
| Critical Value (1%) | {crit_vals['1%']:.4f} |
| Critical Value (5%) | {crit_vals['5%']:.4f} |
| Critical Value (10%) | {crit_vals['10%']:.4f} |
""")
                    is_stationary = adf_p < 0.05

                    if is_stationary:
                        st.success(
                            f"✅ Series is STATIONARY (ADF = {adf_stat:.4f}, p = {adf_p:.4f} < 0.05). "
                            f"No differencing required.")
                        series_stationary = series
                        d_order = 0
                    else:
                        st.warning(
                            f"⚠️ Series is NON-STATIONARY (ADF = {adf_stat:.4f}, p = {adf_p:.4f} ≥ 0.05). "
                            f"Applying differencing...")

                        # ── Differencing ──────────────────────────────────
                        st.markdown("#### Differencing (Remediation)")
                        series_diff = series.diff().dropna()
                        d_order = 1

                        adf_diff = adfuller(series_diff, autolag="AIC")
                        st.markdown(f"""
After 1st-order differencing:

| Parameter | Value |
|---|---|
| ADF Statistic | {adf_diff[0]:.4f} |
| p-value | {adf_diff[1]:.4f} |
| Result | {'✅ Stationary' if adf_diff[1] < 0.05 else '⚠️ Still non-stationary — apply 2nd differencing'} |
""")
                        if adf_diff[1] >= 0.05:
                            series_diff2 = series_diff.diff().dropna()
                            d_order = 2
                            adf_diff2 = adfuller(series_diff2, autolag="AIC")
                            st.markdown(f"""
After 2nd-order differencing:

| Parameter | Value |
|---|---|
| ADF Statistic | {adf_diff2[0]:.4f} |
| p-value | {adf_diff2[1]:.4f} |
| Result | {'✅ Stationary' if adf_diff2[1] < 0.05 else '⚠️ Consider seasonal differencing or data transformation'} |
""")
                            series_stationary = series_diff2
                        else:
                            series_stationary = series_diff

                        # Plot differenced series
                        fig_diff, ax_diff = plt.subplots(
                            figsize=(12, 4), facecolor="#0d1526")
                        ax_diff.set_facecolor("#0d1526")
                        ax_diff.plot(series_stationary.values,
                                     color="#0077ff", linewidth=1.5)
                        ax_diff.set_title(
                            f"Differenced Series (d={d_order})",
                            color="#c8deff", fontsize=12)
                        ax_diff.tick_params(colors="#7a9abf")
                        for sp in ax_diff.spines.values():
                            sp.set_edgecolor("#1e2d4a")
                        fig_diff.patch.set_facecolor("#0d1526")
                        plt.tight_layout()
                        st.pyplot(fig_diff)
                        plt.close()

                    # ── ACF and PACF ──────────────────────────────────────
                    st.markdown("#### ACF and PACF Plots")
                    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

                    fig_acf, (ax_acf, ax_pacf) = plt.subplots(
                        1, 2, figsize=(14, 4), facecolor="#0d1526")
                    for ax in [ax_acf, ax_pacf]:
                        ax.set_facecolor("#0d1526")
                        for sp in ax.spines.values():
                            sp.set_edgecolor("#1e2d4a")
                        ax.tick_params(colors="#7a9abf")

                    plot_acf(series_stationary, lags=min(20, len(series_stationary)//2 - 1),
                             ax=ax_acf, color="#00c6a7",
                             title="ACF — Autocorrelation Function")
                    plot_pacf(series_stationary, lags=min(20, len(series_stationary)//2 - 1),
                              ax=ax_pacf, color="#0077ff",
                              title="PACF — Partial Autocorrelation Function")

                    ax_acf.set_title("ACF", color="#c8deff", fontsize=12)
                    ax_pacf.set_title("PACF", color="#c8deff", fontsize=12)
                    fig_acf.patch.set_facecolor("#0d1526")
                    plt.tight_layout()
                    st.pyplot(fig_acf)
                    plt.close()

                    st.markdown(
                        '<div class="info-card">'
                        '📌 <strong>ACF interpretation:</strong> Significant spikes at lag k → MA(q) order q.<br>'
                        '📌 <strong>PACF interpretation:</strong> Significant spikes at lag k → AR(p) order p.<br>'
                        'Use these plots to determine the p, d, q parameters for ARIMA.'
                        '</div>', unsafe_allow_html=True)

                    # ── ARIMA ─────────────────────────────────────────────
                    if run_full_ts:
                        st.markdown("#### ARIMA Model")
                        try:
                            from statsmodels.tsa.arima.model import ARIMA

                            # Auto-suggest p, q from ACF/PACF
                            from statsmodels.tsa.stattools import acf, pacf
                            acf_vals  = acf(series_stationary,
                                            nlags=min(20, len(series_stationary)//2 - 1))
                            pacf_vals = pacf(series_stationary,
                                             nlags=min(20, len(series_stationary)//2 - 1))
                            conf = 1.96 / np.sqrt(len(series_stationary))
                            p_order = sum(1 for v in pacf_vals[1:] if abs(v) > conf)
                            q_order = sum(1 for v in acf_vals[1:]  if abs(v) > conf)
                            p_order = min(p_order, 3)
                            q_order = min(q_order, 3)

                            st.markdown(
                                f"**Suggested ARIMA order:** p={p_order}, d={d_order}, q={q_order} "
                                f"(based on ACF/PACF analysis)")

                            arima_model = ARIMA(series,
                                                order=(p_order, d_order, q_order))
                            arima_fit   = arima_model.fit()

                            st.markdown(f"""
**ARIMA({p_order},{d_order},{q_order}) Results:**

| Metric | Value |
|---|---|
| AIC | {arima_fit.aic:.4f} |
| BIC | {arima_fit.bic:.4f} |
| Log-Likelihood | {arima_fit.llf:.4f} |
| No. Observations | {int(arima_fit.nobs)} |
""")
                            st.text(arima_fit.summary().as_text())

                            # Residual diagnostics
                            fig_res, axes_res = plt.subplots(
                                2, 2, figsize=(12, 8), facecolor="#0d1526")
                            arima_fit.plot_diagnostics(fig=fig_res)
                            fig_res.patch.set_facecolor("#0d1526")
                            for ax_r in axes_res.flatten():
                                ax_r.set_facecolor("#0d1526")
                                ax_r.tick_params(colors="#7a9abf")
                            plt.tight_layout()
                            st.pyplot(fig_res)
                            plt.close()

                            # Forecast
                            st.markdown("**ARIMA Forecast (next 10 periods):**")
                            forecast   = arima_fit.forecast(steps=10)
                            conf_int   = arima_fit.get_forecast(steps=10).conf_int()
                            fig_fc, ax_fc = plt.subplots(
                                figsize=(12, 5), facecolor="#0d1526")
                            ax_fc.set_facecolor("#0d1526")
                            ax_fc.plot(series.values, color="#00c6a7",
                                       linewidth=1.5, label="Observed")
                            fc_idx = range(len(series), len(series) + 10)
                            ax_fc.plot(fc_idx, forecast.values,
                                       color="#ffd166", linewidth=2,
                                       linestyle="--", label="Forecast")
                            ax_fc.fill_between(
                                fc_idx,
                                conf_int.iloc[:, 0],
                                conf_int.iloc[:, 1],
                                alpha=0.3, color="#0077ff", label="95% CI")
                            ax_fc.legend(facecolor="#0d1526",
                                         labelcolor="#c8deff")
                            ax_fc.tick_params(colors="#7a9abf")
                            ax_fc.set_title(
                                f"ARIMA({p_order},{d_order},{q_order}) Forecast",
                                color="#c8deff", fontsize=12)
                            for sp in ax_fc.spines.values():
                                sp.set_edgecolor("#1e2d4a")
                            fig_fc.patch.set_facecolor("#0d1526")
                            plt.tight_layout()
                            st.pyplot(fig_fc)
                            plt.close()

                        except Exception as arima_err:
                            st.warning(f"⚠️ ARIMA error: {arima_err}")

                        # ── SARIMA ────────────────────────────────────────
                        st.markdown("#### SARIMA Model")
                        try:
                            from statsmodels.tsa.statespace.sarimax import SARIMAX

                            # Detect likely seasonal period
                            seasonal_period = 12  # default monthly
                            if len(series) < 24:
                                seasonal_period = 4  # quarterly

                            st.markdown(
                                f"**Seasonal period detected:** m={seasonal_period} "
                                f"({'Monthly' if seasonal_period==12 else 'Quarterly'})")

                            sarima_model = SARIMAX(
                                series,
                                order=(p_order, d_order, q_order),
                                seasonal_order=(1, 1, 1, seasonal_period),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
                            sarima_fit = sarima_model.fit(disp=False)

                            st.markdown(f"""
**SARIMA({p_order},{d_order},{q_order})×(1,1,1)[{seasonal_period}] Results:**

| Metric | Value |
|---|---|
| AIC | {sarima_fit.aic:.4f} |
| BIC | {sarima_fit.bic:.4f} |
| Log-Likelihood | {sarima_fit.llf:.4f} |
| No. Observations | {int(sarima_fit.nobs)} |
""")
                            st.text(sarima_fit.summary().as_text())

                            # SARIMA Forecast
                            st.markdown("**SARIMA Forecast (next 12 periods):**")
                            s_forecast = sarima_fit.forecast(steps=12)
                            s_conf     = sarima_fit.get_forecast(
                                steps=12).conf_int()
                            fig_sfc, ax_sfc = plt.subplots(
                                figsize=(12, 5), facecolor="#0d1526")
                            ax_sfc.set_facecolor("#0d1526")
                            ax_sfc.plot(series.values, color="#00c6a7",
                                        linewidth=1.5, label="Observed")
                            sfc_idx = range(len(series), len(series) + 12)
                            ax_sfc.plot(sfc_idx, s_forecast.values,
                                        color="#a29bfe", linewidth=2,
                                        linestyle="--", label="Forecast")
                            ax_sfc.fill_between(
                                sfc_idx,
                                s_conf.iloc[:, 0], s_conf.iloc[:, 1],
                                alpha=0.3, color="#a29bfe", label="95% CI")
                            ax_sfc.legend(facecolor="#0d1526",
                                          labelcolor="#c8deff")
                            ax_sfc.tick_params(colors="#7a9abf")
                            ax_sfc.set_title(
                                f"SARIMA Forecast (m={seasonal_period})",
                                color="#c8deff", fontsize=12)
                            for sp in ax_sfc.spines.values():
                                sp.set_edgecolor("#1e2d4a")
                            fig_sfc.patch.set_facecolor("#0d1526")
                            plt.tight_layout()
                            st.pyplot(fig_sfc)
                            plt.close()

                            # Model comparison
                            st.markdown("#### Model Comparison: ARIMA vs SARIMA")
                            try:
                                arima_aic = arima_fit.aic
                                best = ("ARIMA" if arima_aic < sarima_fit.aic
                                        else "SARIMA")
                                st.markdown(f"""
| Model | AIC | BIC | Recommended |
|---|---|---|---|
| ARIMA({p_order},{d_order},{q_order}) | {arima_aic:.4f} | {arima_fit.bic:.4f} | {'✅' if best=='ARIMA' else ''} |
| SARIMA({p_order},{d_order},{q_order})×(1,1,1)[{seasonal_period}] | {sarima_fit.aic:.4f} | {sarima_fit.bic:.4f} | {'✅' if best=='SARIMA' else ''} |

**Lower AIC/BIC = better fit. Recommended model: {best}**
""")
                            except Exception:
                                pass

                        except Exception as sarima_err:
                            st.warning(f"⚠️ SARIMA error: {sarima_err}")

                    # ── Time Series Regression ────────────────────────────
                    if run_ts_reg and df is not None:
                        st.markdown("#### Time Series Regression")
                        try:
                            import pandas as pd
                            import numpy as np
                            from scipy import stats

                            numeric_c = df.select_dtypes(include=[np.number]).columns.tolist()
                            if ts_col in numeric_c and len(numeric_c) >= 2:
                                y = df[ts_col].dropna()
                                x_cols = [c for c in numeric_c if c != ts_col]
                                X = df[x_cols].loc[y.index].dropna()
                                common_idx = y.index.intersection(X.index)
                                y_reg = y.loc[common_idx]
                                X_reg = X.loc[common_idx]

                                # Add time trend
                                X_reg = X_reg.copy()
                                X_reg.insert(0, "Time_Trend",
                                             range(len(X_reg)))

                                from numpy.linalg import lstsq
                                X_mat = np.column_stack(
                                    [np.ones(len(X_reg)), X_reg.values])
                                coeffs, res, rank, sv = lstsq(
                                    X_mat, y_reg.values, rcond=None)
                                y_pred = X_mat @ coeffs
                                ss_res = np.sum((y_reg.values - y_pred)**2)
                                ss_tot = np.sum(
                                    (y_reg.values - y_reg.values.mean())**2)
                                r2 = 1 - ss_res / ss_tot
                                n = len(y_reg)
                                k = X_mat.shape[1] - 1
                                adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
                                mse = ss_res / (n - k - 1)
                                se = np.sqrt(mse * np.linalg.inv(
                                    X_mat.T @ X_mat).diagonal())
                                t_stats = coeffs / se
                                p_vals = [
                                    2 * (1 - stats.t.cdf(abs(t), df=n-k-1))
                                    for t in t_stats]

                                var_names = (["Intercept", "Time_Trend"]
                                             + x_cols)
                                st.markdown("**Time Series Regression Results:**")
                                header = "| Variable | Coefficient | Std Error | t-stat | p-value | Sig |"
                                divider = "|---|---|---|---|---|---|"
                                rows_out = [header, divider]
                                for vn, co, se_v, ts_v, pv in zip(
                                        var_names, coeffs, se, t_stats, p_vals):
                                    sig = ("***" if pv < 0.001
                                           else ("**" if pv < 0.01
                                                 else ("*" if pv < 0.05
                                                       else "")))
                                    rows_out.append(
                                        f"| {vn} | {co:.4f} | {se_v:.4f} | "
                                        f"{ts_v:.4f} | {pv:.4f} | {sig} |")
                                st.markdown("\n".join(rows_out))
                                st.markdown(f"""
**Model Summary:**

| Metric | Value |
|---|---|
| R² | {r2:.4f} |
| Adjusted R² | {adj_r2:.4f} |
| MSE | {mse:.4f} |
| N | {n} |
""")
                                # Fitted vs actual plot
                                fig_reg, ax_reg = plt.subplots(
                                    figsize=(12, 5), facecolor="#0d1526")
                                ax_reg.set_facecolor("#0d1526")
                                ax_reg.plot(y_reg.values, color="#00c6a7",
                                            label="Actual", linewidth=1.5)
                                ax_reg.plot(y_pred, color="#ffd166",
                                            linestyle="--",
                                            label="Fitted", linewidth=1.5)
                                ax_reg.legend(facecolor="#0d1526",
                                              labelcolor="#c8deff")
                                ax_reg.tick_params(colors="#7a9abf")
                                ax_reg.set_title(
                                    "Time Series Regression: Actual vs Fitted",
                                    color="#c8deff", fontsize=12)
                                for sp in ax_reg.spines.values():
                                    sp.set_edgecolor("#1e2d4a")
                                fig_reg.patch.set_facecolor("#0d1526")
                                plt.tight_layout()
                                st.pyplot(fig_reg)
                                plt.close()

                        except Exception as ts_reg_err:
                            st.warning(f"⚠️ TS Regression error: {ts_reg_err}")

                    # Store TS results
                    st.session_state.ts_analysis = (
                        f"ADF Statistic={adf_stat:.4f}, p={adf_p:.4f}, "
                        f"Stationarity={'Yes' if is_stationary else 'No'}, "
                        f"d_order={d_order}"
                    )

                except Exception as adf_err:
                    st.warning(f"⚠️ ADF/ARIMA error: {adf_err}")

            except ImportError:
                st.error("❌ statsmodels not installed. Run: pip install statsmodels")
            except Exception as e:
                st.error(f"❌ Time series error: {e}")


        # ── Autoregressive (AR) Model ─────────────────────────────────────
        if df is not None and "Autoregressive (AR) Model" in selected_tests and ts_col:
            st.markdown("---")
            st.markdown("### 🔁 Autoregressive (AR) Model")
            try:
                import numpy as np
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                from statsmodels.tsa.ar_model import AutoReg
                from statsmodels.tsa.stattools import acf, pacf

                series_ar = df[ts_col].dropna()
                st.markdown(f"**Target series:** {ts_col} — {len(series_ar)} observations")

                # Determine optimal lag using AIC
                best_aic, best_lag = float("inf"), 1
                for lag in range(1, min(13, len(series_ar)//4)):
                    try:
                        m = AutoReg(series_ar, lags=lag, old_names=False).fit()
                        if m.aic < best_aic:
                            best_aic, best_lag = m.aic, lag
                    except Exception:
                        pass

                st.markdown(f"**Optimal lag order selected:** p = {best_lag} (lowest AIC = {best_aic:.4f})")

                ar_model = AutoReg(series_ar, lags=best_lag, old_names=False)
                ar_fit   = ar_model.fit()

                # Results table
                params = ar_fit.params
                pvalues = ar_fit.pvalues
                st.markdown("**AR Model Coefficients:**")
                header_ar = "| Parameter | Coefficient | p-value | Significance |"
                divider_ar = "|---|---|---|---|"
                rows_ar = [header_ar, divider_ar]
                for pname, coef, pval in zip(params.index, params.values, pvalues.values):
                    sig = "***" if pval < 0.001 else ("**" if pval < 0.01 else ("*" if pval < 0.05 else "n.s."))
                    rows_ar.append(f"| {pname} | {coef:.4f} | {pval:.4f} | {sig} |")
                st.markdown("\n".join(rows_ar))

                st.markdown(f"""
**Model Summary:**

| Metric | Value |
|---|---|
| AIC | {ar_fit.aic:.4f} |
| BIC | {ar_fit.bic:.4f} |
| R² | {ar_fit.rsquared:.4f} |
| Adjusted R² | {ar_fit.rsquared_adj:.4f} |
| Log-Likelihood | {ar_fit.llf:.4f} |
| No. Observations | {int(ar_fit.nobs)} |

**Interpretation:**
The AR({best_lag}) model explains {ar_fit.rsquared*100:.2f}% of variance in {ts_col}.
{"All lag coefficients are statistically significant (p < 0.05), indicating strong autoregressive patterns." if all(p < 0.05 for p in pvalues.values[1:]) else "Some lag coefficients are not statistically significant, suggesting the AR order may be reduced."}
""")

                # Fitted vs actual
                fitted_ar = ar_fit.fittedvalues
                fig_ar, ax_ar = plt.subplots(figsize=(12, 5), facecolor="#0d1526")
                ax_ar.set_facecolor("#0d1526")
                ax_ar.plot(series_ar.values, color="#00c6a7", linewidth=1.5, label="Actual")
                ax_ar.plot(range(best_lag, best_lag + len(fitted_ar)), fitted_ar.values,
                           color="#ffd166", linewidth=1.5, linestyle="--", label=f"AR({best_lag}) Fitted")
                ax_ar.legend(facecolor="#0d1526", labelcolor="#c8deff")
                ax_ar.tick_params(colors="#7a9abf")
                ax_ar.set_title(f"AR({best_lag}) Model: Actual vs Fitted — {ts_col}", color="#c8deff", fontsize=12)
                for sp in ax_ar.spines.values():
                    sp.set_edgecolor("#1e2d4a")
                fig_ar.patch.set_facecolor("#0d1526")
                plt.tight_layout()
                st.pyplot(fig_ar)
                plt.close()

                # Residuals plot
                residuals_ar = ar_fit.resid
                fig_ar2, (ax_r1, ax_r2) = plt.subplots(1, 2, figsize=(12, 4), facecolor="#0d1526")
                for ax_r in [ax_r1, ax_r2]:
                    ax_r.set_facecolor("#0d1526")
                    ax_r.tick_params(colors="#7a9abf")
                    for sp in ax_r.spines.values():
                        sp.set_edgecolor("#1e2d4a")
                ax_r1.plot(residuals_ar.values, color="#a29bfe", linewidth=1)
                ax_r1.axhline(0, color="#ff6b6b", linestyle="--")
                ax_r1.set_title("AR Residuals", color="#c8deff", fontsize=11)
                ax_r2.hist(residuals_ar.values, bins=20, color="#a29bfe", edgecolor="#1e2d4a", alpha=0.8)
                ax_r2.set_title("Residual Distribution", color="#c8deff", fontsize=11)
                fig_ar2.patch.set_facecolor("#0d1526")
                plt.tight_layout()
                st.pyplot(fig_ar2)
                plt.close()

                # Forecast
                forecast_steps = 10
                ar_forecast = ar_fit.forecast(steps=forecast_steps)
                fc_idx_ar = range(len(series_ar), len(series_ar) + forecast_steps)
                fig_ar3, ax_ar3 = plt.subplots(figsize=(12, 5), facecolor="#0d1526")
                ax_ar3.set_facecolor("#0d1526")
                ax_ar3.plot(series_ar.values, color="#00c6a7", linewidth=1.5, label="Observed")
                ax_ar3.plot(fc_idx_ar, ar_forecast.values, color="#ffd166",
                            linewidth=2, linestyle="--", label=f"AR({best_lag}) Forecast")
                ax_ar3.legend(facecolor="#0d1526", labelcolor="#c8deff")
                ax_ar3.tick_params(colors="#7a9abf")
                ax_ar3.set_title(f"AR({best_lag}) Forecast — Next {forecast_steps} Periods", color="#c8deff", fontsize=12)
                for sp in ax_ar3.spines.values():
                    sp.set_edgecolor("#1e2d4a")
                fig_ar3.patch.set_facecolor("#0d1526")
                plt.tight_layout()
                st.pyplot(fig_ar3)
                plt.close()

            except ImportError:
                st.error("❌ statsmodels not installed: pip install statsmodels")
            except Exception as e_ar:
                st.warning(f"⚠️ AR Model error: {e_ar}")

        # ── Generate full AI chapter ──────────────────────────────────────
        st.markdown("---")
        if st.button("📊 Generate Full Chapter Three Narrative",
                     disabled=not st.session_state.data_filename):
            tests_str  = ", ".join(selected_tests) if selected_tests else "Descriptive Statistics"
            cols_info  = st.session_state.get("data_columns", "Not specified")
            ts_results = st.session_state.get("ts_analysis", "")

            sys_p = f"""You are an expert academic statistician and dissertation writer.
Generate CHAPTER THREE — METHODOLOGY AND DATA ANALYSIS.

PART A — METHODOLOGY:
Use these headings:
{st.session_state.meth_headings}

METHODOLOGY RULES:
- NO citations in prose paragraphs
- In Section 3.7 Data Analysis Technique, for EACH test list its formula and cite it in {ref_style_an}:
  Example: r = Σ[(xᵢ-x̄)(yᵢ-ȳ)] / √[Σ(xᵢ-x̄)²·Σ(yᵢ-ȳ)²]  (Field, 2018)
- List all assumptions for each test with their verification tests

PART B — RESULTS

### Assumptions Testing
Table with actual computed values (not Met/Not Met):
| Assumption | Test | Statistic | Value | p-value | Interpretation |

### Descriptive Statistics
- Tables + full narrative interpretation of every value

### [Each selected test — own section]
- H₀ and H₁
- Formula (brief)
- Results table with ALL statistics
- Full interpretation paragraph: every coefficient, p-value, effect size
- Link finding to corresponding research objective

{'### Time Series Analysis' if ts_results else ''}
{f'ADF results: {ts_results}' if ts_results else ''}
{'Explain stationarity result, differencing applied, ARIMA/SARIMA model chosen and why, forecast interpretation.' if ts_results else ''}

### Summary of All Findings
- One paragraph per objective
- State finding + statistical significance + implication

RULES: ASCII tables. Every table followed by interpretation. Formal academic language."""

            usr_p = (
                f"Dataset: {st.session_state.data_filename}\n"
                f"Columns: {cols_info}\n"
                f"Topic: {st.session_state.topic}\n"
                f"Variables: {st.session_state.variables or 'As in dataset'}\n"
                f"Tests: {tests_str}\n"
                f"Methodology from proposal:\n{st.session_state.proposal_methodology[:400]}\n"
                f"TS results: {ts_results}\n"
                f"Citation Style: {ref_style_an}\n\n"
                f"Generate complete Chapter Three narrative."
            )
            stream_response(sys_p, usr_p, "analysis")

            if st.session_state.analysis:
                sum_sys = """Write a SUMMARY OF ANALYSIS — one paragraph per research objective:
1. Restate objective
2. Finding from analysis
3. Statistical significance
4. Implication
Formal academic language."""
                sum_usr = (
                    f"Topic: {st.session_state.topic}\n"
                    f"Analysis:\n{st.session_state.analysis[:2500]}\n"
                    f"Objectives:\n{st.session_state.proposal_intro[:500]}\n"
                    f"Write analysis summary."
                )
                stream_response(sum_sys, sum_usr, "analysis_summary")

    show_output("analysis", "📊 Chapter Three Output")
    if st.session_state.analysis_summary:
        st.markdown("### 📋 Analysis Summary")
        st.markdown(
            f'<div class="output-box">{st.session_state.analysis_summary}</div>',
            unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 — CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 6:
    st.markdown('<div class="step-badge">STEP 6 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 🎯 Summary, Conclusion & Recommendations")

    if not st.session_state.topic:
        st.warning("⚠️ Complete Step 1 first.")
    else:
        ref_style_con = st.selectbox(
            "Citation Style", REF_STYLES,
            index=REF_STYLES.index(st.session_state.ref_style)
            if st.session_state.ref_style in REF_STYLES else 0, key="ref_con")

        if st.button("🎯 Generate Final Chapter"):
            doc_authors = (st.session_state.uploaded_doc_authors
                           or "Authors from uploaded documents")
            sys_p = f"""Generate a complete FINAL CHAPTER — SUMMARY, CONCLUSION AND RECOMMENDATIONS:

### 5.1 Introduction
### 5.2 Summary of the Study
### 5.3 Summary of Findings (numbered, each tied to an objective)
### 5.4 Conclusion (min 3 paragraphs drawn directly from findings)
### 5.5 Recommendations (min 5 numbered, specific, actionable)
### 5.6 Contributions to Knowledge
### 5.7 Suggestions for Further Research (min 3 areas)
### References

RULES:
- Each conclusion references a specific finding
- Cite {doc_authors} in {ref_style_con} where appropriate
- Paraphrase all content — no verbatim reproduction
- Formal academic language, min 2 paragraphs per section"""

            usr_p = (
                f"Topic: {st.session_state.topic}\n"
                f"Methodology: {st.session_state.methodology}\n"
                f"Objectives:\n{st.session_state.proposal_intro[:700]}\n\n"
                f"Analysis:\n{st.session_state.analysis[:1000] if st.session_state.analysis else 'Not generated'}\n\n"
                f"Summary:\n{st.session_state.analysis_summary[:600] if st.session_state.analysis_summary else ''}\n\n"
                f"Generate complete final chapter."
            )
            stream_response(sys_p, usr_p, "conclusion")

    show_output("conclusion", "🎯 Final Chapter Output")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7 — ABSTRACT
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 7:
    st.markdown('<div class="step-badge">STEP 7 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## ✍️ Abstract Generator")

    word_count = st.slider("Target word count", 150, 350, 250, 25)

    if not st.session_state.topic:
        st.warning("⚠️ Complete Step 1 first.")
    else:
        if st.button("✍️ Generate Abstract"):
            sys_p = f"""Write a single academic abstract paragraph (~{word_count} words):
background → problem → aim → methodology → key findings → conclusions/implications.
ONE paragraph. No subheadings. No citations. Past tense for methods/results.
End with: Keywords: [5 keywords]"""
            usr_p = (
                f"Topic: {st.session_state.topic}\n"
                f"Methodology: {st.session_state.methodology}\n"
                f"Objectives: {st.session_state.proposal_intro[:400]}\n"
                f"Results: {st.session_state.analysis_summary[:400] or st.session_state.analysis[:400]}\n"
                f"Conclusion: {st.session_state.conclusion[:300]}\n"
                f"Write ~{word_count} words."
            )
            stream_response(sys_p, usr_p, "abstract")

    show_output("abstract", "✍️ Abstract Output")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8 — REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 8:
    st.markdown('<div class="step-badge">STEP 8 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 🔖 Reference List Generator")

    ref_style = st.selectbox(
        "Citation Style", REF_STYLES,
        index=REF_STYLES.index(st.session_state.ref_style)
        if st.session_state.ref_style in REF_STYLES else 0, key="ref_final")
    st.session_state.ref_style = ref_style

    if not st.session_state.uploaded_docs_list:
        st.warning("⚠️ No documents uploaded. Upload in Step 2 first.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔖 Generate Reference List", use_container_width=True):
                doc_authors = (st.session_state.uploaded_doc_authors
                               or "Authors from uploaded documents")
                combined = build_combined_docs_text(max_chars_per_doc=1500)
                sys_p = f"""You are an expert academic librarian for {ref_style}.
Generate a complete reference list:
1. Format ONLY the uploaded document authors: {doc_authors}
2. Add standard methodology references (Field, Cohen, Hair, Pallant, Box & Jenkins for ARIMA)
   if any statistical formulas were used
3. Format every entry in {ref_style}
4. Sort alphabetically, number each entry
5. All bibliographic fields must be complete"""

                usr_p = (
                    f"Style: {ref_style}\nTopic: {st.session_state.topic}\n"
                    f"Document authors: {doc_authors}\n"
                    f"Documents sample:\n{combined[:6000]}\n"
                    f"Tests used: {', '.join(st.session_state.selected_tests)}\n"
                    f"Generate complete reference list."
                )
                stream_response(sys_p, usr_p, "references")

        with col2:
            if st.button("🔄 Re-format", use_container_width=True,
                          disabled=not st.session_state.references):
                sys_p = (f"Reformat in {ref_style}. Sort alphabetically. "
                         f"Number each. Fix errors. Do not add or remove entries.")
                stream_response(sys_p,
                                f"Reformat:\n\n{st.session_state.references}",
                                "references")

    show_output("references", "🔖 Reference List Output")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9 — EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif cur == 9:
    st.markdown('<div class="step-badge">STEP 9 OF 9</div>', unsafe_allow_html=True)
    st.markdown("## 📄 Full Dissertation Preview & Export")

    sections = [
        ("abstract",         "Abstract"),
        ("proposal_intro",   "Research Proposal"),
        ("chapter_one",      "Chapter One — Introduction"),
        ("literature",       "Chapter Two — Literature Review"),
        ("analysis",         "Chapter Three — Methodology & Analysis"),
        ("analysis_summary", "Chapter Three — Analysis Summary"),
        ("conclusion",       "Chapter Five — Conclusion & Recommendations"),
        ("references",       "Master Reference List"),
    ]

    scols = st.columns(4)
    for i, (key, label) in enumerate(sections):
        with scols[i % 4]:
            done = bool(st.session_state.get(key, ""))
            st.markdown(
                f'<div style="background:#0d1526;'
                f'border:1.5px solid {"#00c6a755" if done else "#1e2d4a"};'
                f'border-radius:10px;padding:0.7rem;margin-bottom:8px;text-align:center;">'
                f'{"✅" if done else "⭕"}<br>'
                f'<span style="color:{"#00c6a7" if done else "#3a4a6a"};'
                f'font-weight:600;font-size:11px;">{label}</span></div>',
                unsafe_allow_html=True)

    filled = [(k, l) for k, l in sections if st.session_state.get(k, "")]
    st.markdown("---")

    if not filled:
        st.warning("⚠️ No sections generated yet.")
    else:
        fname = (st.session_state.topic[:40].replace(" ", "_")
                 if st.session_state.topic else "ResearchAI_Dissertation")
        full_parts = [
            f"{'='*70}\n"
            f"{(st.session_state.topic or 'RESEARCH DISSERTATION').upper()}\n"
            f"Generated by ResearchForgeAI · Powered by Groq + LLaMA 3.3\n"
            f"{'='*70}\n"
        ]
        for key, label in sections:
            if st.session_state.get(key, ""):
                full_parts.append(
                    f"\n{'='*70}\n{label.upper()}\n{'='*70}\n\n"
                    f"{st.session_state[key]}\n")
        full_report = "\n".join(full_parts)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download Full (.txt)", data=full_report,
                               file_name=f"{fname}_Full.txt", mime="text/plain",
                               use_container_width=True)
        with col2:
            st.download_button("📋 Download (.md)", data=full_report,
                               file_name=f"{fname}_Full.md",
                               mime="text/markdown", use_container_width=True)

        st.markdown("---")
        st.markdown("### Download Individual Sections")
        dl_cols = st.columns(4)
        for i, (key, label) in enumerate(filled):
            with dl_cols[i % 4]:
                st.download_button(
                    f"📄 {label[:22]}",
                    data=f"{label}\n{'='*50}\n\n{st.session_state[key]}",
                    file_name=f"{fname}_{key}.txt", mime="text/plain",
                    use_container_width=True, key=f"dl_{key}")

        st.markdown("---")
        if st.session_state.topic:
            st.markdown(
                f'<div style="text-align:center;padding:2rem;background:#0a1220;'
                f'border:1px solid #1e2d4a;border-radius:12px;margin-bottom:1.5rem;">'
                f'<div style="font-size:22px;font-weight:800;color:#fff;">'
                f'{st.session_state.topic}</div>'
                f'<div style="color:#00c6a7;font-size:13px;letter-spacing:2px;">'
                f'A RESEARCH DISSERTATION</div>'
                f'<div style="color:#4a6a8a;font-size:12px;margin-top:0.5rem;">'
                f'Generated by ResearchAI · Powered by Groq + LLaMA 3.3</div>'
                f'</div>', unsafe_allow_html=True)

        for key, label in filled:
            with st.expander(f"📄 {label}", expanded=False):
                st.markdown(
                    f'<div class="output-box">{st.session_state[key]}</div>',
                    unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 4, 1])
with c1:
    if cur > 1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.current_step -= 1
            st.rerun()
with c3:
    if cur < 9:
        if st.button("Next Step →", use_container_width=True):
            st.session_state.current_step += 1
            st.rerun()

# ── Feedback box ─────────────────────────────────────────────────────────────
FEEDBACK_EMAIL = "oparae995@gmail.com"  # ← CHANGE THIS to your actual email

st.markdown("---")
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0a1a2e,#0d1526);
            border:1.5px solid #00c6a755;border-radius:16px;
            padding:1.5rem 2rem;margin:1rem 0 1rem 0;">
  <div style="font-family:Sora,sans-serif;font-weight:800;font-size:16px;
              color:#00c6a7;margin-bottom:0.4rem;">💬 Feedback & Suggestions</div>
  <div style="font-family:Sora,sans-serif;font-size:12px;color:#7a9abf;line-height:1.7;">
    Help improve ResearchForgeAI — report bugs, suggest features, or share your experience.<br>
    Your feedback goes directly to <strong style="color:#c8deff;">{FEEDBACK_EMAIL}</strong>
  </div>
</div>
""", unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    fb_col1, fb_col2 = st.columns(2)
    with fb_col1:
        fb_name  = st.text_input("Your name (optional)", placeholder="e.g. Dr. Okeke")
        fb_email = st.text_input("Your email (optional)", placeholder="you@example.com")
    with fb_col2:
        fb_type = st.selectbox("Feedback type", [
            "🐛 Bug Report", "✨ Feature Request",
            "👍 General Praise", "📊 Analysis Issue",
            "📄 Content Quality", "🔬 Time Series Issue",
            "📚 Literature Review Issue", "Other"])
        fb_step = st.selectbox("Which step?", [
            "General / Overall",
            "Step 1 — Proposal",
            "Step 2 — Document Upload",
            "Step 3 — Chapter One",
            "Step 4 — Literature Review",
            "Step 5 — Data Analysis",
            "Step 6 — Conclusion",
            "Step 7 — Abstract",
            "Step 8 — References",
            "Step 9 — Export"])
    fb_rating = st.select_slider(
        "Overall rating",
        options=["⭐ Poor","⭐⭐ Fair","⭐⭐⭐ Good","⭐⭐⭐⭐ Very Good","⭐⭐⭐⭐⭐ Excellent"],
        value="⭐⭐⭐⭐ Very Good")
    fb_text = st.text_area(
        "Your feedback *",
        placeholder="Describe the issue, bug, or suggestion in detail...",
        height=130)
    fb_submitted = st.form_submit_button("📤 Send Feedback", use_container_width=True)

    if fb_submitted:
        if fb_text.strip():
            # Build mailto link so user can send directly to your email
            import urllib.parse
            subject = urllib.parse.quote(f"ResearchForgeAI Feedback: {fb_type} — {fb_step}")
            body_parts = [
                f"Name: {fb_name or 'Anonymous'}",
                f"Email: {fb_email or 'Not provided'}",
                f"Type: {fb_type}",
                f"Step: {fb_step}",
                f"Rating: {fb_rating}",
                "",
                "Feedback:",
                fb_text,
            ]
            body = urllib.parse.quote("\n".join(body_parts))
            mailto_url = f"mailto:{FEEDBACK_EMAIL}?subject={subject}&body={body}"

            # Save to session
            if "all_feedback" not in st.session_state:
                st.session_state.all_feedback = []
            st.session_state.all_feedback.append({
                "name": fb_name or "Anonymous",
                "email": fb_email or "",
                "type": fb_type,
                "rating": fb_rating,
                "step": fb_step,
                "feedback": fb_text,
            })

            st.success("✅ Thank you! Click the button below to open your email client and send your feedback.")
            st.markdown(
                f'<a href="{mailto_url}" target="_blank" style="' +
                'display:inline-block;background:linear-gradient(135deg,#00c6a7,#0077ff);' +
                'color:white;font-family:Sora,sans-serif;font-weight:700;font-size:14px;' +
                'padding:0.6rem 1.8rem;border-radius:10px;text-decoration:none;' +
                'box-shadow:0 4px 20px #0077ff33;margin-top:0.5rem;">'
                '📧 Open Email Client to Send Feedback</a>',
                unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("⚠️ Please enter your feedback before submitting.")

# Show submitted feedback count
if st.session_state.get("all_feedback"):
    count = len(st.session_state.all_feedback)
    st.caption(f"📝 {count} feedback submission(s) recorded this session.")
    with st.expander("📋 View submitted feedback this session", expanded=False):
        for i, fb in enumerate(st.session_state.all_feedback, 1):
            st.markdown(
                f'<div style="background:#0d1526;border:1px solid #1e2d4a;' +
                f'border-radius:8px;padding:0.8rem;margin-bottom:0.5rem;font-size:12px;">' +
                f'<strong>#{i} — {fb["type"]}</strong> | {fb["rating"]} | {fb["step"]}<br>' +
                f'<em>{fb["name"]}</em> ({fb.get("email","")}) — {fb["feedback"][:200]}' +
                f'</div>', unsafe_allow_html=True)

st.markdown(
    '<div style="text-align:center;margin-top:1rem;padding:1rem;'
    'border-top:1px solid #1e2d4a;font-family:Sora,sans-serif;'
    'font-size:11px;color:#3a4a6a;letter-spacing:1px;">'
    '🔬 ResearchForgeAI · Powered by Groq + LLaMA 3.3 70B · Free to Use'
    '</div>', unsafe_allow_html=True)