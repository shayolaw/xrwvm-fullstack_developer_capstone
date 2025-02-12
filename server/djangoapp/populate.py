from .models import CarMake, CarModel


def initiate():
    """Populate database with CarMake and CarModel instances."""

    # Car make data
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    # Create CarMake instances using bulk_create
    car_makes = CarMake.objects.bulk_create([
        CarMake(name=data["name"], description=data["description"])
        for data in car_make_data
    ])

    # Map car make names to instances for easy lookup
    car_make_lookup = {car_make.name: car_make for car_make in car_makes}

    # Car model data
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": "NISSAN"},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": "NISSAN"},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": "NISSAN"},
        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "E-Class", "type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "A4", "type": "SUV", "year": 2023, "car_make": "Audi"},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": "Audi"},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": "Audi"},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": "Kia"},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": "Kia"},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": "Kia"},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": "Toyota"},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": "Toyota"},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": "Toyota"},
    ]

    # Create CarModel instances using bulk_create
    CarModel.objects.bulk_create([
        CarModel(
            name=data["name"],
            car_make=car_make_lookup[data["car_make"]],
            type=data["type"],
            year=data["year"]
        )
        for data in car_model_data
    ])
