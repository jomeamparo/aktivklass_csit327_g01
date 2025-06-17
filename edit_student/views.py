from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from core.models import Student
import json

def edit_student_view(request, student_id):
    """
    Display the edit student form with current student information
    """
    try:
        student = get_object_or_404(Student, student_id=student_id)
        context = {
            'student': student,
            'courses': ['BSIT', 'BSCS', 'BSIS', 'BSCE', 'BSEE', 'BSME', 'BSArch'],
            'years': ['1', '2', '3', '4'],
            'status_choices': Student.STATUS_CHOICES,
        }
        return render(request, 'edit_student/edit_student.html', context)
    except Exception as e:
        messages.error(request, f"Error loading student information: {str(e)}")
        return redirect('student_list_view')

@require_POST
@csrf_exempt
def update_student(request, student_id):
    """
    Update student information in the database
    """
    try:
        student = get_object_or_404(Student, student_id=student_id)
        
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        course = request.POST.get('course', '').strip()
        year = request.POST.get('year', '').strip()
        status = request.POST.get('status', 'ACTIVE')
        
        # Validate required fields
        if not all([first_name, last_name, course, year]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields (First Name, Last Name, Course, Year)'
            })
        
        # Update student information
        student.first_name = first_name
        student.middle_name = middle_name if middle_name else " "
        student.last_name = last_name
        student.course = course
        student.year = year
        student.status = status
        
        student.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Student {student_id} updated successfully!',
            'student_data': {
                'student_id': student.student_id,
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'course': student.course,
                'year': student.year,
                'status': student.status,
            }
        })
        
    except Student.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Student not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })
