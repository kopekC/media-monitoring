# Scraper de Redes Sociales - Instagram, TikTok, Twitter/X y Facebook Pages

Scraper en Python usando Apify para recolectar datos de Instagram, TikTok, Twitter/X y páginas de Facebook para análisis de ciencia de datos sobre derechos reproductivos y temas feministas.

## 📋 Características

- **Scraper de Instagram**: Recolecta publicaciones por hashtags con post_id, usuario, caption, hashtags, likes, comentarios, fecha y URL
- **Scraper de TikTok**: Recolecta videos por hashtags con video_id, usuario, caption, hashtags, vistas, likes, fecha y URL
- **Scraper de Twitter/X**: Recolecta tweets por hashtags con tweet_id, usuario, texto, hashtags, likes, retweets, respuestas, vistas, fecha y URL
- **Scraper de Facebook Pages**: Recolecta información de 55 organizaciones feministas en México incluyendo contacto, likes, followers, y más
- **Scraper de Facebook Posts**: Extrae posts de las 55 organizaciones y filtra por 43 keywords relacionados con derechos reproductivos
- **Filtro por Fecha**: Filtra automáticamente datos desde el 1 de enero de 2025 en adelante (Instagram, TikTok, Twitter, Facebook Posts)
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

### Scraper de Facebook Pages (55 organizaciones)

Ejecuta el scraper de páginas de Facebook para extraer información de las organizaciones:

```bash
python3 scraper_facebook_pages.py
```

### Scraper de Facebook Posts (55 organizaciones × 43 keywords)

Ejecuta el scraper de posts de Facebook que extrae publicaciones de las organizaciones y filtra por keywords:

```bash
python3 scraper_facebook_posts.py
```

El script:
1. Extrae publicaciones de Instagram para todas las keywords
2. Extrae videos de TikTok para todas las keywords
3. Extrae tweets de Twitter/X para todas las keywords
4. Extrae información de 55 páginas de Facebook de organizaciones feministas
5. Guarda los resultados en archivos CSV en el directorio `output/`

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

### Facebook
- `facebook_pages_data.csv` - Información de 55 organizaciones feministas
- `facebook_posts_data.csv` - Posts de las organizaciones que contienen keywords

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

**CSV de Facebook Pages:**
- `nombre_organizacion`: Nombre original de la organización
- `page_name`: Nombre de la página en Facebook
- `page_url`: URL de la página de Facebook
- `page_id`: Identificador único de la página
- `categoria`: Categorías de la página
- `likes`: Número de likes
- `followers`: Número de seguidores
- `intro`: Descripción/biografía de la página
- `website`: Sitio web de la organización
- `email`: Email de contacto
- `telefono`: Teléfono de contacto
- `direccion`: Dirección física
- `rating`: Calificación promedio
- `rating_count`: Número de reseñas
- `messenger`: Enlace de Messenger
- `checkins`: Número de check-ins
- `ad_library_id`: ID de biblioteca de anuncios
- `ad_status`: Estado de anuncios (Sí/No)
- `profile_picture_url`: URL de foto de perfil
- `cover_photo_url`: URL de foto de portada

**CSV de Facebook Posts:**
- `post_id`: Identificador único del post
- `organization_name`: Nombre de la organización
- `page_name`: Nombre de la página en Facebook
- `texto`: Texto completo del post
- `likes`: Número de likes
- `comments`: Número de comentarios
- `shares`: Número de veces compartido
- `fecha`: Fecha del post (YYYY-MM-DD HH:MM:SS)
- `url`: URL directa al post
- `keywords_matched`: Keywords encontrados en el post (separados por comas)

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

## 📘 Organizaciones de Facebook (55 páginas)

El scraper de Facebook Pages extrae información de 55 organizaciones feministas clave en México:

**Organizaciones principales (30):**
- La Cadera de Eva, Luchadoras, Balance A.C., Telefem, GIRE
- Fondo MARIA, Marea Verde México, Necesito Abortar México
- OCNF, Red Nacional de Refugios A.C., Equis Justicia
- Y más...

**Redes de acompañamiento (10):**
- Abortistas del Norte, Las Hijas de Ixchel, Marea Verde QRoo
- Sororas Sonora, Te Acompaño Puebla, Brujas del Mar Acompañan
- Y más...

**Organizaciones contra feminicidios (10):**
- Justicia para Nuestras Hijas, Familias Unidas Contra Feminicidios
- Hasta Encontrarles CDMX, Red Yo Te Creo México
- Y más...

**Defensoras digitales y ciberfeminismo (5):**
- Defensoras Digitales México, Ciberfeministas México
- Lunas Digitales, Sororidad Digital MX
- Y más...

Ver lista completa en `facebook_pages.py`

## 📅 Filtrado por Fecha

Los datos de Instagram, TikTok y Twitter/X se filtran automáticamente para incluir solo publicaciones desde el 1 de enero de 2025 en adelante. El scraper de Facebook Pages extrae información actual de las páginas.

## ⚙️ Configuración

Edita el archivo `.env` para ajustar:
- `APIFY_API_TOKEN`: Tu token de API de Apify
- `MAX_RESULTS_PER_KEYWORD`: Resultados por keyword para Instagram/TikTok/Twitter (predeterminado: 100)
- `RESULTS_LIMIT`: Límite total de resultados (predeterminado: 1000)
- `MAX_POSTS_PER_PAGE`: Posts por página de Facebook (predeterminado: 100)

## 📝 Notas Importantes

- El scraper respeta los límites de tasa de la API con retrasos automáticos
- Los datos se guardan con codificación UTF-8 para soporte adecuado de caracteres en español
- Los captions multilínea se preservan en formato CSV (pueden aparecer entre comillas)
- Algunos hashtags pueden tener disponibilidad limitada dependiendo de la plataforma
- El scraper de Twitter requiere mínimo 50 tweets por keyword según requisitos de la API de Apify
- El scraper de Facebook Pages extrae información pública de las organizaciones sin requerir inicio de sesión
- El scraper de Facebook Pages procesa las páginas en lotes de 10 para optimizar el uso de recursos
- El scraper de Facebook Posts extrae hasta 100 posts por organización y filtra automáticamente por keywords
- El filtrado de keywords en Facebook Posts es case-insensitive y busca coincidencias en el texto completo

## 💰 Costos de API

Apify cobra por uso:
- **Instagram**: Variable según plan
- **TikTok**: Variable según plan  
- **Twitter/X**: $0.40 por 1,000 tweets
- **Facebook Pages**: $6.60 por 1,000 páginas ($0.01 por página)
- **Facebook Posts**: $10 por 1,000 posts (55 páginas × 100 posts = ~$55 USD)

**Costo estimado total para una ejecución completa:** ~$60-80 USD

Revisa tu plan en: https://console.apify.com/billing

## 🛠️ Estructura del Proyecto

```
scraper/
├── README.md                      # Esta guía
├── env_template.txt               # Plantilla de configuración
├── keywords.py                    # Lista de 43 keywords + 19 de control
├── facebook_pages.py              # Lista de 55 páginas de Facebook
├── requirements.txt               # Dependencias de Python
├── scraper.py                     # Scraper principal (43 keywords)
├── scraper_control.py             # Scraper de control (19 keywords)
├── scraper_facebook_pages.py     # Scraper de Facebook Pages (55 organizaciones)
├── scraper_facebook_posts.py     # Scraper de Facebook Posts (55 orgs × 43 keywords)
└── output/                        # Directorio de salida
    ├── instagram_data.csv
    ├── tiktok_data.csv
    ├── twitter_data.csv
    ├── instagram_data_control.csv
    ├── tiktok_data_control.csv
    ├── twitter_data_control.csv
    ├── facebook_pages_data.csv
    └── facebook_posts_data.csv
```

## 📞 Soporte

Para problemas o preguntas sobre las APIs de Apify:
- Instagram: https://apify.com/apify/instagram-scraper
- TikTok: https://apify.com/clockworks/tiktok-scraper
- Twitter: https://apify.com/apidojo/tweet-scraper
- Facebook Pages: https://apify.com/apify/facebook-pages-scraper
- Facebook Posts: https://apify.com/apify/facebook-posts-scraper

---

**Desarrollado para análisis de datos sobre derechos reproductivos y movimientos feministas en América Latina** 🟢⚫🟢
