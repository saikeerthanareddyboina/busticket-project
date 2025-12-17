from django.db import models

class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

class BusDetails(models.Model):
    bus_name = models.CharField(max_length=100)
    travel_company = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

class Booking(models.Model):
    SEAT_TYPES = (
        ("SEATER", "Seater"),
        ("SLEEPER", "Sleeper"),
    )

    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPES)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, default="CONFIRMED")

class SeatAvailability(models.Model):
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    passenger_name = models.CharField(max_length=100)
    passenger_phone = models.CharField(max_length=15)

class Payment(models.Model):
    PAYMENT_MODES = (
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("NETBANKING", "Net Banking"),
        ("WALLET", "Wallet")
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    payment_status = models.CharField(max_length=20, default="PENDING")  # PENDING / SUCCESS / FAILED
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)



class BusTicket(models.Model):
    passenger_name = models.CharField(max_length=100)
    bus_name = models.CharField(max_length=100)
    seat_no = models.CharField(max_length=10)
    travel_date = models.DateField()
    price = models.FloatField()

