from django.db import models
from polls.apps import APP_NAME
from core.models import _,LinkHelper,Page,PersianCalendar,STATIC_URL

class Poll(Page):
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)

    @property
    def options_count(self):
        return len(self.option_set.all())
    @property
    def votes_count(self):
        # a=0
        # for option in self.option_set.all():
        #     a+=option.votes_count()
        # return a
        return len(Vote.objects.filter(option__poll_id=self.pk))
    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
 
    def save(self,*args, **kwargs):
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=="":
            self.class_name="poll"
        return super(Poll,self).save(*args, **kwargs)
        
class Option(models.Model,LinkHelper):
    poll=models.ForeignKey("poll", verbose_name=_("poll"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)
    def thumbnail(self):
        return f"{STATIC_URL}{APP_NAME}/img/pages/thumbnail/option.png"
    class_name="option"
    app_name=APP_NAME
    def __str__(self):
        return f"{self.poll.pk} - {self.title}"

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options")
 
    def save(self,*args, **kwargs):
        return super(Option,self).save(*args, **kwargs)
    @property
    def votes_count(self):
        return len(self.vote_set.all())           
class Vote(models.Model,LinkHelper):
    option=models.ForeignKey("option", verbose_name=_("option"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    app_name=APP_NAME
    class_name="vote"
        

    def __str__(self):
        return f"{self.option.poll.pk} - {self.profile.name} - {self.option.title}"
    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")
 
    def save(self,*args, **kwargs):
        from core.middleware import get_request
        from authentication.models import Profile
        request=get_request()
        if request is not None and request.user is not None:
            profile=Profile.objects.filter(user=request.user).first()
            if profile is not None:
                Vote.objects.filter(profile_id=profile.pk).filter(option__poll_id=self.option.poll.id).delete()
        return super(Vote,self).save(*args, **kwargs)
        