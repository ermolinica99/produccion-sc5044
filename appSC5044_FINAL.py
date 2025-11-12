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

# CSS PERSONALIZADO MEJORADO - Similar a tu diseño Flask
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo degradado hermoso */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Contenedor principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Header hermoso */
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
    
    /* Tarjetas de estadísticas mejoradas */
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
    
    /* Contenedor de filtros */
    .filter-container {
        background: white;
        padding: 30px 40px;
        border-radius: 0 0 16px 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
    }
    
    /* Mejorar selectbox */
    div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
    
    /* Mejorar input */
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: #2575fc !important;
        box-shadow: 0 0 0 3px rgba(37, 117, 252, 0.1) !important;
    }
    
    /* Badges hermosos */
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
    
    .badge-prioridad1 {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(245, 87, 108, 0.3);
        border: none;
    }
    
    .badge-prioridad2 {
        background: linear-gradient(135deg, #ffd140 0%, #ff9900 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(255, 153, 0, 0.3);
        border: none;
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
    
    /* Dataframe mejorado */
    .dataframe {
        font-size: 13px !important;
    }
    
    /* Expander mejorado */
    div[data-testid="stExpander"] {
        background: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 12px;
    }
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
        padding: 16px 20px;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Botones mejorados */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Ruta al archivo JSON
RUTA_JSON = "datos-produccion.json"

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def convertir_fecha_excel(numero_serial):
    """Convierte el número serial de Excel a fecha legible."""
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
    """Parsear fecha en formato DD/MM/YYYY"""
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
    """Obtener fecha del lunes de una semana"""
    d = datetime(fecha.year, fecha.month, fecha.day) if isinstance(fecha, datetime) else fecha
    dia = d.weekday()
    lunes = d - timedelta(days=dia)
    return lunes.replace(hour=0, minute=0, second=0, microsecond=0)

def calcular_prioridad(fechaStr):
    """Determinar a qué prioridad pertenece una fecha"""
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
    """Procesa los datos para convertir fechas y calcular campos adicionales"""
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
        
        atraso = item['ATRASO']
        if atraso >= 14:
            item['CRITICIDAD'] = 'critico'
        elif atraso >= 7:
            item['CRITICIDAD'] = 'alto'
        elif atraso > 0:
            item['CRITICIDAD'] = 'medio'
        else:
            item['CRITICIDAD'] = 'normal'
        
        item['PRIORIDAD_SEMANA'] = calcular_prioridad(item['FECHA_PRODUCTO_FINAL'])
    
    return datos

@st.cache_data
def cargar_datos():
    """Cargar y procesar datos desde el archivo JSON"""
    try:
        if not os.path.exists(RUTA_JSON):
            st.error(f"⚠️ Archivo {RUTA_JSON} no encontrado")
            return None
        
        with open(RUTA_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data_procesada = procesar_datos(data)
        return data_procesada
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return None

def aplicar_filtros(datos, prioridad, estado_corte, urgencia, tipo, familia, busqueda):
    """Aplicar filtros a los datos"""
    datos_filtrados = datos.copy()
    
    if prioridad != "Todas":
        prioridad_num = int(prioridad)
        datos_filtrados = [item for item in datos_filtrados if item.get('PRIORIDAD_SEMANA') == prioridad_num]
    
    if estado_corte != "Todos":
        datos_filtrados = [item for item in datos_filtrados if item.get('CORTE_STATUS', '').lower() == estado_corte.lower()]
    
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
    """Crear badge HTML para estado de corte"""
    if not estado:
        estado = "naranja"
    
    estado_lower = estado.lower()
    clase = f"badge-{estado_lower}"
    
    return f'<span class="badge {clase}">{estado.upper()}</span>'

def formatear_badge_urgencia(urgencia):
    """Crear badge HTML para urgencia"""
    if urgencia == 1:
        return '<span class="badge badge-prioridad1">PRIORIDAD 1</span>'
    elif urgencia == 2:
        return '<span class="badge badge-prioridad2">PRIORIDAD 2</span>'
    else:
        return f'<span class="badge">PRIORIDAD {urgencia}</span>'

def formatear_badge_tipo(tipo):
    """Crear badge HTML para tipo"""
    if tipo == "STOCK":
        return '<span class="badge badge-stock">STOCK</span>'
    else:
        return '<span class="badge badge-personalizado">PERSONALIZADO</span>'

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

# Header personalizado
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

# Obtener listas únicas para filtros
familias = ["Todas"] + sorted(list(set([item.get('FAMILIA', '') for item in datos if item.get('FAMILIA')])))

# Inicializar session state para filtros
if 'prioridad' not in st.session_state:
    st.session_state.prioridad = "Todas"
if 'vista' not in st.session_state:
    st.session_state.vista = "Tabla"

# ============================================
# ESTADÍSTICAS
# ============================================

# Aplicar filtros para estadísticas
estado_corte = st.session_state.get('estado_corte', 'Todos')
urgencia = st.session_state.get('urgencia', 'Todas')
tipo = st.session_state.get('tipo', 'Todos')
familia = st.session_state.get('familia', 'Todas')
busqueda = st.session_state.get('busqueda', '')

datos_filtrados = aplicar_filtros(datos, st.session_state.prioridad, estado_corte, urgencia, tipo, familia, busqueda)

total_ots = len(datos_filtrados)
total_pendiente = int(sum(float(item.get('PENDIENTE', 0)) for item in datos_filtrados))
urgencias_count = len([item for item in datos_filtrados if item.get('URGENCIA') == 1])
estado_rojo = len([item for item in datos_filtrados if item.get('CORTE_STATUS') == 'rojo'])

st.markdown("""
<div style="background: white; padding: 30px 40px; margin: 0;">
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
        <div class="stat-card">
            <h3>TOTAL OTS</h3>
            <div class="value">""" + f"{total_ots:,}" + """</div>
        </div>
        <div class="stat-card">
            <h3>PENDIENTE</h3>
            <div class="value">""" + f"{total_pendiente:,}" + """</div>
        </div>
        <div class="stat-card">
            <h3>URGENCIAS</h3>
            <div class="value">""" + str(urgencias_count) + """</div>
        </div>
        <div class="stat-card">
            <h3>ESTADO CORTE ROJO</h3>
            <div class="value">""" + str(estado_rojo) + """</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# FILTROS
# ============================================

st.markdown('<div class="filter-container">', unsafe_allow_html=True)

# Botones de prioridad
st.markdown("### 📅 Filtrar por Prioridad de Semana")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📋 TODAS", use_container_width=True, type="primary" if st.session_state.prioridad == "Todas" else "secondary"):
        st.session_state.prioridad = "Todas"
        st.rerun()

with col2:
    if st.button("🔴 PRIORIDAD 1 (Esta semana)", use_container_width=True, type="primary" if st.session_state.prioridad == "1" else "secondary"):
        st.session_state.prioridad = "1"
        st.rerun()

with col3:
    if st.button("🟠 PRIORIDAD 2 (Próxima semana)", use_container_width=True, type="primary" if st.session_state.prioridad == "2" else "secondary"):
        st.session_state.prioridad = "2"
        st.rerun()

with col4:
    if st.button("🟡 PRIORIDAD 3 (En 2 semanas)", use_container_width=True, type="primary" if st.session_state.prioridad == "3" else "secondary"):
        st.session_state.prioridad = "3"
        st.rerun()

st.markdown("---")

# Filtros adicionales
col1, col2, col3, col4 = st.columns(4)

with col1:
    estado_corte = st.selectbox("Estado Corte", ["Todos", "Rojo", "Verde", "Naranja"], key="estado_corte")

with col2:
    urgencia = st.selectbox("Urgencia", ["Todas", "1 Alta", "2 Normal"], key="urgencia")

with col3:
    tipo = st.selectbox("Tipo", ["Todos", "STOCK", "PERSONALIZADO"], key="tipo")

with col4:
    familia = st.selectbox("Familia", familias, key="familia")

# Búsqueda
busqueda = st.text_input("🔍 Buscar por OT, SKU o descripción...", key="busqueda")

# Botones de acción
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔍 Aplicar Filtros", use_container_width=True, type="primary"):
        st.rerun()

with col2:
    if st.button("🔄 Limpiar Filtros", use_container_width=True):
        st.session_state.prioridad = "Todas"
        st.session_state.estado_corte = "Todos"
        st.session_state.urgencia = "Todas"
        st.session_state.tipo = "Todos"
        st.session_state.familia = "Todas"
        st.session_state.busqueda = ""
        st.rerun()

with col3:
    if st.button("📦 Vista Agrupada" if st.session_state.vista == "Tabla" else "📋 Vista Tabla", use_container_width=True):
        st.session_state.vista = "Agrupada" if st.session_state.vista == "Tabla" else "Tabla"
        st.rerun()

with col4:
    if len(datos_filtrados) > 0:
        df = pd.DataFrame(datos_filtrados)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        prioridad_texto = st.session_state.prioridad if st.session_state.prioridad != "Todas" else "todas"
        nombre_archivo = f"produccion_sc5044_prioridad{prioridad_texto}_{fecha_actual}.csv"
        
        st.download_button(
            label="📥 Exportar Excel",
            data=csv,
            file_name=nombre_archivo,
            mime="text/csv",
            use_container_width=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MOSTRAR DATOS
# ============================================

st.markdown('<div style="padding: 20px 0;">', unsafe_allow_html=True)

if len(datos_filtrados) == 0:
    st.warning("😕 No se encontraron resultados. Intenta ajustar los filtros.")
else:
    if st.session_state.vista == "Tabla":
        # Crear DataFrame
        df = pd.DataFrame(datos_filtrados)
        
        # Formatear datos para mostrar
        df_display = pd.DataFrame({
            'OT': df['OT'],
            'SKU': df['SKU'],
            'Descripción': df['DESCRIPCION'],
            'Familia': df['FAMILIA'],
            'Cant. Total': df['CANTIDAD_TOTAL'].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "-"),
            'Pendiente': df['PENDIENTE'].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "-"),
            'Fecha Final': df['FECHA_PRODUCTO_FINAL'],
            'Fecha Cosido': df['FECHA_COSIDO'],
            'Atraso': df['ATRASO'],
            'Estado Corte': df['CORTE_STATUS'].apply(lambda x: x.upper() if x else "NARANJA"),
            'Urgencia': df['URGENCIA'].apply(lambda x: f"PRIORIDAD {x}" if pd.notnull(x) else "-"),
            'Semana': df['SEMANA'],
            'Tipo': df['TIPO']
        })
        
        st.dataframe(
            df_display,
            use_container_width=True,
            height=600,
            hide_index=True
        )
        
    else:
        # Vista agrupada
        grupos = {}
        for item in datos_filtrados:
            sku = item.get('SKU', 'SIN_SKU')
            if sku not in grupos:
                grupos[sku] = {
                    'descripcion': item.get('DESCRIPCION', sku),
                    'familia': item.get('FAMILIA', '-'),
                    'ots': [],
                    'total_pendiente': 0,
                    'estados': {'rojo': 0, 'verde': 0, 'naranja': 0}
                }
            
            grupos[sku]['ots'].append(item)
            grupos[sku]['total_pendiente'] += float(item.get('PENDIENTE', 0))
            
            estado = (item.get('CORTE_STATUS', '') or '').lower()
            if estado in grupos[sku]['estados']:
                grupos[sku]['estados'][estado] += 1
        
        grupos_ordenados = sorted(grupos.items(), key=lambda x: x[1]['total_pendiente'], reverse=True)
        
        for sku, grupo in grupos_ordenados:
            with st.expander(
                f"📦 {sku} | {grupo['familia']} | {len(grupo['ots'])} OT{'s' if len(grupo['ots']) != 1 else ''} | {int(grupo['total_pendiente']):,} unidades"
            ):
                for ot in grupo['ots']:
                    # Título de la OT con descripción
                    st.markdown(f"### 🏷️ {ot.get('DESCRIPCION', 'Sin descripción')}")
                    
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.markdown(f"**OT:** {ot.get('OT', '-')}")
                        st.markdown(f"**Tipo:** {formatear_badge_tipo(ot.get('TIPO', 'STOCK'))}", unsafe_allow_html=True)
                    
                    with col2:
                        subcol1, subcol2, subcol3, subcol4 = st.columns(4)
                        
                        with subcol1:
                            st.markdown(f"**📅 Fecha Final:**")
                            st.write(ot.get('FECHA_PRODUCTO_FINAL', '-'))
                        
                        with subcol2:
                            st.markdown(f"**📦 Pendiente:**")
                            st.write(f"{int(ot.get('PENDIENTE', 0)):,} uds")
                        
                        with subcol3:
                            st.markdown(f"**⏰ Atraso:**")
                            st.write(f"{ot.get('ATRASO', 0)} días")
                        
                        with subcol4:
                            st.markdown(f"**🎨 Estado Corte:**")
                            st.markdown(formatear_badge_estado(ot.get('CORTE_STATUS', 'naranja')), unsafe_allow_html=True)
                    
                    st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Desarrollado con ❤️ usando Streamlit | SC5044 Production Management")
