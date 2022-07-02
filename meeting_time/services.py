# --------------------------------------------------------------------------
# matching free time for employees (two person and more)
# (C) 2022 Arashbzz
# Assessment task for lime.com
# Created at 2022-Jul-1,  9:12:48
# Author: Arash Bazaz
# Email: arash.bazaz@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime
import pymongo
import pandas as pd
from rest_framework.exceptions import APIException

# Todo: move the database settings to setting.py
myclient = pymongo.MongoClient("mongodb://db:27017/")
mydb = myclient["mydatabase"]
employees_col = mydb["employees"]
busy_time_col = mydb["schadualed_times"]
reformat = mydb["reformated"]


class ScheduleMeeting:

    @staticmethod
    def employee_selecting(employees: list) -> list:
        """selecting employees and their busy time from database, and generating a data frames series """
        dfs = list()
        for personal_id in employees:
            try:
                employee = employees_col.find({"employee_id": str(personal_id)})
                for emp in employee: name = emp["employee_name"]
            except Exception as e:
                raise APIException(detail=str(e))
            try:
                meeting_times = busy_time_col.find({"employee_id": str(personal_id)})
                dataset = list()
                for x in meeting_times:
                    time_from = datetime.strptime(str(x["time_from"]), "%m/%d/%Y %I:%M:%S %p")
                    time_to = datetime.strptime(str(x["time_to"]), "%m/%d/%Y %I:%M:%S %p")
                    dataset.append({"date": time_from.date(), "time_from": time_from.time(), "time_to": time_to.time()})
                dfs.append(pd.DataFrame(dataset))
            except Exception as e:
                raise APIException(detail=str(e))
        return dfs

    def finding_matching_time(self, dfs: list, day_range: str, duration: int, working_hours: list) -> dict:
        """finding matching time in each day for persons  """
        result = dict()

        try:
            day_from_format = datetime.strptime(day_range[0], "%Y-%m-%d")
            day_to_format = datetime.strptime(day_range[1], "%Y-%m-%d")
        except Exception as e:
            raise APIException(detail=str(e))

        daterange = pd.date_range(day_from_format, day_to_format)
        for day in daterange:
            busy_d = list()
            persons = list()
            for df in dfs:
                x = df.sort_values(by='time_from').loc[df["date"] == day]
                busy_d.append(x)

            # preparing busy times series for each person in day
            for a in busy_d:
                b = list()
                if len(a) == 0:  # condition if the employee does not have any schedule meetings
                    b.append([])
                for i in range(0, len(a)):
                    b.append([str(a.iat[i, 1]), str(a.iat[i, 2])])
                persons.append(b)
            empty_times = list()
            for person in persons:
                empty_times.append(self.free_time(person, working_hours, duration))
            print (persons)
            # condition if the one employee was inputted
            if len(empty_times) == 1:
                empty_times.append(empty_times[0])

            # the initial conditions for recursive meeting_time function
            final = empty_times[0]
            calendar = empty_times[1]

            meetings = self.meeting_time(empty_times,final, calendar, duration)
            result.update({str(day).split()[0]: meetings})
        return result

    @staticmethod
    def free_time(busy_time, working_hours, duration):
        """finding free time in day for a person """
        free_times = list()
        try:
            start_working = datetime.strptime(working_hours[0], "%H:%M:%S")
            end_working = datetime.strptime(working_hours[1], "%H:%M:%S")
        except Exception as e:
            raise APIException(detail=str(e))

        if len(busy_time) == 1:
            free_times.append([str(start_working.time()), str(end_working.time())])
        else:
            try:
                start_busy = datetime.strptime((str(busy_time[0][0])), "%H:%M:%S")
                end_busy = datetime.strptime(str(busy_time[len(busy_time) - 1][1]), "%H:%M:%S")
            except Exception as e:
                raise APIException(detail=str(e))
            min_start = (start_busy - start_working).seconds / 60
            min_end = (end_working - end_busy).seconds / 60
            if min_start >= float(duration):
                free_times.append([working_hours[0], busy_time[0][0]])
            for i in range(len(busy_time) - 1):
                if ((datetime.strptime(busy_time[i + 1][0], "%H:%M:%S") - datetime.strptime(busy_time[i][1],
                                                                        "%H:%M:%S")).seconds / 60) >= float(duration):
                    free_times.append([busy_time[i][1], busy_time[i + 1][0]])
            if min_end >= float(duration):
                free_times.append([busy_time[len(busy_time) - 1][1], working_hours[1]])

        return free_times

    @classmethod
    def meeting_time(cls, empty_times, free_time_person1, free_time_person2, duration):
            """matching free times of employees for each day using recursive algorithm """
            pre_check = list()
            for i in range(len(free_time_person1)):
                for j in range(len(free_time_person2)):
                    a = free_time_person1[i][0]
                    b = free_time_person1[i][1]
                    c = free_time_person2[j][0]
                    d = free_time_person2[j][1]

                    if datetime.strptime(b, "%H:%M:%S") <= datetime.strptime(d, "%H:%M:%S"):
                        if datetime.strptime(a, "%H:%M:%S") >= datetime.strptime(c, "%H:%M:%S"):
                            if ((datetime.strptime(b, "%H:%M:%S") - datetime.strptime(a,
                                                                                      "%H:%M:%S")).seconds / 60) >= float(
                                duration):
                                pre_check.append([a, b])
                        else:
                            if ((datetime.strptime(b, "%H:%M:%S") - datetime.strptime(c,
                                                                                      "%H:%M:%S")).seconds / 60) >= float(
                                duration):
                                pre_check.append([c, b])
                    else:
                        if datetime.strptime(a, "%H:%M:%S") >= datetime.strptime(c, "%H:%M:%S"):
                            if ((datetime.strptime(d, "%H:%M:%S") - datetime.strptime(a,
                                                                                      "%H:%M:%S")).seconds / 60) >= float(
                                duration):
                                pre_check.append([a, d])
                        else:
                            if ((datetime.strptime(d, "%H:%M:%S") - datetime.strptime(c,
                                                                                      "%H:%M:%S")).seconds / 60) >= float(
                                duration):
                                pre_check.append([c, d])
            final_check = list()
            for i in range(len(pre_check)):
                if datetime.strptime(pre_check[i][0], "%H:%M:%S") < datetime.strptime(pre_check[i][1], "%H:%M:%S"):
                    final_check.append([pre_check[i][0], pre_check[i][1]])
            empty_times.pop(0)
            if len(empty_times) != 0:
                return cls.meeting_time(empty_times,final_check, empty_times[0], duration)
            else:
                return final_check
