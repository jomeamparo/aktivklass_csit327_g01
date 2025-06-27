from django.db import models
from core.models import Faculty, Class

class FacultyAttendance(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PRESENT', 'Present'),
            ('LATE', 'Late'),
            ('ABSENT', 'Absent'),
            ('ON_LEAVE', 'On Leave')
        ],
        default='PRESENT'
    )
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('faculty', 'class_instance', 'date')
        ordering = ['-date', '-time_in']

    def __str__(self):
        return f"{self.faculty} - {self.class_instance} - {self.date} ({self.status})"

class AttendanceSchedule(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('class_instance', 'day_of_week')

    def __str__(self):
        return f"{self.class_instance} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"
