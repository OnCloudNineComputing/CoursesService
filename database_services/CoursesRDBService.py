from database_services.RDBService import RDBService


class CoursesRDBService(RDBService):

    def __init__(self):
        super().__init__()

    @classmethod
    def split_course_code(cls, course_code):

        keys = ["course_year", "course_sem", "dept", "course_number", "section"]
        parameters = course_code.split('_')
        values = dict(zip(keys, parameters))
        values["course_year"] = int(values["course_year"])

        return values

    @classmethod
    def find_by_course_id(cls, db_schema, table_name, course_id, field_list):

        template = {"id": course_id}

        return cls.find_by_template(db_schema, table_name, template, field_list)

    @classmethod
    def delete_by_course_id(cls, db_schema, table_name, course_id):

        template = {"id": course_id}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_course_id(cls, db_schema, table_name, course_id, data):

        template = {"id": course_id}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def find_by_course_code(cls, db_schema, table_name, course_code, field_list):

        template = {"course_code": course_code}

        return cls.find_by_template(db_schema, table_name, template, field_list)

    @classmethod
    def delete_by_course_code(cls, db_schema, table_name, course_code):

        template = {"course_code": course_code}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_course_code(cls, db_schema, table_name, course_code, data):

        template = {"course_code": course_code}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def get_name_inputs(cls, person_type, name):
        name_template = dict()
        name_template[person_type] = name
        return name_template

    @classmethod
    def find_by_name(cls, db_schema, table_name, person_type, name, field_list):

        name_template = cls.get_name_inputs(person_type, name)

        return cls.find_by_template(db_schema, table_name, name_template, field_list)

    @classmethod
    def delete_by_name(cls, db_schema, table_name, person_type, name):

        name_template = cls.get_name_inputs(person_type, name)

        return cls.delete_by_template(db_schema, table_name, name_template)

    @classmethod
    def update_by_name(cls, db_schema, table_name, person_type, name, data):

        name_template = cls.get_name_inputs(person_type, name)

        return cls.update_by_template(db_schema, table_name, data, name_template)

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        id_keys = ["course_year", "course_sem", "dept", "course_number", "section"]
        course_id = {key: value for key, value in create_data.items() if key in id_keys}
        course_matches = cls.find_by_template(db_schema, table_name, course_id)
        if not course_matches:
            cols = []
            vals = []
            args = []

            for k, v in create_data.items():
                cols.append(k)
                vals.append('%s')
                args.append(v)

            cols_clause = "(" + ",".join(cols) + ")"
            vals_clause = "VALUES (" + ",".join(vals) + ")"

            sql_stmt = "INSERT INTO " + db_schema + "." + table_name + " " + cols_clause + \
                       " " + vals_clause

            res = cls.run_sql(sql_stmt, args)

            return res
        else:
            return 422
