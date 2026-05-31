import plotly.express as px
import plotly.graph_objects as go

from theme import (
    HIJAU_TUA, HIJAU_MED, HIJAU_MUDA, HIJAU_CERAH, HIJAU_PALE,
    KUNING, KUNING_PALE, MERAH, MERAH_PALE, HIJAU_PALET,
)

_LAYOUT_BASE = dict(
    paper_bgcolor='white',
    plot_bgcolor='white',
    font_color=HIJAU_TUA,
)

_XGRID = dict(gridcolor='#E8F5E9')
_YGRID = dict(gridcolor='#E8F5E9')


# ROW 1
def chart_top10_kota(dff):
    top10 = (
        dff.groupby('Kota/Kabupaten')['Timbulan']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(
        top10,
        x='Timbulan', y='Kota/Kabupaten',
        orientation='h',
        color='Timbulan',
        color_continuous_scale=[[0, HIJAU_PALE], [0.5, HIJAU_MED], [1, HIJAU_TUA]],
        labels={'Timbulan': 'Timbulan (tpd)', 'Kota/Kabupaten': ''},
        text='Timbulan',
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(
        **_LAYOUT_BASE,
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False,
        margin=dict(l=10, r=60, t=10, b=10),
        height=360,
    )
    fig.update_xaxes(**_XGRID)
    return fig


def chart_jenis_tpa(dff):
    jenis = dff['Jenis TPA'].value_counts().reset_index()
    jenis.columns = ['Jenis TPA', 'Jumlah']
    fig = px.pie(
        jenis,
        names='Jenis TPA', values='Jumlah',
        color_discrete_sequence=HIJAU_PALET,
        hole=0.45,
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        **_LAYOUT_BASE,
        margin=dict(l=10, r=10, t=20, b=10),
        height=360,
        showlegend=False,
    )
    return fig

# ROW 2
def chart_pengelolaan_provinsi(dff):
    prov_agg = (
        dff.groupby('Provinsi')[['% S. Terkelola', '% S. Belum Terkelola']]
        .mean()
        .reset_index()
    )
    #  Terkelola 
    prov_agg['Terkelola_pct'] = prov_agg['% S. Terkelola'].round(4)
    prov_agg['Belum_pct']     = prov_agg['% S. Belum Terkelola'].round(2)

    # Bar % Terkelola
    top_t = prov_agg.sort_values('Terkelola_pct', ascending=False).head(15)
    fig_t = px.bar(
        top_t, x='Provinsi', y='Terkelola_pct',
        labels={'Terkelola_pct': '% Terkelola', 'Provinsi': ''},
        text=top_t['Terkelola_pct'].apply(lambda x: f'{x:.4f}'),
    )
    fig_t.update_traces(textposition='outside', marker_color=HIJAU_MUDA)
    fig_t.update_layout(
        **_LAYOUT_BASE,
        title=dict(text='<b>% Sampah Terkelola per Provinsi</b>',
                   font=dict(size=13, color=HIJAU_TUA)),
        margin=dict(l=10, r=10, t=40, b=80),
        height=370,
        xaxis_tickangle=-35,
        yaxis_title='% Terkelola',
        showlegend=False,
    )
    fig_t.update_xaxes(**_XGRID)
    fig_t.update_yaxes(**_YGRID)

    # Bar % Belum Terkelola
    top_b = prov_agg.sort_values('Belum_pct', ascending=False).head(15)
    fig_b = px.bar(
        top_b, x='Provinsi', y='Belum_pct',
        labels={'Belum_pct': '% Belum Terkelola', 'Provinsi': ''},
        text=top_b['Belum_pct'].apply(lambda x: f'{x:.2f}%'),
    )
    fig_b.update_traces(textposition='outside', marker_color=MERAH)
    fig_b.update_layout(
        **_LAYOUT_BASE,
        title=dict(text='<b>% Sampah Belum Terkelola per Provinsi</b>',
                   font=dict(size=13, color=HIJAU_TUA)),
        margin=dict(l=10, r=10, t=40, b=80),
        height=370,
        xaxis_tickangle=-35,
        yaxis_title='% Belum Terkelola',
        showlegend=False,
    )
    fig_b.update_xaxes(**_XGRID)
    fig_b.update_yaxes(**_YGRID)

    return fig_t, fig_b


def chart_scatter(dff):
    fig = px.scatter(
        dff, x='Timbulan', y='% S. Belum Terkelola',
        color='Provinsi',
        hover_data=['Kota/Kabupaten', 'Jenis TPA'],
        labels={'Timbulan': 'Timbulan (tpd)', '% S. Belum Terkelola': '% Belum Terkelola'},
        color_discrete_sequence=px.colors.sequential.Greens_r,
    )
    fig.update_traces(marker=dict(size=7, opacity=0.75))
    fig.update_layout(
        **_LAYOUT_BASE,
        margin=dict(l=10, r=10, t=10, b=10),
        height=370,
        showlegend=False,
    )
    fig.update_xaxes(**_XGRID)
    fig.update_yaxes(**_YGRID)
    return fig

# ROW 3
def chart_timbulan_provinsi(dff):
    prov = (
        dff.groupby('Provinsi')['Timbulan']
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )
    fig = px.bar(
        prov, x='Provinsi', y='Timbulan',
        color='Timbulan',
        color_continuous_scale=[[0, HIJAU_PALE], [1, HIJAU_TUA]],
        labels={'Timbulan': 'Total Timbulan (tpd)'},
        text='Timbulan',
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(
        **_LAYOUT_BASE,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=80),
        height=360,
        xaxis_tickangle=-35,
    )
    fig.update_xaxes(**_XGRID)
    fig.update_yaxes(**_YGRID)
    return fig


def chart_boxplot_tpa(dff):
    fig = px.box(
        dff, x='Jenis TPA', y='Timbulan',
        color='Jenis TPA',
        color_discrete_sequence=HIJAU_PALET,
        labels={'Timbulan': 'Timbulan (tpd)'},
        points='outliers',
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=80),
        height=360,
        xaxis_tickangle=-20,
    )
    fig.update_xaxes(**_XGRID)
    fig.update_yaxes(**_YGRID)
    return fig

# ROW 4
def chart_gauge(dff):
    val = dff['% S. Terkelola'].mean()
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=val,
        number={'suffix': '%', 'font': {'size': 40, 'color': HIJAU_TUA}},
        delta={
            'reference': 50,
            'increasing': {'color': HIJAU_MUDA},
            'decreasing': {'color': MERAH},
        },
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': HIJAU_TUA},
            'bar': {'color': HIJAU_MUDA},
            'bgcolor': HIJAU_PALE,
            'steps': [
                {'range': [0, 30],  'color': MERAH_PALE},   # ← rgba-safe
                {'range': [30, 60], 'color': KUNING_PALE},
                {'range': [60, 100],'color': HIJAU_PALE},
            ],
            'threshold': {
                'line': {'color': HIJAU_TUA, 'width': 4},
                'thickness': 0.75,
                'value': val,
            },
        },
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        margin=dict(l=20, r=20, t=30, b=20),
        height=280,
    )
    return fig


def chart_heatmap(dff):
    top_prov = dff.groupby('Provinsi')['Timbulan'].sum().nlargest(10).index
    pivot = (
        dff[dff['Provinsi'].isin(top_prov)]
        .pivot_table(
            index='Provinsi', columns='Jenis TPA',
            values='% S. Terkelola', aggfunc='mean',
        )
        .round(2)
    )
    fig = px.imshow(
        pivot,
        color_continuous_scale=[[0, MERAH_PALE], [0.5, KUNING], [1, HIJAU_MED]],
        labels={'color': '% Terkelola'},
        aspect='auto',
        text_auto='.1f',
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        xaxis_tickangle=-20,
    )
    return fig

# PETA CHOROPLETH
def _choropleth_base(df_map, geojson, value_col, title, color_scale):
    vmin = df_map[value_col].min()
    vmax = df_map[value_col].max()
    # Midpoint persis di tengah rentang data
    vmid = (vmin + vmax) / 2

    fig = px.choropleth(
        df_map,
        geojson=geojson,
        featureidkey="properties.NAME_1",
        locations="NAME_1",
        color=value_col,
        color_continuous_scale=color_scale,
        range_color=[vmin, vmax],
        hover_name="Provinsi",
        hover_data={value_col: ':.2f', 'NAME_1': False},
        labels={value_col: title},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=40, b=0),
        height=480,
        title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=16, color=HIJAU_TUA)),
        coloraxis_colorbar=dict(
            title=dict(
                text=title,
                font=dict(color=HIJAU_TUA),
            ),
            tickfont=dict(color=HIJAU_TUA),
            tickvals=[vmin, vmid, vmax],
            ticktext=[f"{vmin:.2f}", f"{vmid:.2f}", f"{vmax:.2f}"],
        ),
        font_color=HIJAU_TUA,
    )
    return fig


# Skala 
_SCALE_RYG = [[0, MERAH], [0.5, KUNING], [1, HIJAU_MED]]
# Untuk "belum terkelola": hijau (rendah/bagus) → kuning → merah (tinggi/buruk)
_SCALE_GYR = [[0, HIJAU_MED], [0.5, KUNING], [1, MERAH]]
# Untuk timbulan: hijau muda → kuning → hijau tua (gradasi kepadatan)
_SCALE_TIM = [[0, HIJAU_MED], [0.5, KUNING], [1, MERAH]]


def chart_map_timbulan(df_map, geojson):
    return _choropleth_base(
        df_map, geojson,
        value_col='Timbulan',
        title='Total Timbulan (tpd)',
        color_scale=_SCALE_TIM,
    )


def chart_map_terkelola(df_map, geojson):
    return _choropleth_base(
        df_map, geojson,
        value_col='% S. Terkelola',
        title='% Sampah Terkelola',
        color_scale=_SCALE_RYG,
    )


def chart_map_belum(df_map, geojson):

    return _choropleth_base(
        df_map, geojson,
        value_col='% S. Belum Terkelola',
        title='% Sampah Belum Terkelola',
        color_scale=_SCALE_GYR,
    )