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
    initial_sidebar_state="expanded"  # Sidebar expandido por defecto
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

    /* Sidebar mejorado */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 2px solid #e8ecf1 !important;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stSidebar"] * {
        color: #2d3436 !important;
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
RUTA_TEMPORAL = "fabricacion-temporal.json"


# ============================================
# FUNCIONES PARA FABRICACIÓN TEMPORAL
# ============================================

def cargar_fabricacion_temporal():
    """Cargar datos de fabricación temporal"""
    try:
        if os.path.exists(RUTA_TEMPORAL):
            with open(RUTA_TEMPORAL, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}


def guardar_fabricacion_temporal(datos_temp):
    """Guardar datos de fabricación temporal"""
    try:
        with open(RUTA_TEMPORAL, 'w', encoding='utf-8') as f:
            json.dump(datos_temp, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error al guardar fabricación: {str(e)}")
        return False


def registrar_fabricacion(ot, unidades, usuario):
    """Registrar unidades fabricadas para una OT"""
    datos_temp = cargar_fabricacion_temporal()

    if ot not in datos_temp:
        datos_temp[ot] = {
            "unidades_fabricadas_total": 0,
            "registros": []
        }

    # Agregar registro
    datos_temp[ot]["unidades_fabricadas_total"] += unidades
    datos_temp[ot]["registros"].append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "unidades": unidades,
        "usuario": usuario
    })

    return guardar_fabricacion_temporal(datos_temp)


def obtener_unidades_fabricadas(ot):
    """Obtener total de unidades fabricadas para una OT"""
    datos_temp = cargar_fabricacion_temporal()
    if ot in datos_temp:
        return datos_temp[ot]["unidades_fabricadas_total"]
    return 0


def obtener_historial_fabricacion(ot):
    """Obtener historial de fabricación de una OT"""
    datos_temp = cargar_fabricacion_temporal()
    if ot in datos_temp:
        return datos_temp[ot]["registros"]
    return []


def eliminar_fabricacion_temporal():
    """Eliminar el archivo de fabricación temporal"""
    try:
        if os.path.exists(RUTA_TEMPORAL):
            os.remove(RUTA_TEMPORAL)
            return True
        return True
    except Exception as e:
        st.error(f"Error al eliminar: {str(e)}")
        return False


def obtener_estadisticas_fabricacion():
    """Obtener estadísticas generales de fabricación temporal"""
    datos_temp = cargar_fabricacion_temporal()
    total_ots = len(datos_temp)
    total_unidades = sum(item["unidades_fabricadas_total"] for item in datos_temp.values())
    return total_ots, total_unidades


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

# PANEL DE CONTROL ADMIN
if st.session_state.usuario == "admin":
    st.markdown("---")
    st.markdown("### 🔧 Panel de Administración")

    datos_temp = cargar_fabricacion_temporal()
    if datos_temp:
        total_ots_fab, total_uds_fab = obtener_estadisticas_fabricacion()

        col_admin1, col_admin2, col_admin3 = st.columns(3)

        with col_admin1:
            st.info(f"📦 **{total_ots_fab}** OTs con fabricación registrada")

        with col_admin2:
            st.info(f"✅ **{total_uds_fab:,}** unidades fabricadas (temporal)")

        with col_admin3:
            if st.button("🗑️ Eliminar Datos Temporales", use_container_width=True, type="primary"):
                if eliminar_fabricacion_temporal():
                    st.success("✅ Datos temporales eliminados correctamente")
                    st.rerun()
                else:
                    st.error("❌ Error al eliminar")

        with st.expander("📊 Ver detalle de fabricaciones"):
            for ot, datos in datos_temp.items():
                st.markdown(
                    f"**OT {ot}:** {datos['unidades_fabricadas_total']} uds - {len(datos['registros'])} registros")
    else:
        st.success("✅ No hay datos temporales de fabricación")

st.markdown("---")

# Cargar datos
datos = cargar_datos()
if datos is None:
    st.stop()

familias = ["Todas"] + sorted(list(set([item.get('FAMILIA', '') for item in datos if item.get('FAMILIA')])))

if 'prioridad' not in st.session_state:
    st.session_state.prioridad = "1"
if 'vista' not in st.session_state:
    st.session_state.vista = "Agrupada"  # Vista agrupada por defecto

# ============================================
# SIDEBAR - FILTROS
# ============================================

with st.sidebar:
    st.markdown("## 🔍 FILTROS")
    st.markdown("---")

    # Prioridad
    st.markdown("### 📅 Prioridad")
    prioridad_sel = st.radio(
        "Selecciona prioridad:",
        ["1", "2", "3"],
        index=["1", "2", "3"].index(st.session_state.prioridad),
        format_func=lambda x: f"{'🔴' if x == '1' else '🟠' if x == '2' else '🟡'} Prioridad {x}",
        label_visibility="collapsed"
    )
    if prioridad_sel != st.session_state.prioridad:
        st.session_state.prioridad = prioridad_sel
        st.rerun()

    st.markdown("---")

    # Estado Corte
    st.markdown("### 🎨 Estado Corte")
    estado_corte = st.selectbox("Estado:", ["Todos", "Rojo", "Verde", "Naranja"], label_visibility="collapsed")

    # Urgencia
    st.markdown("### ⚡ Urgencia")
    urgencia = st.selectbox("Urgencia:", ["Todas", "1 Alta", "2 Normal"], label_visibility="collapsed")

    # Tipo
    st.markdown("### 📦 Tipo")
    tipo = st.selectbox("Tipo:", ["Todos", "STOCK", "PERSONALIZADO"], label_visibility="collapsed")

    # Familia
    st.markdown("### 👕 Familia")
    familia = st.selectbox("Familia:", familias, label_visibility="collapsed")

    st.markdown("---")

    # Búsqueda
    st.markdown("### 🔍 Buscar")
    busqueda = st.text_input("OT, SKU o descripción...", label_visibility="collapsed")

    st.markdown("---")

    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Limpiar", use_container_width=True):
            st.session_state.prioridad = "1"
            st.rerun()
    with col2:
        if st.button("📦 Vista", use_container_width=True):
            st.session_state.vista = "Agrupada" if st.session_state.vista == "Tabla" else "Tabla"
            st.rerun()

    # Exportar
    if 'datos_filtrados' in locals() and len(datos_filtrados) > 0:
        df = pd.DataFrame(datos_filtrados)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "📥 Exportar CSV",
            csv,
            f"produccion_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

# ============================================
# CONTENIDO PRINCIPAL
# ============================================

# APLICAR FILTROS
datos_filtrados = aplicar_filtros(datos, st.session_state.prioridad, estado_corte, urgencia, tipo, familia, busqueda)

# ESTADÍSTICAS ARRIBA (3 tarjetas)
total_ots = len(datos_filtrados)
total_pendiente = int(sum(float(item.get('PENDIENTE', 0)) for item in datos_filtrados))
urgencias_count = len([item for item in datos_filtrados if item.get('URGENCIA') == 1])

st.markdown(f"""
<div style="background: white; padding: 30px 40px; margin: 0 0 30px 0; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
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
    </div>
</div>
""", unsafe_allow_html=True)

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
        # Vista agrupada JERÁRQUICA: FAMILIA → SKU → OT
        familias_grupos = {}

        # Agrupar por FAMILIA primero
        for item in datos_filtrados:
            familia_nombre = item.get('FAMILIA', 'SIN_FAMILIA')
            sku = item.get('SKU', 'SIN_SKU')

            if familia_nombre not in familias_grupos:
                familias_grupos[familia_nombre] = {}

            if sku not in familias_grupos[familia_nombre]:
                familias_grupos[familia_nombre][sku] = {
                    'ots': [],
                    'total_pendiente': 0
                }

            familias_grupos[familia_nombre][sku]['ots'].append(item)
            familias_grupos[familia_nombre][sku]['total_pendiente'] += float(item.get('PENDIENTE', 0))

        # Mostrar por FAMILIA → SKU → OT
        for familia_nombre in sorted(familias_grupos.keys()):
            skus_en_familia = familias_grupos[familia_nombre]
            total_ots_familia = sum(len(skus_en_familia[sku]['ots']) for sku in skus_en_familia)
            total_pendiente_familia = sum(skus_en_familia[sku]['total_pendiente'] for sku in skus_en_familia)

            # NIVEL 1: FAMILIA
            with st.expander(f"👕 {familia_nombre} | {total_ots_familia} OTs | {int(total_pendiente_familia):,} uds",
                             expanded=False):

                # NIVEL 2: SKU dentro de la familia
                for sku in sorted(skus_en_familia.keys(), key=lambda x: skus_en_familia[x]['total_pendiente'],
                                  reverse=True):
                    sku_data = skus_en_familia[sku]

                    with st.expander(
                            f"   📦 {sku} | {len(sku_data['ots'])} OTs | {int(sku_data['total_pendiente']):,} uds",
                            expanded=False):

                        # NIVEL 3: OTs dentro del SKU
                        for idx, ot in enumerate(sku_data['ots']):
                            ot_numero = ot.get('OT', '-')
                            pendiente_original = float(ot.get('PENDIENTE', 0))
                            unidades_fabricadas = obtener_unidades_fabricadas(ot_numero)
                            pendiente_real = max(0, pendiente_original - unidades_fabricadas)

                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.markdown(f"**OT:** {ot_numero}")
                                st.markdown(formatear_badge_tipo(ot.get('TIPO', 'STOCK')), unsafe_allow_html=True)
                            with col2:
                                c1, c2, c3, c4 = st.columns(4)
                                with c1:
                                    st.markdown("**📅 Fecha Final:**")
                                    st.write(ot.get('FECHA_PRODUCTO_FINAL', '-'))
                                with c2:
                                    st.markdown("**📦 Pendiente:**")
                                    if unidades_fabricadas > 0:
                                        st.write(f"~~{int(pendiente_original):,}~~ → **{int(pendiente_real):,}** uds")
                                    else:
                                        st.write(f"{int(pendiente_original):,} uds")
                                with c3:
                                    st.markdown("**⏰ Atraso:**")
                                    st.write(f"{ot.get('ATRASO', 0)} días")
                                with c4:
                                    st.markdown("**🎨 Estado:**")
                                    st.markdown(formatear_badge_estado(ot.get('CORTE_STATUS', 'naranja')),
                                                unsafe_allow_html=True)

                            # FORMULARIO DE FABRICACIÓN (Solo para usuario "produccion" o "admin")
                            if st.session_state.usuario in ["produccion", "admin"]:
                                st.markdown("---")
                                st.markdown("### 🏭 Registrar Fabricación")

                                col_form1, col_form2, col_form3 = st.columns([2, 1, 1])

                                with col_form1:
                                    unidades_key = f"unidades_{ot_numero}_{idx}_{familia_nombre}_{sku}"
                                    unidades_fabricar = st.number_input(
                                        "Unidades fabricadas:",
                                        min_value=0,
                                        max_value=int(pendiente_real),
                                        value=0,
                                        step=1,
                                        key=unidades_key
                                    )

                                with col_form2:
                                    if st.button(f"✅ Registrar",
                                                 key=f"btn_registrar_{ot_numero}_{idx}_{familia_nombre}_{sku}",
                                                 use_container_width=True):
                                        if unidades_fabricar > 0:
                                            if registrar_fabricacion(ot_numero, unidades_fabricar,
                                                                     st.session_state.usuario):
                                                st.success(f"✅ {unidades_fabricar} uds registradas correctamente")
                                                st.rerun()
                                            else:
                                                st.error("❌ Error al registrar")
                                        else:
                                            st.warning("⚠️ Debes ingresar unidades mayores a 0")

                                with col_form3:
                                    historial = obtener_historial_fabricacion(ot_numero)
                                    if historial:
                                        if st.button(f"📜 Historial ({len(historial)})",
                                                     key=f"btn_historial_{ot_numero}_{idx}_{familia_nombre}_{sku}",
                                                     use_container_width=True):
                                            st.session_state[
                                                f"mostrar_historial_{ot_numero}"] = not st.session_state.get(
                                                f"mostrar_historial_{ot_numero}", False)

                                # Mostrar historial si está activado
                                if st.session_state.get(f"mostrar_historial_{ot_numero}", False):
                                    st.markdown("#### 📜 Historial de Fabricación")
                                    for reg in reversed(historial):
                                        st.markdown(
                                            f"- **{reg['fecha']}** - {reg['unidades']} uds por *{reg['usuario']}*")

                                # Info para fabricadas
                                if unidades_fabricadas > 0:
                                    st.info(f"ℹ️ Total fabricado (temporal): **{int(unidades_fabricadas):,}** uds")

                            st.markdown("---")

st.caption("SC5044 Production Management")