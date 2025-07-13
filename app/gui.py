"""Este módulo proporciona una interfaz gráfica de usuario (GUI) para analizar el sentimiento en datos de texto utilizando la herramienta de análisis de sentimientos VADER de la biblioteca NLTK.

Permite a los usuarios:

    -Seleccionar un archivo CSV.

    -Analizar el sentimiento del texto contenido en dicho archivo.

    -Exportar los resultados a formatos CSV o PDF.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import csv
import os
from threading import Thread
from queue import Queue, Empty
from analyzer import analyze_sentiment
import logging
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from collections import Counter

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Sentimientos")
        self.file_path = ""
        self.results = []
        self.queue = Queue()

        self.last_path_file = "last_path.txt"
        self.load_last_path()

        self.btn_select = tk.Button(root, text="Seleccionar archivo CSV", command=self.select_file)
        self.btn_select.pack(pady=10)

        self.btn_run = tk.Button(root, text="Analizar sentimientos", command=self.run_analysis)
        self.btn_run.pack(pady=5)

        self.btn_clear = tk.Button(root, text="Limpiar resultados", command=self.clear_results)
        self.btn_clear.pack(pady=5)

        self.btn_export_csv = tk.Button(root, text="Exportar resultados CSV", command=self.export_results_csv)
        self.btn_export_csv.pack(pady=5)

        self.btn_export_pdf = tk.Button(root, text="Exportar resultados PDF", command=self.export_results_pdf)
        self.btn_export_pdf.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_text.pack(pady=10)

        self.progress = tk.DoubleVar()
        import tkinter.ttk as ttk
        self.progress_bar = ttk.Progressbar(root, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill='x', padx=10, pady=5)

        self.root.after(100, self.process_queue)

    def load_last_path(self):
        """Carga la última ruta de archivo seleccionada desde un archivo de texto."""
        if os.path.exists(self.last_path_file):
            with open(self.last_path_file, 'r', encoding='utf-8') as f:
                self.file_path = f.read().strip()

    def save_last_path(self):
        """Guarda la última ruta de archivo seleccionada."""
        with open(self.last_path_file, 'w', encoding='utf-8') as f:
            f.write(self.file_path)

    def select_file(self):
        """Selecciona un archivo CSV y guarda la ruta."""
        path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if path:
            self.file_path = path
            self.save_last_path()
            messagebox.showinfo("Archivo seleccionado", f"Archivo: {self.file_path}")
            logger.info(f"Archivo seleccionado: {self.file_path}")

    def run_analysis(self):
        """Inicia el análisis de sentimientos en un hilo separado."""
        if not self.file_path:
            messagebox.showwarning("Error", "Primero seleccioná un archivo CSV.")
            return

        self.clear_results()

        self.btn_run.config(state=tk.DISABLED)
        self.btn_select.config(state=tk.DISABLED)
        self.btn_export_csv.config(state=tk.DISABLED)
        self.btn_export_pdf.config(state=tk.DISABLED)

        thread = Thread(target=self.analyze_in_thread)
        thread.start()

    def analyze_in_thread(self):
        """Ejecuta el análisis de sentimientos en un hilo separado."""
        try:
            with open(self.file_path, encoding='utf-8') as file:
                reader = list(csv.DictReader(file))
                total = len(reader)

                for i, row in enumerate(reader, 1):
                    text = row.get('review', '')
                    sentiment = analyze_sentiment(text)
                    self.results.append({'review': text, 'sentimiento': sentiment})
                    self.queue.put(f"Texto: {text}\\nSentimiento: {sentiment}\\n{'-'*50}\\n")
                    self.queue.put(('progress', i * 100 / total))
                    logger.info(f"Analizado texto {i}/{total}: '{text[:30]}...' - Sentimiento: {sentiment}")

            self.queue.put('done')
            logger.info("Análisis completado exitosamente.")

        except Exception as e:
            self.queue.put(('error', str(e)))
            logger.error(f"Error durante análisis: {e}")

    def process_queue(self):
        """Procesa los mensajes en la cola."""
        try:
            while True:
                msg = self.queue.get_nowait()
                if isinstance(msg, tuple):
                    if msg[0] == 'progress':
                        self.progress.set(msg[1])
                    elif msg[0] == 'error':
                        messagebox.showerror("Error", msg[1])
                        self.btn_run.config(state=tk.NORMAL)
                        self.btn_select.config(state=tk.NORMAL)
                        self.btn_export_csv.config(state=tk.NORMAL)
                        self.btn_export_pdf.config(state=tk.NORMAL)
                elif msg == 'done':
                    self.btn_run.config(state=tk.NORMAL)
                    self.btn_select.config(state=tk.NORMAL)
                    self.btn_export_csv.config(state=tk.NORMAL)
                    self.btn_export_pdf.config(state=tk.NORMAL)
                    self.progress.set(0)
                else:
                    self.output_text.insert(tk.END, msg)
                    self.output_text.see(tk.END)

        except Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

    def export_results_csv(self):
        """Exporta los resultados a un archivo CSV."""
        if not self.results:
            messagebox.showwarning("Sin datos", "Primero analizá un archivo.")
            logger.warning("Intento de exportar CSV sin resultados.")
            return

        try:
            os.makedirs("resultados", exist_ok=True)
            export_path = "resultados/resultados.csv"

            with open(export_path, mode='w', newline='', encoding='utf-8') as f:
                fieldnames = ['review', 'sentimiento']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)

            messagebox.showinfo("Exportación exitosa", f"Archivo guardado en:\\n{export_path}")
            logger.info(f"Archivo CSV exportado: {export_path}")

        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
            logger.error(f"Error exportando CSV: {e}")

    def export_results_pdf(self):
        """Exporta los resultados a un archivo PDF con gráficos."""

        if not self.results:
            messagebox.showwarning("Sin datos", "Primero analizá un archivo.")
            logger.warning("Intento de exportar PDF sin resultados.")
            return

        try:
            os.makedirs("resultados", exist_ok=True)
            pdf_path = "resultados/resultados.pdf"

            counts = Counter(r['sentimiento'] for r in self.results)
            total = sum(counts.values())
            most_common = counts.most_common(1)[0]

            labels = list(counts.keys())
            sizes = list(counts.values())

            # Gráfico torta
            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=["#8FD9F7","#F38D80","#FFDEB8"])
            plt.title('Distribución de Sentimientos')
            pie_path = "resultados/pie_chart.png"
            plt.savefig(pie_path)
            plt.close()

            # Gráfico barras
            plt.figure(figsize=(6, 4))
            plt.bar(labels, sizes, color=['#8FD9F7','#F38D80','#FFDEB8'])
            plt.title('Cantidad por Sentimiento')
            plt.ylabel('Cantidad')
            plt.xlabel('Sentimiento')
            bar_path = "resultados/bar_chart.png"
            plt.savefig(bar_path)
            plt.close()

            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Resumen de Análisis de Sentimientos")

            c.setFont("Helvetica", 12)
            c.drawString(50, height - 90, f"Total de textos analizados: {total}")
            c.drawString(50, height - 110, f"Sentimiento más frecuente: {most_common[0]} ({most_common[1]} textos)")

            c.drawString(50, height - 140, "Gráfico de torta:")
            c.drawImage(ImageReader(pie_path), 50, height - 380, width=250, height=250)

            c.drawString(320, height - 140, "Gráfico de barras:")
            c.drawImage(ImageReader(bar_path), 320, height - 380, width=250, height=250)

            c.showPage()
            c.save()

            messagebox.showinfo("Exportación PDF exitosa", f"Archivo guardado en:\n{pdf_path}")
            logger.info(f"Archivo PDF exportado: {pdf_path}")

        except Exception as e:
            messagebox.showerror("Error al exportar PDF", str(e))
            logger.error(f"Error exportando PDF: {e}")

    def clear_results(self):
        self.output_text.delete(1.0, tk.END)
        self.results.clear()
        self.progress.set(0)
        logger.info("Resultados limpiados.")

def launch_app():
    logger.info("Lanzando la aplicación de análisis de sentimientos.")
    root = tk.Tk()
    app = SentimentApp(root)
    root.mainloop()

