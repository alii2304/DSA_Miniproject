from collections import deque
from datetime import datetime
import math

# Smart Parking Management System
TOTAL_SLOTS = 10
RATE_PER_HOUR = 20

# Data structures
parking_slots = [None] * TOTAL_SLOTS
vehicle_records = {}  # Hash table: vehicle number -> details
waiting_queue = deque()  # Queue for waiting vehicles


def find_free_slot():
    """Find the first available parking slot."""
    for i, vehicle in enumerate(parking_slots):
        if vehicle is None:
            return i
    return -1


def vehicle_entry():
    vehicle = input("Enter vehicle number: ").strip().upper()

    if not vehicle:
        print("Vehicle number cannot be empty.")
        return

    if vehicle in vehicle_records:
        print("This vehicle is already registered.")
        return

    if any(item["number"] == vehicle for item in waiting_queue):
        print("This vehicle is already in the waiting queue.")
        return

    slot = find_free_slot()

    if slot == -1:
        waiting_queue.append({"number": vehicle})
        print("Parking is full. Vehicle added to waiting queue.")
        return

    parking_slots[slot] = vehicle
    vehicle_records[vehicle] = {
        "slot": slot,
        "entry_time": datetime.now()
    }

    print(f"Vehicle parked successfully in slot P{slot + 1:02d}.")


def vehicle_exit():
    vehicle = input("Enter vehicle number: ").strip().upper()

    if vehicle not in vehicle_records:
        print("Vehicle not found in the parking area.")
        return

    details = vehicle_records[vehicle]
    exit_time = datetime.now()

    duration_seconds = (
        exit_time - details["entry_time"]
    ).total_seconds()

    hours = max(1, math.ceil(duration_seconds / 3600))
    fee = hours * RATE_PER_HOUR

    slot = details["slot"]
    parking_slots[slot] = None
    del vehicle_records[vehicle]

    print("\n--- Parking Receipt ---")
    print("Vehicle number:", vehicle)
    print(f"Slot number: P{slot + 1:02d}")
    print(f"Duration: {duration_seconds / 60:.2f} minutes")
    print(f"Billable hours: {hours}")
    print(f"Parking fee: Rs. {fee}")
    print("-----------------------")

    # Give the freed slot to the next waiting vehicle
    if waiting_queue:
        next_vehicle = waiting_queue.popleft()
        next_number = next_vehicle["number"]

        parking_slots[slot] = next_number
        vehicle_records[next_number] = {
            "slot": slot,
            "entry_time": datetime.now()
        }

        print(
            f"Waiting vehicle {next_number} assigned "
            f"slot P{slot + 1:02d}."
        )


def display_slots():
    print("\n--- Parking Slot Status ---")

    for i, vehicle in enumerate(parking_slots):
        status = vehicle if vehicle else "AVAILABLE"
        print(f"Slot P{i + 1:02d}: {status}")

    occupied = len(vehicle_records)
    available = TOTAL_SLOTS - occupied

    print("\nTotal slots:", TOTAL_SLOTS)
    print("Occupied slots:", occupied)
    print("Available slots:", available)
    print("Waiting vehicles:", len(waiting_queue))


def search_vehicle():
    vehicle = input("Enter vehicle number to search: ").strip().upper()

    if vehicle in vehicle_records:
        details = vehicle_records[vehicle]
        print("Vehicle found.")
        print("Vehicle number:", vehicle)
        print(f"Parking slot: P{details['slot'] + 1:02d}")
        print("Entry time:", details["entry_time"].strftime(
            "%Y-%m-%d %H:%M:%S"
        ))
    elif any(item["number"] == vehicle for item in waiting_queue):
        print("Vehicle is in the waiting queue.")
    else:
        print("Vehicle not found.")


def display_waiting_queue():
    print("\n--- Waiting Queue ---")

    if not waiting_queue:
        print("No vehicles waiting.")
        return

    for position, item in enumerate(waiting_queue, start=1):
        print(f"{position}. {item['number']}")


def main():
    while True:
        print("\n================================")
        print(" SMART PARKING MANAGEMENT SYSTEM")
        print("================================")
        print("1. Vehicle Entry")
        print("2. Vehicle Exit")
        print("3. View Parking Slots")
        print("4. Search Vehicle")
        print("5. View Waiting Queue")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            vehicle_entry()
        elif choice == "2":
            vehicle_exit()
        elif choice == "3":
            display_slots()
        elif choice == "4":
            search_vehicle()
        elif choice == "5":
            display_waiting_queue()
        elif choice == "6":
            print("Thank you for using Smart Parking!")
            break
        else:
            print("Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    main()