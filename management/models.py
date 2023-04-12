from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"

class Attendance(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    grade = models.FloatField()
