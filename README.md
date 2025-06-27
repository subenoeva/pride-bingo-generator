🎵 Generador de Bingos Musicales Pride

Este script en Python permite generar cartones de bingo musical con temática Pride, usando una lista personalizada de canciones y creando un PDF colorido, amigable e inclusivo. Ideal para fiestas, dinámicas sociales y eventos comunitarios.
✨ Características

    Generación de cartones de bingo 5x5 con centro libre

    Formato visual optimizado para impresión (2 cartones por página)

    Estética y colores inspirados en la bandera del orgullo LGBTQ+

    Soporte para caracteres especiales y emojis musicales

    Personalización de fuentes, tamaño de letra y cantidad de cartones

📦 Requisitos

    Python 3.7+

    Librerías Python:

        reportlab

        pandas

Instalación rápida con:

pip install reportlab pandas

📄 Uso

python generador_bingo_pride.py --archivo canciones.txt --salida bingo_pride.pdf --cantidad 10

Argumentos
Argumento	Descripción	Opcional	Por defecto
--archivo	Ruta al archivo .txt con las canciones (una por línea)	❌	—
--salida	Nombre del archivo PDF de salida	✅	cartones_bingo_pride.pdf
--cantidad	Cantidad de cartones a generar	✅	10
--fuente	Tamaño de fuente para los textos en los cartones	✅	7
--por_pagina	Cantidad de cartones por página PDF	✅	2
📁 Formato del archivo de canciones

Debe ser un archivo .txt codificado en UTF-8 (o similar) que contenga una canción por línea:

Like a Prayer - Madonna
Born This Way - Lady Gaga
I Will Survive - Gloria Gaynor
...

💡 Se requieren al menos 24 canciones únicas para generar un cartón.
🏳️‍🌈 Estilo y Diseño

    Usa fuentes que soportan caracteres especiales como DejaVu Sans, Arial Unicode, o Calibri.

    Los cartones incluyen:

        Encabezado temático ("Bingo Polari")

        Casilla central "LIBRE" con diseño especial

        Colores Pride suaves para cada casilla

        Emojis decorativos opcionales

🛠 Personalización

El script puede ser extendido o modificado fácilmente para:

    Agregar más idiomas o estilos de fuente

    Cambiar los colores o emojis usados

    Modificar el layout de los cartones

📌 Ejemplo visual

📄 Al ejecutar el script, obtendrás un PDF como este:

    2 cartones por página

    Cada casilla con una canción

    Diseño listo para imprimir