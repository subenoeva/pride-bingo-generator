import random
import pandas as pd
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import textwrap
import sys
import os
import argparse

class GeneradorBingoMusicalPride:
    def __init__(self, ruta_canciones, tamaño_fuente=7, cartones_por_pagina=2):
        self.canciones = self.cargar_canciones(ruta_canciones)
        self.tamaño_fuente = tamaño_fuente
        self.cartones_por_pagina = cartones_por_pagina
        self.colores_pride = self.obtener_colores_pride()
        self.emojis_pride = ['🏳️‍🌈', '🏳️‍⚧️', '💖', '🌈', '✨', '🎵', '🎶', '💃', '🕺', '🔥', '💫', '⭐']
        self.configurar_fuentes()
        self.verificar_canciones()
    
    def configurar_fuentes(self):
        """Configura fuentes que soporten caracteres especiales"""
        try:
            # Intentar registrar fuentes con soporte UTF-8
            pdfmetrics.registerFont(TTFont('DejaVu-Sans', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVu-Sans-Bold', 'DejaVuSans-Bold.ttf'))
            self.fuente_normal = 'DejaVu-Sans'
            self.fuente_bold = 'DejaVu-Sans-Bold'
            print("✅ Fuentes DejaVu cargadas correctamente")
        except:
            try:
                # Fuentes alternativas más comunes
                pdfmetrics.registerFont(TTFont('Arial-Unicode', 'arial.ttf'))
                self.fuente_normal = 'Arial-Unicode'
                self.fuente_bold = 'Arial-Unicode'
                print("✅ Fuente Arial cargada correctamente")
            except:
                try:
                    # Intentar con fuentes del sistema Windows
                    pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
                    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
                    self.fuente_normal = 'Calibri'
                    self.fuente_bold = 'Calibri-Bold'
                    print("✅ Fuente Calibri cargada correctamente")
                except:
                    # Usar fuentes por defecto de reportlab
                    self.fuente_normal = 'Helvetica'
                    self.fuente_bold = 'Helvetica-Bold'
                    print("⚠️ Usando fuentes por defecto (Helvetica)")
                    print("💡 Para mejor soporte de caracteres especiales, instala:")
                    print("   - DejaVu Sans (recomendado)")
                    print("   - O copia arial.ttf al directorio del script")
    
    def obtener_colores_pride(self):
        """Define los colores del arcoíris para usar en el diseño"""
        return {
            'rojo': colors.Color(0.91, 0.26, 0.21),      # #E8443A
            'naranja': colors.Color(1.0, 0.65, 0.0),     # #FFA500
            'amarillo': colors.Color(1.0, 0.84, 0.0),    # #FFD700
            'verde': colors.Color(0.0, 0.8, 0.4),        # #00CC66
            'azul': colors.Color(0.0, 0.49, 0.8),        # #007DCC
            'morado': colors.Color(0.55, 0.27, 0.8),     # #8B45CC
            'rosa': colors.Color(0.98, 0.44, 0.75),      # #FA70BE
            'celeste': colors.Color(0.5, 0.8, 1.0),      # #80CCFF
            'blanco': colors.white,
            'negro': colors.black
        }
    
    def cargar_canciones(self, ruta):
        """Carga las canciones desde el archivo de texto con encoding UTF-8"""
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(ruta, 'r', encoding=encoding) as f:
                        canciones = [line.strip() for line in f if line.strip()]
                    
                    # Verificar que se cargaron correctamente probando caracteres especiales
                    test_text = ''.join(canciones)
                    if any(char in test_text for char in 'áéíóúñÁÉÍÓÚÑ'):
                        print(f"✅ Archivo cargado con encoding: {encoding}")
                    else:
                        print(f"✅ Archivo cargado con encoding: {encoding} (sin caracteres especiales detectados)")
                    
                    return canciones
                except UnicodeDecodeError:
                    continue
            
            # Si ningún encoding funciona, cargar con errors='replace'
            with open(ruta, 'r', encoding='utf-8', errors='replace') as f:
                canciones = [line.strip() for line in f if line.strip()]
            print("⚠️ Archivo cargado con reemplazo de caracteres problemáticos")
            return canciones
            
        except FileNotFoundError:
            raise FileNotFoundError(f"No se pudo encontrar el archivo: {ruta}")
        except Exception as e:
            raise Exception(f"Error al cargar canciones: {e}")
    
    def limpiar_texto_para_pdf(self, texto):
        """Limpia el texto para evitar problemas con caracteres especiales en PDF"""
        import re
        
        # Reemplazar caracteres problemáticos comunes
        replacements = {
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '…': '...',
            '–': '-',
            '—': '-',
            '´': "'",
            '`': "'",
            '¨': '"',
            '°': 'º',
            '™': '(TM)',
            '®': '(R)',
            '©': '(C)',
            '€': 'EUR',
            '£': 'GBP',
            '¥': 'YEN',
            '§': 'S',
            '¶': 'P',
            '†': '+',
            '‡': '++',
            '•': '*',
            '‰': '%',
            '‹': '<',
            '›': '>',
            '«': '<<',
            '»': '>>',
            '¡': '!',
            '¿': '?',
        }
        
        # Aplicar reemplazos
        for old, new in replacements.items():
            texto = texto.replace(old, new)
        
        # Remover caracteres de control y caracteres no imprimibles
        texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', texto)
        
        # Convertir caracteres no-ASCII problemáticos a ASCII equivalentes
        texto = texto.encode('ascii', 'ignore').decode('ascii')
        
        # Si el texto queda muy corto o vacío después de la limpieza, usar versión más permisiva
        if len(texto.strip()) < 3:
            # Intentar con limpieza menos agresiva
            texto_original = texto
            for old, new in replacements.items():
                texto_original = texto_original.replace(old, new)
            # Solo remover caracteres de control, mantener acentos
            texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', texto_original)
        
        return texto.strip()
    
    def formatear_texto_cancion(self, indice, cancion):
        """Formatea el texto de la canción con índice en negrita y mejor presentación"""
        cancion_limpia = self.limpiar_texto_para_pdf(cancion)
        
        # Crear el HTML para formateo avanzado
        indice_html = f"<b>#{indice:03d}</b>"
        
        # Formatear el nombre de la canción
        # Capitalizar correctamente y mejorar la presentación
        cancion_formateada = cancion_limpia.title()
        
        # Crear párrafo con HTML formatting
        texto_html = f"{indice_html}<br/><font size='{self.tamaño_fuente-1}'>{cancion_formateada}</font>"
        
        return texto_html
    
    def crear_parrafo_cancion(self, indice, cancion):
        """Crea un párrafo con formato mejorado para la canción"""
        # Estilo personalizado para las canciones
        estilo_cancion = ParagraphStyle(
            'CancionStyle',
            fontName=self.fuente_normal,
            fontSize=self.tamaño_fuente,
            textColor=colors.black,
            alignment=TA_CENTER,
            leading=self.tamaño_fuente + 1,
            leftIndent=2,
            rightIndent=2,
            spaceBefore=1,
            spaceAfter=1
        )
        
        texto_html = self.formatear_texto_cancion(indice, cancion)
        return Paragraph(texto_html, estilo_cancion)
    
    def verificar_canciones(self):
        """Verifica que hay suficientes canciones para generar cartones únicos"""
        if len(self.canciones) < 24:
            raise ValueError(f"Se necesitan al menos 24 canciones. Solo hay {len(self.canciones)} disponibles.")
        
        print(f"🏳️‍🌈 Se cargaron {len(self.canciones)} canciones")
        print(f"✨ Se pueden generar aproximadamente {self.calcular_max_cartones()} cartones únicos")
        
        # Mostrar algunas canciones como ejemplo para verificar encoding
        print(f"📝 Ejemplo de canciones cargadas:")
        for i, cancion in enumerate(self.canciones[:3]):
            print(f"   {i+1}. {cancion}")
        if len(self.canciones) > 3:
            print(f"   ... y {len(self.canciones) - 3} más")
    
    def calcular_max_cartones(self):
        """Calcula aproximadamente cuántos cartones únicos se pueden generar"""
        from math import comb
        return min(1000, comb(len(self.canciones), 24) // 1000)
    
    def generar_carton(self, numero_carton):
        """Genera un cartón individual de 5x5 con espacio libre en el centro"""
        if len(self.canciones) < 24:
            raise ValueError("Necesitas al menos 24 canciones diferentes")
        
        # Crear lista de tuplas con índice y canción
        canciones_con_indice = [(i + 1, cancion) for i, cancion in enumerate(self.canciones)]
        
        # Seleccionar 24 canciones aleatorias con sus índices
        canciones_seleccionadas = random.sample(canciones_con_indice, 24)
        
        # Crear matriz 5x5 con espacio libre en el centro
        carton = []
        contador = 0
        
        for fila in range(5):
            fila_carton = []
            for col in range(5):
                if fila == 2 and col == 2:  # Centro del cartón
                    # Crear párrafo especial para la casilla libre
                    estilo_libre = ParagraphStyle(
                        'LibreStyle',
                        fontName=self.fuente_bold,
                        fontSize=self.tamaño_fuente + 1,
                        textColor=self.colores_pride['morado'],
                        alignment=TA_CENTER,
                        leading=self.tamaño_fuente + 2
                    )
                    fila_carton.append(Paragraph("<b>🎵 LIBRE 🎵</b>", estilo_libre))
                else:
                    # Obtener índice y canción
                    indice, cancion = canciones_seleccionadas[contador]
                    parrafo_cancion = self.crear_parrafo_cancion(indice, cancion)
                    fila_carton.append(parrafo_cancion)
                    contador += 1
            carton.append(fila_carton)
        
        return carton
    
    def obtener_color_aleatorio_pride(self):
        """Obtiene un color aleatorio de la paleta Pride"""
        colores = ['rojo', 'naranja', 'amarillo', 'verde', 'azul', 'morado', 'rosa', 'celeste']
        color_nombre = random.choice(colores)
        return self.colores_pride[color_nombre]
    
    def crear_tabla_carton(self, carton, numero_carton):
        """Crea una tabla formateada para el PDF con tema Pride (optimizada para 2 por página)"""
        # Ajustar tamaño de columnas según cartones por página
        col_width = 3.6 * cm if self.cartones_por_pagina == 2 else 3.2 * cm
        row_height = 2.0 * cm if self.cartones_por_pagina == 2 else 1.8 * cm
        
        tabla = Table(carton, colWidths=[col_width]*5, rowHeights=[row_height]*5)
        
        # Colores para cada celda (efecto arcoíris sutil)
        colores_fondo = []
        for fila in range(5):
            for col in range(5):
                if fila == 2 and col == 2:  # Casilla libre
                    colores_fondo.append(('BACKGROUND', (col, fila), (col, fila), 
                                        colors.Color(1.0, 0.84, 0.0, alpha=0.4)))  # Dorado más visible
                else:
                    # Colores alternos suaves del arcoíris
                    color_base = self.obtener_color_aleatorio_pride()
                    color_suave = colors.Color(color_base.red, color_base.green, color_base.blue, alpha=0.2)
                    colores_fondo.append(('BACKGROUND', (col, fila), (col, fila), color_suave))
        
        # Estilo base de la tabla
        estilo_base = [
            # Bordes con colores del arcoíris
            ('GRID', (0, 0), (-1, -1), 1.5, self.colores_pride['morado']),
            ('LINEWIDTH', (0, 0), (-1, -1), 1.5),
            
            # Alineación
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Espaciado optimizado para párrafos
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]
        
        # Combinar estilo base con colores de fondo
        estilo_completo = estilo_base + colores_fondo
        
        tabla.setStyle(TableStyle(estilo_completo))
        return tabla
    
    def crear_encabezado_pride_compacto(self, numero_carton):
        """Crea un encabezado muy compacto para 2 cartones por página"""
        estilos = getSampleStyleSheet()
        
        # Título muy compacto
        estilo_titulo = ParagraphStyle(
            'TituloCompacto',
            parent=estilos['Normal'],
            fontSize=12,
            textColor=self.colores_pride['morado'],
            alignment=TA_CENTER,
            spaceAfter=0.02*cm,
            fontName=self.fuente_bold
        )
        
        # Número de cartón pequeño
        estilo_numero = ParagraphStyle(
            'NumeroCompacto',
            parent=estilos['Normal'],
            fontSize=9,
            textColor=self.colores_pride['rosa'],
            alignment=TA_CENTER,
            spaceAfter=0.02*cm,
            fontName=self.fuente_bold
        )
        
        titulo = Paragraph("🏳️‍🌈 BINGO POLARI 🏳️‍⚧️", estilo_titulo)
        numero = Paragraph(f"<b>CARTÓN #{numero_carton:03d}</b>", estilo_numero)
        
        return [titulo, numero]
    
    def crear_elemento_carton_completo(self, numero_carton):
        """Crea un elemento completo (encabezado + tabla) para un cartón"""
        elementos = []
        
        # Encabezado compacto
        encabezado = self.crear_encabezado_pride_compacto(numero_carton)
        for elemento in encabezado:
            elementos.append(elemento)
        
        # Pequeño espacio entre encabezado y tabla
        elementos.append(Spacer(1, 0.1*cm))
        
        # Generar y añadir cartón
        carton = self.generar_carton(numero_carton)
        tabla = self.crear_tabla_carton(carton, numero_carton)
        elementos.append(tabla)
        
        return elementos
    
    def crear_pagina_multiple_cartones(self, numeros_cartones):
        """Crea una página con múltiples cartones según configuración"""
        elementos = []
        
        for i, num_carton in enumerate(numeros_cartones):
            elementos_carton = self.crear_elemento_carton_completo(num_carton)
            for elemento in elementos_carton:
                elementos.append(elemento)
            
            # Espacio entre cartones (excepto después del último)
            if i < len(numeros_cartones) - 1:
                elementos.append(Spacer(1, 0.4*cm))
        
        return elementos
    
    def generar_pdf(self, num_cartones, nombre_archivo="cartones_bingo_pride_mejorado.pdf"):
        """Genera el PDF con todos los cartones con tema Pride"""
        print(f"\n🏳️‍🌈 Generando {num_cartones} cartones de bingo musical Pride mejorados ({self.cartones_por_pagina} por página)...")
        
        # Crear documento PDF con márgenes optimizados
        doc = SimpleDocTemplate(
            nombre_archivo,
            pagesize=A4,
            rightMargin=0.4*cm,
            leftMargin=0.4*cm,
            topMargin=0.3*cm,
            bottomMargin=0.3*cm
        )
        
        elementos = []
        num_paginas = (num_cartones + self.cartones_por_pagina - 1) // self.cartones_por_pagina
        
        for pagina in range(num_paginas):
            # Calcular qué cartones van en esta página
            inicio = pagina * self.cartones_por_pagina + 1
            fin = min((pagina + 1) * self.cartones_por_pagina, num_cartones)
            numeros_cartones = range(inicio, fin + 1)
            
            print(f"  🌈 Generando página {pagina + 1}/{num_paginas} (cartones {inicio}-{fin})...")
            
            # Crear página con los cartones
            elementos_pagina = self.crear_pagina_multiple_cartones(numeros_cartones)
            
            for elemento in elementos_pagina:
                elementos.append(elemento)
            
            # Salto de página si no es la última
            if pagina < num_paginas - 1:
                elementos.append(PageBreak())
        
        # Construir PDF
        print("  🎨 Aplicando colores del arcoíris y formato mejorado...")
        doc.build(elementos)
        print(f"🎉 ¡Listo! Se generaron {num_cartones} cartones Pride mejorados en {num_paginas} páginas en '{nombre_archivo}'")
        
        return nombre_archivo

def parse_arguments():
    """Configura y parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Generador de Cartones de Bingo Musical con Tema Pride',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '-c', '--canciones',
        type=str,
        default='canciones.txt',
        help='Ruta al archivo de texto con las canciones'
    )
    
    parser.add_argument(
        '-n', '--num-cartones',
        type=int,
        default=100,
        help='Número de cartones a generar'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='cartones_bingo_pride.pdf',
        help='Nombre del archivo PDF de salida'
    )
    
    parser.add_argument(
        '-f', '--fuente',
        type=int,
        default=8,
        help='Tamaño de fuente para los cartones'
    )
    
    parser.add_argument(
        '-p', '--por-pagina',
        type=int,
        choices=[1, 2, 4],
        default=2,
        help='Número de cartones por página (1, 2 o 4)'
    )
    
    return parser.parse_args()

def main():
    """Función principal para ejecutar el generador con parámetros configurables"""
    try:
        args = parse_arguments()
        
        # Mostrar información de configuración
        print("🏳️‍🌈 Iniciando generador de Bingo Musical Pride MEJORADO")
        print(f"📄 Configuración:")
        print(f"  • Archivo de canciones: {args.canciones}")
        print(f"  • Cartones a generar: {args.num_cartones}")
        print(f"  • Cartones por página: {args.por_pagina}")
        print(f"  • Tamaño de fuente: {args.fuente}")
        print(f"  • Archivo de salida: {args.output}")
        
        # Crear generador con configuración personalizada
        generador = GeneradorBingoMusicalPride(
            ruta_canciones=args.canciones,
            tamaño_fuente=args.fuente,
            cartones_por_pagina=args.por_pagina
        )
        
        # Generar PDF
        archivo_generado = generador.generar_pdf(args.num_cartones, args.output)
        
        num_paginas = (args.num_cartones + args.por_pagina - 1) // args.por_pagina
        
        print(f"\n🎊 ¡Proceso completado con éxito!")
        print(f"📁 Archivo generado: {archivo_generado}")
        print(f"🏳️‍🌈 Cartones Pride generados: {args.num_cartones}")
        print(f"📄 Páginas utilizadas: {num_paginas}")
        print(f"🎵 Canciones disponibles: {len(generador.canciones)}")
        print(f"♻️ Papel ahorrado vs 1 por página: {args.num_cartones - num_paginas} páginas")
        print(f"💖 ¡Listo para celebrar la diversidad con música! 🌈")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Consejos:")
        print("- Asegúrate de que el archivo de canciones existe")
        print("- Verifica que hay al menos 24 canciones en el archivo")
        print("- Instala las librerías necesarias: pip install reportlab pandas")
        print("- Usa --help para ver todas las opciones disponibles")

if __name__ == "__main__":
    main()