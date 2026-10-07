"""
Generates realistic SAMPLE business listings (not real businesses).
Use this when scraping is blocked or to top up your dataset to 500+.
Rows are labelled source = "Sample Data" so it is clearly disclosed.

Run:  python mock_data.py   ->  creates listings_mock.csv
"""
import csv
import random
from faker import Faker

fake = Faker("en_IN")
random.seed(42)

CITIES = ["Kolkata", "Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Pune", "Jaipur"]
CATEGORIES = ["Restaurant", "Gym", "Salon", "Dentist", "Pharmacy", "Coaching Centre", "Hotel", "Electronics Shop"]
SUFFIX = {
    "Restaurant": ["Kitchen", "Bistro", "Dhaba", "Cafe"],
    "Gym": ["Fitness", "Gym", "Fit Zone"],
    "Salon": ["Salon", "Beauty Studio", "Unisex Salon"],
    "Dentist": ["Dental Clinic", "Dental Care"],
    "Pharmacy": ["Pharmacy", "Medicos", "Chemist"],
    "Coaching Centre": ["Academy", "Classes", "Institute"],
    "Hotel": ["Residency", "Inn", "Hotel"],
    "Electronics Shop": ["Electronics", "Digital Hub", "Mobile Store"],
}


def make_row():
    category = random.choice(CATEGORIES)
    city = random.choice(CITIES)
    name = f"{fake.last_name()} {random.choice(SUFFIX[category])}"
    address = f"{fake.building_number()}, {fake.street_name()}, {city}"
    phone = f"+91 {random.choice('6789')}{random.randint(10**8, 10**9 - 1)}"
    return {
        "business_name": name,
        "category": category,
        "city": city,
        "address": address,
        "phone": phone,
        "source": "Sample Data",
    }


def generate(n=300, path="listings_mock.csv"):
    rows = [make_row() for _ in range(n)]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {n} rows to {path}")


if __name__ == "__main__":
    generate()
