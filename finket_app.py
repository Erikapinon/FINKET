import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import feedparser
import base64

# Función para cargar imagen como base64
def load_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Cargamos imágenes base64
fondo_inicio = load_base64_image("finket_portada.png")
fondo_general = load_base64_image("finket_background.png")

# Función para aplicar fondo a cada sección
def aplicar_fondo(imagen_base64):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{imagen_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        footer {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# Menú lateral
with st.sidebar:
    st.image("finket_logo.png", width=120)
    menu = st.radio("Selecciona una sección:", [
        "🏠 Inicio",
        "💰 Simulador",
        "📚 Aprende sobre El Ahorro",
        "🌐 Enlaces útiles",
        "📰 Noticias en tiempo real",
        "📖 Nuestra historia"
    ])

# Aplicar fondo según sección
if menu == "🏠 Inicio":
    aplicar_fondo(fondo_inicio)
else:
    aplicar_fondo(fondo_general)

# 🏠 INICIO
if menu == "🏠 Inicio":
    st.markdown("<h1 style='color:black; text-align:center;'>¡Welcome to!</h1>", unsafe_allow_html=True)

# 💰 SIMULADOR
elif menu == "💰 Simulador":
    st.markdown("""
        <style>
        h2, h3, label, p, .stMarkdown {
            color: black !important;
            font-size: 20px !important;
        }
        .stNumberInput > div > input, .stSlider, .stSelectbox {
            font-size: 18px !important;
        }
        .stMetric {
            background-color: rgba(40,180,99,0.2);
            padding: 0.5rem;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2>💰 Simulador de Ahorro e Inversión</h2>", unsafe_allow_html=True)
    st.markdown("Define tu meta y descubre cuál estrategia te conviene más 📊")

    meta = st.number_input("🎯 Meta de ahorro ($)", min_value=0)
    plazo = st.slider("📅 ¿En cuántos meses deseas lograrla?", 1, 60)
    inicial = st.number_input("💵 Ahorro actual ($)", min_value=0)
    mensual = st.number_input("💰 Aporte mensual ($)", min_value=0)
    estrategia = st.selectbox("📈 Estrategia:", ["CETES (Renta Fija)", "Fondo Indexado (Renta Variable)"])

    tasa = 0.10 if estrategia == "CETES (Renta Fija)" else 0.12
    inflacion = 0.045
    acumulado = inicial
    valores = []

    for _ in range(plazo):
        acumulado = (acumulado + mensual) * (1 + tasa / 12)
        valores.append(acumulado)

    valor_real = acumulado / ((1 + inflacion) ** (plazo / 12))

    col1, col2 = st.columns(2)
    col1.metric("💼 Ahorro Final Estimado", f"${acumulado:,.2f}")
    col2.metric("📉 Valor Ajustado por Inflación", f"${valor_real:,.2f}")

    if valor_real >= meta:
        st.success("✅ ¡Meta alcanzada con esta estrategia!")
    else:
        st.warning("⚠️ Ajusta tu plazo o aportaciones para alcanzar la meta.")

    st.markdown("### 📊 Evolución del Ahorro")
    plt.figure(figsize=(10, 4))
    plt.plot(valores, color="#28B463", linewidth=2)
    plt.axhline(meta, color="red", linestyle="--", label="Meta")
    plt.xlabel("Meses")
    plt.ylabel("Monto acumulado ($)")
    plt.title("Proyección del ahorro")
    plt.legend()
    st.pyplot(plt)
elif menu == "🌐 Enlaces útiles":
    st.markdown("""
        <style>
        .links-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .link-card {
            background-color: #2E86C1;
            color: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            font-size: 16px;
            font-weight: 500;
            line-height: 1.4;
        }
        .link-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .link-desc {
            font-size: 14px;
            margin-bottom: 12px;
        }
        .link-button a {
            background-color: white;
            color: #2E86C1;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:black;'>🌐 Plataformas útiles para tu dinero</h2>", unsafe_allow_html=True)

    st.markdown('<div class="links-grid">', unsafe_allow_html=True)

    plataformas = [
        {
            "nombre": "CETESdirecto",
            "descripcion": "Invierte desde $100 en deuda del gobierno. Seguro, fácil y directo.",
            "url": "https://www.cetesdirecto.com"
        },
        {
            "nombre": "GBM+",
            "descripcion": "Invierte en fondos y acciones desde una app. Accesible para todos.",
            "url": "https://www.gbm.com"
        },
        {
            "nombre": "Banxico Edu",
            "descripcion": "Material educativo gratuito sobre inflación, ahorro y banca central.",
            "url": "https://www.banxico.org.mx/educacion-financiera/"
        },
        {
            "nombre": "Bursanet by Actinver",
            "descripcion": "Invierte en bolsa, cursos y portafolios. Plataforma para empezar en la bolsa.",
            "url": "https://www.actinver.com/web/actinver/bursanet"
        },
        {
            "nombre": "Finanzas para todos (CONDUSEF)",
            "descripcion": "Portal educativo oficial para el consumidor financiero en México.",
            "url": "https://www.gob.mx/condusef/acciones-y-programas/educacion-financiera"
        }
    ]

    for plataforma in plataformas:
        st.markdown(f"""
            <div class="link-card">
                <div class="link-title">{plataforma['nombre']}</div>
                <div class="link-desc">{plataforma['descripcion']}</div>
                <div class="link-button"><a href="{plataforma['url']}" target="_blank">Ir al sitio</a></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
elif menu == "📚 Aprende sobre El Ahorro":
    st.markdown("""
        <style>
        .tips-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .tip-card {
            background-color: #2E86C1;
            color: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            font-size: 16px;
            font-weight: 500;
            line-height: 1.4;
        }
        .tip-title {
            font-size: 17px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:black;'>💡 Tips Financieros Enfocados en el Ahorro</h2>", unsafe_allow_html=True)

    tips = [
        "Haz un presupuesto mensual realista y ajústalo cada mes.",
        "Automatiza tu ahorro para que sea lo primero que hagas al recibir tu ingreso.",
        "Establece metas de ahorro claras: corto, mediano y largo plazo.",
        "Sigue el reto de las 52 semanas para ahorrar incrementalmente.",
        "Ahorra tus ingresos extra: bonos, propinas o regalos.",
        "Crea un fondo de emergencia antes de empezar a invertir.",
        "Lleva registro de todos tus gastos, por pequeños que sean.",
        "Evita el 'gasto hormiga': cafés, snacks y apps sin uso.",
        "Usa efectivo en lugar de tarjeta para mantener el control.",
        "Paga tus deudas con intereses altos antes de ahorrar a largo plazo.",
        "Utiliza sobres físicos o digitales para dividir tu dinero en categorías.",
        "Aprovecha promociones solo si son parte de tu presupuesto.",
        "No compres algo en descuento si no lo necesitabas.",
        "Cancela suscripciones que no uses o no recuerdes haber contratado.",
        "Compra por mayoreo si es algo que usas frecuentemente.",
        "Evita usar tus ahorros para gastos emocionales.",
        "Establece una regla personal como: si cuesta más de $500, espera 48h.",
        "Compara precios entre tiendas físicas y en línea antes de comprar.",
        "Evita comprar a meses sin intereses si no lo necesitas.",
        "Aprovecha apps gratuitas para llevar tu control financiero.",
        "Ahorra en conjunto con amigos o familiares para metas compartidas.",
        "Antes de gastar, pregúntate: ¿esto me acerca o aleja de mi meta?",
        "Recuerda: ahorrar no es privarte, es prepararte.",
        "Invierte tu ahorro en productos de bajo riesgo si apenas comienzas.",
        "Celebra tus logros de ahorro sin gastar más: reconócete con algo simbólico."
    ]

    st.markdown('<div class="tips-grid">', unsafe_allow_html=True)

    for i, tip in enumerate(tips):
        st.markdown(f"""
            <div class="tip-card">
                <div class="tip-title">Tip #{i+1}</div>
                {tip}
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
elif menu == "📖 Nuestra historia":
    st.markdown("""
        <style>
        .historia-card {
            background-color: #2E86C1;
            color: black;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
            font-size: 18px;
            line-height: 1.6;
        }
        .historia-title {
            font-size: 28px;
            font-weight: bold;
            color: black;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="historia-card">', unsafe_allow_html=True)
    st.markdown('<div class="historia-title">📖 Nuestra Historia</div>', unsafe_allow_html=True)

    st.markdown("""
    Finket nació del corazón y la mente de una estudiante de Dirección Financiera durante el **Hackathon Fintech 2025**.  
    Su reto era claro: encontrar una solución accesible para enseñar a las personas a **ahorrar con intención**.

    En un mundo donde el gasto impulsivo y la desinformación financiera son comunes, ella imaginó una app amigable y educativa, 
    capaz de simular metas reales, calcular estrategias y **formar el hábito del ahorro desde la acción**.

    Así fue como surgió **Finket**: una herramienta que no solo enseña a ahorrar, sino que transforma la manera en que pensamos 
    sobre el dinero.

    👉 Porque **educar para el ahorro es sembrar libertad financiera** 💚
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📰 Noticias en tiempo real":
    st.markdown("""
        <style>
        .noticias-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .noticia-card {
            background-color: #2E86C1;
            color: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            font-size: 16px;
            font-weight: 500;
            line-height: 1.4;
        }
        .noticia-titulo {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .noticia-desc {
            font-size: 14px;
            margin-bottom: 10px;
        }
        .noticia-link a {
            background-color: white;
            color: #2E86C1;
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:black;'>📰 Portales Confiables de Noticias Financieras</h2>", unsafe_allow_html=True)

    portales = [
        {
            "titulo": "El Economista (México)",
            "descripcion": "Actualidad financiera, mercados y política económica mexicana.",
            "url": "https://www.eleconomista.com.mx/"
        },
        {
            "titulo": "Forbes México",
            "descripcion": "Negocios, startups, inversiones y liderazgo económico.",
            "url": "https://www.forbes.com.mx/"
        },
        {
            "titulo": "BBC Business",
            "descripcion": "Noticias internacionales de negocios, comercio y finanzas.",
            "url": "https://www.bbc.com/news/business"
        },
        {
            "titulo": "CONDUSEF Noticias",
            "descripcion": "Comunicados y alertas para el consumidor financiero en México.",
            "url": "https://www.gob.mx/condusef/acciones-y-programas/boletines-de-prensa"
        },
        {
            "titulo": "Bloomberg",
            "descripcion": "Información en tiempo real sobre mercados globales.",
            "url": "https://www.bloomberg.com/"
        }
    ]

    st.markdown('<div class="noticias-grid">', unsafe_allow_html=True)

    for portal in portales:
        st.markdown(f"""
            <div class="noticia-card">
                <div class="noticia-titulo">{portal['titulo']}</div>
                <div class="noticia-desc">{portal['descripcion']}</div>
                <div class="noticia-link"><a href="{portal['url']}" target="_blank">Visitar</a></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
