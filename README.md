<img width="512" height="512" alt="logo" src="https://github.com/user-attachments/assets/36016caa-0d8d-453f-9330-d4e937c5bb7d" />

# CAM Vs Calandracos

Este pequeño juego web se inspira en el género de "defensa de la base" para recrear un escenario donde la Alcaldía de Cali es atacada por zombis en sus diferentes formas políticas. El trabajo del jugador es evitar que lleguen hasta el edificio principal y conviertan a los funcionarios públicos y contratistas en calandracos.

Se puede jugar desde **smartphones y computadores**, directamente en el navegador.

## Cómo se juega

- Tienes **60 segundos** y un presupuesto inicial para montar tu defensa antes de la primera horda.
- Los humanos (en blanco) se refugian en el CAM. Los enemigos (en rojo) vienen por ellos, del más débil al más fuerte: **calandraco, veedor, líder comunal, edil y concejal**.
- Cuanto más resistas, más sube tu presupuesto... y más grandes son las hordas.
- Pierdes si cae el edificio o si todos los humanos son infectados.

### Defensas

Muro · Mina · Policía · Torreta de bala · Antimotines · Soldado · Torreta de fuego · Francotirador · Torre

Las armas se quedan sin munición (hay que recargarlas), se pueden **mejorar hasta nivel 3**, y cada 5 hordas eliges **una mejora entre tres cartas**.

### Dificultad

Cinco niveles, de **Normal** a **Infernal**. La diferencia es el tamaño de las hordas.

### Controles

| | PC | Celular |
|---|---|---|
| Elegir defensa | `1`-`9` o clic en la barra | Tocar la barra |
| Colocar | Clic | Tocar el mapa |
| Dibujar muros | Arrastrar | Arrastrar |
| Vender / Mejorar / Recargar | `V` / `U` / `R` (`T` recarga todo) | Botones de la barra |
| Zoom y mover | Rueda, `+`/`-`, flechas | Pellizcar y arrastrar con dos dedos |
| Pausa / sonido | `Espacio` / `M` | Botones de arriba |

En celular, juega en **horizontal**.

## El mapa

El mapa es la zona real del Centro Administrativo Municipal de Cali, construido con datos de OpenStreetMap: calles, parques, río y los edificios que están mapeados. Los enemigos solo caminan por calles, plazas y pasto. Las manzanas sin datos se rellenan con edificios generados.

## Correrlo en local

Es un sitio estático (sin dependencias). Necesita servirse por HTTP porque carga `map-data.js`.

```bash
python -m http.server 8765
```

Luego abre `http://localhost:8765`. En Windows también puedes hacer doble clic en `servir.bat`, que además muestra la dirección para probar desde el celular (misma red WiFi).

## Despliegue

Sube `index.html`, `map-data.js` y las imágenes (`logo.*`, `favicon.png`, `apple-touch-icon.png`) a un repositorio y conéctalo a [Vercel](https://vercel.com). No necesita configuración ni comando de build.

## Regenerar el mapa

`bake_map.py` convierte un JSON de Overpass (OpenStreetMap, `out geom`) en `map-data.js`:

```bash
python bake_map.py osm.json
```

## Créditos

- Datos del mapa: © colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright), bajo licencia ODbL.
- Arte de personajes pixelado y sonidos generados por código.
