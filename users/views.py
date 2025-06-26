from django.contrib import messages
from xml.dom.minidom import Document
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import Scholarship, ScholarshipApplication, StudentProfile, Review, ReviewReply  # Your custom user model
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Exam, Question, Option

from . import models

# Create your views here.
def home(request):
    return render(request,'home.html')

#def login(requset):
#    return render(requset,'login.html')

#def studreg(request):
#    return render(request,'studreg.html')

from django.shortcuts import render, redirect
from .forms import StudentProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def studreg(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            password=form.cleaned_data['password']
            # Create a new Django User (for login later)
            # user = User.objects.create_user(
            #     username=form.cleaned_data['email'],
            #     password = make_password(password),
            #     email=form.cleaned_data['email']
            # )
            student = form.save(commit=False)
            student.password=make_password(password)
            student.role="student"
            student.save()
            return redirect('login')  # Or student dashboard
        else:
            print(form.errors)
    else:
        form = StudentProfileForm()
    return render(request, 'studreg.html', {'form': form})




from .forms import SponsorRegistrationForm

def sponreg(request):
    if request.method == 'POST':
        form = SponsorRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            sponsor = form.save(commit=False)
            sponsor.password = make_password(password)
            sponsor.role="sponsor"
            sponsor.save()
            return redirect('login_view')  # Or sponsor-specific login/dashboard
        else:
            print(form.errors)
    else:
        form = SponsorRegistrationForm()
    return render(request, 'sponreg.html', {'form': form})






User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
                return render(request, 'login.html', {'form': form})

            user = authenticate(request, username=user.username, password=password)  # use username under the hood
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_view')

def about(request):
    return render(request,'about.html')

#def examadmin(request):
#    return render(request, 'examadmin.html')

#def sponlist(request):
#    return render(request,'sponlist.html')

#def studdetails(request):
#    return render(request,'studdetails.html')

#def studlist(request):
#    return render(request,'studelist')

#def allscholar(request):
#    return render(request,'allscholar.html')

# def ourscholar(request):
#     return render(request, 'ourscholar.html')

# def addscholar(request):
#     return render(request, 'addscholar.html')
#def sponreg(request):
#    return render(request,'sponreg.html')

@login_required(login_url='login_view')
def addscholar(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        deadline = request.POST.get('deadline')
        scholarship_type = request.POST.get('scholarship_type')
        description = request.POST.get('description')
        education_level = request.POST.get('education_level')
        field = request.POST.get('field')
        gpa = request.POST.get('gpa') or None
        financial_need = request.POST.get('financial_need')
        requirements = request.POST.get('requirements')
        benefits = request.POST.get('benefits')
        contact = request.POST.get('contact')
        image = request.FILES.get('image')

        # create scholarship
        Scholarship.objects.create(
            sponsor=request.user,
            name=name,
            amount=amount,
            deadline=deadline,
            description=description,
            education_level=education_level,
            field=field,
            gpa=gpa,
            financial_need=financial_need,
            requirements=requirements,
            scholarship_type=scholarship_type,
            benefits=benefits,
            contact=contact,
            image=image
        )
        #messages.success(request, 'Scholarship created successfully!')
        return redirect('ourscholar')  # redirect to your scholarship listing page

    return render(request, 'addscholar.html')


@login_required(login_url='login_view')
def ourscholar(request):
    scholarships = Scholarship.objects.filter(sponsor=request.user).order_by('-created_at')
    return render(request, 'ourscholar.html', {'scholarships': scholarships})


# views.py

def allscholar(request):
    scholarships = Scholarship.objects.select_related('sponsor').all()

    # Filters
    field = request.GET.get('field')
    level = request.GET.get('level')
    amount = request.GET.get('amount')
    deadline = request.GET.get('deadline')

    if field:
        scholarships = scholarships.filter(field__iexact=field)
    if level:
        scholarships = scholarships.filter(education_level__iexact=level)
    if amount:
        scholarships = scholarships.filter(amount__gte=int(amount))
    if deadline:
        try:
            days = int(deadline)
            date_limit = timezone.now().date() + timedelta(days=days)
            scholarships = scholarships.filter(deadline__lte=date_limit)
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(scholarships, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'scholarships': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'allscholar.html', context)




# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import StudentProfile


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@login_required
def studlist(request):
    search_query = request.GET.get('q', '')
    students = StudentProfile.objects.filter(role="student")

    if search_query:
        students = students.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(school__icontains=search_query)
        )

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "studlist.html", {
        "students": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj
    })


@login_required
def studdetails(request, student_id):
    student = get_object_or_404(StudentProfile, pk=student_id, role='student')
    # documents = Document.objects.filter(student=student)
    return render(request, 'studdetails.html', {
        'student': student,
        # 'documents': documents,
    })

# @login_required
# @user_passes_test(is_admin)
# def studdetail(request, student_id):
#     student = get_object_or_404(StudentProfile, id=student_id, role="student")
#     return render(request, "studdetail.html", {"student": student})


@login_required
@require_POST
@user_passes_test(is_admin)
def delete_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id, role="student")
    student.delete()
    return redirect("studlist")




from django.db.models import Sum

@login_required
def sponlist(request):
    sponsors = StudentProfile.objects.filter(role="sponsor")

    paginator = Paginator(sponsors, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for sponsor in page_obj:
        sponsor.scholarships = Scholarship.objects.filter(sponsor=sponsor)
        sponsor._students = sponsor.students_sponsored.all()  # ✅ Store for template use
        sponsor._students_count = sponsor._students.count()   # ✅ Optional count
        sponsor.total_funding = sponsor.scholarships.aggregate(
            total=Sum("amount")
        )['total'] or 0

    context = {
        "sponsors": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "sponlist.html", context)



@login_required
def delete_sponsor(request, sponsor_id):
    sponsor = get_object_or_404(StudentProfile, id=sponsor_id, role="sponsor")
    if request.method == "POST":
        sponsor.delete()
        messages.success(request, "Sponsor deleted successfully.")
        return redirect("sponlist")
    return redirect("sponlist")




@login_required
def spondetail(request, sponsor_id):
    sponsor = get_object_or_404(StudentProfile, id=sponsor_id, role="sponsor")
    scholarships = Scholarship.objects.filter(sponsor=sponsor)
    students = sponsor.students_sponsored.all()

    # Calculate total funding
    total_funding = scholarships.aggregate(total=Sum("amount"))['total'] or 0

    context = {
        "sponsor": sponsor,
        "scholarships": scholarships,
        "students": students,
        "total_funding": total_funding,
    }
    return render(request, "spondetail.html", context)



@login_required
def examadmin(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        duration = request.POST.get("duration")
        passing_score = request.POST.get("passing_score")
        scholarship_id = request.POST.get("scholarship_id")

        scholarship = Scholarship.objects.get(id=scholarship_id) if scholarship_id else None

        exam = Exam.objects.create(
            title=title,
            description=description,
            duration=duration,
            passing_score=passing_score,
            scholarship=scholarship
        )

        # Handle dynamic questions
        i = 0
        while f"questions[{i}][text]" in request.POST:
            question_text = request.POST.get(f"questions[{i}][text]")
            correct_option = request.POST.get(f"questions[{i}][correct]")

            question = Question.objects.create(exam=exam, text=question_text)

            for j in range(4):
                option_text = request.POST.get(f"questions[{i}][options][{j}]")
                is_correct = str(j) == correct_option
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )
            i += 1

        return redirect("examadmin")

    exams = Exam.objects.all()
    scholarships = Scholarship.objects.all()
    return render(request, "examadmin.html", {
        "exams": exams,
        "scholarships": scholarships
    })

@login_required
@require_POST
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    #messages.success(request, "Exam deleted.")
    return redirect("examadmin")



# @login_required
# def exam(request, exam_id):
#     exam = get_object_or_404(Exam, id=exam_id)
#     if request.method == "POST":
#         selected_options = {}
#         score = 0
#         total_questions = exam.questions.count()
#         results = []

#         for question in exam.questions.all():
#             selected_option_id = request.POST.get(f"question_{question.id}")
#             if selected_option_id:
#                 try:
#                     selected_option = Option.objects.get(id=selected_option_id, question=question)
#                     is_correct = selected_option.is_correct
#                     if is_correct:
#                         score += 1
#                     results.append({
#                         'text': question.text,
#                         'is_correct': is_correct,
#                         'options': [
#                             {
#                                 'id': opt.id,
#                                 'text': opt.text,
#                                 'is_correct': opt.is_correct
#                             } for opt in question.options.all()
#                         ]
#                     })
#                     selected_options[selected_option.id] = True
#                 except Option.DoesNotExist:
#                     results.append({
#                         'text': question.text,
#                         'is_correct': False,
#                         'options': [
#                             {
#                                 'id': opt.id,
#                                 'text': opt.text,
#                                 'is_correct': opt.is_correct
#                             } for opt in question.options.all()
#                         ]
#                     })
#             else:
#                 results.append({
#                     'text': question.text,
#                     'is_correct': False,
#                     'options': [
#                         {
#                             'id': opt.id,
#                             'text': opt.text,
#                             'is_correct': opt.is_correct
#                         } for opt in question.options.all()
#                     ]
#                 })

#         percentage_score = int((score / total_questions) * 100)
#         passed = percentage_score >= exam.passing_score

#         context = {
#             'exam': exam,
#             'results': results,
#             'score': percentage_score,
#             'passed': passed,
#             'questions': results,
#             'selected_options': selected_options
#         }
#         return render(request, 'exam.html', context)

#     context = {
#         'exam': exam,
#         'results': None
#     }
#     return render(request, 'exam.html', context)


@login_required
def exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        selected_options = {}
        score = 0
        total_questions = exam.questions.count()
        results = []

        for question in exam.questions.all():
            selected_option_id = request.POST.get(f"question_{question.id}")
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id, question=question)
                    is_correct = selected_option.is_correct
                    if is_correct:
                        score += 1
                    selected_options[selected_option.id] = True
                except Option.DoesNotExist:
                    is_correct = False
            else:
                is_correct = False

            results.append({
                'text': question.text,
                'is_correct': is_correct,
                'options': [
                    {'id': opt.id, 'text': opt.text, 'is_correct': opt.is_correct}
                    for opt in question.options.all()
                ]
            })

        percentage_score = int((score / total_questions) * 100)
        passed = percentage_score >= exam.passing_score

        # ✅ Update ScholarshipApplication
        try:
            application = ScholarshipApplication.objects.get(student=request.user, scholarship=exam.scholarship)
            application.has_taken_exam = True
            application.exam_score = percentage_score
            application.is_passed = passed
            application.save()
        except ScholarshipApplication.DoesNotExist:
            pass

        # ✅ Optionally update ExamResult (if model exists)
        # ExamResult.objects.update_or_create(
        #     student=request.user,
        #     exam=exam,
        #     defaults={'score': percentage_score, 'passed': passed}
        # )

        context = {
            'exam': exam,
            'results': results,
            'score': percentage_score,
            'passed': passed,
            'questions': results,
            'selected_options': selected_options
        }
        return render(request, 'exam.html', context)

    context = {
        'exam': exam,
        'results': None
    }
    return render(request, 'exam.html', context)


@login_required
def registered_scholarships(request):
    applications = ScholarshipApplication.objects.filter(student=request.user)
    return render(request, 'registered_scholarships.html', {
        'applications': applications
    })

@login_required
def attend_exam(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    # Add logic to redirect to exam page (assuming you have an exam view setup)
    return redirect('exam', exam_id=scholarship.id)  # adjust if exam_id is different


@login_required
def apply_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)

    # Check if student already applied
    existing_application = ScholarshipApplication.objects.filter(
        student=request.user,
        scholarship=scholarship
    ).first()

    if existing_application:
        messages.success(request, "You've already applied for this scholarship.")
    else:
        # Create new application
        ScholarshipApplication.objects.create(
            student=request.user,
            scholarship=scholarship
        )
        #messages.success(request, "Successfully applied for the scholarship!")

    return redirect('registered_scholarships')  # You can change the redirect target if needed


@login_required
def my_sponsors(request):
    applications = ScholarshipApplication.objects.filter(student=request.user).select_related('scholarship__sponsor')
    sponsors = {app.scholarship.sponsor for app in applications}
    return render(request, 'my_sponsors.html', {'sponsors': sponsors})

@login_required
def applicants_list(request):
    if request.user.role != 'sponsor':
        return render(request, 'unauthorized.html')

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        application = get_object_or_404(ScholarshipApplication, id=app_id, scholarship__sponsor=request.user)
        application.approved = True
        application.save()
        return redirect('applicants_list')  # Reload the page after approval

    applications = ScholarshipApplication.objects.filter(
        scholarship__sponsor=request.user
    ).select_related('student', 'scholarship')

    return render(request, 'applicants.html', {'applications': applications})


@login_required
def review_page(request):
    if request.method == 'POST':
        if 'review_submit' in request.POST:
            review_text = request.POST.get('review')
            if review_text:
                Review.objects.create(student=request.user, text=review_text)
                messages.success(request, 'Review submitted.')

        elif 'reply_submit' in request.POST:
            review_id = request.POST.get('review_id')
            reply_text = request.POST.get('reply_text')
            if reply_text:
                review = get_object_or_404(Review, id=review_id)
                ReviewReply.objects.create(review=review, responder=request.user, reply_text=reply_text)
                messages.success(request, 'Reply submitted.')

    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review_page.html', {'reviews': reviews})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user.is_superuser:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    else:
        messages.error(request, 'Only admin can delete reviews.')
    return redirect('review_page')