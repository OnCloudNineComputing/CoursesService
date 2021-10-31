from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
from datetime import datetime

import utils.rest_utils as rest_utils

from application_services.CoursesResource.courses_service \
    import CoursesResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


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
    3. HTTP GET update all courses that match the provided where clause
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
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("course_collection", inputs)

        if inputs.method == "GET":
            res = CoursesResource.get_by_template(None)
            if res is not None:
                res = CoursesResource.get_links(res)
                rsp = Response(json.dumps(res, default=str), status=200,
                               content_type="application/json")
            else:
                rsp = Response("No data found!", status=404,
                               content_type="text/plain")
        elif inputs.method == "POST":
            res = CoursesResource.create(inputs.data)
            if res == 9:
                rsp = Response("Course already exists!", status=404,
                               content_type="text/plain")
            elif res is not None:
                rsp = Response("Success! Created course with the given " +
                               "information.", status=201,
                               content_type="text/plain")
            else:
                rsp = Response("Failed! Unprocessable entity.",
                               status=422, content_type="text/plain")
        elif inputs.method == "PUT":
            data_template = inputs.data['update_fields']
            where_template = inputs.data['where_fields']
            res = CoursesResource.update_by_template(data_template,
                                                     where_template)
            if res is not None:
                rsp = Response("Success! The given data for the courses "
                               + "that matched was updated as requested.",
                               status=200, content_type="text/plain")
            else:
                rsp = Response("Failed! Matching courses not found or " +
                               "invalid data.", status=404,
                               content_type="text/plain")
        elif inputs.method == "DELETE":
            res = CoursesResource.delete_by_template(None)
            if res is not None:
                rsp = Response("Success! Deleted all courses.",
                               status=200, content_type="text/plain")
            else:
                rsp = Response("Failed! Could not delete all courses.",
                               status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/courses, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/courses/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_course(course_id):
    """
    1. HTTP GET return a specific course by ID.
    2. HTTP PUT match course by ID and update specific fields
    3. HTTP DELETE match course ID and delete it
    :param course_id: course ID as a string in this format -
    "year_sem_dept_number_section" e.g. "2021_Fall_COMS_E6156_001"
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("specific_course", inputs)

        if inputs.method == "GET":
            res = CoursesResource.get_by_course_id(course_id)
            if res is not None:
                res = CoursesResource.get_links(res)
                rsp = Response(json.dumps(res, default=str), status=200,
                               content_type="application/json")
            else:
                rsp = Response("Failed! Course ID not found.", status=404,
                               content_type="text/plain")
        elif inputs.method == "PUT":
            res = CoursesResource.update_by_course_id(course_id,
                                                      inputs.data)
            if res is not None:
                rsp = Response("Success! The given data for the course " +
                               course_id + " was updated as requested.",
                               status=200, content_type="text/plain")
            else:
                rsp = Response("Failed! Course ID not found or invalid " +
                               "data.", status=404,
                               content_type="text/plain")
        elif inputs.method == "DELETE":
            test = CoursesResource.get_by_course_id(course_id)
            if test:
                res = CoursesResource.delete_by_course_id(course_id)
                if res is not None:
                    rsp = Response("Success! Deleted course " + course_id,
                                   status=200, content_type="text/plain")
                else:
                    rsp = Response("Failed! Course ID not found.",
                                   status=404, content_type="text/plain")
            else:
                rsp = Response("No courses with the given Course ID.",
                               status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/courses/" + str(course_id) + ", e = ", e)
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/courses/professor/<professor_name>',
           methods=['GET', 'PUT', 'DELETE'])
def specific_professor(professor_name):
    """
    1. HTTP GET return a specific course by professor name.
    2. HTTP PUT match course by professor name and update specific fields
    3. HTTP DELETE match course by professor name and delete it
    :param professor_name: professor name, use %20 for spaces -
    e.g. "/courses/professor/Donald%20Ferguson"
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("specific_professor", inputs)

        if inputs.method == "GET":
            res = CoursesResource.get_by_name("professors",
                                              professor_name)
            if res is not None:
                res = CoursesResource.get_links(res)
                rsp = Response(json.dumps(res, default=str), status=200,
                               content_type="application/json")
            else:
                rsp = Response("Failed! Professor not found.", status=404,
                               content_type="text/plain")
        elif inputs.method == "PUT":
            res = CoursesResource.update_by_name("professors",
                                                 professor_name,
                                                 inputs.data)
            if res is not None:
                rsp = Response("Success! The given data for the courses "
                               + "taught by " + professor_name +
                               " was updated as requested.",
                               status=200, content_type="text/plain")
            else:
                rsp = Response("Failed! Professor not found or invalid "
                               + "data.", status=404,
                               content_type="text/plain")
        elif inputs.method == "DELETE":
            test = CoursesResource.get_by_name("professors",
                                               professor_name)
            if test:
                res = CoursesResource.delete_by_name("professors",
                                                     professor_name)
                if res is not None:
                    rsp = Response("Success! Deleted courses taught by " +
                                   professor_name, status=200,
                                   content_type="text/plain")
                else:
                    rsp = Response("Failed! Professor not found.",
                                   status=404, content_type="text/plain")
            else:
                rsp = Response("No courses taught by " + professor_name,
                               status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/courses/professor/" + str(professor_name) + ", e = ", e)
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


@app.route('/courses/TA/<ta_name>',
           methods=['GET', 'PUT', 'DELETE'])
def specific_ta(ta_name):
    """
    1. HTTP GET return a specific course by TA name.
    2. HTTP PUT match course by TA name and update specific fields
    3. HTTP DELETE match course by TA name and delete it
    :param ta_name: TA name, use %20 for spaces -
    e.g. "/courses/professor/Pelin%20Cetin"
    :return: response from desired action
    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("specific_TA", inputs)

        if inputs.method == "GET":
            res = CoursesResource.get_by_name("TAs",
                                              ta_name)
            if res is not None:
                res = CoursesResource.get_links(res)
                rsp = Response(json.dumps(res, default=str), status=200,
                               content_type="application/json")
            else:
                rsp = Response("Failed! TA not found.", status=404,
                               content_type="text/plain")
        elif inputs.method == "PUT":
            res = CoursesResource.update_by_name("TAs",
                                                 ta_name,
                                                 inputs.data)
            if res is not None:
                rsp = Response("Success! The given data for the courses "
                               + "supported by " + ta_name +
                               " was updated as requested.",
                               status=200, content_type="text/plain")
            else:
                rsp = Response("Failed! TA not found or invalid "
                               + "data.", status=404,
                               content_type="text/plain")
        elif inputs.method == "DELETE":
            test = CoursesResource.get_by_name("TAs", ta_name)
            if test:
                res = CoursesResource.delete_by_name("TAs",
                                                     ta_name)
                if res is not None:
                    rsp = Response("Success! Deleted courses supported "
                                   + "by " + ta_name, status=200,
                                   content_type="text/plain")
                else:
                    rsp = Response("Failed! TA not found.", status=404,
                                   content_type="text/plain")
            else:
                rsp = Response("No courses supported by " + ta_name,
                               status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:
        # HTTP status code.
        print("/courses/TA/" + str(ta_name) + ", e = ", e)
        rsp = Response("INTERNAL ERROR", status=500,
                       content_type="text/plain")

    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
