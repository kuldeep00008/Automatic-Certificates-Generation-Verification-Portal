from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.form import UploadFileForm
from django.core.files.storage import FileSystemStorage
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from app.models import details
from PIL import ImageFont, ImageDraw,Image
import shortuuid
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
import os
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import datetime

def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'index.html')

@csrf_exempt
def logUser(request):
    context={"flag":False}
    if request.method =="POST" and not request.user.is_authenticated:
        mail = request.POST['mail']
        password = request.POST['password']

        if User.objects.filter(email=mail).exists():
            u = User.objects.get(email=mail)
            print(u.username)
            user = authenticate(request,username=u.username, password=password)
            if user is not None:
                context = {"flag":True, "info":"Welcome back %s"%u.username, 'type':'success'}
                login(request, user)
                return render(request,'index.html',context)
            else:
                context = {"flag":True, "info":"The password you have inputted is  wrong, please try again", 'type':'danger'}
                return render(request, 'login.html',context)    
        else:
            context = {"flag":True, "info":"You are not registered , please register here", 'type':'danger'}
            return render(request, 'registration.html',context)

    elif request.method == "POST":
        return render(request, 'index.html')
        
    if  not  request.user.is_authenticated:
        return render(request,'login.html')
    else:
        context = {"flag":True, "info":"you are already logged in" ,'type':'danger'}
        return render(request, 'index.html',context)
        
        
        

            









def registration(request):
    context = {"flag":False, "info":"no command yet"}
    if request.method =="POST":
        name = request.POST['name']
        mail = request.POST['mail']
        password = request.POST['password']
        if User.objects.filter(username = name).exists():
            context = {'info':"User already exists", 'flag':True, 'type':'danger'}
            print("user already exists")
            return render(request,'registration.html', context)
        elif User.objects.filter(email = mail).exists():
            context ={'info':"Email already exists",'flag':True, 'type':'danger'}
            return render(request, 'registration.html',context)    
            
        else:
            print("created user")
            context = {"flag":True, "info":"user successfully created Please login here", 'type':'success'}
            user = User.objects.create_user(name, mail, password)
            user.save()
            return render(request, 'login.html',context)
    else:    
        return render(request,'registration.html',context)



                               




def logoutView(request):
    logout(request)
    return render(request, 'index.html')    

def generate(request):
    if request.method == "POST":
        fileUpload = request.FILES['file']
        f = FileSystemStorage()
        f.save(fileUpload.name, fileUpload)
        fileName = fileUpload.name
        cur = datetime.datetime.now().strftime("%d.%m.%Y")

        
        df = pd.read_excel('uploads/%s'%fileName, sheet_name='Sheet1')
        n = df.columns[0]
        o = df.columns[1]
        c =  df.columns[2]
        m = df.columns[3]

        fullName = df[n]
        org  = df[o]
        cer =  df[c]
        mail = df[m]
        for i in range(len(df)):
            uniqueId = shortuuid.uuid()
            # Email 
            
            #data base save
            detail = details(name=fullName[i],organization=org[i],certification=cer[i],mail= mail[i],uid=uniqueId )
            detail.save()
            # Email 
            


            
            #certificate generation
            
            
            image = Image.open('certificate/template.jpg')
            font = ImageFont.truetype("arial.ttf",70)
            fontTwo=ImageFont.truetype("arial.ttf",50)
            
            

            draw = ImageDraw.Draw(image)

            # use a bitmap font
            draw.text((685, 772),fullName[i], font=font, fill="black")
            # use a truetype font
            draw.text((1232, 933), cer[i], font=fontTwo , fill ="black")
            draw.text((916, 1012), org[i], font=fontTwo , fill ="black")
            draw.text((121, 1169), 'Date: '+str(cur), font=fontTwo , fill ="black")

            image.save("static/certificates/%s.jpg" %uniqueId)

            # Email
            
            email = EmailMessage(
            'Here is you certificate ',
            'Hi, this is your certificate for completing the course, you can verify this certificate using this unique Verification Link: http://127.0.0.1:8000/static/certificates/%s.jpg'%uniqueId,
            'certificationdjango@gmail.com',
            [mail[i]],
            ['st22356@gmail.com'])
            email.attach_file('static/certificates/%s.jpg'%uniqueId)
            
            
            email.send()
            # Email 
            
            
        os.remove('uploads/%s'%fileName)    
        return render(request,'generate.html')
    else:

        return render(request, 'generate.html')
            




def verify(request,slug):
    #found = False
    context={'info':'NotFound', 'flag':False}
    for f in os.listdir('static/certificates'):
        fn,fext = os.path.splitext(f)
        print(fn)
        if fn == slug:
            context={'info':slug, 'flag':True}
            found = True
            print("found the certificate")
    return render(request, 'verify.html',context)
    


        
   



        


    
    