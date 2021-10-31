from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
import re
from datetime import datetime

import utils.rest_utils as rest_utils

from integrity_services.BaseIntegrityResource import BaseIntegrityResource


class CoursesIntegrity(BaseIntegrityResource):

    def __init__(self):
        super(CoursesIntegrity, self).__init__()

    @classmethod
    def get_responses(cls, res):
        if res is not None:
            return 200
        else:
            return 404

    @classmethod
    def input_validation(cls, data):
        field_list = ["course_name", "course_year", "course_sem", "dept", "course_number", "section", "professor",
                      "TA", "credits", "course_days", "start_time", "end_time", "location", "enrollment"]
        required_fields = ["course_name", "course_year", "course_sem", "dept", "course_number",
                           "section", "professor", "credits", "course_days"]
        input_fields = list(data.keys())

        try:
            for k in data.keys():
                if k not in field_list:
                    raise ValueError("Invalid data fields provided.")

            for r in required_fields:
                if r not in input_fields:
                    raise ValueError("Missing required data fields.")

            if "course_year" in input_fields:
                year = data["course_year"]
                if type(year) != int:
                    raise ValueError("Course year must be an integer.")
                if re.match("^[0-9]{4}$", str(year)) is None:
                    raise ValueError("Invalid course year.")

            if "course_sem" in input_fields:
                sem = data["course_sem"]
                if type(sem) != str or sem not in ["Fall", "Spring", "Summer"]:
                    raise ValueError("Invalid semester provided, must be Fall, Spring, or Summer.")

            if "dept" in input_fields:
                dept = data["dept"]
                if type(dept) != str or re.match("^[a-zA-Z]{4}$", dept) is None:
                    raise ValueError("Invalid department code provided; must be 4 letters.")

            if "course_number" in input_fields:
                cnum = data["course_number"]
                if type(cnum) != str or re.match("\w[0-9]{4}$", cnum) is None:
                    raise ValueError("Invalid course number provided; must be a letter followed by 4 numbers.")

            if "section" in input_fields:
                section = data["section"]
                if type(section) != str or re.match("^[a-zA-Z0-9]{3}$", section) is None:
                    raise ValueError("Invalid section number; must be 3 digits/letters passed in as a string.")

            if "professor" in input_fields:
                prof = data["professor"]
                if type(prof) != str:
                    raise ValueError("Invalid entry for professor.")

            if "TA" in input_fields:
                ta = data["TA"]
                if type(ta) != str:
                    raise  ValueError("Invalid entry for TA.")

            if "credits" in input_fields:
                creds = data["credits"]
                if type(creds) != int or re.match("^[0-9]$", str(creds)) is None:
                    raise ValueError("Invalid value for number of credits.")

            if "course_days" in input_fields:
                days = data["course_days"]
                if type(days) != str or re.match("^[MTWRFO]+$", days) is None:
                    raise ValueError("Invalid entry for course days; acceptable values are any combination of MTWRFO, where O is for an online course.")

            if "start_time" in input_fields:
                start_time = data["start_time"]
                if type(start_time) != str:
                    raise ValueError("Start time must be a string in this format: 'Hour{1-12}:Minute{00-59} AM/PM'.")
                try:
                    datetime.strptime(start_time, "%I:%M %p").time()
                except ValueError:
                    raise ValueError("Invalid start time; must be a string in this format: 'Hour{1-12}:Minute{00-59} AM/PM'.")

            if "end_time" in input_fields:
                end_time = data["end_time"]
                if type(end_time) != str:
                    raise ValueError("End time must be a string in this format: 'Hour{1-12}:Minute{00-59} AM/PM'.")
                try:
                    datetime.strptime(end_time, "%I:%M %p").time()
                except ValueError:
                    raise ValueError("Invalid end time; must be a string in this format: 'Hour{1-12}:Minute{00-59} AM/PM'.")

            if "location" in input_fields:
                loc = data["location"]
                if type(loc) != str:
                    raise ValueError("Invalid entry for location.")

            if "enrollment" in input_fields:
                enrollment = data["enrollment"]
                if type(enrollment) != int:
                    raise ValueError("Enrollment must be a number.")

        except ValueError as v:
            return 400, v

        return 200, "Input Validated"

    @classmethod
    def post_responses(cls, res):
        pass

    @classmethod
    def put_responses(cls, res):
        pass

    @classmethod
    def delete_responses(cls, res):
        pass
