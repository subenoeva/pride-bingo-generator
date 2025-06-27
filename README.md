# 🎵 Generador de Bingo Musical Pride con Spotify 🏳️‍🌈

Un generador avanzado de cartones de bingo musical con temática Pride que permite extraer canciones directamente desde playlists de Spotify o usar archivos de texto personalizados. Genera PDFs coloridos y optimizados para imprimir, perfectos para fiestas, eventos comunitarios y celebraciones inclusivas.

## ✨ Características Principales

- 🎵 **Integración con Spotify**: Extrae canciones automáticamente desde cualquier playlist pública
- 🏳️‍🌈 **Temática Pride**: Colores del arcoíris y diseño inclusivo
- 📄 **Optimizado para impresión**: 1, 2 o 4 cartones por página
- 🌟 **Cartones únicos**: Generación de hasta 1000+ cartones diferentes
- 🎨 **Formato visual mejorado**: Colores suaves, fuentes personalizadas y numeración automática
- 🔤 **Soporte internacional**: Manejo avanzado de caracteres especiales y acentos
- 💾 **Exportación flexible**: Guarda las canciones extraídas para uso futuro

## 📦 Instalación

### Requisitos del sistema
- Python 3.7 o superior

### Dependencias
```bash
pip install reportlab pandas spotipy requests
```

### Fuentes recomendadas (opcional)
Para mejor soporte de caracteres especiales:
- **DejaVu Sans** (recomendado)
- Arial Unicode MS
- Calibri

## 🚀 Uso

### 1. Con Playlist de Spotify (Recomendado)

#### Configuración inicial de Spotify API
1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Inicia sesión con tu cuenta de Spotify
3. Crea una nueva aplicación ("Create an App")
4. Copia tu **Client ID** y **Client Secret**

#### Uso básico
```bash
python bingo_spotify.py \
  --spotify-playlist "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" \
  --spotify-client-id "tu_client_id" \
  --spotify-client-secret "tu_client_secret" \
  --num-cartones 50
```

#### Uso avanzado con Spotify
```bash
python bingo_spotify.py \
  --spotify-playlist "URL_DE_TU_PLAYLIST" \
  --spotify-client-id "TU_CLIENT_ID" \
  --spotify-client-secret "TU_CLIENT_SECRET" \
  --num-cartones 100 \
  --max-canciones-spotify 200 \
  --guardar-canciones canciones_extraidas.txt \
  --por-pagina 2 \
  --fuente 8 \
  --output bingo_pride_spotify.pdf
```

### 2. Con Archivo de Texto

```bash
python bingo_spotify.py \
  --canciones canciones.txt \
  --num-cartones 25 \
  --por-pagina 2
```

## 📋 Argumentos Disponibles

### Fuente de Canciones (obligatorio, uno de los dos)
- `--spotify-playlist URL`: URL de playlist de Spotify
- `--canciones ARCHIVO`: Archivo de texto con canciones

### Credenciales de Spotify (requeridas para Spotify)
- `--spotify-client-id ID`: Client ID de tu app de Spotify
- `--spotify-client-secret SECRET`: Client Secret de tu app

### Opciones de Spotify
- `--incluir-artista`: Incluye el nombre del artista (activado por defecto)
- `--max-canciones-spotify N`: Limita el número de canciones extraídas
- `--guardar-canciones ARCHIVO`: Guarda las canciones en un archivo de texto

### Opciones Generales
- `--num-cartones N`: Número de cartones a generar (default: 100)
- `--output ARCHIVO`: Nombre del PDF de salida (default: cartones_bingo_pride_spotify.pdf)
- `--fuente N`: Tamaño de fuente (default: 8)
- `--por-pagina N`: Cartones por página: 1, 2 o 4 (default: 2)

## 📄 Formato del Archivo de Canciones

Si usas un archivo de texto, debe estar codificado en UTF-8 con una canción por línea:

```
Like a Prayer - Madonna
Born This Way - Lady Gaga
I Will Survive - Gloria Gaynor
Dancing Queen - ABBA
Respect - Aretha Franklin
```

## 🎯 Ejemplos de Uso

### Ejemplo 1: Playlist de éxitos LGBTQ+
```bash
python bingo_spotify.py \
  --spotify-playlist "https://open.spotify.com/playlist/37i9dQZF1DX4OzrY981I1W" \
  --spotify-client-id "abc123..." \
  --spotify-client-secret "def456..." \
  --num-cartones 30 \
  --guardar-canciones pride_hits.txt
```

### Ejemplo 2: Configuración compacta (4 por página)
```bash
python bingo_spotify.py \
  --canciones mi_playlist.txt \
  --num-cartones 40 \
  --por-pagina 4 \
  --fuente 7
```

### Ejemplo 3: Extracción limitada de Spotify
```bash
python bingo_spotify.py \
  --spotify-playlist "URL_PLAYLIST" \
  --spotify-client-id "CLIENT_ID" \
  --spotify-client-secret "CLIENT_SECRET" \
  --max-canciones-spotify 50 \
  --num-cartones 20
```

## 🛠️ Configuración Interactiva

Si ejecutas el script sin credenciales de Spotify, te guiará interactivamente:

```bash
python bingo_spotify.py --spotify-playlist "URL_PLAYLIST"
# Te pedirá las credenciales paso a paso
```

## 🎨 Características del Diseño

- **Colores Pride**: Paleta inspirada en la bandera del orgullo LGBTQ+
- **Numeración automática**: Cada canción tiene un número único para facilitar el juego
- **Centro libre**: Casilla central marcada como "🎵 LIBRE 🎵"
- **Efectos visuales**: Fondos de colores suaves del arcoíris
- **Optimización de espacio**: Diseño que maximiza la legibilidad

## 🔧 Solución de Problemas

### Errores comunes con Spotify
- **Credenciales inválidas**: Verifica tu Client ID y Client Secret
- **Playlist no encontrada**: Asegúrate de que la URL sea correcta y la playlist sea pública
- **Muy pocas canciones**: Algunas playlists pueden tener canciones no disponibles

### Errores con archivos de texto
- **Encoding**: Guarda el archivo en UTF-8
- **Canciones insuficientes**: Se necesitan mínimo 24 canciones únicas
- **Caracteres especiales**: El script maneja automáticamente la mayoría de caracteres

### Problemas de fuentes
El script intentará usar fuentes en este orden:
1. DejaVu Sans (recomendado)
2. Arial
3. Calibri
4. Helvetica (por defecto)

## 📊 Información Técnica

### Algoritmo de generación
- Cada cartón usa 24 canciones aleatorias diferentes
- Centro libre fijo
- Sin repetición de canciones dentro del mismo cartón
- Máximo de cartones únicos calculado automáticamente

### Optimizaciones
- Limpieza automática de caracteres problemáticos
- Ajuste dinámico de tamaños según cartones por página
- Rate limiting para respeto a la API de Spotify
- Manejo robusto de errores de red

## 🎉 Casos de Uso

- **Fiestas temáticas**: Eventos Pride, celebraciones LGBTQ+
- **Dinámicas grupales**: Actividades comunitarias, talleres
- **Eventos musicales**: Conciertos, festivales, karaokes
- **Educación**: Talleres de diversidad e inclusión
- **Entretenimiento**: Noches de juegos, reuniones familiares

## 🌈 Contribuciones

¡Las contribuciones son bienvenidas! Este proyecto celebra la diversidad y la inclusión.

### Ideas para futuras mejoras
- Integración con Apple Music y YouTube Music
- Generación de cartones temáticos (por década, género, etc.)
- Interfaz gráfica (GUI)
- Exportación a otros formatos (PNG, SVG)
- Modo multijugador online

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT. Úsalo, modifícalo y compártelo libremente para crear momentos alegres e inclusivos.

## 🙏 Agradecimientos

Creado para celebrar la diversidad, la música y la comunidad LGBTQ+. ¡Que cada cartón sea una celebración de la inclusión! 🏳️‍🌈

---

**¿Necesitas ayuda?** Usa `python bingo_spotify.py --help` para ver todas las opciones disponibles.

**¿Primera vez?** Ejecuta `python bingo_spotify.py` sin argumentos para ver ejemplos de uso.