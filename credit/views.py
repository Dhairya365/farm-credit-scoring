from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CreditScoreResult
from .serializers import CreditScoreResultSerializer
from .credit_utils import (
    fetch_weather_data,
    fetch_weather_by_coordinates,
    calculate_soil_fertility,
    get_weather_risk_score,
    get_regional_factor,
    get_farm_size_score,
    calculate_credit_score
)


@api_view(['POST'])
def calculate_credit_api(request):
    data = request.data

    try:
        # Required fields
        required_fields = [
            "nitrogen", "phosphorus", "potassium",
            "ph", "organic_carbon", "farm_size"
        ]

        for field in required_fields:
            if data.get(field) in [None, ""]:
                return Response(
                    {"error": f"Missing or empty field: {field}"},
                    status=400
                )

        soil_health = {
            "Nitrogen": float(data["nitrogen"]),
            "Phosphorus": float(data["phosphorus"]),
            "Potassium": float(data["potassium"]),
            "pH": float(data["ph"]),
            "Organic_Carbon": float(data["organic_carbon"])
        }

        farm_size = float(data["farm_size"])

        city = data.get("city")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Location handling
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            weather_condition, temperature, humidity = fetch_weather_by_coordinates(
                latitude, longitude
            )
            regional_score = 1.0  # placeholder (documented GIS logic)

        elif city:
            weather_condition, temperature, humidity = fetch_weather_data(city)
            regional_score = get_regional_factor(city)

        else:
            return Response(
                {"error": "Provide either city or latitude & longitude"},
                status=400
            )

        if weather_condition is None:
            return Response(
                {"error": "Weather data fetch failed"},
                status=400
            )

        # Scoring
        soil_rating = calculate_soil_fertility(soil_health)
        weather_score = get_weather_risk_score(weather_condition)
        farm_score = get_farm_size_score(farm_size)

        final_score = calculate_credit_score(
            soil_rating,
            weather_score,
            regional_score,
            farm_score
        )

        # Save result
        result = CreditScoreResult.objects.create(
            city=city,
            latitude=latitude,
            longitude=longitude,
            nitrogen=soil_health["Nitrogen"],
            phosphorus=soil_health["Phosphorus"],
            potassium=soil_health["Potassium"],
            ph=soil_health["pH"],
            organic_carbon=soil_health["Organic_Carbon"],
            soil_rating=soil_rating,
            weather_condition=weather_condition,
            weather_score=weather_score,
            regional_score=regional_score,
            farm_size=farm_size,
            farm_score=farm_score,
            final_score=final_score
        )

        serializer = CreditScoreResultSerializer(result)
        return Response(serializer.data)

    except ValueError as ve:
        return Response({"error": str(ve)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
