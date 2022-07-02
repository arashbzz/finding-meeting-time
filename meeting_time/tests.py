from .services import ScheduleMeeting
from unittest import  TestCase

# todo: add view, url, database test


class StudentListViewTest(TestCase):
    def test(self):
        persons= [[[]], [['07:00:00', '07:30:00'], ['08:00:00', '16:30:00'], ]]
        print (persons)
        print('--------')
        working_hours= ["07:00:00", "20:00:00"]
        duration =  30
        empty_times = list()
        for person in persons:
            empty_times.append(ScheduleMeeting.free_time(person, working_hours, duration))
        print(empty_times)
        print('--------')
        final = empty_times[0]
        calendar = empty_times[1]
        meetings = ScheduleMeeting.meeting_time(empty_times, final, calendar, duration)
        print(meetings)
        answer = [['07:30:00', '08:00:00'], ['16:30:00', '20:00:00']]
        self.assertEqual(meetings, answer)



