from application_services.BaseApplicationResource import \
    BaseRDBApplicationResource
from database_services.RDBServices.ProfessorCourseRDBService import \
    ProfessorCourseRDBService


class ProfessorCourseResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_uni(cls, uni, order_by=None, limit=None, offset=None,
                   field_list=None):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.find_by_uni(db_name, table_name, uni,
                                                    order_by, limit, offset,
                                                    field_list)
        return res

    @classmethod
    def delete_by_uni(cls, uni):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.delete_by_uni(db_name, table_name, uni)
        return res

    @classmethod
    def update_by_uni(cls, uni, data):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.update_by_uni(db_name,table_name,
                                                      uni, data)
        return res

    @classmethod
    def get_by_professor_name(cls, name, order_by=None, limit=None,
                              offset=None, field_list=None):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.find_by_professor_name(db_name,
                                                               table_name,
                                                               name,
                                                               order_by,
                                                               limit, offset,
                                                               field_list)
        return res

    @classmethod
    def delete_by_professor_name(cls, name):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.delete_by_professor_name(db_name,
                                                                 table_name,
                                                                 name)
        return res

    @classmethod
    def update_by_professor_name(cls, name, data):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.update_by_professor_name(db_name,
                                                                 table_name,
                                                                 name, data)
        return res

    @classmethod
    def get_by_course_id(cls, course_id, order_by=None, limit=None,
                         offset=None, field_list=None):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.find_by_course_id(db_name,
                                                          table_name,
                                                          course_id,
                                                          order_by, limit,
                                                          offset, field_list)
        return res

    @classmethod
    def delete_by_course_id(cls, course_id):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.delete_by_course_id(db_name,
                                                            table_name,
                                                            course_id)
        return res

    @classmethod
    def update_by_course_id(cls, course_id, data):
        db_name, table_name = ProfessorCourseResource.get_data_resource_info()
        res = ProfessorCourseRDBService.update_by_course_id(db_name,
                                                            table_name,
                                                            course_id, data)
        return res

    @classmethod
    def create(cls, data):
        db_name, table_name = cls.get_data_resource_info()
        res = ProfessorCourseRDBService.create(db_name, table_name, data)
        return res

    @classmethod
    def add_course_links(cls, resource_data):
        for r in resource_data:
            course_link = "/api/courses/" + str(r["course_id"])
            r["course_link"] = course_link

        return resource_data

    @classmethod
    def get_links(cls, resource_data, inputs):
        links = []
        path_args = []
        next_path_args = []
        prev_path_args = []

        path = inputs.path
        next_path = inputs.path
        prev_path = inputs.path
        if inputs.args:
            input_args = inputs.args
            for k, v in input_args.items():
                input_args[k] = v.replace(" ", "%20")
            path_args.append("&".join(
                ["=".join([k, str(v)]) for k, v in input_args.items()]))
            next_path_args.append("&".join(
                ["=".join([k, str(v)]) for k, v in input_args.items()]))
            prev_path_args.append("&".join(
                ["=".join([k, str(v)]) for k, v in input_args.items()]))
        if inputs.fields:
            path_args.append("fields=" + inputs.fields)
            next_path_args.append("fields=" + inputs.fields)
            prev_path_args.append("fields=" + inputs.fields)
        if inputs.order_by:
            path_args.append("order_by=" + inputs.order_by)
            next_path_args.append("order_by=" + inputs.order_by)
            prev_path_args.append("order_by=" + inputs.order_by)
        else:
            path_args.append("order_by=course_id")
            next_path_args.append("order_by=course_id")
            prev_path_args.append("order_by=course_id")
        limit = 5
        if inputs.limit:
            if int(inputs.limit) < limit:
                limit = int(inputs.limit)
        path_args.append("limit=" + str(limit))
        next_path_args.append("limit=" + str(limit))
        prev_path_args.append("limit=" + str(limit))
        offset = 0
        if inputs.offset:
            offset = int(inputs.offset)
        path_args.append("offset=" + str(offset))
        next_path_args.append("offset=" + str(offset + limit))
        if offset != 0:
            prev_path_args.append("offset=" + str(offset - limit))

        if path_args:
            path += "?" + "&".join(path_args)
        if next_path_args:
            next_path += "?" + "&".join(next_path_args)
        if prev_path_args:
            prev_path += "?" + "&".join(prev_path_args)

        self_link = {"rel": "self", "href": path}
        links.append(self_link)
        next_link = {"rel": "next", "href": next_path}
        links.append(next_link)
        if offset != 0:
            prev_link = {"rel": "prev", "href": prev_path}
            links.append(prev_link)

        links_dict = {"links": links}
        resource_data.append(links_dict)

        return resource_data

    @classmethod
    def get_data_resource_info(cls):
        return "cloud_computing_f21", "professor_course"
        # return "oh_app", "courses"
