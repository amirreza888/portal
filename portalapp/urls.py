from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('student-list/', views.student_list, name='student-list'),
    path('student-edit/<int:pk>/', views.student_edit, name='edit'),
    path('teacher-list/', views.teacher_list, name='teacher-list'),
    path('lesson-list/', views.lesson_list, name='lesson-list'),
    path('add/<int:lesson_pk>/', views.add_lesson_into_session, name='add'),
    path('final/', views.final_page, name='final'),
    path('add-to-final/', views.add_final_lesson, name='add_final_lesson'),
    path('delete-final/<int:pk>/', views.delete_final, name='delete_final'),
    path('logout/', views.user_logout, name='logout')


]