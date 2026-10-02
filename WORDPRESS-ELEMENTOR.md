# Cómo subir el sitio Neurogenomic a WordPress con Elementor Pro

Guía paso a paso para montar las 4 páginas (Inicio, Servicios, Tecnología y Contacto) con los bloques de la carpeta `elementor/`. Cada bloque se pega en un widget **HTML** de Elementor y ya trae su diseño, sus animaciones y su JavaScript.

> Tiempo estimado: 1–2 horas. Necesitas acceso de **administrador** a WordPress (solo los administradores pueden pegar HTML con scripts) y, para el paso 2, acceso al **Administrador de archivos** del hosting (cPanel, Plesk, hPanel, etc.) o a FTP.

---

## Opción rápida: importar las páginas como plantillas JSON

Esta vía reemplaza los pasos 3 y 4 de abajo: no hay que pegar los bloques uno por uno. Cada página es un archivo `.json` en `elementor-json/`:

| Archivo | Página |
|---|---|
| `neurogenomic-inicio.json` | Inicio (20 contenedores: núcleo, encabezado, historia 3D, todas las secciones y pie) |
| `neurogenomic-servicios.json` | Servicios |
| `neurogenomic-tecnologia.json` | Tecnología |
| `neurogenomic-contacto.json` | Contacto |

1. Haz antes los pasos 1 (preparar WordPress) y 2 (subir `img/`).
2. Crea la página (por ejemplo *Inicio*) y pulsa **Editar con Elementor**.
3. Haz clic en el ícono de **carpeta** (*Añadir plantilla*), pestaña **Mis plantillas**, y luego en el ícono de **subir** (*Importar plantilla*). Elige el `.json` e impórtalo.
4. En la lista de **Mis plantillas**, pulsa **Insertar** en la plantilla importada. Si pregunta por los ajustes de página, acepta **Sí**: así aplica *Elementor Canvas* y el fondo oscuro.
5. Pulsa **Publicar**. Repite con las otras tres páginas.

Cómo quedan las plantillas:
- **Diseño completo:** cada sección es un contenedor con un widget **HTML** que lleva el bloque intacto (estilos, marcado y JavaScript). No se pierde ninguna animación ni ningún contenido.
- **Navegador de Elementor:** cada contenedor lleva el nombre de su sección («03 · Lo que no se dice», «Capítulo 02 · Señales»…). Puedes reordenarlos o desactivarlos desde ahí.
- **Núcleo:** el primer contenedor, «Núcleo Neurogenomic (no borrar)», carga las fuentes, los estilos base y el motor de animaciones una sola vez.
- **Plantilla de página:** usan **Elementor Canvas**, porque ya traen su propio encabezado y pie. Si prefieres el encabezado y pie del Theme Builder (paso 3), borra los contenedores «Encabezado» y «Pie de página» de cada página y cambia la plantilla a *Elementor Ancho completo*.
- **Compatibilidad con el tema:** los bloques traen un blindaje contra los estilos base de Hello Elementor (botones, enlaces, títulos, listas). Se verificó con una simulación del DOM de Elementor más el reset real de Hello: las 4 páginas miden exactamente lo mismo que el sitio original en 1440 y 390 px.
- **Por qué widgets HTML y no widgets nativos:** las animaciones (escena 3D con WebGL, mapas de calor en canvas, demo cuadro a cuadro, GSAP) no tienen equivalente nativo en Elementor. Rehacerlas con widgets nativos las eliminaría.

---

## 0. Qué necesitas tener a mano

Del archivo `neurogenomic-sitio.zip` o del repositorio:

| Carpeta / archivo | Para qué sirve |
|---|---|
| `elementor/` | Los 26 bloques completos (`00-…` a `25-…`). Cada uno funciona solo. |
| `elementor/ligeros/` | Los mismos bloques sin repetir fuentes, estilos base ni núcleo JS, más `00-codigo-personalizado.html` (opción optimizada, paso 6). |
| `img/` | Todas las imágenes, los 80 cuadros de la demo (`img/seq/`) y las imágenes de respaldo de la historia 3D (`img/story/`). |
| `elementor-json/` | Las 4 páginas como plantillas JSON importables (opción rápida). |

---

## 1. Preparar WordPress

1. **Tema:** instala y activa **Hello Elementor** (Apariencia → Temas → Añadir nuevo). Es un tema vacío, así que no impone colores, márgenes ni tipografías.
2. **Plugins:** activa **Elementor** y **Elementor Pro** y conecta tu licencia (Elementor → Licencia).
3. **Ajustes de Elementor** (Elementor → Ajustes):
   - En **General**, marca *Desactivar colores predeterminados* y *Desactivar fuentes predeterminadas*. Así Elementor no pisa los colores y fuentes de los bloques.
   - En **Funciones / Features**, deja activo *Contenedor flexbox* (Flexbox Container).
4. **Ajustes del sitio** (Elementor → abre el editor → menú ☰ → *Ajustes del sitio*):
   - En **Diseño**, pon el *Ancho del contenido* en 1680 px y el *Espacio entre widgets* en 0.
   - En **Fondo**, usa el color `#0A0B0D`.
5. **Enlaces permanentes:** en Ajustes → Enlaces permanentes, elige **Nombre de la entrada**. Los bloques enlazan a `/servicios/`, `/tecnologia/`, `/contacto/`, `/privacidad/` y `/terminos/`.

---

## 2. Subir las imágenes (sin tocar código)

Los bloques buscan las imágenes en **`/img/…`**, es decir, en `https://tudominio.cl/img/`. La forma más simple es subir esa carpeta tal cual:

1. Abre el **Administrador de archivos** del hosting y entra a la carpeta raíz del sitio (normalmente `public_html/`, donde está `wp-config.php`).
2. Sube la carpeta **`img/` completa**, con sus subcarpetas `seq/` y `story/`. Puedes subir `neurogenomic-sitio.zip` y usar *Extraer*; luego borra los `.html` que se extraigan junto a `img/`.
3. Comprueba que abra `https://tudominio.cl/img/ng-phone-600.webp`. Si se ve la imagen, ya está.

**¿Tu hosting no permite subir archivos a la raíz?** (algunos WordPress administrados).
- Sube la carpeta a `wp-content/uploads/neurogenomic/img/`.
- En `build.py`, cambia `IMG_WP = "/img/"` por `IMG_WP = "/wp-content/uploads/neurogenomic/img/"`.
- Ejecuta `python3 build.py`; los bloques de `elementor/` se regeneran con la ruta nueva.

No uses la Biblioteca de medios para esto: renombra los archivos y los reparte en carpetas por mes, y la demo necesita los 80 cuadros con sus nombres exactos.

---

## 3. Encabezado y pie de página (Theme Builder · Elementor Pro)

### Encabezado
1. Ve a **Plantillas → Theme Builder → Encabezado → Añadir nuevo**.
2. Cierra la biblioteca de diseños prediseñados. Agrega un **Contenedor**:
   - Ancho: *Ancho completo*.
   - Relleno: 0 por los 4 lados.
   - Espacio entre elementos (gap): 0.
3. Dentro del contenedor, arrastra un widget **HTML** y pega el contenido completo de **`elementor/00-global-nav.html`**.
4. Pulsa **Publicar** y, en *Condiciones*, elige **Todo el sitio**.

### Pie de página
1. Ve a **Theme Builder → Pie de página → Añadir nuevo** y crea el mismo contenedor (ancho completo, relleno 0).
2. Agrega un widget **HTML** con **`elementor/18-footer.html`**.
3. Publica con la condición **Todo el sitio**.

> En el editor, el menú y las animaciones pueden verse quietos: Elementor desactiva el scroll suave y los efectos mientras editas. Revisa siempre con **Vista previa** o en la página publicada.

---

## 4. Crear las páginas

Crea 4 páginas (Páginas → Añadir nueva) con estos **títulos y slugs**:

| Página | Slug | Plantilla de página |
|---|---|---|
| Inicio | `inicio` (luego la marcas como portada) | Elementor Ancho completo |
| Servicios | `servicios` | Elementor Ancho completo |
| Tecnología | `tecnologia` | Elementor Ancho completo |
| Contacto | `contacto` | Elementor Ancho completo |

- La plantilla **Elementor Ancho completo** (*Elementor Full Width*) mantiene el encabezado y el pie del Theme Builder. **No uses *Elementor Canvas***, porque los oculta.
- Después ve a **Ajustes → Lectura → Tu página de inicio muestra → Una página estática** y elige *Inicio*.
- Crea también las páginas **Privacidad y ética** (`privacidad`) y **Términos de uso** (`terminos`). Ya están enlazadas en el pie y en los formularios.

### Cómo se pega cada bloque
En cada página, con **Editar con Elementor**:
1. Agrega un **Contenedor** con ancho completo, relleno 0, gap 0 y sin fondo.
2. Dentro, agrega un widget **HTML** por cada bloque, uno debajo del otro, en el orden de la tabla siguiente. Abre cada `.html` con un editor de texto (Bloc de notas, VS Code), copia **todo** y pégalo.
3. No agregues *Efectos de movimiento* ni *Animaciones de entrada* de Elementor a estos contenedores. Las animaciones ya vienen en los bloques y esos efectos pueden romper la capa 3D fija.

### Orden de bloques por página

**Inicio** (los números corresponden a `elementor/NN-*.html`):

| # | Bloque | Nota |
|---|---|---|
| 01 | `01-s0-preloader` | Pantalla de calibración inicial |
| 02 | `02-historia-3d` | Capa 3D fija «de la neurona al consumidor». **Una sola vez**, antes del hero |
| 03 | `03-hero` | |
| 04 | `04-cap-01-neurona` | |
| 05 | `05-cap-02-senales` | |
| 06 | `06-asi-mira` | Demo cuadro a cuadro (usa `img/seq/`) |
| 07 | `07-packaging` | Botella con mapa de calor |
| 08 | `08-no-se-dice` | |
| 09 | `09-cap-03-datos-ia` | |
| 10 | `10-tecnologia` | |
| 11 | `11-etica` | |
| 12 | `12-cap-04-estrategia` | |
| 13 | `13-servicios-resumen` | |
| 14 | `14-metodo` | |
| 15 | `15-caso` | |
| 16 | `16-cap-05-consumidor` | |
| 17 | `17-cta-final` | Incluye el micro-formulario |

**Servicios:** `19-pagehead-servicios` → `20-servicios` → `14-metodo` → `21-por-que` → `17-cta-final`

**Tecnología:** `22-pagehead-tecnologia` → `08-no-se-dice` → `10-tecnologia` → `23-asi-mira-bolsa` → `07-packaging` → `15-caso` → `11-etica` → `17-cta-final`

**Contacto:** `24-pagehead-contacto` → `25-contacto-formulario`

La numeración de los encabezados de sección (01, 02…) ya viene calculada para el orden del inicio.

---

## 5. Formularios (correo)

El formulario de contacto (`25-contacto-formulario`) y el micro-formulario del cierre (`17-cta-final`) envían a **cristiangm3005@gmail.com** mediante **FormSubmit**. No necesitan plugin.

1. Con el sitio publicado, envía una prueba desde `/contacto/`.
2. Llega un correo **«Activate Form»** de FormSubmit. Ábrelo y pulsa **Activate**. Desde ese momento llegan todas las solicitudes.
3. Si quieres usar otro correo, cámbialo en `build.py` (`FORM_EMAIL`), ejecuta `python3 build.py` y vuelve a pegar los dos bloques.

---

## 6. (Opcional) Versión optimizada con Código personalizado

Cada bloque completo repite las fuentes, los estilos base y el núcleo JS, unos 23 KB por bloque. Funciona igual, pero con Elementor Pro puedes cargarlos una sola vez:

1. Ve a **Elementor → Código personalizado → Añadir nuevo**. Ponle de título «Neurogenomic núcleo».
2. Pega el contenido de **`elementor/ligeros/00-codigo-personalizado.html`**.
3. Elige **Ubicación: `<head>`** y **Prioridad: 1**.
4. Publica con la condición **Todo el sitio**.
5. En las páginas y en el Theme Builder, usa los bloques de **`elementor/ligeros/`** en vez de los de `elementor/`. Tienen los mismos nombres y van en el mismo orden.

> No mezcles: o todo completo (`elementor/`) o núcleo + ligeros (`elementor/ligeros/`). Si mezclas no se rompe nada, pero se pierde el ahorro.

---

## 7. Plugins de caché y optimización

Los plugins que **retrasan o combinan JavaScript** pueden dejar las animaciones quietas. Por ejemplo: WP Rocket, LiteSpeed Cache, Autoptimize, SG Optimizer o Perfmatters.

- Desactiva **«Retrasar la ejecución de JavaScript» / «Delay JS»**, o excluye estos textos: `NG.boot`, `gsap`, `ScrollTrigger`, `lenis`, `three`.
- Desactiva **«Combinar JavaScript en línea»** (*Combine inline JS*).
- Puedes mantener la caché de página y la compresión de imágenes.
- Si usas **Cloudflare**, desactiva **Rocket Loader**.

---

## 8. SEO básico

Con **Yoast SEO** o **Rank Math**, define en cada página:

| Página | Título SEO | Descripción |
|---|---|---|
| Inicio | Neurogenomic · Neuromarketing e IA para decisiones de marca con evidencia | Agencia chilena de neuromarketing e inteligencia biométrica: eye tracking, facial coding y respuesta galvánica cruzados con IA para optimizar marca, campañas, e-commerce y software. |
| Servicios | Servicios · Neurogenomic — Seis servicios, un framework de evidencia | Branding, Business Intelligence, E-commerce, Marketing Digital, SEO y Desarrollo de Software validados con biometría y modelos de IA. |
| Tecnología | Tecnología · Neurogenomic | Eye tracking, facial coding y respuesta galvánica: cómo medimos la atención y la emoción, y el stack con que procesamos cada estudio. |
| Contacto | Contacto · Neurogenomic | Cuéntanos qué quieres evaluar y te proponemos el método adecuado. |

Agrega también una **imagen para redes** (1200 × 630) en los ajustes sociales del plugin.

---

## 9. Lista de verificación final

- [ ] `https://tudominio.cl/img/ng-phone-600.webp` abre la imagen.
- [ ] El encabezado y el pie aparecen en las 4 páginas.
- [ ] En el celular, el botón «Menú» abre y cierra el menú.
- [ ] En el inicio se ven la neurona 3D, los 5 capítulos, la demo cuadro a cuadro y el comparador de la botella.
- [ ] El formulario de contacto y el micro-formulario envían (después de activar FormSubmit).
- [ ] Los enlaces del pie llevan a `/servicios/`, `/tecnologia/`, `/contacto/`, `/privacidad/` y `/terminos/`.
- [ ] No hay scroll horizontal en el celular.
- [ ] En el navegador (F12 → Consola) no aparecen errores en rojo.

### Si algo no se ve
| Síntoma | Causa probable | Solución |
|---|---|---|
| Imágenes vacías | La carpeta `img/` no está en la raíz | Repite el paso 2 o cambia `IMG_WP` |
| Todo estático, sin animaciones | Plugin de optimización retrasando JS | Paso 7 |
| La capa 3D queda cortada o se mueve con la página | Efectos de movimiento de Elementor en el contenedor | Quítalos (paso 4.3) |
| Márgenes blancos a los lados | Relleno del contenedor o tema distinto a Hello Elementor | Relleno 0 y ancho completo; usa Hello Elementor |
| Encabezado duplicado | Encabezado del tema + Theme Builder | Usa Hello Elementor o desactiva el encabezado del tema |
| No puedo guardar el widget HTML | Tu usuario no es administrador | Pide rol de administrador |
