from django.db import models
from polls.apps import APP_NAME
from core.models import _,LinkHelper,Page,PersianCalendar,STATIC_URL

class Poll(Page):
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)

    def options_length(self):
        return len(self.option_set.all())

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

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
 
    def save(self,*args, **kwargs):
        return super(Option,self).save(*args, **kwargs)
          
class Answer(models.Model,LinkHelper):
    option=models.ForeignKey("option", verbose_name=_("option"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    app_name=APP_NAME
    class_name="answer"
        

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
 
    def save(self,*args, **kwargs):
        return super(Answer,self).save(*args, **kwargs)
        