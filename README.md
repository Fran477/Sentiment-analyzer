
# 🧠 Analizador de Sentimientos con VADER y Tkinter

Esta aplicación permite analizar el sentimiento (positivo, negativo o neutral) de textos contenidos en un archivo `.csv`, utilizando la herramienta **VADER** de `nltk`. Proporciona una **interfaz gráfica (GUI)** amigable desarrollada con `Tkinter`.

Permite:
- Cargar archivos CSV con reseñas.
- Analizar sentimientos línea por línea.
- Exportar los resultados en **CSV** y **PDF**.
- Ver estadísticas y gráficos.
- Barra de progreso, logs y limpieza de resultados.

---

## ✅ Requisitos

- Python 3.8 o superior
- Tkinter (incluido por defecto con Python)
- Librerías adicionales:
  - `nltk`
  - `matplotlib`
  - `reportlab`

---

## ⚙️ Instalación

1. Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

- En **Windows**:
```bash
.venv\Scripts\activate
```

- En **Linux/macOS**:
```bash
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

Desde la terminal, ejecutá:

```bash
python -m app.main
```

---

## 🖱️ Pasos en la interfaz

1. Hacé clic en **"Seleccionar archivo CSV"** y elegí un archivo que contenga una columna `review`.
2. Presioná **"Analizar sentimientos"** para procesar las reseñas.
3. Podés:
   - Exportar los resultados a **CSV** (`resultados/resultados.csv`)
   - Exportar un **PDF** con:
     - Gráfico de barras
     - Gráfico de torta
     - Estadísticas clave (total, más frecuente, etc.)
4. Usá **"Limpiar resultados"** para vaciar la pantalla y empezar de nuevo.

---

## 📁 Estructura recomendada del proyecto

```
sentiment-analyzer-vader/
├── app/
│   ├── analyzer.py
│   ├── gui.py
│   └── main.py
├── .venv/
├── resultados/
├── requirements.txt
└── README.md
```

---

## 📝 Notas

- El programa guarda la **última ruta** usada automáticamente.
- Se genera un archivo de log (`app.log`) con todos los análisis y errores.
- Asegurate de que el archivo CSV tenga una columna llamada `review`.

---

## ✨ Inspirado por el Zen de Python

> Simple es mejor que complejo.  
> Lo obvio es mejor que lo implícito.  
> Si la implementación es difícil de explicar, es una mala idea.

---
