from application_services.BaseApplicationResource import BaseRDBApplicationResource
import database_services.RDBService as db_service


class CoursesResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return "cloud_computing_f21", "courses"
