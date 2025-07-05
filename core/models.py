from django.db import models
import random, string
import uuid
from django.apps import AppConfig
from django.conf import settings
from django.db.models import Count
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Utility for generating unique class codes
def generate_random_code(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

STATUS_CHOICES = [
    ('ACTIVE', 'ACTIVE'),
    ('DISABLED', 'DISABLED'),
    ('Active', 'Active'),
    ('Offline', 'Offline'),
    ('Busy', 'Busy'),
]

STUDENT_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('Busy', 'Busy'),
    ('Offline', 'Offline'),
]

class Class(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, null=True, blank=True, related_name='teaching_classes')
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

class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='default_avatar.jpg', upload_to='student_profiles/')
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    def profile_completion_percentage(self):
        fields = [
            self.bio, self.birth_date, self.website,
            self.major, self.graduation_year
        ]
        completed_fields = sum(1 for field in fields if field)
        total_fields = len(fields)
        
        if self.avatar and self.avatar.name != 'default_avatar.jpg':
            completed_fields += 1
        else:
            pass # No need to do anything if it's the default avatar
            
        total_fields += 1 # Account for avatar field

        if total_fields == 0:
            return 0
        return round((completed_fields / total_fields) * 100)

    def __str__(self):
        return f"{self.student.first_name}'s Profile"

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default='password123')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    email = models.EmailField(unique=True, default='default@example.com')

    def __str__(self):
        return f"{self.faculty_id} - {self.first_name} {self.last_name}"

class ClassJoinRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_requested = models.ForeignKey(Class, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

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
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read=True
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'notifications'

class Conversation(models.Model):
    participants = models.ManyToManyField(Student, related_name='conversations')
    muted_by = models.ManyToManyField(Student, related_name='muted_conversations', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_or_create_conversation(cls, student1, student2):
        conversations = cls.objects.filter(participants=student1).filter(participants=student2)
        if conversations.exists():
            return conversations.first()
        conversation = cls.objects.create()
        conversation.participants.add(student1, student2)
        return conversation

    def get_other_participant(self, user):
        """Return the other participant in the conversation given the current user."""
        return self.participants.exclude(id=user.id).first()

    def get_last_message(self):
        """Return the latest message in the conversation, or None if there are no messages."""
        return self.messages.order_by('-timestamp').first()

    def get_unread_count_for_user(self, user):
        """Return the count of unread messages for the given user (excluding messages sent by that user)."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()

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
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.employee_id})"

class Attendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'class_obj', 'date'], 
                name='unique_student_class_date_attendance'
            )
        ]

# class Activity(models.Model):
#     TYPE_CHOICES = [('Quiz', 'Quiz'), ('Assignment', 'Assignment'), ('Exam', 'Exam')]
#     class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
#     due_date = models.DateField()
#     max_score = models.FloatField()

# class Grade(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
#     score = models.FloatField()
#     feedback = models.TextField(blank=True, null=True)
#     date_graded = models.DateField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.post.title}'

class FacultyProfileAdmin(models.Model):
    list_display = ('first_name', 'last_name', 'department', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department',)

    class Meta:
        app_label = 'faculty_profile'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Analytics(models.Model):
    total_faculty = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Analytics'

    def __str__(self):
        return f'Analytics - {self.created_at.strftime("%Y-%m-%d")}'

    @classmethod
    def update_stats(cls):
        """Update analytics statistics"""
        try:
            analytics = cls.objects.first()
            if not analytics:
                analytics = cls()
            
            analytics.total_faculty = Faculty.objects.count()
            analytics.total_students = Student.objects.count()
            analytics.save()
            return analytics
        except Exception as e:
            print(f"Error updating analytics: {e}")
            return None

class EditAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edit_admin'

class FacultyProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faculty_profile'


class PasswordResetToken(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    admin_user = models.ForeignKey(AdminUser, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


from django.conf import settings
from django.db import models

class FacultyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # ✅ allow nulls
        blank=True  # ✅ allow blank in forms
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    office_location = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    faculty_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    date_hired = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def completion_percentage(self):
        fields = [
            self.first_name, self.last_name, self.department, self.email,
            self.contact_number, self.office_location, self.profile_picture,
            self.bio, self.faculty_id, self.position, self.college,
            self.specialization, self.date_hired, self.birth_date
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)

class Course(models.Model):
    course_id = models.CharField(max_length=255, primary_key=True)
    subject_name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    schedule = models.CharField(max_length=6)
    capacity = models.CharField(max_length=255)
    room = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course_id} - {self.subject_name} {self.subject_code}"



class SeatworkRecord(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.activity} ({self.status})"
        


# Quiz Models
class Quiz(models.Model):
    """Model for storing quiz information"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='quizzes')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='created_quizzes')
    total_points = models.IntegerField(default=100)
    time_limit = models.IntegerField(default=60, help_text="Time limit in minutes")  # 0 for no limit
    is_active = models.BooleanField(default=True)
    allow_multiple_attempts = models.BooleanField(default=False)
    max_attempts = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.class_obj.subject_name}"

    class Meta:
        ordering = ['-created_at']

class QuizQuestion(models.Model):
    """Model for storing individual quiz questions"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    points = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Question {self.order}: {self.question_text[:50]}..."

    class Meta:
        ordering = ['order']

class QuizChoice(models.Model):
    """Model for storing multiple choice options"""
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.choice_text[:30]}..."

    class Meta:
        ordering = ['order']

class QuizAttempt(models.Model):
    """Model for storing student quiz attempts"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    max_score = models.FloatField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} - {self.quiz.title} (Attempt {self.id})"

    class Meta:
        unique_together = ['student', 'quiz']
        ordering = ['-started_at']

class QuizResponse(models.Model):
    """Model for storing student responses to quiz questions"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(QuizChoice, on_delete=models.CASCADE, blank=True, null=True)
    text_response = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(blank=True, null=True)
    points_earned = models.FloatField(default=0)
    
    def __str__(self):
        return f"Response to {self.question} by {self.attempt.student}"

class QuizGrade(models.Model):
    """Model for storing quiz grades that integrates with ActivityRecord"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_grades')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='grades')
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='grade')
    score = models.FloatField()
    max_score = models.FloatField()
    percentage = models.FloatField()
    grade_letter = models.CharField(max_length=2, blank=True)
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Calculate percentage
        if self.max_score > 0:
            self.percentage = (self.score / self.max_score) * 100
        
        # Calculate letter grade
        if self.percentage >= 90:
            self.grade_letter = 'A'
        elif self.percentage >= 80:
            self.grade_letter = 'B'
        elif self.percentage >= 70:
            self.grade_letter = 'C'
        elif self.percentage >= 60:
            self.grade_letter = 'D'
        else:
            self.grade_letter = 'F'
        
        super().save(*args, **kwargs)
        
        # Create or update ActivityRecord
        self.create_activity_record()
    
    def create_activity_record(self):
        """Create or update ActivityRecord for this quiz grade"""
        # Get the enrollment through the through relationship
        enrollment = Enrollment.objects.filter(
            student=self.student,
            enrolled_class=self.quiz.class_obj
        ).first()
        
        if enrollment:
            activity_record, created = ActivityRecord.objects.get_or_create(
                enrollment=enrollment,
                student=self.student,
                activity_type='Quiz',
                activity_name=self.quiz.title,
                defaults={
                    'date': self.graded_at.date(),
                    'faculty': self.graded_by or self.quiz.faculty,
                    'score': self.score,
                    'perfect_score': self.max_score,
                }
            )
            
            if not created:
                # Update existing record
                activity_record.score = self.score
                activity_record.perfect_score = self.max_score
                activity_record.save()
    
    def __str__(self):
        return f"{self.student} - {self.quiz.title}: {self.score}/{self.max_score} ({self.percentage:.1f}%)"

    class Meta:
        unique_together = ['student', 'quiz']
        ordering = ['-graded_at']
        
# Feature 3: Bookmark / Favorite Class # asdasd
class FavoriteCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} favorited {self.course}"
    
    from django.db import models

class Faculty_Attendance(models.Model):
    id_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject} ({self.date})"

