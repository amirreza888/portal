from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Field, Student, Teacher, Lesson
from .forms import StudentForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import authenticate,login,logout
# Create your views here.



def index(request):
    return render(request, "index.html")

@login_required
def student_list(request):
    com_students = Student.objects.filter(field__name='computer')
    elc_students = Student.objects.filter(field__name='Electricity2')
    mc1_students = Student.objects.filter(field__name='Mec1')
    mc2_students = Student.objects.filter(field__name='Mec2')
    return render(request, template_name='student_list.html',  context=locals())

@login_required
def student_edit(request, pk):
    if not request.META.get('HTTP_REFERER'):
        raise Http404

    student = Student.objects.get(pk=int(pk))
    if request.method == 'GET':
        form_student = StudentForm(instance=student)
        return render(request, 'student_edit.html', {'form': form_student})
    elif request.method == 'POST':
        form_student = StudentForm(request.POST, instance=student)
        if form_student.is_valid():
            form_student.save()
            return HttpResponseRedirect(reverse('app:student-list'))

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    field = request.GET.get('field', None)
    if not field:
        return render(request, 'teacher_list.html', context={'teachers':teachers})
    elif field == 'computer':
        teachers = teachers.filter(field__name='computer')
    elif field == 'electricity2':
        teachers = teachers.filter(field__name='Electricity2')
    elif field == 'Mec1':
        teachers = teachers.filter(field__name='Mec1')
    elif field == 'Mec2':
        teachers = teachers.filter(field__name='Mec2')
    return render(request, 'teacher_list.html', context={'teachers': teachers})

@login_required
def lesson_list(request):
    com_lessons = Lesson.objects.filter(term__name='computer')
    elc_lessons = Lesson.objects.filter(term__name='Electricity2')
    mc1_lessons = Lesson.objects.filter(term__name='Mec1')
    mc2_lessons = Lesson.objects.filter(term__name='Mec2')
    return render(request, 'lesson_list.html', context=locals())

@login_required
def add_lesson_into_session(request, lesson_pk):
    lesson_added = Lesson.objects.get(pk=lesson_pk)
    session_value = request.session.get('lessons', False)
    if not session_value:
        request.session['lessons'] = []

    lessons=Lesson.objects.filter(pk__in=request.session['lessons'])
    sum_of_unit=0
    for lesson in lessons:
        sum_of_unit += lesson.number_of_unit

    student = Student.objects.get(user=request.user)
    final_selected_lessons = Lesson.objects.filter(students=student)

    for lesson in final_selected_lessons:
        sum_of_unit += lesson.number_of_unit

    if sum_of_unit+lesson_added.number_of_unit <= 6 and lesson_pk not in request.session['lessons']:
        if request.session['lessons']:
            if request.session['lessons'][0].term.name != lesson_added.term.name:
                request.session['lessons'].append(lesson_pk)
            else :
                messages.warning(request, ("فقط از یک رشته قابل اخذ است"))
        else:
            request.session['lessons'].append(lesson_pk)
    else:
        if sum_of_unit+lesson_added.number_of_unit > 6:
            messages.warning(request, ("حداکثر 6 واحد قابل اخذ است"))
        else :
            messages.warning(request, ("امکان اخذ دوباره وجود ندارد"))



    return HttpResponseRedirect('/lesson-list/')

@login_required
def final_page(request):
    session_value = request.session.get('lessons', False)
    session_lessons = []
    if session_value:
        session_lessons=Lesson.objects.filter(pk__in=session_value)
    student = Student.objects.get(user=request.user)
    final_selected_lessons = Lesson.objects.filter(students=student)
    return render(request, 'final_page.html', {'session_lessons': session_lessons, 'final_selected_lessons': final_selected_lessons})

@login_required
def add_final_lesson(request):
    session_value = request.session.get('lessons', False)

    if session_value:
        final_lessons = Lesson.objects.filter(pk__in=session_value)
        student = Student.objects.get(user=request.user)
        for lesson in final_lessons:
            lesson.students.add(student)
            lesson.save()
        del request.session['lessons']
    return HttpResponseRedirect(reverse('app:final'))

@login_required
def delete_final(request,pk):
    lesson=Lesson.objects.get(pk=pk)
    student = Student.objects.get(user=request.user)
    lesson.students.remove(student)
    return HttpResponseRedirect(reverse('app:final'))


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user1 = authenticate(username=username,password=password)

        if user1:
            if user1.is_active:
                login(request,user1)
                return HttpResponseRedirect(reverse('app:index'))
            else:
                return HttpResponse("Account not active")

        else:
            print("SomeOne tried to Login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:index'))


















