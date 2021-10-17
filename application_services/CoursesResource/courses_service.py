from application_services.BaseApplicationResource import BaseRDBApplicationResource
import database_services.RDBService as db_service


class CoursesResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        for r in resource_data:
            links = []

            id_values = []
            id_keys = ["course_year", "course_sem", "dept", "course_number", "section"]
            for key in id_keys:
                id_values.append(str(r.get(key)))

            course_id_str = "_".join(id_values)

            self_link = {"rel": "self", "href": "/courses/" + course_id_str}
            links.append(self_link)

            r["links"] = links

        return resource_data


    @classmethod
    def get_data_resource_info(cls):
        # return "cloud_computing_f21", "courses"
        return "oh_app", "courses"
