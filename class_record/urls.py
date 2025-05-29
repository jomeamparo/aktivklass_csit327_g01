from django.urls import path
from .views import class_record_detail, enroll_student, save_class_records, search_students, upload_class_list, save_uploaded_students_to_class, get_class_students, clear_uploaded_students_session

urlpatterns = [
    path('<int:class_id>/', class_record_detail, name='class_record_detail'),
    path('search_students/', search_students, name='search_students'),
    path('class/<int:class_id>/upload/', upload_class_list, name='upload_class_list'),
    path('class_record/class/<int:class_id>/upload/', upload_class_list, name='upload_class_list'),
    path('class_record/class/<int:class_id>/save/', save_uploaded_students_to_class, name='save_uploaded_students_to_class'),
    path('class/<int:class_id>/students/', get_class_students, name='get_class_students'),
    path('clear_uploaded_students/', clear_uploaded_students_session, name='clear_uploaded_students_session'),
    path('enroll_student/', enroll_student, name='enroll_student'),
    path('class_record/<int:class_id>/<str:role>/', class_record_detail, name='class_record_detail'),
    path('save_class_records/', save_class_records, name='save_class_records'),
]
