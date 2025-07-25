from faker import Faker
from datetime import datetime

SUPPORTED_TYPES = {"name", "integer", "email", "phone_number", "address", "date"}

fake = Faker()

def generate_data(schema, count):
    """
    Generate test data based on schema and count.
    schema: dict mapping field names to {type, ...}
    count: number of records to generate
    Returns: list of dicts
    """
    data = []
    for _ in range(count):
        row = {}
        for field, spec in schema.items():
            ftype = spec.get("type")
            if ftype not in SUPPORTED_TYPES:
                raise ValueError(f"Unsupported field type: {ftype} for field '{field}'. Supported types: {', '.join(SUPPORTED_TYPES)}")
            if ftype == "name":
                row[field] = fake.name()
            elif ftype == "integer":
                minv = spec.get("min", 0)
                maxv = spec.get("max", 100)
                row[field] = fake.random_int(min=minv, max=maxv)
            elif ftype == "email":
                row[field] = fake.email()
            elif ftype == "phone_number":
                row[field] = fake.phone_number()
            elif ftype == "address":
                row[field] = fake.address().replace("\n", ", ")
            elif ftype == "date":
                start = spec.get("start", "1970-01-01")
                end = spec.get("end", "2000-12-31")
                try:
                    start_date = datetime.strptime(start, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError(f"Invalid date format for field '{field}'. Use YYYY-MM-DD.")
                row[field] = str(fake.date_between(start_date=start_date, end_date=end_date))
        data.append(row)
    return data 