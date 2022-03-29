from pytest_mock import MockFixture

from beans.apps.impex.views import download_template_view, UploadCsvView
from factories.model_factories import UserFactory


def test_download_template_view(rf):
    request = rf.request()
    response = download_template_view(request)
    assert 200 == response.status_code
    assert {"Content-Disposition": 'attachment; filename="beans_template.csv"', "Content-Type": "text/csv"} == response.headers
    assert (b"coffee_name;country;processing;roaster;roasting_date;rating;variety;tasting_" b"notes\r\n") == response.content


def test_upload_csv_view_form_process_data(db, rf, mocker: MockFixture):
    mock_csv_to_coffees = mocker.patch("beans.apps.impex.views.csv_to_coffees")
    mock_file = mocker.MagicMock()
    mock_text_io_wrapper = mocker.patch("beans.apps.impex.views.TextIOWrapper", return_value=mock_file)

    request = rf.post("upload")
    request.user = UserFactory.create()

    view = UploadCsvView()
    view.request = request

    valid_data = {"file": "in memory file"}

    view.process_data(valid_data)

    mock_text_io_wrapper.assert_called_once_with(valid_data["file"], encoding="ascii", errors="replace")
    mock_csv_to_coffees.assert_called_once_with(request.user, mock_file)
