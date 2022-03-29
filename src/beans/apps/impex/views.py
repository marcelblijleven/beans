import csv
from io import TextIOWrapper

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import FormView

from beans.apps.impex.forms import UploadFileForm
from beans.apps.impex.utils import csv_to_coffees, get_csv_headers


class UploadCsvView(LoginRequiredMixin, FormView):
    """
    In this view the user can upload csv files for import
    """

    template_name = "upload_file.html"
    form_class = UploadFileForm
    success_url = "/coffees"

    def form_valid(self, form: UploadFileForm):
        self.process_data(form.cleaned_data)
        return super(UploadCsvView, self).form_valid(form)

    def process_data(self, valid_data):
        file = TextIOWrapper(valid_data["file"], encoding="ascii", errors="replace")
        csv_to_coffees(self.request.user, file)


def download_template_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="beans_template.csv"',
        },
    )

    writer = csv.writer(response, delimiter=";")
    writer.writerow(get_csv_headers())
    return response
