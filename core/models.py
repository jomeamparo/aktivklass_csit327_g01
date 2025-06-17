from django.db import models
import random, string

# Utility for generating unique class codes
def generate_random_code(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

STATUS_CHOICES = [
    ('ACTIVE', 'ACTIVE'),
    ('DISABLED', 'DISABLED'),
]

STUDENT_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('Busy', 'Busy'),
    ('Offline', 'Offline'),
]

class Class(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)
    description = models.TextField()
    schedule = models.CharField(max_length=100)
    room = models.CharField(max_length=50)
    class_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.class_code:
            new_code = generate_random_code()
            while Class.objects.filter(class_code=new_code).exists():
                new_code = generate_random_code()
            self.class_code = new_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='default@example.com')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STUDENT_STATUS_CHOICES, default='Available')
    enrolled_classes = models.ManyToManyField(Class, through='Enrollment', related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default='password123')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"{self.faculty_id} - {self.first_name} {self.last_name}"

class ClassJoinRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_requested = models.ForeignKey(Class, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # pending, approved, rejected

    def __str__(self):
        return f"{self.student} -> {self.class_requested} ({self.status})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.student:
            return f"Student {self.student} enrolled in {self.enrolled_class}"
        elif self.faculty:
            return f"Faculty {self.faculty} assigned to {self.enrolled_class}"
        else:
            return f"Enrollment record for unknown person in {self.enrolled_class}"

class ActivityRecord(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='activity_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='activity_records')
    date = models.DateField()

    ACTIVITY_TYPE_CHOICES = [
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Seatwork', 'Seatwork'),
        ('Laboratory', 'Laboratory'),
        ('Prelim', 'Prelim'),
        ('Midterm', 'Midterm'),
        ('Pre-Final', 'Pre-Final'),
        ('Final', 'Final'),
    ]

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    activity_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    perfect_score = models.FloatField(null=False, blank=False, default=100)

    class Meta:
        unique_together = ('enrollment', 'activity_type', 'activity_name')

    def __str__(self):
        return f"{self.enrollment.student} - {self.activity_type} {self.activity_name}: {self.score}/{self.perfect_score}"

class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'notifications'

class Conversation(models.Model):
    participants = models.ManyToManyField(Student, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation ({self.id})"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} at {self.timestamp}"

class AdminUser(models.Model):
    employee_id = models.CharField(max_length=20, unique=True, null=False, blank=False, default="default")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.employee_id})"

class Attendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Activity(models.Model):
    TYPE_CHOICES = [('Quiz', 'Quiz'), ('Assignment', 'Assignment'), ('Exam', 'Exam')]
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    due_date = models.DateField()
    max_score = models.FloatField()

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    score = models.FloatField()
    feedback = models.TextField(blank=True, null=True)
    date_graded = models.DateField(auto_now_add=True)
