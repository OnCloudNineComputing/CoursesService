from abc import ABC, abstractmethod
from database_services.RDBService import RDBService


class BaseApplicationException(Exception):

    def __init__(self):
        pass


class BaseApplicationResource(ABC):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_by_template(cls, template):
        pass

    @classmethod
    @abstractmethod
    def delete_by_template(cls, template):
        pass

    @classmethod
    @abstractmethod
    def update_by_template(cls, data_template, where_template):
        pass

    @classmethod
    @abstractmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(cls):
        pass


class BaseRDBApplicationResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template, field_list=None):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.find_by_template(db_name, table_name,
                                          template, field_list)
        return res

    @classmethod
    def delete_by_template(cls, template):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.delete_by_template(db_name, table_name,
                                            template)
        return res

    @classmethod
    def update_by_template(cls, data_template, where_template):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.update_by_template(db_name, table_name,
                                            data_template, where_template)
        return res

    @classmethod
    def get_by_course_id(cls, course_id, field_list=None):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.find_by_course_id(db_name, table_name,
                                           course_id, field_list)
        return res

    @classmethod
    def delete_by_course_id(cls, course_id):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.delete_by_course_id(db_name, table_name,
                                             course_id)
        return res

    @classmethod
    def update_by_course_id(cls, course_id, data):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.update_by_course_id(db_name, table_name,
                                             course_id, data)
        return res

    @classmethod
    def get_by_name(cls, person_type, name, field_list=None):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.find_by_name(db_name, table_name,
                                      person_type, name, field_list)
        return res

    @classmethod
    def delete_by_name(cls, person_type, name):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.delete_by_name(db_name, table_name,
                                        person_type, name)
        return res

    @classmethod
    def update_by_name(cls, person_type, name, data):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.update_by_name(db_name, table_name,
                                        person_type, name, data)
        return res

    @classmethod
    def create(cls, data):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.create(db_name, table_name, data)
        return res

    @classmethod
    @abstractmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(cls):
        pass
