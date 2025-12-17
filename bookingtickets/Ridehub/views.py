from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails,BusDetails,Booking,SeatAvailability,Payment,BusTicket
import uuid


def Ride(request):
    return HttpResponse("WELCOME TO RIDEBUS  HAPPY JOURNEY  AND SAFE JOURNEY !!!😊")

#Query parameters#
def bus_info(request):
    bus=request.GET.get("bus")
    data=request.GET.get("data")
    return JsonResponse({"status":"success","result":{"bus_name":bus,"offers":data}},status=200)
#userdetails#

@csrf_exempt
def Users_details(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        # Save to database
        user = UserDetails.objects.create(
            name=name,
            email=email,
            phone=phone
        )

        return JsonResponse({
            "status": "success",
            "message": "User details saved",
            "user_id": user.id,
            "name": name,
            "email": email,
            "phone": phone
        }, status=200)
    
@csrf_exempt

def bus_list(request):
    if request.method == "POST":
        data = json.loads(request.body)

        bus_name = data.get("bus_name")
        travel_company = data.get("travel_company")
        source = data.get("source")
        destination = data.get("destination")
        departure_time = data.get("departure_time")
        arrival_time = data.get("arrival_time")

        bus = BusDetails.objects.create(
            bus_name=bus_name,
            travel_company=travel_company,
            source=source,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time
        )
        return JsonResponse({
            "status": "success",
            "message": "Bus details saved",
            "bus_id": bus.id,
            "bus_name": bus_name,
            "travel_company": travel_company,
            "source": source,
            "destination": destination,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
        }, status=200)

    # GET → Return all bus data
    elif request.method == "GET":
        buses = BusDetails.objects.all().values()
        return JsonResponse(list(buses), safe=False, status=200)
    
@csrf_exempt
def busbooking(request):

    if request.method == "POST":
        data = json.loads(request.body)

        user_id = data.get("user_id")
        bus_id = data.get("bus_id")
        seat_number = data.get("seat_number")
        seat_type = data.get("seat_type")   # SEATER / SLEEPER
        booking_date = data.get("booking_date")

        # Check missing data
        if not all([user_id, bus_id, seat_number, seat_type, booking_date]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Validate seat type
        if seat_type not in ["SEATER", "SLEEPER"]:
            return JsonResponse({"error": "seat_type must be SEATER or SLEEPER"}, status=400)

        user = UserDetails.objects.get(id=user_id)
        bus = BusDetails.objects.get(id=bus_id)

        # Check if seat is already booked
        seat_taken = Booking.objects.filter(
            bus=bus,
            seat_number=seat_number,
            booking_date=booking_date
        ).exists()

        if seat_taken:
            return JsonResponse({
                "status": "failed",
                "message": f"Seat {seat_number} is already booked!"
            }, status=409)

        # Create booking
        booking = Booking.objects.create(
            user=user,
            bus=bus,
            seat_number=seat_number,
            seat_type=seat_type,
            booking_date=booking_date
        )

        return JsonResponse({
            "status": "success",
            "message": "Seat booked successfully!",
            "booking_id": booking.id,
            "seat_number": seat_number,
            "seat_type": seat_type
        }, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def check_seat(request, bus_id, seat_number):
    exists = Booking.objects.filter(bus_id=bus_id, seat_number=seat_number).exists()

    if exists:
        return JsonResponse({
            "seat_available": False,
            "message": "Seat already booked"
        })

    return JsonResponse({
        "seat_available": True,
        "message": "Seat is available"
    })
@csrf_exempt
def make_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        booking_id = data.get("booking_id")
        amount = data.get("amount")
        payment_mode = data.get("payment_mode")

        booking = Booking.objects.get(id=booking_id)

        pay = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_mode=payment_mode,
            payment_status="SUCCESS",
            transaction_id=str(uuid.uuid4())
        )

        # ✅ CREATE TICKET
        ticket = BusTicket.objects.create(
            passenger_name=booking.user.name,
            bus_name=booking.bus.bus_name,
            seat_no=booking.seat_number,
            travel_date=booking.booking_date,
            price=amount
        )

        return JsonResponse({
            "message": "Payment successful",
            "ticket_id": ticket.id,
            "payment_id": pay.id
        }, status=201)

@csrf_exempt
def update_ticket(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)

        ticket = BusTicket.objects.filter(id=id).first()
        if not ticket:
            return JsonResponse({"error": "Ticket not found"}, status=404)

        ticket.passenger_name = data.get("passenger_name", ticket.passenger_name)
        ticket.bus_name = data.get("bus_name", ticket.bus_name)
        ticket.seat_no = data.get("seat_no", ticket.seat_no)
        ticket.travel_date = data.get("travel_date", ticket.travel_date)
        ticket.price = data.get("price", ticket.price)

        ticket.save()
        return JsonResponse({"message": "Ticket Updated Successfully"}, status=200)

    return JsonResponse({"error": "Only PUT method allowed"}, status=405)

@csrf_exempt
def delete_ticket(request, id):
    if request.method == "DELETE":
        ticket = BusTicket.objects.filter(id=id).first()

        if ticket is None:
            return JsonResponse({"error": "Ticket Not Found"}, status=404)

        ticket.delete()
        return JsonResponse({"message": "Ticket Deleted Successfully"})

    return JsonResponse({"error": "Invalid Request Method"}, status=400)
