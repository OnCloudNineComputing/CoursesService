from flask import Response
import json

from integrity_services.BaseIntegrityResource import BaseIntegrityResource


class ProfessorCourseIntegrity(BaseIntegrityResource):

    def __init__(self):
        super(ProfessorCourseIntegrity, self).__init__()

    field_list = ["professor", "uni", "course_id"]
    required_fields = ["professor", "uni", "course_id"]

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
                if k not in ProfessorCourseIntegrity.field_list:
                    raise ValueError("Invalid data fields provided.")
        except ValueError as v:
            errors["fields"] = str(v)

        try:
            if "professor" in input_fields:
                professor_name = data["professor"]
                if type(professor_name) != str:
                    raise ValueError("Invalid entry for professor name, " +
                                     "must be a string.")
        except ValueError as v:
            errors["professor"] = str(v)

        try:
            if "uni" in input_fields:
                uni = data["uni"]
                if type(uni) != str:
                    raise ValueError("Invalid uni provided, must be " +
                                     "a string.")
        except ValueError as v:
            errors["uni"] = str(v)

        try:
            if "course_id" in input_fields:
                course_id = data["course_id"]
                if type(course_id) != int:
                    raise ValueError("Invalid value for course ID.")
        except ValueError as v:
            errors["course_id"] = str(v)

        if errors:
            return 400, errors

        return 200, "Data Types Validated"

    @classmethod
    def input_validation(cls, data):
        input_fields = list(data.keys())
        errors = {}

        try:
            for r in ProfessorCourseIntegrity.required_fields:
                if r not in input_fields:
                    raise ValueError("Missing required data fields; " +
                                     "professor, uni, and course_id are "
                                     "required.")
        except ValueError as v:
            errors["required_fields"] = str(v)

        type_errors = ProfessorCourseIntegrity.type_validation(data)

        if type_errors[0] == 400:
            errors.update(type_errors[1])

        if errors:
            return 400, errors

        return 200, "Input Validated"

    @classmethod
    def post_responses(cls, res):
        rsp = ""
        if res == 422:
            rsp = Response("This professor is already added to this course!",
                           status=422, content_type="text/plain")
        elif type(res) == tuple:
            if res[0] == 400:
                rsp = Response(json.dumps(res[1], default=str), status=res[0],
                               content_type="application/json")
        elif res is not None:
            rsp_dict = {"Response": "Success! Added professor to the specified "
                                    "course.", "Location": "/api/professor/" +
                                                           res}
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
    def professor_get_responses(cls, res):
        status = ProfessorCourseIntegrity.get_responses(res)
        if status == 200:
            rsp = Response(json.dumps(res, default=str), status=status,
                           content_type="application/json")
        else:
            rsp = Response("No data found!", status=status,
                           content_type="text/plain")

        return rsp

    @classmethod
    def professor_put_responses(cls, res):
        status = ProfessorCourseIntegrity.put_responses(res)
        rsp = ""
        if status == 422:
            rsp = Response("Update violates data integrity!", status=status,
                           content_type="text/plain")
        elif status == 400:
            rsp = Response(json.dumps(res[1], default=str), status=status,
                           content_type="application/json")
        elif status == 200:
            rsp = Response("Success! The given data for the professor records "
                           + "that matched was updated as requested.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Matching professor and/or course not found "
                           "or unexpected error.",
                           status=422, content_type="text/plain")

        return rsp

    @classmethod
    def professor_delete_responses(cls, res):
        status = ProfessorCourseIntegrity.delete_responses(res)
        if status == 204:
            rsp = Response("Success! Deleted all professor records.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! Could not delete all professor records.",
                           status=status, content_type="text/plain")

        return rsp

    @classmethod
    def professor_by_uni_get_responses(cls, res):
        status = ProfessorCourseIntegrity.get_responses(res)
        if status == 200:
            rsp = Response(json.dumps(res, default=str), status=status,
                           content_type="application/json")
        else:
            rsp = Response("Failed! No records found for given UNI.",
                           status=status, content_type="text/plain")

        return rsp

    @classmethod
    def professor_by_uni_put_responses(cls, res, uni):
        status = ProfessorCourseIntegrity.put_responses(res)
        rsp = ""
        if status == 422:
            rsp = Response("Update violates data integrity!", status=status,
                           content_type="text/plain")
        elif status == 400:
            rsp = Response(json.dumps(res[1], default=str), status=status,
                           content_type="application/json")
        elif status == 200:
            rsp = Response("Success! The given records for the professor with "
                           "UNI " + str(uni) + " were updated as requested.",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! UNI not found or unexpected error.",
                           status=422, content_type="text/plain")

        return rsp

    @classmethod
    def professor_by_uni_delete_responses(cls, res, uni):
        status = ProfessorCourseIntegrity.delete_responses(res)
        if status == 204:
            rsp = Response("Success! Deleted records for professor with UNI " +
                           str(uni) + ".",
                           status=status, content_type="text/plain")
        else:
            rsp = Response("Failed! UNI not found.",
                           status=status, content_type="text/plain")

        return rsp
