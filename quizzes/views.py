from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Q, Max, Min
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
from core.models import QuizGrade, Class, Student, Quiz, QuizAttempt, ActivityRecord
import json

def quizzes_view(request):
    """Open quizzes view without faculty restrictions"""
    # Get all classes with quizzes (not limited to faculty)
    classes_with_quizzes = Class.objects.filter(
        quizzes__isnull=False
    ).annotate(
        quiz_count=Count('quizzes'),
        student_count=Count('students', distinct=True)
    ).order_by('subject_name')
    
    # Get all quizzes for these classes
    all_quizzes = Quiz.objects.filter(
        class_obj__in=classes_with_quizzes
    ).annotate(
        question_count=Count('questions')
    ).order_by('class_obj__subject_name', 'title')
    
    # Get all students (not limited to enrolled)
    students = Student.objects.prefetch_related(
        'quiz_grades',
        'quiz_grades__quiz'
    ).distinct()
    
    # Calculate statistics without faculty filter
    stats = QuizGrade.objects.aggregate(
        avg_score=Avg('percentage'),
        max_score=Max('percentage'),
        min_score=Min('percentage'),
        passing_count=Count('id', filter=Q(percentage__gte=75)),
        total_count=Count('id')
    )
    
    passing_rate = (stats['passing_count'] / stats['total_count'] * 100) if stats['total_count'] > 0 else 0
    
    # Prepare student data
    student_quiz_data = []
    for class_obj in classes_with_quizzes:
        class_grades = QuizGrade.objects.filter(
            quiz__class_obj=class_obj
        ).select_related('student', 'quiz')
        
        grades_by_student = {}
        for grade in class_grades:
            if grade.student.id not in grades_by_student:
                grades_by_student[grade.student.id] = {
                    'student': grade.student,
                    'quiz_scores': {},
                    'total_score': 0,
                    'total_max': 0
                }
            grades_by_student[grade.student.id]['quiz_scores'][grade.quiz.title] = {
                'score': grade.score,
                'max_score': grade.max_score,
                'grade_id': grade.id,
                'percentage': grade.percentage
            }
            grades_by_student[grade.student.id]['total_score'] += grade.score
            grades_by_student[grade.student.id]['total_max'] += grade.max_score
        
        for student_data in grades_by_student.values():
            average = (student_data['total_score'] / student_data['total_max'] * 100) if student_data['total_max'] > 0 else 0
            student_quiz_data.append({
                'student': student_data['student'],
                'class_obj': class_obj,
                'quiz_scores': student_data['quiz_scores'],
                'average': round(average, 2)
            })
    
    context = {
        'student_quiz_data': student_quiz_data,
        'classes_with_quizzes': classes_with_quizzes,
        'all_quizzes': all_quizzes,
        'total_students': students.count(),
        'class_average': round(stats['avg_score'] or 0, 2),
        'highest_score': round(stats['max_score'] or 0, 2),
        'lowest_score': round(stats['min_score'] or 0, 2),
        'passing_rate': round(passing_rate, 1),
    }
    
    return render(request, 'quizzes/quizzes.html', context)

@csrf_exempt
@require_POST
def update_quiz_score(request):
    """Grade update without faculty restrictions"""
    try:
        data = json.loads(request.body)
        grade_id = data.get('grade_id')
        quiz_id = data.get('quiz_id')
        student_id = data.get('student_id')
        new_score = float(data.get('score', 0))
        
        with transaction.atomic():
            if grade_id:
                # Update existing grade
                grade = get_object_or_404(QuizGrade, id=grade_id)
                
                if not (0 <= new_score <= grade.max_score):
                    return JsonResponse({
                        'success': False,
                        'error': f'Score must be between 0 and {grade.max_score}',
                        'notification': {
                            'title': 'Error',
                            'message': f'Invalid score range (0-{grade.max_score})',
                            'type': 'error'
                        }
                    })
                
                grade.score = new_score
                grade.percentage = (new_score / grade.max_score) * 100
                grade.save()
                
                # Update related attempt
                grade.attempt.score = new_score
                grade.attempt.save()
                
                message = f"Updated grade for {grade.student}: {new_score}/{grade.max_score}"
                
            elif quiz_id and student_id:
                # Create new grade
                quiz = get_object_or_404(Quiz, id=quiz_id)
                student = get_object_or_404(Student, id=student_id)
                
                if not (0 <= new_score <= quiz.total_points):
                    return JsonResponse({
                        'success': False,
                        'error': f'Score must be between 0 and {quiz.total_points}',
                        'notification': {
                            'title': 'Error',
                            'message': f'Invalid score range (0-{quiz.total_points})',
                            'type': 'error'
                        }
                    })
                
                # Create attempt
                attempt = QuizAttempt.objects.create(
                    student=student,
                    quiz=quiz,
                    score=new_score,
                    max_score=quiz.total_points,
                    is_completed=True,
                    completed_at=timezone.now()
                )
                
                # Create grade
                grade = QuizGrade.objects.create(
                    student=student,
                    quiz=quiz,
                    attempt=attempt,
                    score=new_score,
                    max_score=quiz.total_points,
                    percentage=(new_score / quiz.total_points) * 100
                )
                
                message = f"Created new grade for {student}: {new_score}/{quiz.total_points}"
            
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required parameters',
                    'notification': {
                        'title': 'Error',
                        'message': 'Missing quiz or student information',
                        'type': 'error'
                    }
                })
            
            # Create activity log (if needed)
            ActivityRecord.objects.create(
                student=grade.student,
                activity_type='Quiz',
                activity_name=grade.quiz.title,
                score=grade.score,
                perfect_score=grade.max_score,
                date=timezone.now().date()
            )
            
            return JsonResponse({
                'success': True,
                'grade_id': grade.id,
                'percentage': grade.percentage,
                'notification': {
                    'title': 'Success',
                    'message': message,
                    'type': 'success'
                }
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'notification': {
                'title': 'Error',
                'message': f'An error occurred: {str(e)}',
                'type': 'error'
            }
        })

@csrf_exempt
@require_POST
def delete_quiz_grade(request):
    """Grade deletion without restrictions"""
    try:
        data = json.loads(request.body)
        grade_id = data.get('grade_id')
        
        if not grade_id:
            return JsonResponse({
                'success': False,
                'error': 'No grade ID provided',
                'notification': {
                    'title': 'Error',
                    'message': 'No grade specified for deletion',
                    'type': 'error'
                }
            })
        
        grade = get_object_or_404(QuizGrade, id=grade_id)
        student_name = f"{grade.student.first_name} {grade.student.last_name}"
        quiz_title = grade.quiz.title
        score = f"{grade.score}/{grade.max_score}"
        
        with transaction.atomic():
            grade.attempt.delete()
            grade.delete()
        
        return JsonResponse({
            'success': True,
            'notification': {
                'title': 'Deleted',
                'message': f"Deleted grade for {student_name} on {quiz_title} ({score})",
                'type': 'success'
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'notification': {
                'title': 'Error',
                'message': f'Failed to delete grade: {str(e)}',
                'type': 'error'
            }
        })