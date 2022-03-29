from django.urls import path

from beans.apps.impex.views import UploadCsvView, download_template_view

urlpatterns = [
    path("upload/", UploadCsvView.as_view(), name="upload"),
    path("download-template", download_template_view, name="download-template"),
]
