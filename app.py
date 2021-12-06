from flask import Flask, Response, request, redirect, url_for
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
import json
import logging
from datetime import datetime
import os

import utils.rest_utils as rest_utils

from application_services.CoursesResource.courses_service \
    import CoursesResource
from application_services.CoursesResource.ta_course_service import \
    TACourseResource
from application_services.CoursesResource.professor_course_service import \
    ProfessorCourseResource
from integrity_services.CoursesIntegrityResource import CoursesIntegrity
from integrity_services.TACourseIntegrityResource import TACourseIntegrity
from integrity_services.ProfessorCourseIntegrityResource import \
    ProfessorCourseIntegrity
from database_services.RDBServices.CoursesRDBService import CoursesRDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "supersekrit"
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = \
    os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = \
    os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
google_bp = make_google_blueprint(scope=["profile", "email"],
                                  redirect_url="/api/login")
app.register_blueprint(google_bp, url_prefix="/login")

CORS(app)


#########################################################################

@app.route("/api/login", methods=["GET"])
def authorization():
    if not google.authorized:
        return {'url': url_for("google.login")}
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return redirect("http://localhost:4200/dashboard")


#########################################################################

# This path simply echoes to check that the app is working.
# The path is /health and the only method is GETs
@app.route("/api/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="app/json")
    return rsp


@app.route('/api')
def landing_page():
    return '<u>OH Application Courses Microservice</u>'


@app.route('/api/courses', methods=['GET', 'POST', 'PUT', 'DELETE'])
def course_collection():
    """
    1. HTTP GET return all courses.
    2. HTTP POST with body --> create a course, i.e --> Machine Learning
    3. HTTP PUT update all courses that match the provided where clause
    with the updated data
    --> JSON must be nested as follows
    {
        "update_fields": {
            "field1": "value",
            "field2": "value",
            ...
            "last_field": "value"
        },
        "where_fields": {
            "field1": "value",
            "field2": "value",
            ...
            "last_field": "value"
        }
    4. HTTP DELETE delete all courses from the database
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("course_collection", inputs)

        if inputs.method == "GET":
            limit = 5
            if inputs.limit:
                if int(inputs.limit) < limit:
                    limit = int(inputs.limit)
            offset = 0
            if inputs.offset:
                offset = int(inputs.offset)
            order_by = inputs.order_by
            res = CoursesResource.get_by_template(inputs.args,
                                                  order_by=order_by,
                                                  limit=limit, offset=offset,
                                                  field_list=inputs.fields)
            if res:
                res = CoursesResource.get_links(res, inputs)
            rsp = CoursesIntegrity.course_collection_get_responses(res)
        elif inputs.method == "POST":
            validation = CoursesIntegrity.input_validation(inputs.data)
            if validation[0] == 200:
                inputs.data["start_time"] = datetime.strptime(
                    inputs.data["start_time"], "%I:%M %p").time()
                inputs.data["end_time"] = datetime.strptime(
                    inputs.data["end_time"], "%I:%M %p").time()
                res = CoursesResource.create(inputs.data)
                if res == 1:
                    res = CoursesRDBService.generate_course_code(inputs.data)
            else:
                res = validation
            rsp = CoursesIntegrity.post_responses(res)
        elif inputs.method == "PUT":
            data_template = inputs.data['update_fields']
            where_template = inputs.data['where_fields']
            update_fields_val = CoursesIntegrity.type_validation(data_template)
            where_fields_val = CoursesIntegrity.type_validation(where_template)
            if update_fields_val[0] == 200 and where_fields_val[0] == 200:
                res = CoursesResource.update_by_template(data_template,
                                                         where_template)
            else:
                error_code = 0
                errors = {}
                if update_fields_val[0] != 200:
                    error_code = update_fields_val[0]
                    errors["Errors in update_fields"] = update_fields_val[1]
                if where_fields_val[0] != 200:
                    error_code = where_fields_val[0]
                    errors["Errors in where_fields"] = where_fields_val[1]
                res = (error_code, errors)
            rsp = CoursesIntegrity.course_collection_put_responses(res)
        elif inputs.method == "DELETE":
            res = CoursesResource.delete_by_template(inputs.args)
            rsp = CoursesIntegrity.course_collection_delete_responses(res)
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/api/courses, e = ", str(e))
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/api/courses/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def course_by_id(course_id):
    """
    1. HTTP GET return a specific course by ID.
    2. HTTP PUT match course by ID and update specific fields
    --> JSON must be nested as follows for update
    {
        "field1": "value",
        "field2": "value",
        ...
        "last_field": "value"
    }
    3. HTTP DELETE match course by ID and delete it
    :param course_id: course ID number, autogenerated in data table, or course
    code as a string in this format -
    "year_sem_dept_number_section" e.g. "2021_Fall_COMS_E6156_001"
    :return: response from desired action
    """
    try:
        try:
            test_id = int(course_id)
            id_type = "id"
        except ValueError as v:
            test_id = course_id
            id_dict = CoursesRDBService.split_course_code(test_id)
            if len(id_dict.keys()) != 5:
                raise ValueError("Invalid course code provided!")
            id_validation = CoursesIntegrity.type_validation(id_dict)
            if id_validation[0] == 400:
                raise ValueError(id_validation[1])
            else:
                id_type = "course_code"

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("course_by_id", inputs)

        if inputs.method == "GET":
            limit = 5
            if inputs.limit:
                if int(inputs.limit) < limit:
                    limit = int(inputs.limit)
            offset = 0
            if inputs.offset:
                offset = int(inputs.offset)
            order_by = inputs.order_by
            if id_type == "id":
                res = CoursesResource.get_by_course_id(course_id,
                                                       order_by=order_by,
                                                       limit=limit,
                                                       offset=offset,
                                                       field_list=inputs.fields)
            else:
                res = CoursesResource.get_by_course_code(course_id,
                                                         order_by=order_by,
                                                         limit=limit,
                                                         offset=offset,
                                                         field_list=
                                                         inputs.fields)
            if res:
                res = CoursesResource.get_links(res, inputs)
            if id_type == "id":
                rsp = CoursesIntegrity.course_by_id_get_responses(res)
            else:
                rsp = CoursesIntegrity.course_by_code_get_responses(res)
        elif inputs.method == "PUT":
            validation = CoursesIntegrity.type_validation(inputs.data)
            if validation[0] == 200:
                if id_type == "id":
                    res = CoursesResource.update_by_course_id(course_id,
                                                              inputs.data)
                else:
                    res = CoursesResource.update_by_course_code(course_id,
                                                                inputs.data)
            else:
                res = validation
            if id_type == "id":
                rsp = CoursesIntegrity.course_by_id_put_responses(res,
                                                                  course_id)
            else:
                rsp = CoursesIntegrity.course_by_code_put_responses(res,
                                                                    course_id)
        elif inputs.method == "DELETE":
            if id_type == "id":
                test = CoursesResource.get_by_course_id(course_id)
                if test:
                    res = CoursesResource.delete_by_course_id(course_id)
                else:
                    res = None
            else:
                test = CoursesResource.get_by_course_code(course_id)
                if test:
                    res = CoursesResource.delete_by_course_code(course_id)
                else:
                    res = None
            if id_type == "id":
                rsp = CoursesIntegrity.course_by_id_delete_responses(res,
                                                                     course_id)
            else:
                rsp = CoursesIntegrity.course_by_code_delete_responses(res,
                                                                       course_id
                                                                       )
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except ValueError as v:
        print("/api/courses/" + str(course_id))
        if type(v) == str:
            rsp = Response(str(v), status=400, content_type="text/plain")
        else:
            rsp = Response(json.dumps(v, default=str), status=400,
                           content_type="application/json")

    except Exception as e:
        # HTTP status code.
        print("/api/courses/" + str(course_id) + ", e = ", str(e))
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/api/ta', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ta_course():
    """
    1. HTTP GET return all TAs for all courses.
    2. HTTP POST with body --> add a TA to a course
    3. HTTP PUT update all TA records that match the provided where clause
    with the updated data
    --> JSON must be nested as follows
    {
        "update_fields": {
            "field1": "value",
            "field2": "value",
            ...
            "last_field": "value"
        },
        "where_fields": {
            "field1": "value",
            "field2": "value",
            ...
            "last_field": "value"
        }
    4. HTTP DELETE delete all TAs for all courses
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("ta_course", inputs)

        if inputs.method == "GET":
            limit = 5
            if inputs.limit:
                if int(inputs.limit) < limit:
                    limit = int(inputs.limit)
            offset = 0
            if inputs.offset:
                offset = int(inputs.offset)
            order_by = inputs.order_by
            res = TACourseResource.get_by_template(inputs.args,
                                                   order_by=order_by,
                                                   limit=limit,
                                                   offset=offset,
                                                   field_list=inputs.fields)
            if res:
                res = TACourseResource.add_course_links(res)
                res = TACourseResource.get_links(res, inputs)
            rsp = TACourseIntegrity.ta_get_responses(res)
        elif inputs.method == "POST":
            validation = TACourseIntegrity.input_validation(inputs.data)
            if validation[0] == 200:
                res = TACourseResource.create(inputs.data)
                if res == 1:
                    res = inputs.data["uni"]
            else:
                res = validation
            rsp = TACourseIntegrity.post_responses(res)
        elif inputs.method == "PUT":
            data_template = inputs.data['update_fields']
            where_template = inputs.data['where_fields']
            update_fields_val = TACourseIntegrity.type_validation(data_template)
            where_fields_val = TACourseIntegrity.type_validation(where_template)
            if update_fields_val[0] == 200 and where_fields_val[0] == 200:
                res = TACourseResource.update_by_template(data_template,
                                                          where_template)
            else:
                error_code = 0
                errors = {}
                if update_fields_val[0] != 200:
                    error_code = update_fields_val[0]
                    errors["Errors in update_fields"] = update_fields_val[1]
                if where_fields_val[0] != 200:
                    error_code = where_fields_val[0]
                    errors["Errors in where_fields"] = where_fields_val[1]
                res = (error_code, errors)
            rsp = TACourseIntegrity.ta_put_responses(res)
        elif inputs.method == "DELETE":
            res = TACourseResource.delete_by_template(inputs.args)
            rsp = TACourseIntegrity.ta_delete_responses(res)
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/api/ta, e = ", str(e))
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/api/ta/<uni>', methods=['GET', 'PUT', 'DELETE'])
def ta_course_by_uni(uni):
    """
    1. HTTP GET return matching records for the given TA by UNI.
    2. HTTP PUT match records by TA UNI and update specific fields
    --> JSON must be nested as follows for update
    {
        "field1": "value",
        "field2": "value",
        ...
        "last_field": "value"
    }
    3. HTTP DELETE match records by TA UNI and delete them
    :param uni: TA's UNI
    :return: response from desired action
    """
    try:
        uni_validation = TACourseIntegrity.type_validation({"uni": uni})
        if uni_validation[0] == 400:
            raise ValueError(uni_validation[1])

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("ta_course_by_uni", inputs)

        if inputs.method == "GET":
            limit = 5
            if inputs.limit:
                if int(inputs.limit) < limit:
                    limit = int(inputs.limit)
            offset = 0
            if inputs.offset:
                offset = int(inputs.offset)
            order_by = inputs.order_by
            res = TACourseResource.get_by_uni(uni, order_by=order_by,
                                              limit=limit, offset=offset,
                                              field_list=inputs.fields)
            if res:
                res = TACourseResource.add_course_links(res)
                res = TACourseResource.get_links(res, inputs)
            rsp = TACourseIntegrity.ta_by_uni_get_responses(res)
        elif inputs.method == "PUT":
            validation = TACourseIntegrity.type_validation(inputs.data)
            if validation[0] == 200:
                res = TACourseResource.update_by_uni(uni, inputs.data)
            else:
                res = validation
            rsp = TACourseIntegrity.ta_by_uni_put_responses(res, uni)
        elif inputs.method == "DELETE":
            test = TACourseResource.get_by_uni(uni)
            if test:
                res = TACourseResource.delete_by_uni(uni)
            else:
                res = None
            rsp = TACourseIntegrity.ta_by_uni_delete_responses(res, uni)
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except ValueError as v:
        print("/api/ta/" + str(uni))
        if type(v) == str:
            rsp = Response(str(v), status=400, content_type="text/plain")
        else:
            rsp = Response(json.dumps(v, default=str), status=400,
                           content_type="application/json")

    except Exception as e:
        # HTTP status code.
        print("/api/ta/" + str(uni) + ", e = ", str(e))
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/api/professor', methods=['GET', 'POST', 'PUT', 'DELETE'])
def professor_course():
    """
    1. HTTP GET return all professors for all courses.
    2. HTTP POST with body --> add a professor to a course
    3. HTTP PUT update all professor records that match the provided where
    clause with the updated data
    --> JSON must be nested as follows
    {
        "update_fields": {
            "field1": "value",
            "field2": "value",
            ...
            "last_field": "value"
        },
        "where_fields": {
            "field1": "value",
            "field2": "value",
            ...
            "last_field": "value"
        }
    4. HTTP DELETE delete all professors for all courses
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("professor_course", inputs)

        if inputs.method == "GET":
            limit = 5
            if inputs.limit:
                if int(inputs.limit) < limit:
                    limit = int(inputs.limit)
            offset = 0
            if inputs.offset:
                offset = int(inputs.offset)
            order_by = inputs.order_by
            res = ProfessorCourseResource.get_by_template(inputs.args,
                                                          order_by=order_by,
                                                          limit=limit,
                                                          offset=offset,
                                                          field_list=
                                                          inputs.fields)
            if res:
                res = ProfessorCourseResource.add_course_links(res)
                res = ProfessorCourseResource.get_links(res, inputs)
            rsp = ProfessorCourseIntegrity.professor_get_responses(res)
        elif inputs.method == "POST":
            validation = ProfessorCourseIntegrity.input_validation(inputs.data)
            if validation[0] == 200:
                res = ProfessorCourseResource.create(inputs.data)
                if res == 1:
                    res = inputs.data["uni"]
            else:
                res = validation
            rsp = ProfessorCourseIntegrity.post_responses(res)
        elif inputs.method == "PUT":
            data_template = inputs.data['update_fields']
            where_template = inputs.data['where_fields']
            update_fields_val = ProfessorCourseIntegrity.type_validation(
                data_template)
            where_fields_val = ProfessorCourseIntegrity.type_validation(
                where_template)
            if update_fields_val[0] == 200 and where_fields_val[0] == 200:
                res = ProfessorCourseResource.update_by_template(
                    data_template, where_template)
            else:
                error_code = 0
                errors = {}
                if update_fields_val[0] != 200:
                    error_code = update_fields_val[0]
                    errors["Errors in update_fields"] = update_fields_val[1]
                if where_fields_val[0] != 200:
                    error_code = where_fields_val[0]
                    errors["Errors in where_fields"] = where_fields_val[1]
                res = (error_code, errors)
            rsp = ProfessorCourseIntegrity.professor_put_responses(res)
        elif inputs.method == "DELETE":
            res = ProfessorCourseResource.delete_by_template(inputs.args)
            rsp = ProfessorCourseIntegrity.professor_delete_responses(res)
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/api/professor, e = ", str(e))
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/api/professor/<uni>', methods=['GET', 'PUT', 'DELETE'])
def professor_course_by_uni(uni):
    """
    1. HTTP GET return matching records for the given professor by UNI.
    2. HTTP PUT match records by professor UNI and update specific fields
    --> JSON must be nested as follows for update
    {
        "field1": "value",
        "field2": "value",
        ...
        "last_field": "value"
    }
    3. HTTP DELETE match records by professor UNI and delete them
    :param uni: professor's UNI
    :return: response from desired action
    """
    try:
        uni_validation = ProfessorCourseIntegrity.type_validation({"uni": uni})
        if uni_validation[0] == 400:
            raise ValueError(uni_validation[1])

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("professor_course_by_uni", inputs)

        if inputs.method == "GET":
            limit = 5
            if inputs.limit:
                if int(inputs.limit) < limit:
                    limit = int(inputs.limit)
            offset = 0
            if inputs.offset:
                offset = int(inputs.offset)
            order_by = inputs.order_by
            res = ProfessorCourseResource.get_by_uni(uni, order_by=order_by,
                                                     limit=limit,
                                                     offset=offset,
                                                     field_list=inputs.fields)
            if res:
                res = ProfessorCourseResource.add_course_links(res)
                res = ProfessorCourseResource.get_links(res, inputs)
            rsp = ProfessorCourseIntegrity.professor_by_uni_get_responses(res)
        elif inputs.method == "PUT":
            validation = ProfessorCourseIntegrity.type_validation(inputs.data)
            if validation[0] == 200:
                res = ProfessorCourseResource.update_by_uni(uni, inputs.data)
            else:
                res = validation
            rsp = ProfessorCourseIntegrity.professor_by_uni_put_responses(
                res, uni)
        elif inputs.method == "DELETE":
            test = ProfessorCourseResource.get_by_uni(uni)
            if test:
                res = ProfessorCourseResource.delete_by_uni(uni)
            else:
                res = None
            rsp = ProfessorCourseIntegrity.professor_by_uni_delete_responses(
                res, uni)
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except ValueError as v:
        print("/api/professor/" + str(uni))
        if type(v) == str:
            rsp = Response(str(v), status=400, content_type="text/plain")
        else:
            rsp = Response(json.dumps(v, default=str), status=400,
                           content_type="application/json")

    except Exception as e:
        # HTTP status code.
        print("/api/professor/" + str(uni) + ", e = ", str(e))
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
