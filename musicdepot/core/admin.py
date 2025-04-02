# core/admin.py

from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Client, Instructor, Room, Schedule, Payment, Payroll, Attendance


# Customizing the admin site header and title
admin.site.site_header = "Music Depo Administration"
admin.site.site_title = "Music Depo Admin Portal"
admin.site.index_title = "Welcome to the Music Depo Admin Dashboard"

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'instrument_preference')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'skillset', 'max_hours_weekly')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('skillset',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'capacity', 'room_type')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('client', 'instructor', 'room', 'start_datetime', 'end_datetime', 'status')
    list_filter = ('instructor', 'room', 'status')
    search_fields = ('client__first_name', 'client__last_name', 'instructor__first_name', 'instructor__last_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'payment_date', 'method', 'status')
    list_filter = ('method', 'status')
    search_fields = ('client__first_name',)

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'total_classes', 'total_earnings')
    readonly_fields = ('total_earnings',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'status', 'notes')
    list_filter = ('status',)
