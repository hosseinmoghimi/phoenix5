from authentication.repo import ProfileRepo
from stock.models import ShareHolder


class ShareHolderRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ShareHolder.objects.all()
        self.me=ShareHolder.objects.filter(profile=self.profile)
    def list(self,*args, **kwargs):
        return self.objects.filter(app_name=self.app_name)
    def share_holder(self,*args, **kwargs):
        if 'share_holder_id' in kwargs:
            pk=kwargs['share_holder']
            share_holder= self.objects.filter(pk=pk).first()
            return share_holder
        if 'pk' in kwargs:
            pk=kwargs['pk']
            share_holder= self.objects.filter(pk=pk).first()
            return share_holder