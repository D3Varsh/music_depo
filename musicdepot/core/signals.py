# core/signals.py

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Payment, Schedule, Payroll

# Signal to update payment status automatically
@receiver(post_save, sender=Payment)
def update_payment_status(sender, instance, **kwargs):
    if instance.status == "completed":
        print(f"Payment of {instance.amount} by {instance.client} marked as completed.")

# Signal to check for overlapping schedules
@receiver(pre_save, sender=Schedule)
def validate_schedule(sender, instance, **kwargs):
    overlapping_schedules = Schedule.objects.filter(
        room=instance.room,
        start_datetime__lt=instance.end_datetime,
        end_datetime__gt=instance.start_datetime,
        status='scheduled'
    ).exclude(pk=instance.pk)

    instructor_conflict = Schedule.objects.filter(
        instructor=instance.instructor,
        start_datetime__lt=instance.end_datetime,
        end_datetime__gt=instance.start_datetime,
        status='scheduled'
    ).exclude(pk=instance.pk)

    client_conflict = Schedule.objects.filter(
        client=instance.client,
        start_datetime__lt=instance.end_datetime,
        end_datetime__gt=instance.start_datetime,
        status='scheduled'
    ).exclude(pk=instance.pk)

    if overlapping_schedules.exists():
        raise ValidationError(f"Room '{instance.room}' is already booked for this time slot.")
    
    if instructor_conflict.exists():
        raise ValidationError(f"Instructor '{instance.instructor}' is already scheduled for this time slot.")
    
    if client_conflict.exists():
        raise ValidationError(f"Client '{instance.client}' is already scheduled for this time slot.")
    
# Signal to auto-calculate payroll total earnings
@receiver(pre_save, sender=Payroll)
def update_payroll_earnings(sender, instance, **kwargs):
    if instance.total_classes and instance.pay_per_class:
        instance.total_earnings = instance.total_classes * instance.pay_per_class
        print(f"Updated total earnings for {instance.instructor} to {instance.total_earnings:.2f}")
