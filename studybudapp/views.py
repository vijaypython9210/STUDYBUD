from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import CreteRoomForm,UserForm
from django.db.models import Q
from .models import Room,Topic,Message,UserProfile

# Create your views here.
def home(request):
    # Room filter with query from addressbar
    query=request.GET.get('q') if request.GET.get('q')!=None  else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(description__icontains=query) |
        Q(name__icontains=query)
        )

    # TopicName and TopicCount
    topics=Topic.objects.all()
    topicsProperty=[]
    for i in topics:
        roomCount=Room.objects.filter(Q(topic__name=i.name)).count()
        data={'topic':i.name,'topicCount':roomCount}
        topicsProperty.append(data)
    
    # Messages fetch using query
    messages=Message.objects.filter(Q(room__topic__name__icontains=query)).order_by('-created')

    context={
        'rooms':rooms,
        'topicsProperty':topicsProperty,
        'room_count':rooms.count(),
        'messages':messages,
        'userprofile':UserProfile.objects.get(user=request.user) if request.user.is_authenticated else ''
    }
    return render(request,'home.html',context)

def room(request,pk):
    # Basic of Rooms fields
    room=Room.objects.get(id=pk)
    room_message=Message.objects.filter(room=pk).order_by('-created')
    participants=room.participants.all()


    if request.method=='POST':
        # Message Create 
        Message.objects.create(
            userhost=getUserProfileId(request),
            room=room,
            body=request.POST.get('body')
        )
        if room.host.user!=request.user:
            room.participants.add(getUserProfileId(request))
        return redirect('room',pk=room.id)
    else:
        context={
            'room':room,
            'room_messages':room_message,
            'participants':participants,
            'userprofile':getUserProfileId(request) if request.user.is_authenticated else ''
        }
        return render(request,'room.html',context)

# For UserProfile Fetch using request
def getUserProfileId(request):
    userProfile=UserProfile.objects.get(user=request.user)
    return userProfile

#Here @login_required represent if you want to create a room you must login and create it.
# For Room Create
@login_required(login_url='home')
def createRoom(request):
    form=CreteRoomForm()
    if request.method=='POST':
        form=CreteRoomForm(request.POST)
        form.host=getUserProfileId(request)
        if form.is_valid():
            # Room Create
            Room.objects.create(
                host=getUserProfileId(request),
                name=form.cleaned_data['name'],
                topic=form.cleaned_data['topic'],
                description=form.cleaned_data['description'],
            )
            return redirect('home')
        else:
            messages.error('Invalid form data')
    context={
        'form':form
    }
    return render(request,'create_room_form.html',context)

# For Room Update
@login_required(login_url='home')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=CreteRoomForm(instance=room)

    if request.method=='POST':
        form=CreteRoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'create_room_form.html',{'form':form})

# For Room Update
@login_required(login_url='home')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'delete_room.html',{'obj':room.name})

# For UserProfile Details
def userProfile(request,pk):
    userProfile=UserProfile.objects.get(id=pk)
    rooms=Room.objects.filter(Q(
        host__user=userProfile.user
    ))
    messages=userProfile.message_set.all()

    topics=Topic.objects.all()
    topicsProperty=[]
    for i in topics:
        roomCount=Room.objects.filter(Q(
            topic__name=i.name , 
            host__user=userProfile.user)).count()
        data={'topic':i.name,'topicCount':roomCount}
        topicsProperty.append(data)

    context={
        'user':userProfile,
        'rooms':rooms,
        'messages':messages,
        'topicsProperty':topicsProperty,
        'userprofile':getUserProfileId(request) if request.user.is_authenticated else ''
    }

    return render(request,'userProfile.html',context)

# LoginUser
def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
            user=authenticate(request,username=username,password=password)

            if user!=None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Username and Password has not exists')
        except:
            messages.error(request,'User not exists')
        

    return render(request,'loginpage.html',{'page':'login'})

# LogoutUser
def logoutpage(request):
    logout(request)
    return redirect('home')

# RegisterUser with UserProfile
def registerpage(request):
    if request.method=='POST':  
        # New User Add   
        form=UserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            form.save()

            # Userprofile Add using user
            UserProfile.objects.create(
                user=user,
                userImage=request.FILES.get('userImage')
            )
            return redirect('home')             
        else:
           return HttpResponse('UserProfile not exists')
    else:
        form=UserForm()
        return render(request,'loginpage.html',{'page':'register','form':form})

# Delete Message
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.method=='POST':
        message.room.participants.remove(pk)
        message.delete()
        return redirect('home')
    return render(request,'delete_room.html',{'obj':message.body})

# Follow to Room
def follow(request,pk):
    room=Room.objects.get(id=pk)
    try:
        room.participants.add(getUserProfileId(request))
        return redirect('room',pk=pk)
    except:
        return redirect('home')