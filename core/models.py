from django.db import models
import random, string


def generate_random_code(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

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
    student_id = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        default="default"
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=50)
    course = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DISABLED', 'Disabled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    enrolled_classes = models.ManyToManyField(Class, through='Enrollment', related_name='students')

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"
    
class ClassJoinRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # or your Student model
    class_requested = models.ForeignKey(Class, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # pending, approved, rejected

    def __str__(self):
        return f"{self.student} -> {self.class_requested} ({self.status})"



class Faculty(models.Model):
    faculty_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, default="")
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    
    COLLEGE_CHOICES = [
        ('CCS', 'CCS'),
        ('CASE', 'CASE'),
    ]
    college_name = models.CharField(max_length=10, choices=COLLEGE_CHOICES)

    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('Arts', 'Arts'),
        ('Science', 'Science'),
        ('Education', 'Education'),
    ]
    department_name = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    STATUS_CHOICES = [
        ('Fulltime', 'Fulltime'),
        ('Parttime', 'Parttime'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name} ({self.faculty_id})"

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
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='activity_records'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_records'
    )  # ✅ New field for direct student reference

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
    activity_name = models.CharField(max_length=100)  # e.g., "Quiz 3", entered by user
    
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    perfect_score = models.FloatField(null=False, blank=False, default=100)  # NEW field for perfect score

    class Meta:
        unique_together = ('enrollment', 'activity_type', 'activity_name')

    def __str__(self):
        return f"{self.enrollment.student} - {self.activity_type} {self.activity_name}: {self.score}/{self.perfect_score}"



class AdminUser(models.Model):
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        default="default"
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=50)
    
    password = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.employee_id})"
    
class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'notifications' 
    
class Faculty_Attendance(models.Model):
    id_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
