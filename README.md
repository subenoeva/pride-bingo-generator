# 🎵 Generador de Bingos Musicales Pride

Este script en Python permite generar cartones de bingo musical con temática Pride, usando una lista personalizada de canciones y creando un PDF colorido, amigable e inclusivo. Ideal para fiestas, dinámicas sociales y eventos comunitarios.

# ✨ Características

 - Generación de cartones de bingo 5x5 con centro libre
 - Formato visual optimizado para impresión (2 cartones por página)
 - Estética y colores inspirados en la bandera del orgullo LGBTQ+
 - Soporte para caracteres especiales y emojis musicales
 - Personalización de fuentes, tamaño de letra y cantidad de cartones

# 📦 Requisitos

    Python 3.7+

    Librerías Python:

        reportlab

        pandas

Instalación rápida con:
```
pip install reportlab pandas
```

# 📄 Uso
```
python generador_bingo_pride.py --archivo canciones.txt --salida bingo_pride.pdf --cantidad 10# Generador de Cartones de Bingo Musical Pride 🌟🏳️‍🌈

Este script en Python permite generar cartones de bingo musical personalizados con temática Pride. Usa una lista de canciones como insumo y genera un PDF con cartones coloridos y optimizados para imprimir.

---

## 📁 Requisitos

* Python 3.7 o superior
* Librerías:

  * `reportlab`
  * `pandas`

Puedes instalarlas con:

```bash
pip install reportlab pandas
```

---

## 📜 Uso básico

```bash
python generador_bingo_pride.py --archivo canciones.txt --cantidad 10
```

### Argumentos disponibles:

* `--archivo`: Ruta al archivo `.txt` con la lista de canciones (una por línea).
* `--cantidad`: Número de cartones a generar.
* `--fuente`: Tamaño de fuente (opcional, default: 7).
* `--por_pagina`: Cartones por página (opcional, default: 2).
* `--salida`: Nombre del archivo PDF resultante (opcional).

---

## 📕 Formato del archivo de canciones

Un archivo de texto plano (`.txt`) codificado en UTF-8, donde cada línea contiene una canción:

```
Like a Prayer - Madonna
Born This Way - Lady Gaga
Vogue - Madonna
... (etc)
```

---

## 💡 Características destacadas

* ✨ Temática visual Pride con colores del arcoíris.
* 🎶 Centro libre con mensaje decorativo.
* 🖊️ Fuentes personalizadas para mejor soporte de caracteres especiales.
* ⚖️ Optimizado para imprimir 1 o 2 cartones por página.
* 🌈 Incluye emojis y tipografía divertida.
* 🧰 Estimación de combinaciones únicas posibles.

---

## 🌐 Ejemplo de ejecución

```bash
python generador_bingo_pride.py --archivo canciones.txt --cantidad 20 --fuente 8 --por_pagina 2 --salida bingo_pride.pdf
```

---

## 📖 Estructura del código

El script está compuesto por una clase principal:

### `GeneradorBingoMusicalPride`

* Carga y limpia la lista de canciones.
* Verifica encoding y calidad del texto.
* Genera cartones con selección aleatoria de canciones.
* Usa `reportlab` para construir un PDF estilizado con tablas, colores y fuentes personalizadas.

---

## 🚫 Recomendaciones

* Asegúrate de tener instalada la fuente **DejaVu Sans** para mejor soporte de caracteres y emojis.
* Evita canciones duplicadas o listas muy cortas (¡se necesitan al menos 24 canciones!).

---

## 🎉 Crédito

Este script fue creado para celebrar la diversidad y la música en eventos inclusivos como bingos, fiestas o festivales comunitarios.

---

## 🚀 Próximas mejoras sugeridas

* Exportación a PNG o SVG.
* Personalización del estilo de encabezado.
* Interfaz gráfica (GUI).

---

## 🏠 Licencia

Este proyecto es de uso libre y comunitario bajo licencia MIT. ¡Disfrútalo y compártelo! 🌈
