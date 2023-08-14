from django.shortcuts import render, redirect
from django.urls import reverse
from  .forms import DirUploadForm
from .models import DirUploadModel
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.conf import settings
from googleapiclient.http import MediaFileUpload
import fsutil
import secrets
import string
import datetime
import os
import asyncio
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = f'{settings.BASE_DIR}\\client_secrets.json'
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# Create your views here.
# def index(request):
#     return render(request, 'file_exchanger/index.html')

# def storage_func(path, file):
#     with open(f'uploads/{path}/{file.name}', 'wb+') as f:
#         for chunk in file.chunks():
#             f.write(chunk)
# def handle_uploaded_file(f, path):
#     with open(f'/uploads/mouse/{path}/%s' % f.name, 'wb+') as new_file:
#         for chunk in f.chunks():
#             new_file.write(chunk)
# def create_set_id():
#     letters_and_digits = string.ascii_letters + string.digits
#     set_id = ''.join(secrets.choice(letters_and_digits) for i in range(16))
#     return set_id

class MouseFormView(FormView):
    form_class = DirUploadForm
    template_name = 'file_exchanger/index.html'
    success_url = f'list'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        files = []
        for key in form.files.keys():
            files += [form.files[key]]
        letters_and_digits = string.ascii_letters + string.digits
        set_id = ''.join(secrets.choice(letters_and_digits) for i in range(16))
        files_paths = []
        for f in files:
            # create line in DB
            file = DirUploadModel(set_id=set_id, file=f, timestamp=datetime.datetime.now().timestamp())
            file.save()
            # making list of files paths for zip archive
            filep = fsutil.search_files(f'{settings.BASE_DIR}\\uploads\\', f'{file.file}')
            files_paths += filep
            # send file to google drive
            googlef = drive.CreateFile({'parents': [{'id': '1TWbuKeahtEyy0VMgafTj1WIssV6tAQOP'}],
                                        'title': f'{set_id}-{file.file}'
                                        })
            googlef.SetContentFile(f'{file.file.file}')
            googlef.Upload()
        # create zip with posted files
        fsutil.create_zip_file(f'{settings.BASE_DIR}\\uploads\\{set_id}.zip', files_paths)
        # send zip to google drive
        googlez = drive.CreateFile({'parents': [{'id': '1TWbuKeahtEyy0VMgafTj1WIssV6tAQOP'}], 'title': f'{set_id}.zip'})
        googlez.SetContentFile(f'{settings.BASE_DIR}\\uploads\\{set_id}.zip')
        # googlez.InsertPermission(new_permission)
        googlez.Upload()


        # delete from server
        del_list = fsutil.list_files(f'{settings.BASE_DIR}\\uploads\\mouse')
        for f in del_list:
            try:
                with open(f,'r') as check:
                    pass
                fsutil.delete_file(f)
            except:
                pass
        # fsutil.delete_files(files_paths)
        # fsutil.delete_file(f'{settings.BASE_DIR}\\uploads\\{set_id}.zip')

        return redirect(self.get_success_url(), set_id=set_id)




class MouseListView(ListView):
    template_name = 'file_exchanger/list.html'
    model = DirUploadModel
    context_object_name = 'list'

    def get_context_data(self, *, object_list=None, **kwargs):

        # drive = GoogleDrive(gauth)
        context = super().get_context_data(**kwargs)
        # qs = DirUploadModel.objects.filter(set_id=self.kwargs['set_id'])
        # get urls of files from google drive for links at 'list' template
        file_list = drive.ListFile({'q': f"'1TWbuKeahtEyy0VMgafTj1WIssV6tAQOP' in parents and trashed=false"}).GetList()
        # sort needed files/archive and pack urls in context
        links_list = []
        for file in file_list:
            if self.kwargs['set_id']+'-' in file['title']:
                # midfile = drive.CreateFile({'id': file['id']})
                # midfile.GetContentFile(file['title'])
                links_list += [file['webContentLink']]
            elif self.kwargs['set_id']+'.zip' in file['title']:
                # here i need to dig in db for timestamp of file (i think i made it unnecessary difficult) and set date for timer
                qs = DirUploadModel.objects.filter(set_id=f'{self.kwargs["set_id"]}')
                dt = datetime.datetime.fromtimestamp(qs[0].timestamp)+datetime.timedelta(seconds=10000)
                context['date_for_timer'] = dt.strftime('%B %d, %Y %H:%M:%S')
                context['set_id'] = file['selfLink']
                context['set_id_download'] = file['downloadUrl']+'&key='+settings.API_KEY

        context['links_list'] = links_list

        # delete from server last used (closed) files because i dont know how it's done properly
        # THAT was very annoying so i chose to NOT give this process whole separate fuction
        del_list = fsutil.list_files(f'{settings.BASE_DIR}\\uploads\\mouse')
        for f in del_list:
            try:
                with open(f, 'r') as check:
                    pass
                fsutil.delete_file(f)
            except:
                pass
        del_zip = fsutil.list_files(f'{settings.BASE_DIR}\\uploads')
        for f in del_zip:
            try:
                with open(f, 'r') as check:
                    pass
                fsutil.delete_file(f)
            except:
                pass

        clean_up_qs = DirUploadModel.objects.all()
        for obj in clean_up_qs:
            if datetime.datetime.now().timestamp() - obj.timestamp > 10000:  #604800
                # delete from google
                file_delete_list = drive.ListFile({'q': f"'1TWbuKeahtEyy0VMgafTj1WIssV6tAQOP' in parents and trashed=false"}).GetList()
                for file in file_delete_list:
                    if obj.set_id in file['title']:
                        file.Delete()
                # delete from db
                obj.delete()
        return context

def oops(request):
    return render(request, 'file_exchanger/oops.html')