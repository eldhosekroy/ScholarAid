from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

class StudentProfile(AbstractUser):

    role=models.TextField(max_length=20,default="admin")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=150, blank=True, null=True)
    student_class = models.CharField(max_length=50, blank=True, null=True)
    FINANCIAL_STATUS_CHOICES = [
        ('low', 'Low Income'),
        ('middle', 'Middle Income'),
        ('high', 'High Income'),
    ]
    financial_status = models.CharField(max_length=10, choices=FINANCIAL_STATUS_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    sponsors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='students_sponsored',
        limit_choices_to={'role': 'sponsor'},
        blank=True
    )


    # Sponsor-specific fields
    org_address = models.TextField(blank=True, null=True)
    org_name = models.CharField(max_length=255, blank=True, null=True)
    org_license = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"



class Scholarship(models.Model):
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'sponsor'})
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    deadline = models.DateField()
    description = models.TextField()

    education_level = models.CharField(max_length=50, choices=[
        ('high_school', 'High School'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('phd', 'PhD'),
        ('vocational', 'Vocational/Trade School')
    ])
    field = models.CharField(max_length=255, blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    financial_need = models.CharField(max_length=20, choices=[
        ('not_required', 'Not Required'),
        ('preferred', 'Preferred'),
        ('required', 'Required')
    ], default='not_required')
    requirements = models.TextField(blank=True, null=True)

    # ✅ New field here
    scholarship_type = models.CharField(
        max_length=50,
        choices=[
            ('money', 'Money Based'),
            ('materials', 'Study Materials'),
            ('books', 'Books'),
            ('uniform', 'Uniform/Dress'),
            ('mixed', 'Mixed Support'),
        ],
        default='money'
    )

    benefits = models.TextField(blank=True, null=True)
    contact = models.EmailField()
    image = models.ImageField(upload_to='scholarship_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    



class Exam(models.Model):
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    passing_score = models.PositiveIntegerField(help_text="Percentage")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f"Question for {self.exam.title}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option for {self.question.text[:50]}"
    

from django.db import models
from django.conf import settings

class ScholarshipApplication(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scholarship = models.ForeignKey('Scholarship', on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    has_taken_exam = models.BooleanField(default=False)
    exam_score = models.IntegerField(null=True, blank=True)

    is_passed = models.BooleanField(default=False)  # True if passed, False if failed
    approved = models.BooleanField(default=False)   # Admin can set this to True when approved

    def __str__(self):
        return f"{self.student.username} applied for {self.scholarship.name}"

    
class Review(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.student.username}"


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.responder.username} on {self.review.id}"
