
import math


def parse_booking(text):
    if not isinstance(text, str):
        raise ValueError("Booking must be a string.")

    if text.count(":") != 1:
        raise ValueError("Use the format pet:days.")

    pet, days_text = text.split(":")
    pet = pet.strip()
    days_text = days_text.strip()

    if not pet or not days_text:
        raise ValueError("Pet name and stay length are required.")

    try:
        days = float(days_text)
    except ValueError:
        raise ValueError("Stay length must be a number.") from None

    if not math.isfinite(days) or days < 0:
        raise ValueError("Stay length must be finite and non-negative.")

    return pet.title(), days


def stay_average(days_csv):
    if not isinstance(days_csv, str) or not days_csv.strip():
        raise ValueError("Stay lengths must be a non-empty CSV string.")

    parts = days_csv.split(",")

    if any(not part.strip() for part in parts):
        raise ValueError("Empty stay length is not allowed.")

    try:
        values = [int(part.strip()) for part in parts]
    except ValueError:
        raise ValueError("Every stay length must be an integer.") from None

    if any(value < 0 for value in values):
        raise ValueError("Stay lengths must be non-negative.")

    return sum(values) / len(values)


def payable_fee(text):
    if not isinstance(text, str):
        raise ValueError("Fee input must be a string.")

    if text.count("|") != 1:
        raise ValueError("Use the format fee|discount.")

    fee_text, discount_text = text.split("|")
    fee_text = fee_text.strip()
    discount_text = discount_text.strip()

    if not fee_text or not discount_text:
        raise ValueError("Fee and discount are required.")

    try:
        fee = float(fee_text)
        discount = float(discount_text)
    except ValueError:
        raise ValueError("Fee and discount must be numbers.") from None

    if not math.isfinite(fee) or not math.isfinite(discount):
        raise ValueError("Fee and discount must be finite.")

    if fee < 0 or discount < 0:
        raise ValueError("Fee and discount must be non-negative.")

    total = fee * 1.18 - discount
    return max(total, 0.0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    try:
        print("Pet and Days:", parse_booking(user_input))
    except ValueError as error:
        print("Invalid booking:", error)

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    try:
        print("Average Stay:", stay_average(user_input))
    except ValueError as error:
        print("Invalid stay lengths:", error)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    try:
        print("Payable Fee:", payable_fee(user_input))
    except ValueError as error:
        print("Invalid fee:", error)


if __name__ == "__main__":
    main()
