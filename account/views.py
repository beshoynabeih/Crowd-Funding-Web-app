from django.contrib.auth.models import User
from .forms import  UserProfile, DenoteForm
from project.models import Project, Denote
from project.forms import ProjectForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, Http404
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from .utils import generate_token
from django.views import View
from .models import MyUser
# Create your views here.


def home(request):
    return render(request, 'account/base.html')


def signup(request):
    form = UserProfile()
    if request.method == 'POST':
        form = UserProfile(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('account/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            send_mail(
                'Active your account',
                message,
                'noreply@gmail.com',
                [user.email]
            )
            # login(request, user)
            return redirect('login')

    return render(request, 'account/signup.html', {'form': form})


class ActiveAccountView(View):

    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(MyUser, pk=uid)
        if user and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        return redirect('home')



message = {}


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    projects = Project.objects.filter(user=user)
    donations = Denote.objects.filter(user=user)
    projectform = ProjectForm()
    donationform = DenoteForm()
    userform = UserForm()
    print(message)
    context = {
        'user': user,
        'projects': projects,
        'donations': donations,
        'projectform': projectform,
        'donationform': donationform,
        'userform': userform,
        'message': message
    }

    return render(request, 'profile.html', context)


def update_user_information(request, user_id):
    global message
    print("update user information")
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST)
        # remove constrains on username fields
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            # user.phone=form.cleaned_data.get('phone')
            # user.birthdate=form.cleaned_data.get('birthdate')
            # user.country=form.cleaned_data.get('country')
            # user.facebook_profile=form.cleaned_data.get('facebook_profile')
            user.save()
            message = {'status': "alert-success", 'message': "Update Successfully"}
        else:
            message = {'status': 'alert-danger', 'message': 'Update Failure'}

    return redirect('profile_page', user_id=user_id)


# not logic using POST , GET in Update and delete (Html 5 -- problem) can solve by using ajax request later
def update_project(request, user_id, project_id):
    global message
    print("update project")
    print(user_id)
    print(project_id)
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(User, pk=user_id)
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project.title = form.cleaned_data.get('title')
            project.details = form.cleaned_data.get('details')
            project.total_target = form.cleaned_data.get('total_target')
            project.start_date = form.cleaned_data.get('start_date')
            project.end_date = form.cleaned_data.get('end_date')
            # project.category=form.cleaned_data.get('category')
            project.save()
            message = {'status': "alert-success", 'message': "Update Successfully"}
        else:
            print("form error")
            message = {'status': 'alert-danger', 'message': 'Update Failure'}

    return redirect('profile_page', user_id=user_id)


def delete_project(request, user_id, project_id):
    print("delete projet")
    global message
    if request.method == 'POST':
        Project.objects.filter(pk=project_id)[0].delete()
        message = {'status': "alert-success", 'message': "Delete Successfully"}
    return redirect('profile_page', user_id=user_id)


def update_donation(request, user_id, donation_id):
    print("update_donation")
    global message
    donation = get_object_or_404(Denote, pk=donation_id)
    if request.method == "POST":
        form = DenoteForm(request.POST)
        if form.is_valid():
            # donation.project = form.cleaned_data.get('project')
            donation.amount = form.cleaned_data.get('amount')
            donation.save()
            message = {'status': "alert-success", 'message': "Update Successfully"}
        else:
            message = {'status': 'alert-danger', 'message': 'Update Failure'}

    return redirect('profile_page', user_id=user_id)


def delete_donation(request, user_id, donation_id):
    print(" delete_donation")
    global message
    if request.method == "POST":
        Denote.objects.filter(pk=donation_id)[0].delete()
        message = {'status': "alert-success", 'message': "Delete Successfully"}
    return redirect('profile_page', user_id=user_id)


def delete_account(request, user_id):
    print("delete account")
    print(user_id)
    # check user password then logout then delete user
    if request.method == "POST":
        User.objects.filter(pk=user_id)[0].delete()
    return HttpResponse("<h1> go to home page <h1>")