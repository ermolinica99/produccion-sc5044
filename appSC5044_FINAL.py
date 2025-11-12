import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Producción SC5044",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PERSONALIZADO MEJORADO
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }

    .custom-header {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 30px 40px;
        border-radius: 16px 16px 0 0;
        margin-bottom: 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }

    .custom-header h1 {
        font-size: 28px;
        font-weight: 600;
        margin: 0 0 10px 0;
    }

    .custom-header p {
        opacity: 0.9;
        font-size: 14px;
        margin: 0;
    }

    .stat-card {
        background: white;
        padding: 24px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.3s ease;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }

    .stat-card h3 {
        font-size: 12px;
        color: #6c757d;
        margin: 0 0 12px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }

    .stat-card .value {
        font-size: 36px;
        font-weight: 700;
        color: #2575fc;
        margin: 0;
        line-height: 1;
    }

    .filter-container {
        background: white;
        padding: 30px 40px;
        border-radius: 0 0 16px 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
    }

    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        white-space: nowrap;
    }

    .badge-naranja {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }

    .badge-verde {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .badge-rojo {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .badge-stock {
        background: #007bff;
        color: white;
        box-shadow: 0 2px 6px rgba(0, 123, 255, 0.3);
        border: none;
    }

    .badge-personalizado {
        background: #6f42c1;
        color: white;
        box-shadow: 0 2px 6px rgba(111, 66, 193, 0.3);
        border: none;
    }

    /* Expander con fondo blanco y letras negras */
    div[data-testid="stExpander"] {
        background: white;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .streamlit-expanderHeader {
        background: white !important;
        color: #212529 !important;
        border-radius: 10px;
        font-weight: 600;
        padding: 16px 20px !important;
    }

    .streamlit-expanderHeader:hover {
        background: #f8f9fa !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }

    /* Icono del expander también negro */
    .streamlit-expanderHeader svg {
        fill: #212529 !important;
    }
</style>
""", unsafe_allow_html=True)

RUTA_JSON = "datos-produccion.json"


def convertir_fecha_excel(numero_serial):
    try:
        if numero_serial == "" or numero_serial is None:
            return ""
        serial = float(numero_serial)
        fecha_base = datetime(1899, 12, 30)
        fecha = fecha_base + timedelta(days=serial)
        return fecha.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return str(numero_serial)


def parsear_fecha(fechaStr):
    if not fechaStr:
        return None
    partes = fechaStr.split('/')
    if len(partes) != 3:
        return None
    try:
        return datetime(int(partes[2]), int(partes[1]), int(partes[0]))
    except:
        return None


def obtener_lunes_de_semana(fecha):
    d = datetime(fecha.year, fecha.month, fecha.day) if isinstance(fecha, datetime) else fecha
    dia = d.weekday()
    lunes = d - timedelta(days=dia)
    return lunes.replace(hour=0, minute=0, second=0, microsecond=0)


def calcular_prioridad(fechaStr):
    fecha = parsear_fecha(fechaStr)
    if not fecha:
        return None
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    lunes_esta_semana = obtener_lunes_de_semana(hoy)
    lunes_proxima_semana = lunes_esta_semana + timedelta(days=7)
    lunes_semana_3 = lunes_proxima_semana + timedelta(days=7)
    domingo_esta_semana = lunes_esta_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)
    domingo_proxima_semana = lunes_proxima_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)
    domingo_semana_3 = lunes_semana_3 + timedelta(days=6, hours=23, minutes=59, seconds=59)

    if lunes_esta_semana <= fecha <= domingo_esta_semana:
        return 1
    elif lunes_proxima_semana <= fecha <= domingo_proxima_semana:
        return 2
    elif lunes_semana_3 <= fecha <= domingo_semana_3:
        return 3
    return None


def procesar_datos(datos):
    for item in datos:
        item['FECHA_PRODUCTO_FINAL'] = convertir_fecha_excel(item.get('FECHA_PRODUCTO_FINAL', ''))
        item['FECHA_COSIDO'] = convertir_fecha_excel(item.get('FECHA_COSIDO', ''))
        try:
            item['ATRASO'] = int(item.get('ATRASO', 0))
        except (ValueError, TypeError):
            item['ATRASO'] = 0
        try:
            item['PENDIENTE'] = float(item.get('PENDIENTE', 0))
        except (ValueError, TypeError):
            item['PENDIENTE'] = 0
        item['PRIORIDAD_SEMANA'] = calcular_prioridad(item['FECHA_PRODUCTO_FINAL'])
    return datos


def cargar_datos():
    try:
        if not os.path.exists(RUTA_JSON):
            st.error(f"⚠️ Archivo {RUTA_JSON} no encontrado")
            return None
        with open(RUTA_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return procesar_datos(data)
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return None


def aplicar_filtros(datos, prioridad, estado_corte, urgencia, tipo, familia, busqueda):
    datos_filtrados = datos.copy()
    # Filtrar por prioridad (solo 1, 2 o 3)
    if prioridad in ["1", "2", "3"]:
        prioridad_num = int(prioridad)
        datos_filtrados = [item for item in datos_filtrados if item.get('PRIORIDAD_SEMANA') == prioridad_num]
    if estado_corte != "Todos":
        datos_filtrados = [item for item in datos_filtrados if
                           item.get('CORTE_STATUS', '').lower() == estado_corte.lower()]
    if urgencia != "Todas":
        urgencia_num = int(urgencia.split()[0])
        datos_filtrados = [item for item in datos_filtrados if item.get('URGENCIA') == urgencia_num]
    if tipo != "Todos":
        datos_filtrados = [item for item in datos_filtrados if item.get('TIPO') == tipo]
    if familia != "Todas":
        datos_filtrados = [item for item in datos_filtrados if item.get('FAMILIA') == familia]
    if busqueda:
        busqueda = busqueda.lower()
        datos_filtrados = [
            item for item in datos_filtrados
            if busqueda in str(item.get('OT', '')).lower()
               or busqueda in str(item.get('SKU', '')).lower()
               or busqueda in str(item.get('DESCRIPCION', '')).lower()
               or busqueda in str(item.get('FAMILIA', '')).lower()
        ]
    datos_filtrados.sort(key=lambda x: parsear_fecha(x.get('FECHA_PRODUCTO_FINAL', '')) or datetime.max)
    return datos_filtrados


def formatear_badge_estado(estado):
    if not estado:
        estado = "naranja"
    estado_lower = estado.lower()
    return f'<span class="badge badge-{estado_lower}">{estado.upper()}</span>'


def formatear_badge_tipo(tipo):
    if tipo == "STOCK":
        return '<span class="badge badge-stock">STOCK</span>'
    else:
        return '<span class="badge badge-personalizado">PERSONALIZADO</span>'


# Header
st.markdown("""
<div class="custom-header">
    <h1>📊 Gestión de Producción SC5044</h1>
    <p>Control de órdenes de trabajo en tiempo real</p>
</div>
""", unsafe_allow_html=True)

# Cargar datos
datos = cargar_datos()
if datos is None:
    st.stop()

familias = ["Todas"] + sorted(list(set([item.get('FAMILIA', '') for item in datos if item.get('FAMILIA')])))

if 'prioridad' not in st.session_state:
    st.session_state.prioridad = "1"
if 'vista' not in st.session_state:
    st.session_state.vista = "Tabla"

# FILTROS
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
st.markdown("### 📅 Filtrar por Prioridad de Semana")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 PRIORIDAD 1", use_container_width=True,
                 type="primary" if st.session_state.prioridad == "1" else "secondary"):
        st.session_state.prioridad = "1"
        st.rerun()
with col2:
    if st.button("🟠 PRIORIDAD 2", use_container_width=True,
                 type="primary" if st.session_state.prioridad == "2" else "secondary"):
        st.session_state.prioridad = "2"
        st.rerun()
with col3:
    if st.button("🟡 PRIORIDAD 3", use_container_width=True,
                 type="primary" if st.session_state.prioridad == "3" else "secondary"):
        st.session_state.prioridad = "3"
        st.rerun()

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    estado_corte = st.selectbox("Estado Corte", ["Todos", "Rojo", "Verde", "Naranja"])
with col2:
    urgencia = st.selectbox("Urgencia", ["Todas", "1 Alta", "2 Normal"])
with col3:
    tipo = st.selectbox("Tipo", ["Todos", "STOCK", "PERSONALIZADO"])
with col4:
    familia = st.selectbox("Familia", familias)

busqueda = st.text_input("🔍 Buscar por OT, SKU o descripción...")

# APLICAR FILTROS
datos_filtrados = aplicar_filtros(datos, st.session_state.prioridad, estado_corte, urgencia, tipo, familia, busqueda)

# Botones
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("🔍 Aplicar Filtros", use_container_width=True, type="primary")
with col2:
    if st.button("🔄 Limpiar", use_container_width=True):
        st.session_state.prioridad = "1"
        st.rerun()
with col3:
    if st.button("📦 Vista Agrupada" if st.session_state.vista == "Tabla" else "📋 Vista Tabla",
                 use_container_width=True):
        st.session_state.vista = "Agrupada" if st.session_state.vista == "Tabla" else "Tabla"
        st.rerun()
with col4:
    if len(datos_filtrados) > 0:
        df = pd.DataFrame(datos_filtrados)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Exportar", csv, f"produccion_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv",
                           use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ESTADÍSTICAS (después de filtros)
total_ots = len(datos_filtrados)
total_pendiente = int(sum(float(item.get('PENDIENTE', 0)) for item in datos_filtrados))
urgencias_count = len([item for item in datos_filtrados if item.get('URGENCIA') == 1])
estado_rojo = len([item for item in datos_filtrados if item.get('CORTE_STATUS') == 'rojo'])

st.markdown(f"""
<div style="background: white; padding: 30px 40px; margin: 20px 0;">
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
        <div class="stat-card">
            <h3>TOTAL OTS</h3>
            <div class="value">{total_ots:,}</div>
        </div>
        <div class="stat-card">
            <h3>PENDIENTE</h3>
            <div class="value">{total_pendiente:,}</div>
        </div>
        <div class="stat-card">
            <h3>URGENCIAS</h3>
            <div class="value">{urgencias_count}</div>
        </div>
        <div class="stat-card">
            <h3>ESTADO CORTE ROJO</h3>
            <div class="value">{estado_rojo}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# MOSTRAR DATOS
if len(datos_filtrados) == 0:
    st.warning("😕 No se encontraron resultados")
else:
    if st.session_state.vista == "Tabla":
        df = pd.DataFrame(datos_filtrados)
        df_display = pd.DataFrame({
            'OT': df['OT'],
            'SKU': df['SKU'],
            'Familia': df['FAMILIA'],
            'Pendiente': df['PENDIENTE'].apply(lambda x: f"{int(x):,}"),
            'Fecha Final': df['FECHA_PRODUCTO_FINAL'],
            'Atraso': df['ATRASO'],
            'Estado': df['CORTE_STATUS'].apply(lambda x: x.upper() if x else "NARANJA"),
            'Tipo': df['TIPO']
        })
        st.dataframe(df_display, use_container_width=True, height=600, hide_index=True)
    else:
        grupos = {}
        for item in datos_filtrados:
            sku = item.get('SKU', 'SIN_SKU')
            if sku not in grupos:
                grupos[sku] = {'familia': item.get('FAMILIA', '-'), 'ots': [], 'total_pendiente': 0}
            grupos[sku]['ots'].append(item)
            grupos[sku]['total_pendiente'] += float(item.get('PENDIENTE', 0))

        for sku, grupo in sorted(grupos.items(), key=lambda x: x[1]['total_pendiente'], reverse=True):
            with st.expander(
                    f"📦 {sku} | {grupo['familia']} | {len(grupo['ots'])} OTs | {int(grupo['total_pendiente']):,} uds"):
                for ot in grupo['ots']:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**OT:** {ot.get('OT', '-')}")
                        st.markdown(formatear_badge_tipo(ot.get('TIPO', 'STOCK')), unsafe_allow_html=True)
                    with col2:
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.markdown("**📅 Fecha Final:**")
                            st.write(ot.get('FECHA_PRODUCTO_FINAL', '-'))
                        with c2:
                            st.markdown("**📦 Pendiente:**")
                            st.write(f"{int(ot.get('PENDIENTE', 0)):,} uds")
                        with c3:
                            st.markdown("**⏰ Atraso:**")
                            st.write(f"{ot.get('ATRASO', 0)} días")
                        with c4:
                            st.markdown("**🎨 Estado:**")
                            st.markdown(formatear_badge_estado(ot.get('CORTE_STATUS', 'naranja')),
                                        unsafe_allow_html=True)
                    st.markdown("---")

st.caption("SC5044 Production Management")