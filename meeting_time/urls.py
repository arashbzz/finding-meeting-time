from django.urls import re_path

from .views import ImportFile, FindingMeetingTime,Employees

urlpatterns = [
    re_path(
        r'^[/]?$',
        ImportFile.as_view(),
        name='importfile'
    ),
    re_path(
        r'^findingmeetingtime[/]?$',
        FindingMeetingTime.as_view(),
        name= 'findingmeetingtime'
    ),
    re_path(
        r'^employees[/]?$',
        Employees.as_view(),
        name='employeeslist'
    ),
]
