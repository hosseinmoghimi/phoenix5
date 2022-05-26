from phoenix.settings import ADMIN_URL
from django.shortcuts import reverse

def str_to_html(value):
    html=""
    lines=value.splitlines()
    for line in lines:
        html=html+line+"<br>"
    return html





class LinkHelper():
    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
    def get_absolute_url(self):
        return reverse(f"{self.app_name}:{self.class_name}",kwargs={'pk':self.pk})
    def get_delete_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/delete/"
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="ویرایش" href="{self.get_edit_url()}">
            <i class="fa fa-edit text-warning">
            </i>
          </a>
        """
    def get_delete_btn(self):
        return f"""
          <a target="_blank" title="حذف" href="{self.get_delete_url()}">
            <i class="fa fa-trash text-danger">
            </i>
          </a>
        """