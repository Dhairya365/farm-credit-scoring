from django.db import models


class CreditScoreResult(models.Model):
    city = models.CharField(max_length=100, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    ph = models.FloatField()
    organic_carbon = models.FloatField()

    soil_rating = models.FloatField()
    weather_condition = models.CharField(max_length=50)
    weather_score = models.FloatField()
    regional_score = models.FloatField()

    farm_size = models.FloatField()
    farm_score = models.FloatField()
    final_score = models.FloatField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Credit Score: {self.final_score}"
