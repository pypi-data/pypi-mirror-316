import json
import os

def _load_countries():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'countries.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_countries():
    """Get all countries information."""
    return _load_countries()

def get_country_by_name(name):
    """Get country information by name."""
    countries = _load_countries()
    return next((country for country in countries if country['name'].lower() == name.lower()), None)

def get_country_by_code(code):
    """Get country information by ISO code."""
    countries = _load_countries()
    return next((country for country in countries if country['code'].lower() == code.lower()), None)
