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
    def generate_course_code(cls, data):
        keys = ["course_year", "course_sem", "dept", "course_number", "section"]
        values = []

        for key in keys:
            values.append(data[key])

        code = '_'.join(map(str, values))

        return code

    @classmethod
    def find_by_course_id(cls, db_schema, table_name, course_id,
                          order_by=None, limit=None, offset=None,
                          field_list=None):

        template = {"id": course_id}

        return cls.find_by_template(db_schema, table_name, template,
                                    order_by, limit, offset, field_list)

    @classmethod
    def delete_by_course_id(cls, db_schema, table_name, course_id):

        template = {"id": course_id}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_course_id(cls, db_schema, table_name, course_id, data):

        template = {"id": course_id}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def find_by_course_code(cls, db_schema, table_name, course_code,
                            order_by=None, limit=None, offset=None,
                            field_list=None):

        template = {"course_code": course_code}

        return cls.find_by_template(db_schema, table_name, template,
                                    order_by, limit, offset, field_list)

    @classmethod
    def delete_by_course_code(cls, db_schema, table_name, course_code):

        template = {"course_code": course_code}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_course_code(cls, db_schema, table_name, course_code, data):

        template = {"course_code": course_code}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        id_keys = ["course_year", "course_sem", "dept", "course_number",
                   "section"]
        course_id = {key: value for key, value in create_data.items() if key
                     in id_keys}
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

            sql_stmt = "INSERT INTO " + db_schema + "." + table_name + " " + \
                       cols_clause + " " + vals_clause

            res = cls.run_sql(sql_stmt, args)

            return res
        else:
            return 422
