import os
import json
import pandas as pd
import streamlit as st

# MAPPING NAMA PROVINSI
NAME_MAP = {
    'Aceh'              : 'ACEH',
    'Bali'              : 'BALI',
    'BangkaBelitung'    : 'BANGKA BELITUNG',
    'Banten'            : 'BANTEN',
    'Bengkulu'          : 'BENGKULU',
    'Gorontalo'         : 'GORONTALO',
    'JakartaRaya'       : 'DKI JAKARTA',
    'Jambi'             : 'JAMBI',
    'JawaBarat'         : 'JAWA BARAT',
    'JawaTengah'        : 'JAWA TENGAH',
    'JawaTimur'         : 'JAWA TIMUR',
    'KalimantanBarat'   : 'KALIMANTAN BARAT',
    'KalimantanSelatan' : 'KALIMANTAN SELATAN',
    'KalimantanTengah'  : 'KALIMANTAN TENGAH',
    'KalimantanTimur'   : 'KALIMANTAN TIMUR',
    'KalimantanUtara'   : 'KALIMANTAN UTARA',
    'KepulauanRiau'     : 'KEPULAUAN RIAU',
    'Lampung'           : 'LAMPUNG',
    'Maluku'            : 'MALUKU',
    'MalukuUtara'       : 'MALUKU UTARA',
    'NusaTenggaraBarat' : 'NUSA TENGGARA BARAT',
    'NusaTenggaraTimur' : 'NUSA TENGGARA TIMUR',
    'Papua'             : 'PAPUA',
    'PapuaBarat'        : 'PAPUA BARAT',
    'Riau'              : 'RIAU',
    'SulawesiBarat'     : 'SULAWESI BARAT',
    'SulawesiSelatan'   : 'SULAWESI SELATAN',
    'SulawesiTengah'    : 'SULAWESI TENGAH',
    'SulawesiTenggara'  : 'SULAWESI TENGGARA',
    'SulawesiUtara'     : 'SULAWESI UTARA',
    'SumateraBarat'     : 'SUMATERA BARAT',
    'SumateraSelatan'   : 'SUMATERA SELATAN',
    'SumateraUtara'     : 'SUMATERA UTARA',
    'Yogyakarta'        : 'DI YOGYAKARTA',
}

REV_MAP = {v: k for k, v in NAME_MAP.items()}


@st.cache_data
def load_data():
    candidates = [
        "asset/data_sampah_clean.xlsx",
        "/mnt/user-data/uploads/data_sampah_clean.xlsx",
    ]
    for path in candidates:
        if os.path.exists(path):
            df = pd.read_excel(path)
            df = _clean(df)
            return df
    st.error("❌ File `data_sampah_clean.xlsx` tidak ditemukan.")
    st.stop()


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    df['Jenis TPA'] = df['Jenis TPA'].fillna('Tidak Diketahui')

    if df['Timbulan'].dtype == object:
        df['Timbulan'] = (
            df['Timbulan'].astype(str)
            .str.replace('tpd', '', regex=False)
            .str.strip()
        )
    df['Timbulan'] = pd.to_numeric(df['Timbulan'], errors='coerce')

    for col in ['% S. Terkelola', '% S. Belum Terkelola']:
        if df[col].dtype == object:
            df[col] = (
                df[col].astype(str)
                .str.replace(',', '.', regex=False)
                .str.replace('%', '', regex=False)
                .str.strip()
            )
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


@st.cache_data
def load_geojson():
    candidates = [
        "asset/gadm41_IDN_1.json",
        "/mnt/user-data/uploads/gadm41_IDN_1.json",
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    return None


def apply_filters(df: pd.DataFrame, provinsi_sel, jenis_tpa_sel, timbulan_range):
    mask = (
        df['Provinsi'].isin(provinsi_sel)
        & df['Jenis TPA'].isin(jenis_tpa_sel)
        & df['Timbulan'].between(timbulan_range[0], timbulan_range[1])
    )
    return df[mask].copy()


def agg_provinsi(dff: pd.DataFrame) -> pd.DataFrame:
    timbulan = dff.groupby('Provinsi')['Timbulan'].sum().reset_index()
    persen   = (
        dff.groupby('Provinsi')[['% S. Terkelola', '% S. Belum Terkelola']]
        .mean()
        .reset_index()
    )
    merged = timbulan.merge(persen, on='Provinsi')
    merged['NAME_1'] = merged['Provinsi'].map(REV_MAP)
    return merged