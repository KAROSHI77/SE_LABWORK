
"""Restaurant dining order billing and kitchen ticket manager."""

import hashlib
import json
import secrets
from pathlib import Path
from typing import Any

ORDERS: dict[str, dict[str, Any]] = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}
ITEM_PRICE = 15.0


def place_table_order(
    table_id: str,
    guest: str,
    items_count: int,
    order_log: list[str] | None = None,
) -> bool:
    """Create a new table order and optionally add an entry to a log."""
    if table_id in ORDERS or items_count <= 0 or not guest.strip():
        return False

    ORDERS[table_id] = {
        "guest": guest.strip(),
        "items": items_count,
        "bill": round(ITEM_PRICE * items_count, 2),
        "is_settled": False,
    }
    if order_log is not None:
        order_log.append(
            f"Created order for {table_id} with {items_count} dishes"
        )
    return True


def void_table_order(table_id: str) -> bool:
    """Remove an order if it exists and report whether it was removed."""
    return ORDERS.pop(table_id, None) is not None


def check_table_status(table_id: str) -> bool:
    """Return True if a table exists and its bill is unsettled."""
    order = ORDERS.get(table_id)
    return order is not None and not order["is_settled"]


def calculate_discounted_bill(
    table_id: str,
    discount_percent: float,
) -> float:
    """Calculate the bill after validating a percentage discount."""
    if table_id not in ORDERS:
        raise KeyError(f"Unknown table: {table_id}")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100 percent.")

    base_bill = float(ORDERS[table_id]["bill"])
    return round(base_bill * (1 - discount_percent / 100), 2)


def generate_ticket_hash(table_id: str) -> str:
    """Return a SHA-256 digest of a ticket identifier."""
    return hashlib.sha256(table_id.encode("utf-8")).hexdigest()


def generate_pos_pin() -> str:
    """Generate a four-digit PIN with a secure random generator."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def export_kitchen_orders(
    filename: str = "kitchen_orders.txt",
) -> None:
    """Export unsettled orders as JSON for the kitchen."""
    active_orders = {
        table_id: order
        for table_id, order in ORDERS.items()
        if not order["is_settled"]
    }
    output_path = Path(filename)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(active_orders, output_file, indent=2)
        output_file.write("\n")
    print(f"Kitchen orders exported to {output_path}")


def get_pending_summary(
    order_data: dict[str, dict[str, Any]],
) -> int:
    """Count orders that have not been settled."""
    return sum(
        not details["is_settled"] for details in order_data.values()
    )


def main() -> None:
    """Run sample restaurant billing operations."""
    discount_input = input("Discount percentage [10]: ").strip()
    try:
        discount_percent = (
            10.0 if not discount_input else float(discount_input)
        )
    except ValueError:
        print("Invalid discount. Using the default 10%.")
        discount_percent = 10.0

    try:
        place_table_order("T4", "Olivia", 2)
        void_table_order("T2")
        print("Is T1 pending:", check_table_status("T1"))
        print(
            "Discounted Bill:",
            calculate_discounted_bill("T1", discount_percent),
        )
        print("Ticket Hash:", generate_ticket_hash("T1"))
        print("POS PIN:", generate_pos_pin())
        export_kitchen_orders()
        print("Pending tables:", get_pending_summary(ORDERS))
    except (KeyError, ValueError, OSError) as error:
        print(f"Could not complete the restaurant operation: {error}")


if __name__ == "__main__":
    main()
