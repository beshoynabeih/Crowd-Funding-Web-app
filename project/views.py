from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Project, ProjectPicture, Category
from .forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.models import User
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect

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
        "project": project
    }
    return render(request, 'project/project_detail.html', context)
    #send email
    
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
# class ProjectCreateView(CreateView):
#     model = Project
#     template_name = 'project/createproject.html'    
#     form_class = ProjectForm
#     queryset = Project.objects.all()

#     def form_valid(self, form):
#         project = form.instance
#         user = User.objects.first()
#         project.user = user
#         for image in self.request.FILES.getlist('images'):
#             ProjectPicture.objects.create(project)
#         return super(ProjectCreateView, self).form_valid(form)

