from game.data.airport_seed_data import airport_list
from game.models import Airport, Country
import random


def build_airports():
    airports = []
    for airport in airport_list:
        print(airport)
        country_code = airport['country_code']
        IATA_code = airport['code']
        try:
            country = Country.objects.get(code=country_code)
        except:
            print("country does not exist.")
            continue
        data = {
            'name': airport['name'],
            'city': airport['CITY'],
            'latitude': airport['lat'],
            'longitude': airport['lon'],
            'timezone_offset': airport['timezoneoffset']
        }
        ap, created = country.add_airport(IATA_code, data)
        if created:
            airports.append(ap)
            print(ap.IATA_code, "added to DB.")
        else:
            print("error adding to database.")
    return airports


def calculate_price(y1, x1, y2, x2):
    x_dist = abs(x2 - x1)
    lateral_travel = x_dist if (x_dist < 180) else (180-(x_dist - 180))
    vertical_travel = abs(y2 - y1)
    distance = lateral_travel + vertical_travel
    time = distance * 8
    hours = int(time // 60)
    minutes = int(time % 60)
    duration = f"PT{hours:02d}H{minutes:02d}M"
    price = int(distance * 20)
    return (duration, price)


def build_flights():
    aircrafts = [
        "Boeing 737", "Boeing 747", "Cessna 172",
        "Airbus A320", "Airbus Voyager KC2", "Eclipse 500",
        "Cessna 208 Caravan", "Beechcraft Starship",
        "Gossamer Albatross", "Beech Baron", "Cessna Mustang",
        "Quicksilver MX-2", "Gulfstream G650",
        "Beechcraft King Air"
    ]
    flights = []
    origins = list(Airport.objects.all())
    destinations = list(Airport.objects.all())
    for i, origin in enumerate(origins):
        for destination in destinations[i:]:
            if origin.IATA_code == destination.IATA_code:
                continue
            duration, price = calculate_price(
                origin.latitude, origin.longitude, destination.latitude, destination.longitude)
            code = "LIMAS"
            carrier = "Lima Platoon Airlines"
            aircraft = random.choice(aircrafts)
            other_details = {
                'duration': duration,
                'carrier_code': code,
                'aircraft_code': aircraft,
                'price': price
            }
            flight = f"{destination.id}{origin.id:02d}A"
            new_flight, created = origin.add_departure_flight(
                destination, carrier, flight, other_details)
            if created:
                flights.append(new_flight)
            flight = f"{origin.id}{destination.id:02d}B"
            new_flight, created = destination.add_departure_flight(
                origin, carrier, flight, other_details)
            if created:
                flights.append(new_flight)
        print("Added all outbound and return flights to this airport:",origin.IATA_code)
    return flights

