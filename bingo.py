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
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from urllib.parse import urlparse, parse_qs
import requests
import time

class SpotifyExtractor:
    """Clase para extraer canciones de playlists de Spotify"""
    
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = None
        
        if client_id and client_secret:
            self.configurar_spotify_api()
    
    def configurar_spotify_api(self):
        """Configura la conexión con la API de Spotify"""
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            
            # Test de conexión
            self.sp.user('spotify')
            print("✅ Conexión con Spotify API establecida correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando Spotify API: {e}")
            print("💡 Asegúrate de tener credenciales válidas de Spotify")
            return False
    
    def extraer_playlist_id(self, url):
        """Extrae el ID de la playlist desde una URL de Spotify"""
        patterns = [
            r'spotify:playlist:([a-zA-Z0-9]+)',
            r'open\.spotify\.com/playlist/([a-zA-Z0-9]+)',
            r'spotify\.com/playlist/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"No se pudo extraer el ID de la playlist de la URL: {url}")
    
    def obtener_canciones_playlist(self, playlist_url, incluir_artista=True, max_canciones=None):
        """Obtiene todas las canciones de una playlist de Spotify"""
        if not self.sp:
            raise Exception("Spotify API no configurada. Proporciona client_id y client_secret.")
        
        try:
            playlist_id = self.extraer_playlist_id(playlist_url)
            print(f"🎵 Extrayendo canciones de la playlist ID: {playlist_id}")
            
            # Obtener información de la playlist
            playlist_info = self.sp.playlist(playlist_id)
            nombre_playlist = playlist_info['name']
            total_tracks = playlist_info['tracks']['total']
            
            print(f"📋 Playlist: '{nombre_playlist}'")
            print(f"🔢 Total de canciones en la playlist: {total_tracks}")
            
            canciones = []
            offset = 0
            limit = 100  # Máximo por request de Spotify
            
            while True:
                # Obtener batch de canciones
                results = self.sp.playlist_tracks(
                    playlist_id,
                    offset=offset,
                    limit=limit,
                    fields='items(track(name,artists(name),explicit)),next'
                )
                
                tracks = results['items']
                if not tracks:
                    break
                
                for item in tracks:
                    track = item.get('track')
                    if not track or not track.get('name'):
                        continue
                    
                    nombre_cancion = track['name']
                    artistas = [artist['name'] for artist in track.get('artists', [])]
                    
                    if incluir_artista and artistas:
                        cancion_completa = f"{nombre_cancion} - {', '.join(artistas)}"
                    else:
                        cancion_completa = nombre_cancion
                    
                    canciones.append(cancion_completa)
                    
                    # Aplicar límite si se especifica
                    if max_canciones and len(canciones) >= max_canciones:
                        break
                
                if max_canciones and len(canciones) >= max_canciones:
                    break
                
                if not results['next']:
                    break
                
                offset += limit
                time.sleep(0.1)  # Rate limiting cortés
            
            print(f"✅ Se extrajeron {len(canciones)} canciones de la playlist")
            
            if len(canciones) < 24:
                print(f"⚠️ Advertencia: Solo se encontraron {len(canciones)} canciones.")
                print("Se necesitan al menos 24 para generar cartones de bingo.")
            
            return canciones, nombre_playlist
            
        except Exception as e:
            raise Exception(f"Error obteniendo canciones de Spotify: {e}")
    
    def obtener_canciones_sin_api(self, playlist_url):
        """Método alternativo para obtener canciones sin API (web scraping básico)"""
        print("⚠️ Intentando método alternativo sin API de Spotify...")
        print("💡 Nota: Este método puede ser menos confiable y obtener menos canciones.")
        
        try:
            # Extraer ID de playlist
            playlist_id = self.extraer_playlist_id(playlist_url)
            
            # Intentar obtener datos públicos (método simplificado)
            # Este es un placeholder - en un caso real necesitarías implementar
            # web scraping más sofisticado o usar APIs alternativas
            
            print("❌ Método alternativo no implementado completamente.")
            print("💡 Para obtener canciones de Spotify, necesitas configurar las credenciales de API.")
            
            return [], "Playlist sin nombre"
            
        except Exception as e:
            raise Exception(f"Error en método alternativo: {e}")

class GeneradorBingoMusicalPride:
    def __init__(self, ruta_canciones=None, playlist_url=None, spotify_client_id=None, 
                 spotify_client_secret=None, tamaño_fuente=7, cartones_por_pagina=2,
                 incluir_artista=True, max_canciones_spotify=None):
        
        self.tamaño_fuente = tamaño_fuente
        self.cartones_por_pagina = cartones_por_pagina
        self.colores_pride = self.obtener_colores_pride()
        self.emojis_pride = ['🏳️‍🌈', '🏳️‍⚧️', '💖', '🌈', '✨', '🎵', '🎶', '💃', '🕺', '🔥', '💫', '⭐']
        self.configurar_fuentes()
        
        # Configurar extractor de Spotify
        self.spotify_extractor = SpotifyExtractor(spotify_client_id, spotify_client_secret)
        
        # Cargar canciones desde archivo o Spotify
        if playlist_url:
            self.canciones, self.nombre_fuente = self.cargar_canciones_spotify(
                playlist_url, incluir_artista, max_canciones_spotify
            )
        elif ruta_canciones:
            self.canciones = self.cargar_canciones_archivo(ruta_canciones)
            self.nombre_fuente = os.path.basename(ruta_canciones)
        else:
            raise ValueError("Debes proporcionar una URL de playlist de Spotify o un archivo de canciones")
        
        self.verificar_canciones()
    
    def cargar_canciones_spotify(self, playlist_url, incluir_artista=True, max_canciones=None):
        """Carga canciones desde una playlist de Spotify"""
        try:
            canciones, nombre_playlist = self.spotify_extractor.obtener_canciones_playlist(
                playlist_url, incluir_artista, max_canciones
            )
            
            if not canciones:
                # Intentar método alternativo
                print("🔄 Intentando método alternativo...")
                canciones, nombre_playlist = self.spotify_extractor.obtener_canciones_sin_api(playlist_url)
            
            if not canciones:
                raise Exception("No se pudieron obtener canciones de la playlist")
            
            # Limpiar y procesar canciones
            canciones_limpias = []
            for cancion in canciones:
                cancion_limpia = self.limpiar_texto_para_pdf(cancion)
                if cancion_limpia and len(cancion_limpia) > 2:
                    canciones_limpias.append(cancion_limpia)
            
            return canciones_limpias, nombre_playlist
            
        except Exception as e:
            print(f"❌ Error cargando canciones de Spotify: {e}")
            print("💡 Verifica la URL de la playlist y las credenciales de API")
            raise
    
    def cargar_canciones_archivo(self, ruta):
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
        
        print(f"🏳️‍🌈 Se cargaron {len(self.canciones)} canciones desde: {self.nombre_fuente}")
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
    
    def generar_pdf(self, num_cartones, nombre_archivo="cartones_bingo_pride_spotify.pdf"):
        """Genera el PDF con todos los cartones con tema Pride"""
        print(f"\n🏳️‍🌈 Generando {num_cartones} cartones de bingo musical Pride desde Spotify ({self.cartones_por_pagina} por página)...")
        
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
        print(f"🎉 ¡Listo! Se generaron {num_cartones} cartones Pride desde Spotify en {num_paginas} páginas en '{nombre_archivo}'")
        
        return nombre_archivo

def parse_arguments():
    """Configura y parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Generador de Cartones de Bingo Musical con Tema Pride - Con Soporte para Spotify',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Grupo mutuamente excluyente para fuente de canciones
    source_group = parser.add_mutually_exclusive_group(required=True)
    
    source_group.add_argument(
        '-c', '--canciones',
        type=str,
        help='Ruta al archivo de texto con las canciones'
    )
    
    source_group.add_argument(
        '-s', '--spotify-playlist',
        type=str,
        help='URL de la playlist de Spotify (ej: https://open.spotify.com/playlist/...)'
    )
    
    # Credenciales de Spotify
    parser.add_argument(
        '--spotify-client-id',
        type=str,
        help='Client ID de la aplicación de Spotify'
    )
    
    parser.add_argument(
        '--spotify-client-secret',
        type=str,
        help='Client Secret de la aplicación de Spotify'
    )
    
    # Opciones de Spotify
    parser.add_argument(
        '--incluir-artista',
        action='store_true',
        default=True,
        help='Incluir nombre del artista junto con el nombre de la canción'
    )
    
    parser.add_argument(
        '--max-canciones-spotify',
        type=int,
        help='Máximo número de canciones a extraer de la playlist (por defecto: todas)'
    )
    
    # Opciones generales
    parser.add_argument(
        '-n', '--num-cartones',
        type=int,
        default=100,
        help='Número de cartones a generar'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='cartones_bingo_pride_spotify.pdf',
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
    
    # Opciones de configuración
    parser.add_argument(
        '--guardar-canciones',
        type=str,
        help='Guardar las canciones extraídas de Spotify en un archivo de texto'
    )
    
    return parser.parse_args()

def configurar_credenciales_spotify():
    """Guía interactiva para configurar credenciales de Spotify"""
    print("\n🎵 CONFIGURACIÓN DE SPOTIFY API")
    print("=" * 50)
    print("Para usar playlists de Spotify necesitas crear una aplicación en Spotify Developer:")
    print("1. Ve a: https://developer.spotify.com/dashboard/applications")
    print("2. Inicia sesión con tu cuenta de Spotify")
    print("3. Haz clic en 'Create an App'")
    print("4. Completa el formulario (nombre y descripción de tu app)")
    print("5. Copia el 'Client ID' y 'Client Secret'")
    print("6. No necesitas configurar redirect URIs para este uso")
    print("=" * 50)
    
    client_id = input("Ingresa tu Spotify Client ID: ").strip()
    client_secret = input("Ingresa tu Spotify Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Credenciales no proporcionadas")
        return None, None
    
    return client_id, client_secret

def main():
    """Función principal para ejecutar el generador con parámetros configurables"""
    try:
        args = parse_arguments()
        
        # Mostrar información de configuración
        print("🏳️‍🌈 Iniciando generador de Bingo Musical Pride MEJORADO con Spotify")
        print(f"📄 Configuración:")
        
        # Determinar fuente de canciones
        if args.spotify_playlist:
            print(f"  • Fuente: Playlist de Spotify")
            print(f"  • URL de playlist: {args.spotify_playlist}")
            print(f"  • Incluir artista: {'Sí' if args.incluir_artista else 'No'}")
            if args.max_canciones_spotify:
                print(f"  • Máximo de canciones: {args.max_canciones_spotify}")
            
            # Configurar credenciales de Spotify
            client_id = args.spotify_client_id
            client_secret = args.spotify_client_secret
            
            if not client_id or not client_secret:
                print("⚠️ No se proporcionaron credenciales de Spotify")
                respuesta = input("¿Quieres configurarlas ahora? (s/n): ").lower()
                if respuesta in ['s', 'sí', 'si', 'y', 'yes']:
                    client_id, client_secret = configurar_credenciales_spotify()
                    if not client_id or not client_secret:
                        print("❌ No se pueden obtener canciones de Spotify sin credenciales")
                        return
                else:
                    print("❌ No se pueden obtener canciones de Spotify sin credenciales")
                    return
            
            # Crear generador con Spotify
            generador = GeneradorBingoMusicalPride(
                playlist_url=args.spotify_playlist,
                spotify_client_id=client_id,
                spotify_client_secret=client_secret,
                tamaño_fuente=args.fuente,
                cartones_por_pagina=args.por_pagina,
                incluir_artista=args.incluir_artista,
                max_canciones_spotify=args.max_canciones_spotify
            )
            
            # Guardar canciones si se solicita
            if args.guardar_canciones:
                print(f"💾 Guardando canciones en: {args.guardar_canciones}")
                with open(args.guardar_canciones, 'w', encoding='utf-8') as f:
                    for cancion in generador.canciones:
                        f.write(cancion + '\n')
                print(f"✅ Se guardaron {len(generador.canciones)} canciones en {args.guardar_canciones}")
            
        else:
            print(f"  • Fuente: Archivo de texto")
            print(f"  • Archivo de canciones: {args.canciones}")
            
            # Crear generador con archivo
            generador = GeneradorBingoMusicalPride(
                ruta_canciones=args.canciones,
                tamaño_fuente=args.fuente,
                cartones_por_pagina=args.por_pagina
            )
        
        print(f"  • Cartones a generar: {args.num_cartones}")
        print(f"  • Cartones por página: {args.por_pagina}")
        print(f"  • Tamaño de fuente: {args.fuente}")
        print(f"  • Archivo de salida: {args.output}")
        
        # Generar PDF
        archivo_generado = generador.generar_pdf(args.num_cartones, args.output)
        
        num_paginas = (args.num_cartones + args.por_pagina - 1) // args.por_pagina
        
        print(f"\n🎊 ¡Proceso completado con éxito!")
        print(f"📁 Archivo generado: {archivo_generado}")
        print(f"🏳️‍🌈 Cartones Pride generados: {args.num_cartones}")
        print(f"📄 Páginas utilizadas: {num_paginas}")
        print(f"🎵 Canciones disponibles: {len(generador.canciones)}")
        print(f"🎯 Fuente de canciones: {generador.nombre_fuente}")
        print(f"♻️ Papel ahorrado vs 1 por página: {args.num_cartones - num_paginas} páginas")
        print(f"💖 ¡Listo para celebrar la diversidad con música! 🌈")
        
    except KeyboardInterrupt:
        print("\n⏹️ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Consejos:")
        if "spotify" in str(e).lower():
            print("- Verifica que la URL de la playlist de Spotify sea correcta")
            print("- Asegúrate de tener credenciales válidas de Spotify Developer")
            print("- La playlist debe ser pública o ser tuya")
            print("- Instala spotipy: pip install spotipy")
        else:
            print("- Asegúrate de que el archivo de canciones existe")
            print("- Verifica que hay al menos 24 canciones disponibles")
            print("- Instala las librerías necesarias:")
            print("  pip install reportlab pandas spotipy requests")
        print("- Usa --help para ver todas las opciones disponibles")

def ejemplo_uso():
    """Muestra ejemplos de uso del script"""
    print("\n🌈 EJEMPLOS DE USO:")
    print("=" * 60)
    print("1. Usar playlist de Spotify:")
    print("   python bingo_spotify.py \\")
    print("   --spotify-playlist 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M' \\")
    print("   --spotify-client-id 'tu_client_id' \\")
    print("   --spotify-client-secret 'tu_client_secret' \\")
    print("   --num-cartones 50")
    print()
    print("2. Usar archivo de texto:")
    print("   python bingo_spotify.py --canciones canciones.txt --num-cartones 25")
    print()
    print("3. Spotify con opciones avanzadas:")
    print("   python bingo_spotify.py \\")
    print("   --spotify-playlist 'URL_PLAYLIST' \\")
    print("   --spotify-client-id 'CLIENT_ID' \\")
    print("   --spotify-client-secret 'CLIENT_SECRET' \\")
    print("   --max-canciones-spotify 100 \\")
    print("   --guardar-canciones canciones_extraidas.txt \\")
    print("   --por-pagina 4 \\")
    print("   --fuente 7")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        ejemplo_uso()
    main()