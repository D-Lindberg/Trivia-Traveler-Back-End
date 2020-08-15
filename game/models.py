from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    currency_on_hand = models.FloatField(default=0.00)
    Turns_taken = models.IntegerField(default=0)


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    price = models.FloatField(default=0.00, null=False)
    currency_modifier = models.FloatField(default=0.00, null=False)
    duration = models.IntegerField(default=1)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    code = models.CharField(max_length=2, unique=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    flag_url = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} {self.name}, {self.code}"

    def add_airport(self, IATA_code, other_details):
        airport, created = Airport.objects.get_or_create(
            country=self,
            IATA_code=IATA_code,
            defaults=other_details
        )
        return airport, created


class Flight(models.Model):
    origin = models.ForeignKey(
        'Airport', related_name='departing', on_delete=models.CASCADE)
    destination = models.ForeignKey(
        'Airport', related_name='arriving', on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)
    carrier_code = models.CharField(max_length=5)
    carrier_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=10)
    aircraft_code = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f"\n{self.carrier_name} {self.flight_number}\nOrigin: {self.origin}\nDestination: {self.destination}\nPrice: {self.price}\n"

    class Meta:
        unique_together = ['origin', 'destination',
                           'carrier_name', 'flight_number']


class Airport(models.Model):
    country = models.ForeignKey(
        Country, related_name='airports', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    IATA_code = models.CharField(max_length=4, unique=True, blank=False)
    latitude = models.FloatField(default=0.0, null=False)
    longitude = models.FloatField(default=0.0, null=False)
    timezone_offset = models.CharField(max_length=8, default="0", blank=False)
    flights = models.ManyToManyField('self', through='Flight', through_fields=(
        'origin', 'destination'), symmetrical=False, related_name='other')

    def __str__(self):
        return f"{self.city}, {self.country.name} {self.name}\nIATA code {self.IATA_code}\n"

    def add_departure_flight(self, airportObj, carrier_name, flight_number, other_details):
        flight, created = Flight.objects.get_or_create(
            origin=self,
            destination=airportObj,
            carrier_name=carrier_name,
            flight_number=flight_number,
            defaults=other_details
        )
        return flight, created

    def remove_departure_flight(self, airportObj, carrier_name, flight_number):
        Flight.objects.filter(
            origin=self,
            destination=airportObj,
            carrier_name=carrier_name,
            flight_number=flight_number
        ).delete()
        return

    def get_airports_with_flights_from_here(self):
        return list(set(self.flights.filter(
            arriving__origin=self
        )))

    def get_airports_with_flights_to_here(self):
        return list(set(self.other.filter(
            departing__destination=self
        )))

    def get_all_departing_flights(self):
        return list(self.departing.all())

    def get_all_arriving_flights(self):
        return list(self.arriving.all())

    def get_flights(self):
        flight_list = self.get_all_departing_flights()
        flight_list.extend(self.get_all_arriving_flights())
        return flight_list

    def no_back_tracking(self, previous_airport_IATA_codes):
        return list(self.departing.all()).exclude(IATA_code__in=previous_airport_IATA_codes)


class Inventory(models.Model):
    STATUS_CHOICES = [('av', 'Available'), {'ac', 'Active'}, {'us', 'used'}]
    user = models.ForeignKey(
        CustomUser, related_name='inventory', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, related_name='inventory', on_delete=models.CASCADE)
    turn_purchased = models.IntegerField(default=1, null=False)
    turns_remaining = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='av', blank=False)


class UserFlights(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='itinerary', on_delete=models.CASCADE)
    flight = models.ForeignKey(
        Flight, related_name='manifest', on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    turn_count = models.IntegerField(default=1, null=False)



    class Meta:
        ordering = ['booked_at', 'turn_count']


