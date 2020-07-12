from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id_num = models.IntegerField(unique=True)
    field = models.ForeignKey('Field', related_name='student', on_delete=models.CASCADE)
    number_of_unit = models.IntegerField()
    grade = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def edit_link(self):
        return reverse("app:edit",kwargs={'pk': self.pk})

    def __str__(self):
        return self.first_name


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id_num = models.IntegerField()
    field = models.ForeignKey('Field', on_delete=models.CASCADE)
    academic_rank = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name


class Field(models.Model):
    Choice = (
        ('computer', 'کامپوتر ترم 1'),
        ('Electricity2', 'برق ترم 2'),
        ('Mec1', 'مکانیک ترم 1'),
        ('Mec2', 'مکانیک ترم 2'),
    )
    name = models.CharField(max_length=15, choices=Choice, unique=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=256)
    id_number = models.IntegerField()
    number_of_unit = models.IntegerField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    number_of_student = models.IntegerField()
    term = models.ForeignKey('Field', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student',blank=True)

    def __str__(self):
        return self.name


