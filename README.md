# Simple Vector Tiles

A minimal setup to serve OpenStreetMap vector tiles from a local `.pbf` extract using Docker.

## Quick Start

### 1. Download an OSM Extract
Go to [Geofabrik](https://download.geofabrik.de/) and download a `.osm.pbf` file for your desired region.

Place the file into the `data/` folder:

### 2. Start the Server

```bash
docker-compose up
```

### 3. View the Map

Once the server is running, open your browser and navigate to:

```
http://localhost:80
```

## Project Structure

```
.
├── data/                 # Drop your .osm.pbf file here
├── docker-compose.yml    # Launches the tile server stack
└── ...
```

## Requirements

- Docker
- Docker Compose

## Tile Access

Vector tiles are served from:

```
http://localhost:80
```
