# TEMA WARNA 
HIJAU_TUA   = "#1B5E20"
HIJAU       = "#2E7D32"
HIJAU_MED   = "#388E3C"
HIJAU_MUDA  = "#4CAF50"
HIJAU_CERAH = "#81C784"
HIJAU_PALE  = "#C8E6C9"
KUNING      = "#FDD835"
MERAH       = "#C62828"
MERAH_PALE  = "#FFCDD2"
KUNING_PALE = "#FFF9C4"
ABU         = "#ECEFF1"

# Palette urutan untuk bar/pie
HIJAU_PALET = [HIJAU_TUA, HIJAU_MED, HIJAU_MUDA, HIJAU_CERAH, HIJAU_PALE, "#A5D6A7", "#69F0AE"]

CSS = f"""
<style>
    /* ── BASE ── */
    .stApp {{
        background-color: #F1F8E9;
    }}

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {HIJAU_TUA} 0%, {HIJAU_MED} 100%);
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {{
        color: {HIJAU_PALE} !important;
        font-weight: 600;
    }}

    /* ── HEADER ── */
    .dashboard-header {{
        background: linear-gradient(135deg, {HIJAU_TUA} 0%, {HIJAU_MED} 60%, {HIJAU_MUDA} 100%);
        padding: 1.5rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 20px rgba(27,94,32,0.25);
    }}
    .dashboard-header h1 {{
        color: white;
        font-size: clamp(1.1rem, 4vw, 2rem);
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }}
    .dashboard-header p {{
        color: {HIJAU_PALE};
        margin: 0.4rem 0 0 0;
        font-size: clamp(0.75rem, 2.5vw, 1rem);
    }}

    /* ── METRIC CARDS ── */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.75rem;
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background: white;
        border-left: 5px solid {HIJAU_MUDA};
        border-radius: 12px;
        padding: 1rem 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    }}
    .metric-card .label {{
        color: #555;
        font-size: clamp(0.65rem, 1.5vw, 0.82rem);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.3rem;
    }}
    .metric-card .value {{
        color: {HIJAU_TUA};
        font-size: clamp(1.2rem, 3vw, 2rem);
        font-weight: 800;
        line-height: 1.1;
    }}
    .metric-card .sub {{
        color: #888;
        font-size: clamp(0.65rem, 1.5vw, 0.8rem);
        margin-top: 0.3rem;
    }}

    /* ── SECTION TITLE ── */
    .section-title {{
        color: {HIJAU_TUA};
        font-size: clamp(0.95rem, 2.5vw, 1.15rem);
        font-weight: 700;
        border-bottom: 3px solid {HIJAU_MUDA};
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }}

    h1, h2, h3 {{
        color: {HIJAU_TUA};
    }}

    /* ── MOBILE ≤ 768px ── */
    @media (max-width: 768px) {{
        /* Sidebar collapse otomatis di mobile — tidak perlu override */

        .dashboard-header {{
            padding: 1rem 1rem;
            border-radius: 10px;
        }}

        /* KPI: 2 kolom di mobile */
        .kpi-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}

        /* Plotly chart: pastikan tidak overflow */
        .stPlotlyChart {{
            overflow-x: auto !important;
        }}
        iframe {{
            max-width: 100% !important;
        }}

        /* Padding konten lebih sempit */
        .block-container {{
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1rem !important;
        }}

        /* Section title lebih kecil */
        .section-title {{
            font-size: 0.95rem;
        }}

        /* Tab label tidak terpotong */
        [data-testid="stTabs"] button {{
            font-size: 0.75rem !important;
            padding: 0.4rem 0.5rem !important;
        }}
    }}

    /* ── SMALL MOBILE ≤ 480px ── */
    @media (max-width: 480px) {{
        .kpi-grid {{
            grid-template-columns: 1fr 1fr;
        }}
        .metric-card .value {{
            font-size: 1.3rem;
        }}
        .dashboard-header h1 {{
            font-size: 1.1rem;
        }}
    }}
</style>
"""