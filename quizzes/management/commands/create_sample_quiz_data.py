from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Quiz, QuizGrade, Student, Class, Faculty, Enrollment, QuizAttempt
import random

class Command(BaseCommand):
    help = 'Create sample quiz data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample quiz data...')
        
        # Get existing data
        students = list(Student.objects.all())
        classes = list(Class.objects.all())
        faculty = Faculty.objects.first()
        
        if not students or not classes:
            self.stdout.write(self.style.ERROR('No students or classes found. Please create some first.'))
            return
            
        if not faculty:
            self.stdout.write(self.style.ERROR('No faculty found. Please create a faculty member first.'))
            return
        
        # Create additional quizzes if needed
        quiz_titles = [
            'Midterm Exam',
            'Final Exam', 
            'Quiz 1 - Introduction',
            'Quiz 2 - Basic Concepts',
            'Quiz 3 - Advanced Topics',
            'Lab Quiz 1',
            'Lab Quiz 2',
            'Practice Test 1',
            'Practice Test 2'
        ]
        
        created_quizzes = 0
        for class_obj in classes:
            for i, title in enumerate(quiz_titles[:3]):  # Create 3 quizzes per class
                quiz, created = Quiz.objects.get_or_create(
                    title=f"{title} - {class_obj.subject_code}",
                    class_obj=class_obj,
                    defaults={
                        'description': f'Sample quiz for {class_obj.subject_name}',
                        'faculty': faculty,
                        'total_points': 100,
                        'time_limit': random.randint(30, 120),
                        'max_attempts': 2,
                        'is_active': True,
                        'due_date': timezone.now() + timezone.timedelta(days=random.randint(1, 30))
                    }
                )
                if created:
                    created_quizzes += 1
        
        self.stdout.write(f'Created {created_quizzes} new quizzes')
        
        # Create quiz attempts and grades for students
        created_grades = 0
        for student in students:
            for class_obj in classes:
                # Check if student is enrolled in this class
                if Enrollment.objects.filter(student=student, enrolled_class=class_obj).exists():
                    quizzes = Quiz.objects.filter(class_obj=class_obj)
                    for quiz in quizzes:
                        # Create quiz attempt
                        attempt, attempt_created = QuizAttempt.objects.get_or_create(
                            student=student,
                            quiz=quiz,
                            defaults={
                                'score': random.randint(60, 100),
                                'max_score': quiz.total_points,
                                'is_completed': True,
                                'completed_at': timezone.now()
                            }
                        )
                        
                        if attempt_created:
                            # Create grade
                            score = attempt.score
                            max_score = attempt.max_score
                            percentage = (score / max_score) * 100
                            
                            grade, grade_created = QuizGrade.objects.get_or_create(
                                student=student,
                                quiz=quiz,
                                attempt=attempt,
                                defaults={
                                    'score': score,
                                    'max_score': max_score,
                                    'percentage': percentage,
                                    'graded_by': faculty,
                                    'feedback': f'Sample grade for {student.first_name}'
                                }
                            )
                            if grade_created:
                                created_grades += 1
        
        self.stdout.write(f'Created {created_grades} new quiz grades')
        self.stdout.write(self.style.SUCCESS('Sample quiz data created successfully!'))
        
        # Show summary
        total_quizzes = Quiz.objects.count()
        total_grades = QuizGrade.objects.count()
        self.stdout.write(f'Total quizzes in database: {total_quizzes}')
        self.stdout.write(f'Total quiz grades in database: {total_grades}') 