import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from collections import defaultdict
from datetime import date, datetime

from core.models import Class, Faculty, Student, Enrollment, ActivityRecord


from django.shortcuts import get_object_or_404, render

def pad_scores(scores, length=5):
        scores.sort(key=lambda x: x[0])  # sort by id
        score_values = [s[1] for s in scores]
        while len(score_values) < length:
            score_values.append("")
        return score_values[:length]

def get_class_activity_scores_grouped_sorted(request, class_id, role):
    class_obj = get_object_or_404(Class, id=class_id)
    if role == 'student':
        student_id = request.session.get('user_id')
        enrollments = Enrollment.objects.filter(
            enrolled_class=class_obj,
            student__student_id=student_id
        ).select_related('student')
    else:
        enrollments = Enrollment.objects.filter(
            enrolled_class=class_obj
        ).select_related('student').order_by('student__last_name', 'student__first_name', 'student__middle_name')

    activity_order_main = ['Quiz', 'Seatwork', 'Assignment', 'Laboratory']
    activity_order_final = ['Prelim', 'Midterm', 'Pre-Final', 'Final']

    initial_data = []
    print("enrollments:: ", enrollments)
    for enrollment in enrollments:
        student = enrollment.student
        activities = ActivityRecord.objects.filter(enrollment=enrollment)
        print("activities::: ", activities)
        type_map = {atype: [] for atype in activity_order_main + activity_order_final}

        for record in activities:
            score_type = record.activity_type
            if score_type in type_map:
                type_map[score_type].append((record.id, record.score))

        for atype in activity_order_main:
            type_map[atype] = pad_scores(type_map[atype])

        combined_final_scores = []
        for atype in activity_order_final:
            sorted_scores = sorted(type_map[atype], key=lambda x: x[0])
            combined_final_scores.extend([score for _, score in sorted_scores])

        while len(combined_final_scores) < 5:
            combined_final_scores.append("")

        combined_final_scores = combined_final_scores[:4]

        student_row = [
            student.student_id,
            f"{student.last_name}, {student.first_name} {student.middle_name}"
        ]

        for atype in activity_order_main:
            student_row.extend(type_map[atype])

        student_row.extend(combined_final_scores)
        print(combined_final_scores)
         # TODO: Compute Midterm Grade and Final Grade. Dummy for now.
        student_row.extend(['5.0', '5.0',"Passed"])

        initial_data.append(student_row)
        print("initial_data:::: ", initial_data)
    return initial_data

def class_record_detail(request, class_id, role='faculty'):
    class_obj = get_object_or_404(Class, id=class_id)

    uploaded_students = request.session.get('uploaded_students', None)

    initial_data = get_class_activity_scores_grouped_sorted(request, class_id, role)

    if uploaded_students:
        enrolled = uploaded_students.get('enrolled', [])
        unenrolled = uploaded_students.get('unenrolled', [])
    else:
        enrolled = []
        unenrolled = []

    context = {
        'class': class_obj,
        'uploaded_students': uploaded_students,
        'enrolled': enrolled,
        'unenrolled': unenrolled,
        'exams': initial_data,
        'role': role
    }
    
    template_name = 'class_record/class_record_detail_student.html' if role == 'student' else 'class_record/class_record_detail.html'
    return render(request, template_name, context)

@require_GET
def search_students(request):
    query = request.GET.get('q', '').strip()
    students = []
    if query:
        words = query.split()
        students_qs = Student.objects.filter(
            Q(student_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query)
        )

        if len(words) > 1:
            first_name_part = words[0]
            last_name_part = ' '.join(words[1:])
            students_qs |= Student.objects.filter(
                Q(first_name__icontains=first_name_part) &
                Q(last_name__icontains=last_name_part)
            )
        students = list(students_qs.values('id', 'student_id', 'first_name', 'middle_name', 'last_name').distinct()[:20])

    # If AJAX or expects JSON, return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({'students': students})
    # Otherwise, render an HTML template
    return render(request, 'class_record/search_students.html', {
        'students': students,
        'query': query
    })

@require_POST
def upload_class_list(request, class_id):
    excel_file = request.FILES.get('class_list')
    if not excel_file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    print ('upload_class_list')
    try:
        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.lower()

        required_columns = {'student_id', 'first_name', 'middle_name', 'last_name', 'course', 'year'}
        if not required_columns.issubset(df.columns):
            return JsonResponse({
                'error': 'Excel file must contain columns: student_id, first_name, middle_name, last_name, course, year'
            }, status=400)

        df = df[list(required_columns)].fillna('')
        uploaded_students = df.to_dict(orient='records')

        enrolled_students = []
        unenrolled_students = []

        for student in uploaded_students:
            student_id = student.get('user_id')
            print ('upload_class_list', student_id)
            try:
                existing_student = Student.objects.get(student_id=student_id)
                enrolled_students.append({
                    'student_id': existing_student.student_id,
                    'first_name': existing_student.first_name,
                    'middle_name': existing_student.middle_name,
                    'last_name': existing_student.last_name,
                    'course': existing_student.course,
                    'year': existing_student.year
                })
                print ('upload_class_list TRY', enrolled_students)
            except Student.DoesNotExist:
                unenrolled_students.append({
                    'student_id': student.get('user_id'),
                    'first_name': student.get('first_name'),
                    'middle_name': student.get('middle_name'),
                    'last_name': student.get('last_name'),
                    'course': student.get('course', ''),
                    'year': student.get('year', '')
                })
                print ('upload_class_list EX', enrolled_students)
        print('enrolled_students:: ', enrolled_students)
        print('unenrolled_students:: ', unenrolled_students)
        # Save both lists to session
        request.session['uploaded_students'] = {
            'enrolled': enrolled_students,
            'unenrolled': unenrolled_students
        }

        request.session['enrolled'] = enrolled_students
        request.session['unenrolled'] = unenrolled_students

    except Exception as e:
        return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=400)
    print('===================================================================================')
    return redirect('class_record_detail', class_id=class_id)



@csrf_exempt
@require_POST
def save_uploaded_students_to_class(request, class_id):
    try:
        print(f"Saving students to class_id: {class_id}")
        class_obj = get_object_or_404(Class, id=class_id)
        print(f"Fetched class object: {class_obj.subject_name} {class_obj.subject_code} {class_id}")
        print(f"Class object: {class_obj}, ID: {getattr(class_obj, 'id', None)}")
        data = json.loads(request.body)
        students_data = data.get('students', [])
        print(f"Number of students: {len(students_data)}")

        with transaction.atomic():
            for student_data in students_data:
                print(f"Processing student: {student_data}")
                print(f"Processing student: {student_data['student_id']}")
                try:
                    student, created = Student.objects.get_or_create(
                        student_id=student_data['student_id'],
                        defaults={
                            'first_name': student_data['first_name'],
                            'middle_name': student_data['middle_name'],
                            'last_name': student_data['last_name'],
                            'enrolled_class': class_obj,   # <-- IMPORTANT
                        }
                    )
                except Exception as e:
                    print(f"Failed to create or get Student with student_id={student_data['student_id']}: {e}")
                    raise
                print(f"student: {student}")
                enrollment, enrollment_created = Enrollment.objects.get_or_create(
                student=student,
                enrolled_class=class_obj
            )
            print(f"{'Created' if enrollment_created else 'Found'} enrollment for student {student.student_id}")

        request.session.pop('uploaded_students', None)

        return JsonResponse({'success': True})

    except Exception as e:
        print(f"Error saving students: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


@require_GET
def get_class_students(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    students_qs = Student.objects.filter(enrollment__enrolled_class=class_obj).distinct()
    students = list(students_qs.values('id', 'student_id', 'first_name', 'last_name'))
    return JsonResponse({'students': students})

@require_POST
def clear_uploaded_students_session(request):
    if 'uploaded_students' in request.session:
        del request.session['uploaded_students']
        request.session.modified = True
    return JsonResponse({'status': 'success'})

@csrf_exempt
def enroll_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        faculty_id = request.session.get('user_id')
        class_id = data.get('class_id')
        student_id = data.get('student_id')
        subject_code = data.get('subject_code')
        print('student_id', student_id, subject_code)

        if not student_id or not subject_code:
            print('Missing student ID or subject code')
            return JsonResponse({'error': 'Missing student ID or subject code'}, status=400)
        print('Searching Student')

        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            print('Student not found')
            return JsonResponse({'error': 'Student not found'}, status=404)
        print('1 Searching Student')
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
        except Faculty.DoesNotExist:
            print('Faculty not found')
            return JsonResponse({'error': 'Faculty not found'}, status=404)
        print('2 Searching Student')
        try:
            enrolled_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            print('Class not found')
            return JsonResponse({'error': 'Class not found'}, status=404)
        print('3 Searching Student')
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            enrolled_class=enrolled_class,
            faculty=faculty
        )

        return JsonResponse({'success': True, 'enrolled': created})

@csrf_exempt
def save_class_records(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        class_id = data.get('class_id')
        students = data.get('students', [])
        faculty_id = request.session.get('user_id')

        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
        except Faculty.DoesNotExist:
            print('Faculty not found')
            return JsonResponse({'error': 'Faculty not found'}, status=404)

        try:
            enrolled_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Class not found'})
        print('students::: ', students)

        for record in students:
            student_id = record.get('id_number')
            print('student_id:: ', student_id)
            print('record:: ', record)
            try:
                student = Student.objects.get(student_id=student_id)
                enrollment = Enrollment.objects.get(student=student, enrolled_class=enrolled_class)
            except (Student.DoesNotExist, Enrollment.DoesNotExist):
                continue  # Skip if student or enrollment not found

            # Save activity records (Quizzes, Assignments, Seatworks, Laboratory Works)
            for category, type_name in [
                ('quizzes', 'Quiz'),
                ('assignments', 'Assignment'),
                ('seatworks', 'Seatwork'),
                ('laboratory_works', 'Laboratory')
            ]:
                activities = record.get(category, {})
                print('activities::', activities)
                for activity_name, score in activities.items():
                    if score not in [None, '', 'null']:
                        ActivityRecord.objects.update_or_create(
                            enrollment=enrollment,
                            activity_type=type_name,
                            activity_name=activity_name,
                            faculty=faculty,
                            defaults={
                                'score': float(score),
                                'date': date.today()
                            }
                        )

            # # Save major exam scores (PE, ME, PFE, FE, MG, FG)
            # for key, type_name in [
            #     ('pe', 'Prelim'),
            #     ('me', 'Midterm'),
            #     ('pfe', 'Pre-Final'),
            #     ('fe', 'Final'),
            #     ('mg', 'Midterm'),  # Optional: rename or handle separately
            #     ('fg', 'Final')     # Optional: rename or handle separately
            # ]:
            #     score = record.get(key)
            #     if score not in [None, '', 'null']:
            #         ActivityRecord.objects.update_or_create(
            #             enrollment=enrollment,
            #             activity_type=type_name,
            #             activity_name=type_name,  # Or use f"{type_name} Grade" if you want to clarify
            #             faculty=faculty,
            #             defaults={
            #                 'score': float(score),
            #                 'date': date.today()
            #             }
            #         )


            # Remarks - if needed, store it in a separate model or Enrollment
            # Here's an example assuming you want to add remarks as text somewhere:
            # enrollment.remarks = record.get('remarks', '')
            # enrollment.save()

        return JsonResponse({'success': True})
