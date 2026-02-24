import requests
import pandas as pd

# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = "https://world.openfoodfacts.org/cgi/search.pl"
PARAMS = {
    "search_terms": "energy drink caffeine",
    "action": "process",
    "json": 1,
    "page_size": 20,
    "fields": "product_name,nutriments"
}

# ============================================================
# PASO 1: LLAMADA A LA API DE OPEN FOOD FACTS
# ============================================================

response = requests.get(URL, params=PARAMS, timeout=10)

if response.status_code == 200:
    data = response.json()
    products = data.get("products", [])
    print(f"Productos obtenidos de la API: {len(products)}")

    # Extraer nombre y cafeína de cada producto
    records = []
    for p in products:
        caffeine = p.get("nutriments", {}).get("caffeine_100g")
        if caffeine:
            records.append({
                "product_name": p.get("product_name", "Unknown"),
                "caffeine_per_100ml": float(caffeine)
            })

    df_api = pd.DataFrame(records)
    print(df_api)

else:
    print(f"Error en la solicitud: {response.status_code}")
    # Tabla de referencia validada como fallback
    df_api = pd.DataFrame([
        {"product_name": "Water / No caffeine",          "caffeine_per_100ml": 0},
        {"product_name": "Herbal Tea",                   "caffeine_per_100ml": 5},
        {"product_name": "Green Tea / Black Tea",        "caffeine_per_100ml": 35},
        {"product_name": "Instant Coffee / Espresso",   "caffeine_per_100ml": 80},
        {"product_name": "Red Bull / Monster Energy",   "caffeine_per_100ml": 34},
        {"product_name": "Cold Brew / Bang Energy",     "caffeine_per_100ml": 150},
        {"product_name": "5-hour Energy / Multi-drinks","caffeine_per_100ml": 200},
    ])

# ============================================================
# PASO 2: ASIGNAR FUENTE DE CAFEÍNA A CADA ESTUDIANTE
# ============================================================

def assign_caffeine_source(mg):
    if mg == 0:        return "Water / No caffeine",         "none",      "none"
    elif mg <= 30:     return "Herbal Tea",                  "very_low",  "low"
    elif mg <= 80:     return "Green Tea / Black Tea",        "low",       "low"
    elif mg <= 150:    return "Instant Coffee / Espresso",   "medium",    "moderate"
    elif mg <= 250:    return "Red Bull / Monster Energy",   "medium",    "moderate"
    elif mg <= 350:    return "Cold Brew / Bang Energy",     "high",      "high"
    else:              return "5-hour Energy / Multi-drinks","very_high", "very_high"

# ============================================================
# PASO 3: CARGAR DATASET, ENRIQUECER Y GUARDAR
# ============================================================

df = pd.read_csv("student_productivity_distraction_dataset_20000.csv")

results = df['coffee_intake_mg'].apply(assign_caffeine_source)
df['caffeine_source']     = results.apply(lambda x: x[0])
df['caffeine_category']   = results.apply(lambda x: x[1])
df['caffeine_risk_level'] = results.apply(lambda x: x[2])

df.to_csv("student_productivity_enriched.csv", index=False)
print(f"\nDataset enriquecido guardado: {df.shape}")
print(df['caffeine_category'].value_counts())
