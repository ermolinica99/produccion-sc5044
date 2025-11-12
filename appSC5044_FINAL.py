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

# CSS PERSONALIZADO MEJORADO - Diseño Moderno (Forzar tema claro)
st.markdown("""
<style>
    /* FORZAR TEMA CLARO - Ignorar tema oscuro del sistema */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Forzar colores claros en todos los textos */
    .stMarkdown, .stText, p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: #2d3436 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fondo degradado suave y elegante */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
        background: transparent !important;
    }

    /* Header moderno con sombra suave */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 50px;
        border-radius: 20px 20px 0 0;
        margin-bottom: 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }

    .custom-header h1 {
        font-size: 32px;
        font-weight: 700;
        margin: 0 0 10px 0;
        letter-spacing: -0.5px;
    }

    .custom-header p {
        opacity: 0.95;
        font-size: 16px;
        margin: 0;
        font-weight: 300;
    }

    /* Tarjetas de estadísticas premium */
    .stat-card {
        background: white;
        padding: 30px 25px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.4s ease;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    .stat-card h3 {
        font-size: 11px;
        color: #8b95a5;
        margin: 0 0 15px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .stat-card .value {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
    }

    /* Contenedor de filtros elegante */
    .filter-container {
        background: white;
        padding: 35px 50px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 30px;
        border-top: 3px solid #667eea;
    }

    /* Botones mejorados */
    .stButton button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        padding: 12px 24px;
        font-size: 14px;
    }

    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    /* Botones primarios con gradiente */
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    /* Select boxes modernos - FORZAR FONDO BLANCO */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
        border: 2px solid #e8ecf1 !important;
        transition: all 0.3s ease;
        background: white !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: #667eea !important;
    }

    /* Forzar texto negro en selects */
    div[data-baseweb="select"] > div {
        background: white !important;
        color: #2d3436 !important;
    }

    /* Input moderno - FORZAR FONDO BLANCO */
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #e8ecf1 !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        transition: all 0.3s ease;
        background: white !important;
        color: #2d3436 !important;
    }

    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        background: white !important;
    }

    /* Forzar labels en modo claro */
    .stTextInput label, .stSelectbox label {
        color: #2d3436 !important;
        font-weight: 600 !important;
    }

    /* Badges premium */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .badge-naranja {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        color: #d63031;
    }

    .badge-verde {
        background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);
        color: #00441b;
    }

    .badge-rojo {
        background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
        color: white;
    }

    .badge-stock {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
    }

    .badge-personalizado {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        color: white;
    }

    /* Expander premium */
    div[data-testid="stExpander"] {
        background: white;
        border-radius: 16px;
        border: 2px solid #e8ecf1;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }

    div[data-testid="stExpander"]:hover {
        border-color: #667eea;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.15);
    }

    .streamlit-expanderHeader {
        background: white !important;
        color: #2d3436 !important;
        border-radius: 16px;
        font-weight: 700;
        padding: 20px 24px !important;
        font-size: 15px;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%) !important;
    }

    .streamlit-expanderHeader svg {
        fill: #667eea !important;
    }

    /* Dataframe mejorado - FORZAR MODO CLARO */
    .dataframe {
        font-size: 14px !important;
        border-radius: 12px !important;
        background: white !important;
    }

    /* Forzar encabezados de tabla en blanco */
    .dataframe thead tr {
        background: #f8f9fa !important;
    }

    .dataframe thead th {
        background: #f8f9fa !important;
        color: #2d3436 !important;
        font-weight: 700 !important;
    }

    /* Forzar filas de tabla en blanco */
    .dataframe tbody tr {
        background: white !important;
    }

    .dataframe tbody tr:hover {
        background: #f8f9ff !important;
    }

    .dataframe tbody td {
        color: #2d3436 !important;
        background: white !important;
    }

    /* Forzar todos los elementos de streamlit en blanco */
    [data-testid="stDataFrame"] {
        background: white !important;
    }

    [data-testid="stDataFrame"] * {
        color: #2d3436 !important;
    }

    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f3f5;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Animación suave al cargar */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stat-card, .filter-container, div[data-testid="stExpander"] {
        animation: fadeIn 0.6s ease-out;
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

# ============================================
# SISTEMA DE AUTENTICACIÓN
# ============================================

# Credenciales (CAMBIA ESTAS CONTRASEÑAS)
USUARIOS = {
    "admin": "sc5044admin",
    "produccion": "produccion2024",
    "supervisor": "super2024"
}

# Verificar si el usuario está autenticado
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# Si no está autenticado, mostrar login
if not st.session_state.autenticado:
    st.markdown('<div class="filter-container" style="max-width: 500px; margin: 100px auto;">', unsafe_allow_html=True)
    st.markdown("### 🔐 Acceso Restringido")
    st.markdown("Por favor, introduce tus credenciales para acceder al sistema")

    usuario = st.text_input("👤 Usuario", key="login_usuario")
    password = st.text_input("🔑 Contraseña", type="password", key="login_password")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 Iniciar Sesión", use_container_width=True, type="primary"):
            if usuario in USUARIOS and USUARIOS[usuario] == password:
                st.session_state.autenticado = True
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.stop()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  # Detener la ejecución aquí si no está autenticado

# Mostrar botón de cerrar sesión
col_logout1, col_logout2 = st.columns([6, 1])
with col_logout2:
    if st.button("🚪 Salir", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.rerun()

st.markdown(f"👤 **Usuario:** {st.session_state.usuario}")
st.markdown("---")

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