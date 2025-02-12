from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """Model representing a car manufacturer."""
    name = models.CharField(max_length=100, verbose_name="Car Make Name")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Model representing a car model under a car make."""
    # Choices for car type
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]

    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=100, verbose_name="Car Model Name")
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV',
         verbose_name="Car Type"
    )
    year = models.IntegerField(
        default=2023,
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
        verbose_name="Manufacturing Year",
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
