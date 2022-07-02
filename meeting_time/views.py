from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
import json
import pymongo
from .services import ScheduleMeeting
from .serializers import FileSerializer

# Todo: move the database settings to setting.py
myclient = pymongo.MongoClient("mongodb://db:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["employees"]
mycol_2 = mydb["schadualed_times"]
reformat = mydb["reformated"]


class ImportFile(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        # Todo: checking the file more for security reasons
        #Todo: preventing to add duplicated data
        if file_serializer.is_valid():
            file_serializer.save()
            new_file_name = (str(file_serializer['file'].value).split('/')[2])
            file = default_storage.open(new_file_name, 'r')
            lines = file.readlines()
            for line in lines:
                splited_line = str(line).split(';')
                # todo : add more condition for different data
                if len(splited_line) == 2:
                    # todo : changing the appropriate name for column
                    mydict = {"employee_id": splited_line[0], "employee_name": splited_line[1]}
                    mycol.insert_one(mydict)
                elif len(splited_line) == 4:
                    mydict = {"employee_id": splited_line[0], "time_from": splited_line[1], "time_to": splited_line[2],
                              "meeting_id": splited_line[3]}
                    mycol_2.insert_one(mydict)
            print(mycol_2.count_documents({}))
            return Response(status=status.HTTP_201_CREATED)


class FindingMeetingTime(APIView):
    def post(self, request):
        if request.method == "POST":
            # todo: cheking the inputting data
            json_string = request.body
            json_dict = json.loads(json_string)
            employees = (json_dict['employees'])
            day_range = (json_dict['day_range'])
            working_hours = (json_dict['working_hours'])
            time_def = json_dict['time_def']
            dfs = ScheduleMeeting().employee_selecting(employees)
            result = ScheduleMeeting().finding_matching_time(dfs, day_range, time_def, working_hours)
            return Response(result, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Employees(APIView):
    def get(self, request):
        result = dict()
        for x in mycol.find():
            result.update({str(x["employee_id"]): x["employee_name"]})
        return Response(result, status=status.HTTP_200_OK)
