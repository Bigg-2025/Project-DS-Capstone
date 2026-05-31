import streamlit as st
import pandas as pd


def render_kpi(dff: pd.DataFrame):
    """Render 5 KPI metric cards dengan CSS grid (responsive mobile)."""
    total_timbulan   = f"{dff['Timbulan'].sum():,.0f}"
    rata_terkelola   = f"{dff['% S. Terkelola'].mean():.4f}"
    rata_belum       = f"{dff['% S. Belum Terkelola'].mean():.2f}%"
    jml_kota         = str(dff['Kota/Kabupaten'].nunique())
    jml_provinsi     = str(dff['Provinsi'].nunique())

    html = f"""
    <div class="kpi-grid">
        <div class="metric-card">
            <div class="label">Total Timbulan</div>
            <div class="value">{total_timbulan}</div>
            <div class="sub">ton/hari (tpd)</div>
        </div>
        <div class="metric-card">
            <div class="label">Rata-rata Terkelola</div>
            <div class="value">{rata_terkelola}</div>
            <div class="sub">dari total sampah</div>
        </div>
        <div class="metric-card">
            <div class="label">Rata-rata Belum Terkelola</div>
            <div class="value">{rata_belum}</div>
            <div class="sub">dari total sampah</div>
        </div>
        <div class="metric-card">
            <div class="label">Jumlah Kota/Kab</div>
            <div class="value">{jml_kota}</div>
            <div class="sub">wilayah tercakup</div>
        </div>
        <div class="metric-card">
            <div class="label">Jumlah Provinsi</div>
            <div class="value">{jml_provinsi}</div>
            <div class="sub">provinsi aktif</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)