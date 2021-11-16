from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
import re
from datetime import datetime
import requests

import utils.rest_utils as rest_utils

from integrity_services.BaseIntegrityResource import BaseIntegrityResource


class CoursesIntegrity(BaseIntegrityResource):

    def __init__(self):
        super(CoursesIntegrity, self).__init__()

    field_list = ["course_name", "course_year", "course_sem", "dept",
                  "course_number", "section", "professor", "TA", "credits",
                  "course_days", "start_time", "end_time", "location",
                  "enrollment"]
    required_fields = ["course_name", "course_year", "course_sem", "dept",
                       "course_number", "section", "professor", "credits",
                       "course_days"]

    @classmethod
    def get_responses(cls, res):
        if res:
            return 200
        else:
            return 404

    @classmethod
    def type_validation(cls, data):
        input_fields = list(data.keys())
        errors = {}

        try:
            for k in data.keys():
                if k not in CoursesIntegrity.field_list:
                    raise ValueError("Invalid data fields provided.")
        except ValueError as v:
            errors["fields"] = str(v)

        try:
            if "course_year" in input_fields:
                year = data["course_year"]
                if type(year) != int:
                    raise ValueError("Course year must be an integer.")
                if re.match("^[0-9]{4}$", str(year)) is None:
                    raise ValueError("Invalid course year.")
        except ValueError as v:
            errors["course_year"] = str(v)

        try:
            if "course_sem" in input_fields:
                sem = data["course_sem"]
                if type(sem) != str or sem not in ["Fall", "Spring", "Summer"]:
                    raise ValueError("Invalid semester provided, must be " +
                                     "Fall, Spring, or Summer.")
        except ValueError as v:
            errors["course_sem"] = str(v)

        try:
            if "dept" in input_fields:
                dept = data["dept"]
                if type(dept) != str or re.match("^[a-zA-Z]{4}$", dept) is None:
                    raise ValueError("Invalid department code provided; must " +
                                     "be 4 letters.")
        except ValueError as v:
            errors["dept"] = str(v)

        try:
            if "course_number" in input_fields:
                cnum = data["course_number"]
                if type(cnum) != str or re.match("\w[0-9]{4}$", cnum) is None:
                    raise ValueError("Invalid course number provided; must " +
                                     "be a letter followed by 4 numbers.")
        except ValueError as v:
            errors["course_number"] = str(v)

        try:
            if "section" in input_fields:
                section = data["section"]
                if type(section) != str or re.match("^[a-zA-Z0-9]{3}$",
                                                    section) is None:
                    raise ValueError("Invalid section number; must be 3 " +
                                     "digits/letters passed in as a string.")
        except ValueError as v:
            errors["section"] = str(v)

        try:
            if "professor" in input_fields:
                prof = data["professor"]
                if type(prof) != str:
                    raise ValueError("Invalid entry for professor, must be a " +
                                     "string.")
        except ValueError as v:
            errors["professor"] = str(v)

        try:
            if "TA" in input_fields:
                ta = data["TA"]
                if type(ta) != str:
                    raise  ValueError("Invalid entry for TA, must be a string.")
        except ValueError as v:
            errors["TA"] = str(v)

        try:
            if "credits" in input_fields:
                creds = data["credits"]
                if type(creds) != int or re.match("^[0-9]$", str(creds)) is \
                        None:
                    raise ValueError("Invalid value for number of credits.")
        except ValueError as v:
            errors["credits"] = str(v)

        try:
            if "course_days" in input_fields:
                days = data["course_days"]
                if type(days) != str or re.match("^[MTWRFO]+$", days) is None:
                    raise ValueError("Invalid entry for course days; " +
                                     "acceptable values are any combination " +
                                     "of MTWRFO, where O is for an online " +
                                     "course.")
        except ValueError as v:
            errors["course_days"] = str(v)

        try:
            if "start_time" in input_fields:
                start_time = data["start_time"]
                if type(start_time) != str:
                    raise ValueError("Start time must be a string in this " +
                                     "format: 'Hour{1-12}:Minute{00-59} AM/PM'"
                                     + ".")
                try:
                    datetime.strptime(start_time, "%I:%M %p").time()
                except ValueError:
                    raise ValueError("Invalid start time; must be a string " +
                                     "in this format: " +
                                     "'Hour{1-12}:Minute{00-59} AM/PM'.")
        except ValueError as v:
            errors["start_time"] = str(v)

        try:
            if "end_time" in input_fields:
                end_time = data["end_time"]
                if type(end_time) != str:
                    raise ValueError("End time must be a string in this " +
                                     "format: 'Hour{1-12}:Minute{00-59} AM/PM'"
                                     + ".")
                try:
                    datetime.strptime(end_time, "%I:%M %p").time()
                except ValueError:
                    raise ValueError("Invalid end time; must be a string in " +
                                     "this format: " +
                                     "'Hour{1-12}:Minute{00-59} AM/PM'.")
        except ValueError as v:
            errors["end_time"] = str(v)

        try:
            if "location" in input_fields:
                loc = data["location"]
                if type(loc) != str:
                    raise ValueError("Invalid entry for location, " +
                                     "must be a string.")
        except ValueError as v:
            errors["location"] = str(v)

        try:
            if "enrollment" in input_fields:
                enrollment = data["enrollment"]
                if type(enrollment) != int:
                    raise ValueError("Enrollment must be a number.")
        except ValueError as v:
            errors["enrollment"] = str(v)

        if errors:
            return 400, errors

        return 200, "Data Types Validated"

    @classmethod
    def external_validation(cls, data):
        # check Vergil API for universal course ID info
        base_url = 'https://doc.search.columbia.edu/' \
                   'vergil-search-query.php?key='
        query_str = data["dept"] + data["course_number"] + '_' + data[
            "section"] + '_' + str(data["course_year"]) + '_'
        semester_dict = {'Fall': '3', 'Spring': '1', 'Summer': '2'}
        if data["course_sem"] in semester_dict:
            query_str += semester_dict[data["course_sem"]]

        payload = {}
        headers = {}
        response = requests.request("GET", base_url + query_str,
                                    headers=headers, data=payload)
        json_res = json.loads(response.text[5:])
        if len(json_res['items']) > 0:
            return False
        return True

    @classmethod
    def input_validation(cls, data):
        input_fields = list(data.keys())
        errors = {}

        try:
            for r in CoursesIntegrity.required_fields:
                if r not in input_fields:
                    raise ValueError("Missing required data fields; " +
                                     "course_name, course_year, course_sem, " +
                                     "dept, course_number, section, professor, "
                                     + "credits, and course_days are required.")
        except ValueError as v:
            errors["required_fields"] = str(v)

        type_errors = CoursesIntegrity.type_validation(data)

        if type_errors[0] == 400:
            errors.update(type_errors[1])

        if errors:
            return 400, errors

        vergil_errors = CoursesIntegrity.external_validation(data)
        if vergil_errors:
            errors['Course Info Validation'] = "This course does not exist " \
                                               "on Vergil"
            return 400, errors

        return 200, "Input Validated"

    @classmethod
    def post_responses(cls, res):
        rsp = ""
        if res == 422:
            rsp = Response("Course already exists!", status=422,
                           content_type="text/plain")
        elif type(res) == tuple:
            if res[0] == 400:
                rsp = Response(json.dumps(res[1], default=str), status=res[0],
                               content_type="application/json")
        elif res is not None:
            rsp_dict = {"Response": "Success! Created course with the given " +
                                    "information.", "Location": "/api/courses/"
                                                                + res}
            rsp = Response(json.dumps(rsp_dict), status=201,
                           content_type="application/json")
        else:
            rsp = Response("Failed! Unprocessable entity.",
                           status=422, content_type="text/plain")

        return rsp

    @classmethod
    def put_responses(cls, res):
        if res == 422:
            return 422
        elif type(res) == tuple and len(res) == 2:
            if res[0] == 400:
                return res[0]
        elif res is not None:
            return 200

    @classmethod
    def delete_responses(cls, res):
        if res is not None:
            return 204
        else:
            return 422

    @classmethod
    def course_collection_get_responses(cls, res):
        status = CoursesIntegrity.get_responses(res)
        if status == 200:
            rsp = Response(json.dumps(res, default=str), status=status,
                           content_type="application/json")
        else:
            rsp = Response("No data found!", status=status,
                           content_type="text/plain")

        return rsp

    @classmethod
    def course_collection_put_responses(cls, res):
        status = CoursesIntegrity.put_responses(res)
        rsp = ""
        if status == 422:
            rsp = Response("Update violates data integrity!", status=status,
                           content_type="text/plain")
        elif status == 400:
            rsp = Response(json.dumps(res[1], default=str), status=status,
                           content_type="application/json")
        elif status == 200:
            rsp = Response("Success! The given data for the courses " +
                           "that matched was updated as requested.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Matching courses not found or unexpected "
                            + "error.",
                           status=422, content_type="text/plain")

        return rsp

    @classmethod
    def course_collection_delete_responses(cls, res):
        status = CoursesIntegrity.delete_responses(res)
        if status == 204:
            rsp = Response("Success! Deleted all courses.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Could not delete all courses.",
                           status=status, content_type="text/plain")

        return rsp

    @classmethod
    def course_by_id_get_responses(cls, res):
        status = CoursesIntegrity.get_responses(res)
        if status == 200:
            rsp = Response(json.dumps(res, default=str), status=status,
                           content_type="application/json")
        else:
            rsp = Response("Failed! Course ID not found.", status=status,
                           content_type="text/plain")

        return rsp

    @classmethod
    def course_by_id_put_responses(cls, res, course_id):
        status = CoursesIntegrity.put_responses(res)
        rsp = ""
        if status == 422:
            rsp = Response("Update violates data integrity!", status=status,
                           content_type="text/plain")
        elif status == 400:
            rsp = Response(json.dumps(res[1], default=str), status=status,
                           content_type="application/json")
        elif status == 200:
            rsp = Response("Success! The given data for the course with ID " +
                           str(course_id) + " was updated as requested.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Course ID not found or unexpected error.",
                           status=422, content_type="text/plain")

        return rsp

    @classmethod
    def course_by_id_delete_responses(cls, res, course_id):
        status = CoursesIntegrity.delete_responses(res)
        if status == 204:
            rsp = Response("Success! Deleted course with ID " +
                           str(course_id) + ".",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Course ID not found.",
                           status=status, content_type="text/plain")

        return rsp

    @classmethod
    def course_by_code_get_responses(cls, res):
        status = CoursesIntegrity.get_responses(res)
        if status == 200:
            rsp = Response(json.dumps(res, default=str), status=status,
                           content_type="application/json")
        else:
            rsp = Response("Failed! Course code not found.", status=status,
                           content_type="text/plain")

        return rsp

    @classmethod
    def course_by_code_put_responses(cls, res, course_code):
        status = CoursesIntegrity.put_responses(res)
        rsp = ""
        if status == 422:
            rsp = Response("Update violates data integrity!", status=status,
                           content_type="text/plain")
        elif status == 400:
            rsp = Response(json.dumps(res[1], default=str), status=status,
                           content_type="application/json")
        elif status == 200:
            rsp = Response("Success! The given data for the course with code " +
                           str(course_code) + " was updated as requested.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Course code not found or unexpected error.",
                           status=422, content_type="text/plain")

        return rsp

    @classmethod
    def course_by_code_delete_responses(cls, res, course_code):
        status = CoursesIntegrity.delete_responses(res)
        if status == 204:
            rsp = Response("Success! Deleted course with code " +
                           str(course_code) + ".",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Course code not found.",
                           status=status, content_type="text/plain")

        return rsp
