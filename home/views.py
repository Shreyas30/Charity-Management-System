from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import CharityUser,Donor
from django.contrib.auth import authenticate, login, logout
from home.models import Contact
from django.contrib.auth.decorators import login_required


# Create your views here.


def Home(request):
    charities = CharityUser.objects.all()
    params ={'charities' : charities}
    return render(request, 'home.html', params)


def About(request):
    # return HttpResponse('About Page')
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')

def Message(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        #Saving Message form Contact Us
        contact = Contact()
        contact.name = name
        contact.email = email
        contact.message = message

        contact.save()

        messages.success(request, "Your Message is Delivered Successfully")
        #Redirecting To Home Page
        return redirect('Home')


def CharitySignUpPage(request):
    # return HttpResponse('CharitySignUpPage')
    return render(request,'charity_signup.html')


def CharitySignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        description = request.POST['description']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        image = request.FILES['image']

        # Form Validations
        if password != cpassword:
            messages.error(request, "Password Mismatch")
            return redirect('DonorSignUpPage')
        if username.isalnum() == False:
            messages.error(request, "Username must contain Characters and Numbers Only")
            return redirect('DonorSignUpPage')
        if len(username)<4 :
            messages.error(request, "Username must contain atleast 4 Characters")
            return redirect('DonorSignUpPage')
        if len(password)<4 :
            messages.error(request, "Password must contain atleast 4 Characters")
            return redirect('DonorSignUpPage')

        #Saving Iamge
        fs = FileSystemStorage()
        fs.save(image.name, image)

        # Create New User in Django USer Model
        newUser = User.objects.create_user(username, password = password)
        newUser.first_name = name
        newUser.save()

        #Create Same USer in Charity USer model
        newCharityUser = CharityUser()
        newCharityUser.username = username
        newCharityUser.name = name
        newCharityUser.description = description
        newCharityUser.image = image.name
        newCharityUser.save()

        messages.success(request, "Sign Up Successful. You can Proceed to Login Now")
        #Redirecting To Home Page
        return redirect('Home')
    else:
        return HttpResponse('404 Not Found')

    # return HttpResponse('CharitySignUp')


def DonorSignUpPage(request):
    # return HttpResponse('DonorSignUpPage')
    return render(request,'donor_signup.html')


def DonorSignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        # Form Validations
        if password != cpassword:
            messages.error(request, "Password Mismatch")
            return redirect('DonorSignUpPage')
        if username.isalnum() == False:
            messages.error(request, "Username must contain Characters and Numbers Only")
            return redirect('DonorSignUpPage')
        if len(username)<4 :
            messages.error(request, "Username must contain atleast 4 Characters")
            return redirect('DonorSignUpPage')
        if len(password)<4 :
            messages.error(request, "Password must contain atleast 4 Characters")
            return redirect('DonorSignUpPage')
        
        #Create New User
        newUser = User.objects.create_user(username, password = password)
        newUser.first_name = fname
        newUser.last_name = lname
        newUser.save()

        messages.success(request, "Sign Up Successful. You can Proceed to Login Now")
        #Redirecting To Home Page
        return redirect('Home')
    else:
        return HttpResponse('404 Not Found')
    # return HttpResponse('DonorSignUp')
    # return redirect('DonorSignUpPage')


def LoginPage(request):
    # return HttpResponse('Login Page')
    return render(request,'login.html')


def Login(request):
    if request.method == 'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']

        user = authenticate(username=loginUsername, password=loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, f"Login Successful. We welcome you {loginUsername} ")
            return redirect('Home')
        else:
            messages.error(request,"Bad Credentials")
            return redirect('LoginPage')
    else:
        return HttpResponse("404 Not Found")

    return HttpResponse('Login')
    # return render(request,'contact.html')

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Home')


def Charity(request,slug):
    # If user has not logged in 
    if not request.user.is_authenticated:
        messages.error(request, "You need to Login first")
        return redirect('Home')

    print(request.user.username)
    # If user has logged in  
    charity = CharityUser.objects.get(username = slug)
    params = {
        "Charity":charity
    }
    return render(request,'payment.html',params)
    # return HttpResponse(f"{charity.username} {charity.name} {charity.description} ")

@login_required(login_url='/')
def Payment(request):
    if request.method == 'POST':
        username = request.POST['username']
        charityusername = request.POST['charityusername']
        amount = request.POST['amount']

        # Saving Payment Details
        donation = Donor()
        donation.username = username
        donation.charityusername = charityusername
        donation.amount = amount
        donation.save()

        # Updating Variables
        charity = CharityUser.objects.get(username = charityusername)
        charity.donors += 1
        charity.amount += int(amount)
        charity.save()

        #Successful Message
        messages.success(request, "Payment Successful")        
        return redirect(request. META['HTTP_REFERER'])