from database_services.RDBService import RDBService


class TACourseRDBService(RDBService):

    def __init__(self):
        super().__init__()

    @classmethod
    def find_by_uni(cls, db_schema, table_name, uni, order_by=None,
                    limit=None, offset=None, field_list=None):

        template = {"uni": uni}

        return cls.find_by_template(db_schema, table_name, template,
                                    order_by, limit, offset, field_list)

    @classmethod
    def delete_by_uni(cls, db_schema, table_name, uni):

        template = {"uni": uni}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_uni(cls, db_schema, table_name, uni, data):

        template = {"uni": uni}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def find_by_ta_name(cls, db_schema, table_name, name, order_by=None,
                        limit=None, offset=None, field_list=None):

        template = {"TA": name}

        return cls.find_by_template(db_schema, table_name, template,
                                    order_by, limit, offset, field_list)

    @classmethod
    def delete_by_ta_name(cls, db_schema, table_name, name):

        template = {"TA": name}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_ta_name(cls, db_schema, table_name, name, data):

        template = {"TA": name}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def find_by_course_id(cls, db_schema, table_name, course_id,
                          order_by=None, limit=None, offset=None,
                          field_list=None):

        template = {"course_id": course_id}

        return cls.find_by_template(db_schema, table_name, template,
                                    order_by, limit, offset, field_list)

    @classmethod
    def delete_by_course_id(cls, db_schema, table_name, course_id):

        template = {"course_id": course_id}

        return cls.delete_by_template(db_schema, table_name, template)

    @classmethod
    def update_by_course_id(cls, db_schema, table_name, course_id, data):

        template = {"course_id": course_id}

        return cls.update_by_template(db_schema, table_name, data, template)

    @classmethod
    def create(cls, db_schema, table_name, create_data):
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
