# Dinámica de la Inflación Impulsada por el Fiscal
### Aplicación Interactiva de Pensamiento Crítico y Aprendizaje Activo
**Universidad Internacional de las Américas (U.I.A.)**  
*Carrera de Economía | Primer Ingreso | Sesión Sincrónica & Mastery Flip*

---

## 📌 Descripción General del Proyecto y Propósito

Este proyecto consiste en una aplicación web interactiva desarrollada en **Streamlit** concebida para la enseñanza de la macroeconomía moderna y el fortalecimiento del **pensamiento crítico**. La herramienta traslada marcos pedagógicos rigurosos a un entorno de simulación digital con el fin de superar el aprendizaje pasivo, la memorización ciega de fórmulas y la repetición no razonada de modelos económicos.

El núcleo temático aborda el dilema de la **dinámica de la inflación impulsada por el gasto fiscal** frente a la inflación generada por el crédito bancario comercial, contrastando los regímenes macroeconómicos históricos de las décadas de **1940**, **1970** y **2020**, con base en el marco analítico de **Lyn Alden** (*Fiscal-Driven Inflation*, mayo de 2021).

### Marco Pedagógico Integrado
1. **Los 4 Principios del Diseño Didáctico de M. David Merrill:**
   - **Activación:** Conectar con modelos mentales intuitivos previos y derribar esquemas conceptuales erróneos.
   - **Demostración:** Hacer visible lo invisible a través de paneles visuales y dinámica causal interactiva (*how-to* / *what-happens*).
   - **Aplicación:** Resolución y toma de decisiones en un simulador intrínseco de política monetaria y dominancia fiscal.
   - **Integración:** Transferencia dialógica, defensa oral pública y coevaluación entre pares.
2. **El Enfoque Mastery Flip (Jon Bergmann, 2026):**
   - Transición del aula tradicional hacia la comprobación de maestría mediante argumentación auténtica, defensas orales sincrónicas y diálogo evaluativo.
3. **La Técnica de Feynman de Aprendizaje Profundo:**
   - Desafío de formular conceptos complejos de banca central y balances fiscales en analogías cotidianas y sin jerga técnica vacía.

---

## ✨ Características Principales Implementadas

- **🏛️ Identidad Visual Institucional UIA:** Integración del logotipo oficial de la universidad, paleta de colores académica y barra lateral de contexto didáctico.
- **👤 Registro y Trazabilidad de Sesión:** Captura del nombre del estudiante y persistencia dinámica acumulativa de todo el recorrido mediante `st.session_state`.
- **🧭 Módulo 1 (Activación):**
  - Selector histórico intuitivo (décadas de 1940s, 1970s y 2020s).
  - Ejercicio Feynman: Distinción entre dinero bancario (deuda privada) e inyección fiscal (déficit público) sin tecnicismos.
- **📊 Módulo 2 (Demostración Visual FRED):**
  - Gráficos interactivos de alta definición con **Plotly** (M2 vs. Déficit Fiscal/PIB y Ratio Deuda/PIB 1935–2025).
  - Marcadores interactivos para los picos bélicos (1940s), de choque petrolero (1970s) y de pandemia (2020s).
  - Ejercicio Feynman: Grabación de audio simulada explicando la monetización del déficit mediante una metáfora de la vida cotidiana.
- **🎛️ Módulo 3 (Aplicación y Simulación Causal):**
  - Simulador paramétrico con palancas de Deuda/PIB (30% - 160%), Tasas de la Fed (0% - 15%) y Paquetes de Estímulo Fiscal.
  - Modelado intrínseco de la **Trampa de Dominancia Fiscal**, costo financiero del servicio de la deuda y regímenes de **represión financiera** (tasas reales negativas).
  - Ejercicio Feynman: Redacción de una carta explicativa para un niño de 12 años / inversionista novato.
- **🗣️ Módulo 4 (Integración y Mastery Flip):**
  - Redacción del argumento central para la defensa oral sincrónica.
  - Rúbrica de coevaluación digital crítica de argumentos entre pares.
  - Ejercicio Feynman Oral: Síntesis de la tesis central de Lyn Alden en menos de 2 minutos sin jerga.
- **🤖 Motor de Feedback Formativo Inteligente:**
  - Evaluación heurística del razonamiento del estudiante en cada fase sin revelar respuestas predeterminadas.
- **📥 Certificación y Exportación Consolidada:**
  - Panel de calificaciones desglosadas y promedio general.
  - Generador y botón de descarga con un solo clic del reporte integral de la sesión en formato Markdown (`.md`).

---

## 🛠️ Requisitos Técnicos

- **Lenguaje:** Python 3.10 o superior (compatible con Python 3.11, 3.12 y 3.13).
- **Entorno Recomendado:** Virtualenv (`venv` o `conda`).
- **Librerías Clave Requeridas:**
  - `streamlit>=1.35.0`
  - `plotly>=5.20.0`
  - `pandas>=2.0.0`
  - `numpy>=1.24.0`
  - `pypdf>=4.0.0`
  - `pillow>=10.0.0`

*(Todas las dependencias exactas se encuentran registradas en el archivo `requirements.txt`).*

---

## 🚀 Instrucciones de Instalación Paso a Paso

Sigue estos pasos en tu terminal (PowerShell, Bash o CMD) para clonar y ejecutar el entorno en tu máquina local:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/randallnunezsancho-netizen/S4OBN-2.git
cd S4OBN-2
```

### 2. Crear y Activar el Entorno Virtual

- **En Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Iniciar la Aplicación en Streamlit
```bash
streamlit run app.py
```

La plataforma se abrirá de inmediato en tu navegador predeterminado en la dirección local:  
👉 **`http://localhost:8501`**

---

## 📖 Guía de Uso con Ejemplos Básicos

1. **Paso 1: Identificación:**  
   Ingresa tu nombre y apellidos en el menú lateral izquierdo. Esto habilitará la barra de progreso y asociará tus respuestas al certificado de entrega final.
2. **Paso 2: Navegación por Fases (Pestañas Superiores):**  
   - Ve a **1️⃣ Fase de Activación**: Explora cómo influyen los modelos mentales preconcebidos y responde el ejercicio Feynman sin usar términos complejos.
   - Ve a **2️⃣ Fase de Demostración**: Haz *hover* en los picos de 1940 y 2020 en el gráfico FRED interactivo. Observa cómo el déficit impulsó a M2 sin necesidad de intermediación crediticia.
   - Ve a **3️⃣ Fase de Aplicación**: En el simulador, incrementa la deuda a **125%** y eleva la tasa de interés al **8%**. Observa cómo el indicador alerta sobre el costo insostenible de intereses del Estado.
   - Ve a **4️⃣ Fase de Integración**: Prepárate para el Mastery Flip evaluando la afirmación del compañero y resumiendo la tesis central de Lyn Alden.
3. **Paso 3: Exportación del Informe:**  
   En la pestaña **📑 Resumen y Certificación**, haz clic en el botón verde **"📄 Descargar Reporte Consolidado (.md)"** para guardar tu expediente completo de evaluación.

---

## 📂 Estructura del Proyecto

```text
S4OBN-2/
│
├── app.py                                                # Aplicación interactiva principal en Streamlit
├── requirements.txt                                      # Especificación completa de dependencias de Python
├── README.md                                             # Documentación técnica, pedagógica y funcional
├── Especificacion de requisitos.md                      # Especificación pedagógica y requerimientos didácticos
├── Logo-solo- UIA.png                                   # Logotipo institucional oficial de la UIA
│
├── 2021 05 - Inflación impulsada por el fiscal.pdf       # Paper de investigación macroeconómica de Lyn Alden
├── MasteryFlip-A_Guide_to_the_Future_of_Educcation.pdf   # Guía del modelo Mastery Flip por Jon Bergmann
├── substack.com-Los 4 principios del diseño didáctico.pdf# Documento sobre los 4 principios de David Merrill
│
└── venv/                                                 # Entorno virtual de Python (ignorado en commits)
```

---

## 🧠 Interpretación de Resultados de Manera Pedagógica

| Situación Económica Simulada | Mecanismo Causal Subyacente | Lección Pedagógica Central |
| :--- | :--- | :--- |
| **Inflación por Bancos (1970s)** | Familias y empresas toman créditos; la deuda privada crece rápidamente con baja deuda pública inicial (~30% del PIB). | La Reserva Federal puede subir las tasas fuertemente (Volcker) sin quebrar el presupuesto del Estado. |
| **Inflación Fiscal (1940s y 2020s)** | El Tesoro realiza transferencias directas y compras masivas financiadas con emisión monetaria de la Fed. | Subir drásticamente las tasas de interés es inviable cuando la deuda supera el 100% del PIB, forzando la **represión financiera**. |
| **"Inflación Transitoria"** | Desaceleración en el *porcentaje anual* de subida una vez que se estabiliza la cadena de suministros. | **No significa que los precios bajen:** el nivel de precios alcanzado permanece permanentemente más alto debido a la nueva masa de dinero circulante. |

---

## ⚖️ Licencia y Nota Educativa

> **Aviso de Fines Pedagógicos:**  
> Este software y sus materiales asociados han sido diseñados y desarrollados con **fines estrictamente educativos y formativos** para los estudiantes y docentes de la **Universidad Internacional de las Américas (U.I.A.)**. Los modelos matemáticos y gráficos son representaciones didácticas orientadas a ilustrar dinámicas macroeconómicas y no constituyen asesoría de inversión, pronóstico financiero oficial ni consultoría profesional.

Distribuido bajo la licencia educativa institucional de la **Universidad Internacional de las Américas**.  
*Desarrollado para el fortalecimiento del pensamiento crítico en las ciencias económicas.*
