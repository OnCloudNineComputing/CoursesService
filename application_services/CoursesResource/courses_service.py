from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.CoursesRDBService import CoursesRDBService


class CoursesResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_course_id(cls, course_id, field_list=None):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.find_by_course_id(db_name, table_name,
                                                  course_id, field_list)
        return res

    @classmethod
    def delete_by_course_id(cls, course_id):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.delete_by_course_id(db_name, table_name,
                                                    course_id)
        return res

    @classmethod
    def update_by_course_id(cls, course_id, data):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.update_by_course_id(db_name, table_name,
                                                    course_id, data)
        return res

    @classmethod
    def get_by_course_code(cls, course_code, field_list=None):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.find_by_course_code(db_name, table_name,
                                                  course_code, field_list)
        return res

    @classmethod
    def delete_by_course_code(cls, course_code):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.delete_by_course_code(db_name, table_name,
                                                    course_code)
        return res

    @classmethod
    def update_by_course_code(cls, course_code, data):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.update_by_course_code(db_name, table_name,
                                                    course_code, data)
        return res

    @classmethod
    def get_by_name(cls, person_type, name, field_list=None):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.find_by_name(db_name, table_name,
                                             person_type, name, field_list)
        return res

    @classmethod
    def delete_by_name(cls, person_type, name):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.delete_by_name(db_name, table_name,
                                               person_type, name)
        return res

    @classmethod
    def update_by_name(cls, person_type, name, data):
        db_name, table_name = CoursesResource.get_data_resource_info()
        res = CoursesRDBService.update_by_name(db_name, table_name,
                                               person_type, name, data)
        return res

    @classmethod
    def create(cls, data):
        db_name, table_name = cls.get_data_resource_info()
        res = CoursesRDBService.create(db_name, table_name, data)
        return res

    @classmethod
    def get_links(cls, resource_data):
        for r in resource_data:
            links = []

            id_values = []
            id_keys = ["course_year", "course_sem", "dept", "course_number", "section"]
            for key in id_keys:
                id_values.append(str(r.get(key)))

            course_id_str = "_".join(id_values)

            self_link_1 = {"rel": "self", "href": "/api/courses/" + str(r.get("id"))}
            self_link_2 = {"rel": "self", "href": "/api/courses/" + course_id_str}
            links.append(self_link_1)
            links.append(self_link_2)

            r["links"] = links

        return resource_data

    @classmethod
    def get_data_resource_info(cls):
        return "cloud_computing_f21", "courses"
        # return "oh_app", "courses"
