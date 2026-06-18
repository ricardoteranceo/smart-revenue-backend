from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Smart Revenue Systems B2B - Motor Calibrado Ricardo")

# Configuración estricta de dominios autorizados (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://smartrevenue.schomarclub.com",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estructura de datos que espera recibir el servidor
class PriceRequest(BaseModel):
    hotel_id: str
    base_price: float
    occupancy: float
    lat: float = 0.0
    lon: float = 0.0
    city: str = "Quito"
    room_type: str = "Doble"
    hotel_website: str = ""
    available_services: list = []

@app.post("/api/v1/calculate-price")
async def calculate_price(request: PriceRequest):
    # 1. Recuperar variables enviadas por la interfaz web
    occupancy = request.occupancy
    base_price = request.base_price
    city = request.city or "Quito"
    available_services = request.available_services or ["restaurante", "spa", "bar_lounge"]

    # 2. Algoritmo base de Revenue Management
    optimal_price = base_price
    increase_percentage = 0
    
    if occupancy < 40:
        optimal_price = base_price * 0.90  # Descuento del 10% por baja demanda
        increase_percentage = -10
    elif occupancy > 75:
        optimal_price = base_price * 1.20  # Incremento del 20% por alta demanda
        increase_percentage = 20

    # 3. Lógica del Evento Fijo de la Ciudad (Quito)
    event_name = "Megaconcierto Iron Maiden & Judas Priest"
    event_date = datetime(2026, 12, 10)
    today = datetime.now()
    days_left = (event_date - today).days
    weekday = today.weekday()  # 0=Lunes, 6=Domingo

    # 4. Mensajes comerciales dinámicos según el día de la consulta
    if days_left > 30:
        if weekday in [0, 1, 2]:  # Lunes, Martes, Miércoles
            marketing_advice = f"Faltan {days_left} días para el evento. Enfoque corporativo de inicio de semana: Bloquea tarifas preventa exclusivas para socios comerciales de Schomar Club."
        else:  # Jueves, Viernes, Sábado, Domingo
            marketing_advice = f"¡Planificación de fin de semana! Faltan {days_left} días para el concierto. Lanza campañas de marketing digital apuntando a paquetes turísticos familiares."
    else:
        marketing_advice = f"⚠️ ¡ALERTA CRÍTICA! Faltan solo {days_left} días para el evento. Sube tarifas base un 15% y exige un mínimo de 2 noches de estadía obligatoria."

    # Si hay un gran evento en la ciudad, el algoritmo infla un extra el precio óptimo
    if city.lower() == "quito" and days_left > 0:
        optimal_price = optimal_price * 1.15
        increase_percentage += 15

    # 5. Motor Inteligente de Venta Cruzada (Cross-Selling)
    upselling_packages = []

    if "restaurante" in available_services or "bar_lounge" in available_services:
        upselling_packages.append({
            "title": "Experiencia Pre-Party Rock",
            "description": "Incluye transporte exclusivo de ida al concierto + un cóctel temático de bienvenida en el bar del hotel antes del show por $15 adicionales por huésped."
        })
    
    if "spa" in available_services:
        upselling_packages.append({
            "title": "Paquete Relax Post-Concierto",
            "description": "Añadir un 20% de descuento en masajes de desintoxicación y relajación en el Spa del hotel para la mañana siguiente al evento."
        })

    # Estructura del evento cercano para pintar en la interfaz
    city_events = [
        {
            "name": event_name,
            "date": event_date.strftime("%Y-%m-%d"),
            "impact": "Alto",
            "description": f"Concierto internacional masivo en Quito. Faltan {days_left} días."
        }
    ] if city.lower() == "quito" else []

    # Respuesta unificada que consume el Frontend
    return {
        "optimal_price": round(optimal_price, 2),
        "increase_percentage": increase_percentage,
        "marketing_advice": marketing_advice,
        "city_events": city_events,
        "upselling_packages": upselling_packages
    }
