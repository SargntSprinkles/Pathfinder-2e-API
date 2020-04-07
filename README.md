# Pathfinder-2e-API

## Purpose
Provide a standardized set of Pathfinder Second Edition data for community use.

## Goals
- Fast
- Lightweight
- Current

## Data Source
The API gets its data from the official SRD - [Archives of Nethys](http://2e.aonprd.com/). It caches data it retrieves for 20 minutes, which is tracked per item (e.g. the Human Ancestry will go stale separately from the Dwarf Ancestry).

## How to Use V1
Access (url)/api/v1/(resource)?(options)

### Ancestries
(resource) = ancestries

Options:
- name
    - Not case sensitive
    - (url)/api/v1/ancestries?name=dwarf
    - (url)/api/v1/ancestries?name=dWaRF


## Running Locally
1. Navigate to the repo directory and execute:
    ```bash
    python3 api.py
    ```

1. Open a browser and point it to [http://localhost:5000](http://localhost:5000)