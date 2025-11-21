# Scraper de Redes Sociales - Instagram, TikTok y Twitter/X

Scraper en Python usando Apify para recolectar datos de Instagram, TikTok y Twitter/X para análisis de ciencia de datos sobre derechos reproductivos y temas feministas.

## 📋 Características

- **Scraper de Instagram**: Recolecta publicaciones por hashtags con post_id, usuario, caption, hashtags, likes, comentarios, fecha y URL
- **Scraper de TikTok**: Recolecta videos por hashtags con video_id, usuario, caption, hashtags, vistas, likes, fecha y URL
- **Scraper de Twitter/X**: Recolecta tweets por hashtags con tweet_id, usuario, texto, hashtags, likes, retweets, respuestas, vistas, fecha y URL
- **Filtro por Fecha**: Filtra automáticamente datos desde el 1 de enero de 2025 en adelante
- **Exportación a CSV**: Todos los datos se exportan a archivos CSV listos para ciencia de datos
- **Grupo de Control**: Incluye keywords de control para análisis comparativo

## 🚀 Configuración

### 1. Instalar Dependencias

```bash
pip3 install -r requirements.txt
```

### 2. Configurar Token de API

Crea un archivo `.env` con tu token de Apify:

```bash
APIFY_API_TOKEN=tu_token_aqui
MAX_RESULTS_PER_KEYWORD=100
RESULTS_LIMIT=1000
```

Obtén tu token de API en: https://console.apify.com/account/integrations

## 📊 Uso

### Scraper Principal (43 keywords)

Ejecuta el scraper principal con todas las keywords relacionadas a derechos reproductivos y feminismo:

```bash
python3 scraper.py
```

### Grupo de Control (19 keywords)

Ejecuta el scraper del grupo de control con keywords de comparación:

```bash
python3 scraper_control.py
```

El script:
1. Extrae publicaciones de Instagram para todas las keywords
2. Extrae videos de TikTok para todas las keywords
3. Extrae tweets de Twitter/X para todas las keywords
4. Guarda los resultados en archivos CSV en el directorio `output/`

## 📁 Archivos de Salida

Todos los archivos CSV se guardan en el directorio `output/`:

### Grupo Principal
- `instagram_data.csv` - Publicaciones de Instagram
- `tiktok_data.csv` - Videos de TikTok
- `twitter_data.csv` - Tweets de Twitter/X

### Grupo de Control
- `instagram_data_control.csv` - Publicaciones de Instagram (control)
- `tiktok_data_control.csv` - Videos de TikTok (control)
- `twitter_data_control.csv` - Tweets de Twitter/X (control)

### Esquemas de Salida

**CSV de Instagram:**
- `post_id`: Identificador único de la publicación
- `usuario`: Nombre de usuario
- `caption`: Texto de la publicación
- `hashtags`: Hashtags separados por comas
- `likes`: Número de likes
- `comments`: Número de comentarios
- `fecha`: Fecha de publicación (YYYY-MM-DD HH:MM:SS)
- `url`: URL directa a la publicación
- `keyword`: Keyword de búsqueda utilizada

**CSV de TikTok:**
- `video_id`: Identificador único del video
- `usuario`: Nombre de usuario
- `caption`: Texto del video
- `hashtags`: Hashtags separados por comas
- `views`: Número de vistas
- `likes`: Número de likes
- `fecha`: Fecha de publicación (YYYY-MM-DD HH:MM:SS)
- `url`: URL directa al video
- `keyword`: Keyword de búsqueda utilizada

**CSV de Twitter/X:**
- `tweet_id`: Identificador único del tweet
- `usuario`: Nombre de usuario
- `texto`: Texto del tweet
- `hashtags`: Hashtags separados por comas
- `likes`: Número de likes
- `retweets`: Número de retweets
- `replies`: Número de respuestas
- `views`: Número de visualizaciones
- `fecha`: Fecha del tweet (YYYY-MM-DD HH:MM:SS)
- `url`: URL directa al tweet
- `keyword`: Keyword de búsqueda utilizada

## 🔑 Keywords

### Grupo Principal (43 keywords)
El scraper busca 43 keywords relacionadas con derechos reproductivos y feminismo en regiones de habla hispana:

- Derechos reproductivos: #aborto, #abortolegal, #abortolibre, #ile, #ive, #misoprostol, #cytotec
- Movimientos feministas: #feminismo, #niunamenos, #mareaverde, #8m, #mareafeminista
- Violencia de género: #feminicidio, #violenciaobstetrica, #violenciadigital
- Educación y salud: #educacionsexual, #saludreproductiva, #planificacionfamiliar
- Y más...

Ver lista completa en `keywords.py`

### Grupo de Control (19 keywords)
Keywords de control para análisis comparativo:

- #energiamasculina, #energiafemenina
- #masculinidadtoxica, #redpill, #mgtow
- #alfamacho, #tradwife, #feminidad
- #provida, #antiabortista
- Y más...

Ver lista completa en `keywords.py`

## 📅 Filtrado por Fecha

Todos los datos se filtran automáticamente para incluir solo publicaciones desde el 1 de enero de 2025 en adelante.

## ⚙️ Configuración

Edita el archivo `.env` para ajustar:
- `APIFY_API_TOKEN`: Tu token de API de Apify
- `MAX_RESULTS_PER_KEYWORD`: Resultados por keyword (predeterminado: 100)
- `RESULTS_LIMIT`: Límite total de resultados (predeterminado: 1000)

## 📝 Notas Importantes

- El scraper respeta los límites de tasa de la API con retrasos automáticos
- Los datos se guardan con codificación UTF-8 para soporte adecuado de caracteres en español
- Los captions multilínea se preservan en formato CSV (pueden aparecer entre comillas)
- Algunos hashtags pueden tener disponibilidad limitada dependiendo de la plataforma
- El scraper de Twitter requiere mínimo 50 tweets por keyword según requisitos de la API de Apify

## 💰 Costos de API

Apify cobra por uso:
- **Instagram**: Variable según plan
- **TikTok**: Variable según plan  
- **Twitter/X**: $0.40 por 1,000 tweets

Revisa tu plan en: https://console.apify.com/billing

## 🛠️ Estructura del Proyecto

```
scraper/
├── README.md                      # Esta guía
├── env_template.txt               # Plantilla de configuración
├── keywords.py                    # Lista de 43 keywords + 19 de control
├── requirements.txt               # Dependencias de Python
├── scraper.py                     # Scraper principal (43 keywords)
├── scraper_control.py             # Scraper de control (19 keywords)
└── output/                        # Directorio de salida
    ├── instagram_data.csv
    ├── tiktok_data.csv
    ├── twitter_data.csv
    ├── instagram_data_control.csv
    ├── tiktok_data_control.csv
    └── twitter_data_control.csv
```

## 📞 Soporte

Para problemas o preguntas sobre las APIs de Apify:
- Instagram: https://apify.com/apify/instagram-scraper
- TikTok: https://apify.com/clockworks/tiktok-scraper
- Twitter: https://apify.com/apidojo/tweet-scraper

---

**Desarrollado para análisis de datos sobre derechos reproductivos y movimientos feministas en América Latina** 🟢⚫🟢
