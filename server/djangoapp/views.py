from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from datetime import datetime

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Logger instance
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle user login."""
    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        response_data = {
            "userName": username,
            "status": "Authenticated" if user else "Failed",
        }

        if user:
            login(request, user)

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        logger.error(f"Login error: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


def logout_request(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({"username": ""})


def get_cars(request):
    """Retrieve car models and manufacturers."""
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})


@csrf_exempt
def registration(request):
    """Handle user registration."""
    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"userName": username, "error": "Already Registered"},
                status=400,
            )

        # Create and login user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)

        return JsonResponse({"userName": username, "status": "Authenticated"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


def get_dealerships(request, state="All"):
    """Fetch list of dealerships."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)

    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Retrieve dealer reviews with sentiment analysis."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail["review"])
        review_detail["sentiment"] = response.get("sentiment")

    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    """Fetch specific dealer details."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)

    return JsonResponse({"status": 200, "dealer": dealership})


def add_review(request):
    """Submit a new review."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"}, status=403)

    try:
        data = json.loads(request.body)
        post_review(data)

        return JsonResponse({"status": 200})

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": 400, "message": "Invalid JSON format"}, status=400
        )
    except Exception as e:
        logger.error(f"Error posting review: {e}")
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"}, status=401
        )
