from .apps import APP_NAME
from .enums import IconEnum, LanguageEnum
from .models import Resume, ResumeCategory, ResumeFact, ResumeIndex, ResumePortfolio, ResumeService, ResumeSkill, ResumeTestimonial,ContactMessage
from authentication.repo import ProfileRepo

class ResumeIndexRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.language=LanguageEnum.ENGLISH
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'language' in kwargs:
            self.language=kwargs['language']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumeIndex.objects.filter(language=self.language)
    def resume_index(self,*args, **kwargs):
        pk=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            resume_index= self.objects.filter(profile_id=profile_id).first()
            if resume_index is None:
                profile=ProfileRepo(forced=True).profile(profile_id=profile_id)
                resume_index=ResumeIndex(profile_id=profile_id,title=profile.name,language=self.language)
                resume_index.save()
                # from django.utils import timezone
                # t1=ResumeTestimonial(resume_index=resume_index,teller="aa",body="sdsd",teller_description="aa1",title="aa2",footer="saa2",date_added=timezone.now())
                # t1.save()
            return resume_index
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_index= ResumeIndex.objects.filter(pk=pk).first()
        return resume_index
class PortfolioRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumePortfolio.objects.all()
    def category_list(self,*args, **kwargs):
        category_list=[]
        try:
            category_list=(i[0] for i in self.objects.values('category').distinct('category'))
        except:
            for ii in self.objects.all():
                category=ii.category
                if not category in category_list:
                    category_list.append(category)

        return category_list
    def filter_list(self,*args, **kwargs):
        filter_list=[]
        try:
            filter_list=(i[0] for i in self.objects.values('filter').distinct('filter'))
        except:
            for ii in self.objects.all():
                filter=ii.filter
                if not filter in filter_list:
                    filter_list.append(filter)

        return filter_list
    def portfolio(self,*args, **kwargs):
        pk=0
        if 'portfolio_id' in kwargs:
            pk=kwargs['portfolio_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        portfolio= self.objects.filter(pk=pk).first()
        return portfolio
class ResumeServiceRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumeService.objects.all()
    
    def resume_service(self,*args, **kwargs):
        pk=0
        if 'resume_service_id' in kwargs:
            pk=kwargs['resume_service_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_service= self.objects.filter(pk=pk).first()
        return resume_service
class ResumeRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
    
    def resume(self,*args, **kwargs):
        pk=0
        if 'resume_id' in kwargs:
            pk=kwargs['resume_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume= Resume.objects.filter(pk=pk).first()
        return resume
    def resume_category(self,*args, **kwargs):
        pk=0
        if 'resume_category_id' in kwargs:
            pk=kwargs['resume_category_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_category= ResumeCategory.objects.filter(pk=pk).first()
        return resume_category

class ResumeFactRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.language=LanguageEnum.ENGLISH
        
        if 'language' in kwargs:
            self.language=kwargs['language']        
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumeFact.objects.all()#.filter(language=self.language)
    
    def resume_fact(self,*args, **kwargs):
        pk=0
        if 'resume_fact_id' in kwargs:
            pk=kwargs['resume_fact_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_fact= self.objects.filter(pk=pk).first()
        return resume_fact
    def add(self,*args, **kwargs):
        if 'resume_index_id' in kwargs:
            resume_index_id=kwargs['resume_index_id']
            resume_index=ResumeIndex.objects.filter(pk=resume_index_id).first()
            if resume_index is None:
                return None
            if self.user.has_perm(APP_NAME+".add_resumefact") or self.profile==resume_index.profile:
                pass
            else:
                return None
            resume_fact=ResumeFact()
            resume_fact.icon=IconEnum.award
            resume_fact.color="#0563bb"
            resume_fact.resume_index=resume_index
            if 'title' in kwargs:
                resume_fact.title=kwargs['title']
            if 'count' in kwargs:
                resume_fact.count=kwargs['count']
            if 'color' in kwargs:
                resume_fact.color=kwargs['color']
            if 'priority' in kwargs:
                resume_fact.priority=kwargs['priority']
            if 'icon' in kwargs:
                resume_fact.icon=kwargs['icon']
            resume_fact.save()
            return resume_fact

 
class ResumeSkillRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.language=LanguageEnum.ENGLISH
        
        if 'language' in kwargs:
            self.language=kwargs['language']        
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumeSkill.objects.all()
    
    def resume_skill(self,*args, **kwargs):
        pk=0
        if 'resume_skill_id' in kwargs:
            pk=kwargs['resume_skill_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_skill= self.objects.filter(pk=pk).first()
        return resume_skill
    def add(self,*args, **kwargs):
        if 'resume_index_id' in kwargs:
            resume_index_id=kwargs['resume_index_id']
            resume_index=ResumeIndex.objects.filter(language=self.language).filter(pk=resume_index_id).first()
            if resume_index is None:
                return None
            if self.user.has_perm(APP_NAME+".add_resumeskill") or self.profile==resume_index.profile:
                pass
            else:
                return None
            resume_skill=ResumeSkill()
            resume_skill.priority=100
            resume_skill.resume_index=resume_index
            if 'title' in kwargs:
                resume_skill.title=kwargs['title']
            if 'percentage' in kwargs:
                resume_skill.percentage=kwargs['percentage']
            if 'priority' in kwargs:
                resume_skill.priority=kwargs['priority']
            resume_skill.save()
            return resume_skill

            

class ContactMessageRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.app_name=""
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        self.objects = ContactMessage.objects
        self.me=ProfileRepo(user=self.user).me
    def add(self,*args, **kwargs):
        contact_message=ContactMessage()
        contact_message.app_name=self.app_name
        if 'full_name' in kwargs:
            contact_message.full_name=kwargs['full_name']
        if 'resume_index_id' in kwargs:
            contact_message.resume_index_id=kwargs['resume_index_id']
        if 'subject' in kwargs:
            contact_message.subject=kwargs['subject']
        if 'email' in kwargs:
            contact_message.email=kwargs['email']
        if 'message' in kwargs:
            contact_message.message=kwargs['message']
        if 'mobile' in kwargs:
            contact_message.mobile=kwargs['mobile']
        contact_message.save()
        return contact_message