from django.http import JsonResponse
from .models import BusDetails,Booking,SeatAvailability,Payment

class BusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # When user accesses /buses/ with GET -> return all bus list
        if request.path == "/buses/" and request.method == "GET":
            buses = BusDetails.objects.all().values()
            return JsonResponse(list(buses), safe=False)

        return self.get_response(request)
    
class BookingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/bookings/" and request.method == "GET":
            bookings = Booking.objects.all().values()
            return JsonResponse(list(bookings), safe=False)

        return self.get_response(request)
class SeatCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Handle seat checking
        if request.path == "/check-seat/" and request.method == "GET":

            bus_id = request.GET.get("bus_id")
            seat_number = request.GET.get("seat_number")

            # Validate fields
            if not bus_id or not seat_number:
                return JsonResponse({
                    "error": "bus_id and seat_number are required"
                }, status=400)

            # Check if seat is booked
            seat_booked = Booking.objects.filter(
                bus_id=bus_id,
                seat_number=seat_number
            ).exists()

            if seat_booked:
                return JsonResponse({
                    "seat_available": False,
                    "message": f"Seat {seat_number} is already BOOKED"
                }, status=200)

            return JsonResponse({
                "seat_available": True,
                "message": f"Seat {seat_number} is AVAILABLE"
            }, status=200)

        return self.get_response(request)
    
class PaymentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/make_payment/" and request.method == "GET":
            from .models import Payment
            payments = Payment.objects.all().values()
            return JsonResponse(list(payments), safe=False)

        return self.get_response(request)
