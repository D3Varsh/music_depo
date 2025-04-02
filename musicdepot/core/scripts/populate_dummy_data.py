# core/scripts/populate_dummy_data.py
from core.models import Client, Instructor, Room, LessonType, Schedule, Payment, Attendance, Payroll
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
import random

print("Cleaning up existing data...")
Attendance.objects.all().delete()
Payment.objects.all().delete()
Schedule.objects.all().delete()
LessonType.objects.all().delete()
Room.objects.all().delete()
Instructor.objects.all().delete()
Client.objects.all().delete()
Payroll.objects.all().delete()
print("Existing data cleared.")

print("Creating dummy data...")

for i in range(5):
    client, created = Client.objects.get_or_create(
        email=f"client{i+1}@example.com",
        defaults={
            'first_name': f"Client{i+1}",
            'last_name': f"LastName{i+1}",
            'phone': f"123-456-78{i+1}",
            'instrument_preference': "Piano",
        }
    )

    instructor, created = Instructor.objects.get_or_create(
        email=f"instructor{i+1}@example.com",
        defaults={
            'first_name': f"Instructor{i+1}",
            'last_name': f"Teacher{i+1}",
            'phone': f"987-654-32{i+1}",
            'skillset': "Guitar, Piano",
            'max_hours_weekly': 15,
        }
    )

    room, created = Room.objects.get_or_create(
        room_name=f"Room{i+1}",
        defaults={
            'capacity': 10,
            'room_type': "individual",
        }
    )

    lesson_type, created = LessonType.objects.get_or_create(
        name=f"LessonType{i+1}",
        defaults={
            'duration': 45,
        }
    )

    start_datetime = timezone.now() + timedelta(days=i)
    end_datetime = start_datetime + timedelta(hours=1)

    schedule, created = Schedule.objects.get_or_create(
        client=client,
        instructor=instructor,
        room=room,
        lesson_type=lesson_type,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        status="scheduled"
    )

    payment, created = Payment.objects.get_or_create(
        client=client,
        amount=random.uniform(50.0, 100.0),
        payment_date=timezone.now().date(),
        method="Credit Card",
        status="Completed"
    )

    attendance, created = Attendance.objects.get_or_create(
        schedule=schedule,
        status="present",
        defaults={
            'notes': "Good performance.",
        }
    )

    # Generate Payroll data
    total_classes = random.randint(5, 20)
    pay_per_class = Decimal(random.uniform(20.0, 50.0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total_earnings = (pay_per_class * total_classes).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Use get_or_create with all required fields
    payroll, created = Payroll.objects.get_or_create(
        instructor=instructor,
        defaults={
            'total_classes': total_classes,
            'pay_per_class': pay_per_class,
            'total_earnings': total_earnings,
        }
    )

    print(f"Created payroll for {instructor.first_name} {instructor.last_name} - Classes: {total_classes}, Pay per Class: ${pay_per_class:.2f}, Earnings: ${total_earnings:.2f}")

print("Dummy data successfully created!")
