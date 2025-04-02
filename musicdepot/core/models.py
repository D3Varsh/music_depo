# core/models.py

from django.utils import timezone
from django.db import models
from django.forms import ValidationError

# Client Model
class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    instrument_preference = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Instructor Model
class Instructor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    skillset = models.TextField()
    max_hours_weekly = models.IntegerField(default=10)

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Room Model
class Room(models.Model):
    room_name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    
    ROOM_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('piano', 'Piano'),
        ('percussion', 'Percussion'),
        ('vocal', 'Vocal'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    def __str__(self):
        return self.room_name


# Lesson Type Model
class LessonType(models.Model):
    name = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name


# Schedule Model
class Schedule(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    lesson_type = models.ForeignKey(LessonType, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.client} with {self.instructor} at {self.start_datetime}"
    
    def clean(self):
        # Validate start before end
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("Start time must be before end time.")

        # Check for schedule conflicts (only scheduled)
        overlapping_schedules = Schedule.objects.filter(
            room=self.room,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
            status='scheduled'  # Only consider scheduled lessons
        ).exclude(pk=self.pk)

        if overlapping_schedules.exists():
            raise ValidationError(f"Room '{self.room}' is already booked for this time slot.")

        # Check instructor availability (only scheduled)
        instructor_conflict = Schedule.objects.filter(
            instructor=self.instructor,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
            status='scheduled'  # Only consider scheduled lessons
        ).exclude(pk=self.pk)

        if instructor_conflict.exists():
            raise ValidationError(f"Instructor '{self.instructor}' is already scheduled for this time slot.")

        # Check client availability (only scheduled)
        client_conflict = Schedule.objects.filter(
            client=self.client,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
            status='scheduled'  # Only consider scheduled lessons
        ).exclude(pk=self.pk)

        if client_conflict.exists():
            raise ValidationError(f"Client '{self.client}' is already scheduled for this time slot.")

    def save(self, *args, **kwargs):
        # Simplify timezone handling by storing in UTC
        if timezone.is_naive(self.start_datetime):
            self.start_datetime = timezone.make_aware(self.start_datetime, timezone.utc)
        if timezone.is_naive(self.end_datetime):
            self.end_datetime = timezone.make_aware(self.end_datetime, timezone.utc)

        # Validate before saving
        self.full_clean()
        super().save(*args, **kwargs)


# Payment Model
class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('online', 'Online Payment'),
    ]
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit_card')
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Payment of {self.amount} from {self.client}"


# Payroll Model
class Payroll(models.Model):
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    total_classes = models.IntegerField()
    pay_per_class = models.DecimalField(max_digits=6, decimal_places=2)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Automatically update total earnings before saving
        self.total_earnings = self.total_classes * self.pay_per_class
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

    def clean(self):
        """Ensure that each instructor has only one payroll record."""
        if Payroll.objects.filter(instructor=self.instructor).exclude(id=self.id).exists():
            raise ValidationError(f"Payroll for {self.instructor} already exists.")

    def recalculate_earnings(self):
        """Recalculate earnings based on current total classes and pay per class."""
        self.total_earnings = self.total_classes * self.pay_per_class
        self.save()

    def update_total_classes(self, new_class_count):
        """Update the total number of classes and recalculate earnings."""
        self.total_classes = new_class_count
        self.recalculate_earnings()

    def get_summary(self):
        """Return a string summary of the payroll details."""
        return f"{self.instructor}: {self.total_classes} classes - Total Earnings: ${self.total_earnings}"

    def __str__(self):
        return f"Payroll for {self.instructor} - {self.total_earnings}"

# Attendance Model
class Attendance(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused Absence'),
        ('unexcused', 'Unexcused Absence'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.schedule} - {self.status}"
