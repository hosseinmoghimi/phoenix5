import imp
from rest_framework.authtoken.models import Token
from django.utils import timezone
from core.constants import FAILED, SUCCEED
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile
from .apps import APP_NAME

class ProfileRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.me=None
        self.objects=None   
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'forced' in kwargs and kwargs['forced']:
            self.objects = Profile.objects.all()
        else:
            self.objects = Profile.objects.filter(enabled=True)

        if self.user is not None and self.user and self.user.is_authenticated:
            self.me = self.objects.filter(user=self.user).first()
            if self.user.has_perm(APP_NAME+".view_profile"):
                self.objects = Profile.objects.all()


    def login_by_token(self,*args, **kwargs):
        if 'token' in kwargs:
            token=kwargs['token']
        else:
            token=self.request.headers['token']
        token=Token.objects.filter(key=token).first()
        if token is not None:
            user=token.user
            return self.login_as_user(user.username,force=True)

    def reset_password(self,*args, **kwargs):
        result=FAILED
        message=""
        profile=None
        username=""
        old_password=""
        new_password=""
        request=None
        if 'request' in kwargs:
            request=kwargs['request']
        if 'username' in kwargs:
            username=kwargs['username']
        if 'old_password' in kwargs:
            old_password=kwargs['old_password']
        if 'new_password' in kwargs:
            new_password=kwargs['new_password']
            
        selected_user=User.objects.filter(username=username).first()
        
        if selected_user is None :            
            result=FAILED
            profile=None
            message="چنین کاربری وجود ندارد."
            return (result,profile,request,message)

    
        if self.user.has_perm(APP_NAME+".change_profile"):
            selected_user.set_password(new_password)
            selected_user.save()
            request=self.login(request=request,username=username,password=new_password)
            result=SUCCEED
            profile=Profile.objects.filter(user=selected_user).first()
            message="کلمه عبور با موفقیت تغییر یافت."
            return (result,profile,request,message)

        selected_user=authenticate(request=request,username=username,password=old_password)  
        if selected_user is not None:
            selected_user.set_password(new_password)
            selected_user.save()
            if selected_user is not None:
                request=authenticate(request=request,username=username,password=new_password)
                result=SUCCEED
                profile=Profile.objects.filter(user=selected_user).first()
                message="کلمه عبور با موفقیت تغییر یافت."
                return (result,profile,request,message)
        
        message="ناموفق"
        return (result,profile,request,message)
    def change_profile_image(self,profile_id,image):
        profile=self.profile(profile_id=profile_id)
        if profile is not None:
            profile.image_origin = image
            profile.save()
            return True
        return False
       
    def profile(self,*args, **kwargs):
        pk=0
        if 'profile_id' in kwargs:
            pk=kwargs['profile_id']
            return self.objects.filter(pk=pk).first()
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
        elif 'username' in kwargs:
            username=kwargs['username']
            return self.objects.filter(user__username=username).first()
        elif 'user' in kwargs:
            user=kwargs['user']
            return self.objects.filter(user=user).first()

    
    def logout(self,*args, **kwargs):
        if 'request' in kwargs:
            logout(request=kwargs['request'])
        else:
            logout(request=self.request)
            

    def login(self,request,*args, **kwargs):
        logout(request=request)
        if 'user' in kwargs:
            user=kwargs['user']
            if user is not None:
                login(request,user)
                if user.is_authenticated:
                    return (request,user)
        if 'username' in kwargs and 'password' in kwargs:
            user=authenticate(request=request,username=kwargs['username'],password=kwargs['password'])
            if user is not None:
                login(request,user)
                if user.is_authenticated:
                    return (request,user)
    def login_as_user(self,username,*args, **kwargs):
        if 'force' in kwargs and kwargs['force']:
            pass
        elif self.user.has_perm(APP_NAME+".change_profile"):
            pass
        else:
            return
        user=User.objects.filter(username=username).first()
        if user is None:
            return None
        logout(request=self.request)
        login(request=self.request,user=user,backend='django.contrib.auth.backends.ModelBackend')
        return self.request
        
    def list(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".view_profile"):
            return Profile.objects.all()
        return Profile.objects.filter(pk=0)
    

    def edit_profile(self,*args, **kwargs):
        profile_id=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        if self.user.has_perm(APP_NAME+".change_profile") or (self.me is not None and self.me.id==profile_id):
            pass
        else:
            return False

        edited_profile=Profile.objects.get(pk=profile_id)
        
        edited_user=edited_profile.user
        # first_name=""
        # last_name=""
        # mobile=""
        # slogan=""
        # address=""
        # bio=""
        if 'first_name' in kwargs:
            edited_user.first_name=kwargs['first_name']
            first_name=kwargs['first_name']
        if 'last_name' in kwargs:
            edited_user.last_name=kwargs['last_name']
            last_name=kwargs['last_name']
        if 'email' in kwargs:
            edited_user.email=kwargs['email']
            email=kwargs['email']
        if 'bio' in kwargs:
            edited_profile.bio=kwargs['bio']
            bio=kwargs['bio']
        if 'mobile' in kwargs:
            edited_profile.mobile=kwargs['mobile']
            mobile=kwargs['mobile']
        if 'address' in kwargs:
            edited_profile.address=kwargs['address']
            address=kwargs['address']
        
        edited_user.save()
        edited_profile.save()
        return True
        
    def add_profile(self,*args, **kwargs):
        user=User.objects.filter(username="leonolan2020").delete()
        if self.user.has_perm(APP_NAME+".add_profile"):
            pass
        else:
            
            return (FAILED,None,"دسترسی غیر مجاز")
        

        if 'first_name' in kwargs:
            first_name=kwargs['first_name']
        else:
            first_name=None

        
        if 'last_name' in kwargs:
            last_name=kwargs['last_name']
        else:
            last_name=None

        
        if 'email' in kwargs:
            email=kwargs['email']
        else:
            email=None

        
        if 'bio' in kwargs:
            bio=kwargs['bio']
        else:
            bio=None

        
        if 'mobile' in kwargs:
            mobile=kwargs['mobile']
        else:
            mobile=None

        
        if 'address' in kwargs:
            address=kwargs['address']
        else:
            address=None

        

        if 'username' in kwargs:
            username=kwargs['username']
        else:
            username=None

        if 'password' in kwargs:
            password=kwargs['password']
        else:
            password=None
        if not is_not_blank(username) or not is_not_blank(password):
            return (FAILED,None,"نام کاربری و کلمه عبور نا معتبر می باشد.")

            
        new_user=User.objects.filter(username=username).first()
        if new_user is not None:
            return (FAILED,None,"نام کاربری وارد شده ، تکراری می باشد.")  
        
        new_user=User.objects.filter(first_name=first_name).filter(last_name=last_name).first()
        if new_user is not None:
            return (FAILED,None,"نام و نام خانوادگی وارد شده ، تکراری می باشد.")  


        user=User.objects.create(first_name=kwargs['first_name'],email=kwargs['email'],last_name=kwargs['last_name'],username=kwargs['username'],password=kwargs['password'])
        user.save()
        user.set_password(kwargs['password'])
        user.save()  
        from utility.mail import send_mail
        send_mail(subject="your new account in phoenix",message=f"password for your new account in phoenix :{password}",receiver_email=email)
 
        profile=Profile.objects.filter(user=user).first()
        if profile is None:
            return (FAILED,None,"خطای 126")
        profile.user=user
        profile.bio=bio
        profile.mobile=mobile
        profile.address=address

        profile.save()
        return (SUCCEED,profile,"ایجاد پروفایل با موفقیت انجام شد.")
        
    def register(self,*args, **kwargs):
        # if not self.user.has_perm(APP_NAME+".add_profile"):
        #     return (FAILED,None,"")

        from django.contrib.auth.models import User
        username=""
        password=""
        email=""
        mobile=""
        last_name=""
        first_name=""
        if 'username' in kwargs:
            username=kwargs['username']
        if 'mobile' in kwargs:
            mobile=kwargs['mobile']
        if 'password' in kwargs:
            password=kwargs['password']
        if 'email' in kwargs:
            email=kwargs['email']
        if 'last_name' in kwargs:
            last_name=kwargs['last_name']
        if 'first_name' in kwargs:
            first_name=kwargs['first_name']
        if len(User.objects.filter(username=username))>0:
            return (FAILED,None,"نام کاربری تکراری")
        if len(User.objects.filter(email=email))>0:
            return (FAILED,None,"ایمیل تکراری")
        if len(Profile.objects.filter(mobile=mobile))>0:
            return (FAILED,None,"موبایل تکراری")
        profile=Profile()
        user=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        profile=Profile.objects.filter(user=user).first()
        if profile is None:
            profile=Profile(user=user)
        if 'bio' in kwargs:
            profile.bio=kwargs['bio']
        if 'mobile' in kwargs:
            profile.mobile=kwargs['mobile']
        if 'address' in kwargs:
            profile.address=kwargs['address']
        profile.save()
        result=SUCCEED
        message="successfully!"
        return (result,profile,message)



    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects