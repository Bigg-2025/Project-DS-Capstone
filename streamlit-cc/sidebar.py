import streamlit as st
import pandas as pd
def render_sidebar(df: pd.DataFrame):
    with st.sidebar:
        st.markdown("## ♻️ Filter Data")
        st.markdown("---")

        provinsi_list = sorted(df['Provinsi'].dropna().unique().tolist())
        provinsi_sel = st.multiselect(
            "Provinsi",
            options=provinsi_list,
            default=provinsi_list,
            help="Pilih satu atau lebih provinsi",
        )

        jenis_tpa_list = sorted(df['Jenis TPA'].dropna().unique().tolist())
        jenis_tpa_sel = st.multiselect(
            "Jenis TPA",
            options=jenis_tpa_list,
            default=jenis_tpa_list,
        )

        timbulan_min = int(df['Timbulan'].min())
        timbulan_max = int(df['Timbulan'].max())
        timbulan_range = st.slider(
            "Rentang Timbulan (tpd)",
            min_value=timbulan_min,
            max_value=timbulan_max,
            value=(timbulan_min, timbulan_max),
        )

        st.markdown("---")
        st.markdown(f"**Total Record:** {len(df):,}")
        st.markdown(f"**Provinsi:** {df['Provinsi'].nunique()}")

    return provinsi_sel, jenis_tpa_sel, timbulan_range