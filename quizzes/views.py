from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from core.models import QuizGrade, Class, Student, Faculty, ActivityRecord, Enrollment, Quiz, AdminUser, QuizAttempt
import json

def quizzes_view(request):
    """Main quizzes view that displays quiz records and statistics for faculty"""
    
    # Get all quiz grades with related data
    quiz_grades = QuizGrade.objects.select_related(
        'student', 'quiz', 'quiz__class_obj', 'graded_by'
    ).order_by('-graded_at')
    
    # Get unique classes that have quizzes
    classes_with_quizzes = Class.objects.filter(quizzes__isnull=False).distinct()
    
    # Get all students who have quiz grades OR are enrolled in classes with quizzes
    students_with_grades = Student.objects.filter(quiz_grades__isnull=False).distinct()
    enrolled_students = Student.objects.filter(
        enrolled_classes__in=classes_with_quizzes
    ).distinct()
    
    # Combine both sets of students
    all_students = (students_with_grades | enrolled_students).distinct()
    
    # Calculate statistics
    total_students = all_students.count()
    class_average = quiz_grades.aggregate(avg=Avg('percentage'))['avg'] or 0
    highest_score = quiz_grades.aggregate(max=Avg('percentage'))['max'] or 0
    lowest_score = quiz_grades.aggregate(min=Avg('percentage'))['min'] or 0
    
    # Calculate passing rate (≥75%)
    passing_grades = quiz_grades.filter(percentage__gte=75).count()
    total_grades = quiz_grades.count()
    passing_rate = (passing_grades / total_grades * 100) if total_grades > 0 else 0
    
    # Get all unique quizzes for table headers
    all_quizzes = Quiz.objects.filter(class_obj__in=classes_with_quizzes).order_by('class_obj__subject_name', 'title')
    
    # Group quiz grades by student and class for the table
    student_quiz_data = {}
    
    # First, add all students who have grades or are enrolled
    for student in all_students:
        for class_obj in classes_with_quizzes:
            student_key = f"{student.id}_{class_obj.id}"
            student_quiz_data[student_key] = {
                'student': student,
                'class_obj': class_obj,
                'quiz_scores': {},  # Will store quiz scores by quiz title
                'total_score': 0,
                'total_max_score': 0,
                'quiz_count': 0,
                'average': 0  # Default average
            }
    
    # Then add the actual quiz grades
    for grade in quiz_grades:
        student_key = f"{grade.student.id}_{grade.quiz.class_obj.id}"
        
        if student_key in student_quiz_data:
            # Store quiz scores by quiz title
            student_quiz_data[student_key]['quiz_scores'][grade.quiz.title] = {
                'score': grade.score,
                'max_score': grade.max_score,
                'percentage': grade.percentage,
                'grade_id': grade.id
            }
            
            student_quiz_data[student_key]['total_score'] += grade.score
            student_quiz_data[student_key]['total_max_score'] += grade.max_score
            student_quiz_data[student_key]['quiz_count'] += 1
    
    # Calculate averages for each student
    for student_data in student_quiz_data.values():
        if student_data['total_max_score'] > 0:
            student_data['average'] = (student_data['total_score'] / student_data['total_max_score']) * 100
        else:
            student_data['average'] = 0
    
    context = {
        'quiz_grades': quiz_grades,
        'student_quiz_data': list(student_quiz_data.values()),
        'classes_with_quizzes': classes_with_quizzes,
        'all_quizzes': all_quizzes,
        'total_students': total_students,
        'class_average': round(class_average, 2),
        'highest_score': round(highest_score, 2),
        'lowest_score': round(lowest_score, 2),
        'passing_rate': round(passing_rate, 1),
        'fullname': 'Faculty User',  # This should come from session/authentication
    }
    
    return render(request, 'quizzes/quizzes.html', context)

@csrf_exempt
@require_POST
def update_quiz_score(request):
    """AJAX endpoint to update or create quiz scores"""
    try:
        data = json.loads(request.body)
        
        grade_id = data.get('grade_id')
        new_score = float(data.get('score', 0))
        quiz_id = data.get('quiz_id')
        student_id = data.get('student_id')

        if grade_id:
            # Update existing grade
            grade = get_object_or_404(QuizGrade, id=grade_id)
            if new_score < 0 or new_score > grade.max_score:
                return JsonResponse({
                    'success': False,
                    'error': f'Score must be between 0 and {grade.max_score}'
                })
            grade.score = new_score
            grade.save()
            return JsonResponse({
                'success': True,
                'new_score': grade.score,
                'new_percentage': grade.percentage,
                'new_grade_letter': grade.grade_letter,
                'grade_id': grade.id,
                'message': 'Score updated successfully!'
            })
        elif quiz_id and student_id:
            # Create new grade and attempt
            quiz = get_object_or_404(Quiz, id=quiz_id)
            student = get_object_or_404(Student, id=student_id)
            max_score = quiz.total_points
            if new_score < 0 or new_score > max_score:
                return JsonResponse({
                    'success': False,
                    'error': f'Score must be between 0 and {max_score}'
                })
            
            # Check if attempt already exists, if not create one
            attempt, created = QuizAttempt.objects.get_or_create(
                student=student,
                quiz=quiz,
                defaults={
                    'score': new_score,
                    'max_score': max_score,
                    'is_completed': True,
                    'completed_at': timezone.now()
                }
            )
            
            # If attempt already existed, update it
            if not created:
                attempt.score = new_score
                attempt.max_score = max_score
                attempt.is_completed = True
                attempt.completed_at = timezone.now()
                attempt.save()
            
            # Check if grade already exists, if not create one
            grade, grade_created = QuizGrade.objects.get_or_create(
                student=student,
                quiz=quiz,
                defaults={
                    'attempt': attempt,
                    'score': new_score,
                    'max_score': max_score,
                    'percentage': (new_score / max_score) * 100,
                    'graded_by': None
                }
            )
            
            # If grade already existed, update it
            if not grade_created:
                grade.attempt = attempt
                grade.score = new_score
                grade.max_score = max_score
                grade.percentage = (new_score / max_score) * 100
                grade.save()
            
            return JsonResponse({
                'success': True,
                'new_score': grade.score,
                'new_percentage': grade.percentage,
                'new_grade_letter': grade.grade_letter,
                'grade_id': grade.id,
                'message': 'Grade created successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Insufficient data to update or create grade.'
            })
    except (ValueError, TypeError) as e:
        return JsonResponse({
            'success': False,
            'error': f'Invalid score value: {str(e)}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@csrf_exempt
@require_POST
def delete_quiz_grade(request):
    """AJAX endpoint to delete quiz grades"""
    try:
        data = json.loads(request.body)
        grade_id = data.get('grade_id')
        
        if grade_id:
            grade = get_object_or_404(QuizGrade, id=grade_id)
            grade.delete()
            return JsonResponse({'success': True, 'message': 'Grade deleted successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'No grade ID provided'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def archive_quiz_grades(request):
    try:
        data = json.loads(request.body)
        grade_ids = data.get('grade_ids', [])
        
        if grade_ids:
            QuizGrade.objects.filter(id__in=grade_ids).update(is_archived=True)
            return JsonResponse({'success': True, 'message': f'{len(grade_ids)} records archived'})
        return JsonResponse({'success': False, 'error': 'No grade IDs provided'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})