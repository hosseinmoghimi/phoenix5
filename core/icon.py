from core.enums import PictureNameEnum
from core.views import DownloadView
from django.views import View
from django.http import Http404

from phoenix.server_settings import MEDIA_ROOT

class FavIconView(View):
    def  get(self,request,*args, **kwargs):

        file_path = str(MEDIA_ROOT)
        # return JsonResponse({'download:':str(file_path)})
        import os
        os.path.join(MEDIA_ROOT,"favicon.png")
        from django.http import HttpResponse
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
        raise Http404
