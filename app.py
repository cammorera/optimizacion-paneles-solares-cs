import streamlit as st
from modelo import resolver_optimizacion

# Configuración de la página
st.set_page_config(page_title='Solar Optimizer CR', page_icon='☀️', layout='wide')
st.title('☀️ PanelOpt — Optimizador de Inversión Solar')
st.write('Construir y publicar una aplicación funcional basada en el modelo de paneles solares.') #

# Parámetros ajustables en el Sidebar
st.sidebar.header('⚙️ Parámetros del Proyecto')

# Seleccionamos una casa base (Datos de Tarea 1)
casa = st.sidebar.selectbox("Perfil de la Casa", ["Casa 1", "Casa 2", "Casa 3", "Personalizado"])

if casa == "Casa 1":
    area_def, cons_def = 150.0, 445.0 #
elif casa == "Casa 2":
    area_def, cons_def = 188.0, 404.0 #
elif casa == "Casa 3":
    area_def, cons_def = 228.0, 125.0 #
else:
    area_def, cons_def = 100.0, 300.0

area_disponible = st.sidebar.slider('Área de techo (m²)', 50, 300, int(area_def))
consumo_mes     = st.sidebar.slider('Consumo (kWh/mes)', 100, 600, int(cons_def))
horas_pico      = st.sidebar.slider('Horas pico solar/día', 3.0, 6.0, 4.5) #

if st.button('🚀 Optimizar Inversión'):
    # Llamamos a la lógica del modelo
    res = resolver_optimizacion(area_disponible, consumo_mes, horas_pico)
    
    if res["status"] == "Optimal":
        st.success(f'✅ Inversión mínima requerida: Z* = ${res["costo"]:,.2f}')
        
        # Métricas principales
        c1, c2, c3 = st.columns(3)
        c1.metric('🔵 Paneles Tipo A', int(res["x"]))
        c2.metric('🟠 Paneles Tipo B', int(res["y"]))
        c3.metric('🟢 Paneles Tipo C', int(res["z"]))
        
        # Gráfico de barras
        st.bar_chart({'Panel A': res["x"], 'Panel B': res["y"], 'Panel C': res["z"]})
        
        # Interpretación Gerencial (Requerido por la Tarea 3)
        st.markdown(f"""
        ### 📊 Interpretación Ejecutiva
        La solución óptima para la **{casa}** minimiza la inversión inicial a un costo de **${res["costo"]:,.2f}**. 
        
        **Detalles técnicos:**
        * Se cubre la demanda total de **{consumo_mes} kWh/mes**.
        * El área utilizada es de **{res["area_usada"]:.2f} m²**, lo cual es físicamente viable dentro de los **{area_disponible} m²** disponibles.
        * Se cumple con la premisa de **{horas_pico} horas pico solares** diarias en el Valle Central.
        """)
    else:
        st.error('❌ No hay solución viable: El área del techo es insuficiente para cubrir el consumo solicitado.')
