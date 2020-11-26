from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Project, ProjectPicture, Category, ProjectReport, Comment, CommentReport, Denote
from .forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.models import User
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail


# Create your views here.


def index(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'project/index.html', context)


@login_required
def create_project(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = User.objects.first()
            # project.user = User.objects.first()
            project.slug = slugify(project.title)
            project.save()
            form.save_m2m()
            for image in request.FILES.getlist('images'):
                ProjectPicture.objects.create(project=project, image=image)
            messages.success(request, 'project has been created')
            return redirect('home')
        return render(request, 'project/createproject.html', {"form": form, 'categories': categories})
    return render(request, 'project/createproject.html', {"form": form, 'categories': categories})


def project_detail(request, project_id):
    categories = Category.objects.all()
    project = get_object_or_404(Project, pk=project_id)
    context = {
        "categories": categories,
        "project": project,
        "project_target_collected": Denote.objects.filter(project=project).aggregate(Sum('amount'))['amount__sum'] or 0.0
    }
    return render(request, 'project/project_detail.html', context)


@login_required
def project_report(request):
    rec = ProjectReport.objects.create(user=request.user, body=request.GET.get('body'), project_id=request.GET.get('project'))
    if rec:
        data = {'return': True}
    else:
        data = {'return': False}
    return JsonResponse(data)


@login_required
def post_comment(request, project_id):
    if request.method == "POST":
        if Project.objects.filter(pk=project_id).exists():
            comment = Comment.objects.create(body=request.POST.get('comment-body'), user=request.user, project_id=project_id)
            return redirect('project_detail', project_id)
    return redirect('project_detail', project_id)


def comment_report(request, comment_id):
    if Comment.objects.filter(pk=comment_id).exists():
        rec = CommentReport.objects.create(body=request.GET.get('body'), user=request.user, comment_id=comment_id)
    if rec:
        return JsonResponse({"return": True})
    return JsonResponse({"return": False})


def fund_project(request, project_id):
    if request.method == 'POST':
        if Project.objects.filter(pk=project_id).exists():
            rec = Denote.objects.create(user=request.user, project_id=project_id, amount=request.POST.get('amount'))
            if rec:
                messages.success(request, 'Your fund has been submitted')
                return redirect('project_detail', project_id)
            else:
                messages.success(request, 'error submitting the fund')
                return redirect('project_detail', project_id)


def signup(request, my_app=None):
    if request.method=="post":
      username=request.post["username"]
      passward = request.post["passward"]
      email = request.post["email"]
      user = User.objects.create_user(
             username=username,
             password=passward,
             email=email
      )

      login(request,user)
      subject = 'welcome to GFG world'
      message = f'Hi {user.username}, thank you for registering'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [user.email, ]
      send_mail(subject, message, email_from, recipient_list)
      return redirect("/dashboard/")
      return render(request,"signup.html")

