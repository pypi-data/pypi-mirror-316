# Countries Info

A comprehensive Python library for accessing detailed country information including names, codes, capitals, continents, population, and area.

## Installation

```bash
pip install countries-info-mg
```

## Usage

```python
from countries_info import get_all_countries, get_country_by_name, get_country_by_code

# Get all countries
countries = get_all_countries()

# Get country by name
france = get_country_by_name("France")

# Get country by code
usa = get_country_by_code("US")
```

## Features

- Get detailed information about countries
- Search countries by name or code
- Access data about:
  - Official names
  - Country codes
  - Capitals
  - Continents
  - Population
  - Area
  - And more!

## Data Structure

Each country object contains:
```python
{
    "name": str,           # Country name
    "code": str,           # ISO 2-letter code
    "capital": str,        # Capital city
    "continent": str,      # Continent
    "population": int,     # Population
    "area": float,         # Area in square kilometers
}
```

## License

MIT License
