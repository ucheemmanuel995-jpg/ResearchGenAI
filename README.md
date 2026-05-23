#🔬 ResearchAI — End-to-End Research & Dissertation Platform

> AI-powered academic research assistant that takes you from topic to 
> full dissertation — proposal, literature review, data analysis, 
> conclusion, abstract, and references — all in one platform.

#🚀 Live Demo
👉 [Click here to use ResearchAI](https://researchgenai.streamlit.app/)

# 📌 What is ResearchAI?

ResearchAI is a free, AI-powered web application built for students, 
researchers, project writers, and academics. It guides you through every 
stage of academic research — from writing your proposal to generating a 
complete, formatted dissertation — using uploaded source documents as the 
foundation for all content.

Unlike generic AI writing tools, ResearchAI is structured around 
real academic standards: proper chapter formatting, in-text citations 
from your actual sources, statistical analysis with interpretation, 
and anti-plagiarism paraphrasing throughout.

# ✨ Key Features

### 📋 Step 1 — Research Proposal
- Generates a formal proposal with Introduction and Methodology only
- Future tense, no citations, professionally structured
- Editable headings to match your institution's format

### 📁 Step 2 — Document Upload Centre
- Upload unlimited PDFs, DOCX, and TXT files
- Each document processed individually — author, year, title, and 
  reference extracted automatically
- Formatted reference shown below each uploaded file for confirmation
- Image uploads supported with caption and source input boxes
- Content extracted from: Abstract, Results, Summary, Conclusion, 
  and Recommendations sections

### 📘 Step 3 — Chapter One (Introduction)
- Citations appear ONLY in Section 1.1 Background of the Study
- Only the authors of your uploaded documents are cited — 
  no secondary references
- Background is long, detailed, and fully curated from your documents
- All other sections (objectives, questions, hypotheses, scope) 
  are citation-free and derived from your proposal

### 📚 Step 4 — Literature Review (Chapter Two)
- Comprehensive, long-form, professional prose
- No headings by default — flows as continuous academic writing
- Each paragraph begins with an uploaded document author and their study
- Optional subheadings box available
- Fully paraphrased from Results, Summary, Conclusion, Abstract, 
  and Recommendations of every uploaded document
- Anti-plagiarism: no verbatim copying, complete sentence restructuring

### 📊 Step 5 — Data Analysis (Chapter Three)
- Upload Excel or CSV dataset
- Methodology section auto-generated from your proposal — no citations 
  in prose, but every formula is shown with a citation
- Full assumption testing with ACTUAL values (not "Met/Not Met"):
  - Normality (Shapiro-Wilk): W-statistic and p-value shown
  - Homoscedasticity (Levene's): F-statistic and p-value shown
  - Multicollinearity (VIF): exact VIF values per variable
  - Autocorrelation (Durbin-Watson): DW statistic shown
- When an assumption FAILS: remedy is named, formula shown, 
  and the corrective test is automatically carried out:
  - Heteroscedasticity → Welch's t-test + Log transformation applied
  - Autocorrelation → AR model recommended and executed
- Statistical tests available (16 total):
  - Descriptive Statistics
  - Pearson & Spearman Correlation
  - Simple & Multiple Regression
  - Time Series Regression
  - Binary Logistic Regression
  - Independent & Paired Samples T-Test
  - One-Way & Two-Way ANOVA
  - Chi-Square Test
  - Mann-Whitney U & Kruskal-Wallis
  - Autoregressive (AR) Model
  - Full Time Series Analysis:
    - ADF Stationarity Test (with exact values)
    - Auto-differencing (1st and 2nd order if needed)
    - ACF and PACF plots
    - ARIMA (auto p,d,q from ACF/PACF)
    - SARIMA (seasonal detection)
    - Model comparison (AIC/BIC)
    - Forecast with 95% confidence interval
- Every table is followed by a full interpretation paragraph
- Descriptive graphs: Histograms, Box plots, Bar charts, 
  Line graphs, Area charts, Frequency polygons, 
  Stacked bar charts, Correlation heatmap, Scatter plots
- Auto-generated Analysis Summary at the end

### 🎯 Step 6 — Conclusion & Recommendations (Chapter Five)
- Summary of findings linked to each objective
- Formal conclusion paragraphs
- At least 5 numbered, actionable recommendations
- Contributions to knowledge
- Suggestions for further research

### ✍️ Step 7 — Abstract
- Single paragraph, 150–350 words (user-controlled slider)
- Covers background, objectives, methodology, findings, conclusions
- Ends with 5 keywords
- No citations

### 🔖 Step 8 — References
- Master reference list compiled from all uploaded documents only
- No external sources added
- Formatted in chosen citation style: 
  APA 7th, APA 6th, MLA, Chicago, Harvard, or Vancouver
- One-click re-format option

### 📄 Step 9 — Export
- Full dissertation preview with collapsible sections
- Download full dissertation as .txt or .md
- Download individual chapters separately
- Live section completion tracker

## 🧠 Powered By
- **Groq API** — ultra-fast LLaMA 3.3 70B inference (free tier available)
- **Streamlit** — interactive web interface
- **statsmodels** — time series, ARIMA, SARIMA, regression
- **matplotlib** — all charts and graphs
- **pdfplumber** — PDF text extraction
- **pandas / numpy / scipy** — data analysis

## 🔧 How to Run Locally

### 1. Clone the repository
git clone https://github.com/ucheemmanuel995/researchgenai.git
cd researchgenai

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your Groq API key
Create .streamlit/secrets.toml:
GROQ_API_KEY = "gsk_your_key_here"

Get a FREE key at: https://console.groq.com

### 4. Run the app
streamlit run research_ai.py

## 📦 Requirements

streamlit>=1.32.0
groq>=0.9.0
pandas>=2.0.0
openpyxl>=3.1.0
pdfplumber>=0.10.0
python-docx>=1.1.0
matplotlib>=3.8.0
numpy>=1.26.0
scipy>=1.12.0
statsmodels>=0.14.0

## 🎯 Who Is This For?

- 🎓 Undergraduate and postgraduate students writing dissertations
- 🔬 Academic researchers conducting quantitative or qualitative studies
- 📊 Data analysts who need statistical reporting with interpretation
- ✍️ Project writers and consultants producing research reports
- 🏫 Lecturers and supervisors demonstrating research methodology

## ⚠️ Ethical Use

ResearchAI is a writing and analysis assistance tool. Users are 
responsible for verifying all generated content, ensuring accuracy 
of citations, and complying with their institution's academic 
integrity policies. The platform paraphrases uploaded content to 
support originality — final review and editing remain the 
responsibility of the researcher.

## 💬 Feedback & Contributions

Found a bug or have a feature request?
Use the in-app feedback form (bottom of every page) or open a GitHub issue.

## 📄 License
MIT License — free to use, modify, and distribute.

---

Built with ❤️ for African researchers and students by [Your Name]
