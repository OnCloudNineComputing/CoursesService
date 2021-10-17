import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:

    def __init__(self):
        pass

    @classmethod
    def get_db_connection(cls):

        db_connect_info = context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = context.get_db_info()

        db_connection = pymysql.connect(
            **db_info,
            autocommit=True
        )
        return db_connection

    @classmethod
    def run_sql(cls, sql_statement, args, fetch=False):

        conn = RDBService.get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            conn.close()
            raise e

        return res

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):

        conn = RDBService.get_db_connection()
        cur = conn.cursor()

        sql = "SELECT * FROM " + db_schema + "." + table_name + " WHERE " + \
              column_name + " LIKE " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_where_clause_args(cls, template):

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                if k == "TAs":
                    terms.append("FIND_IN_SET(%s, " + k + ")")
                elif k == "professors":
                    terms.append("FIND_IN_SET(%s, " + k + ")")
                else:
                    terms.append(k + "=%s")
                args.append(v)

            clause = " WHERE " + " AND ".join(terms)

        return clause, args

    @classmethod
    def find_by_template(cls, db_schema, table_name, template, field_list=None):

        wc, args = RDBService.get_where_clause_args(template)

        conn = RDBService.get_db_connection()
        cur = conn.cursor()

        sql = "SELECT * FROM " + db_schema + "." + table_name + " " + wc
        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def delete_by_template(cls, db_schema, table_name, template):

        wc, args = RDBService.get_where_clause_args(template)

        conn = RDBService.get_db_connection()
        cur = conn.cursor()

        sql = "DELETE FROM " + db_schema + "." + table_name + " " + wc
        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def update_by_template(cls, db_schema, table_name, data_template, where_template):

        wc, where_args = RDBService.get_where_clause_args(where_template)

        terms = []
        data_args = []
        clause = None

        if data_template is None or data_template == {}:
            clause = ""
            args = None
        else:
            for k, v in data_template.items():
                terms.append(k + "=%s")
                data_args.append(v)

        args = data_args + where_args

        conn = RDBService.get_db_connection()
        cur = conn.cursor()

        sql = "UPDATE " + db_schema + "." + table_name + " SET " + ", ".join(terms) + wc
        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def split_course_id(cls, course_id):

        id_keys = ["course_year", "course_sem", "dept", "course_number", "section"]
        parameters = course_id.split('_')
        id_values = dict(zip(id_keys, parameters))

        return id_values

    @classmethod
    def find_by_course_id(cls, db_schema, table_name, course_id, field_list):

        id_values = RDBService.split_course_id(course_id)

        return RDBService.find_by_template(db_schema, table_name, id_values, field_list)

    @classmethod
    def delete_by_course_id(cls, db_schema, table_name, course_id):

        id_values = RDBService.split_course_id(course_id)

        return RDBService.delete_by_template(db_schema, table_name, id_values)

    @classmethod
    def update_by_course_id(cls, db_schema, table_name, course_id, data):

        id_values = RDBService.split_course_id(course_id)

        return RDBService.update_by_template(db_schema, table_name, data, id_values)

    @classmethod
    def get_name_inputs(cls, person_type, name):
        name_template = dict()
        name_template[person_type] = name
        return name_template

    @classmethod
    def find_by_name(cls, db_schema, table_name, person_type, name, field_list):

        name_template = RDBService.get_name_inputs(person_type, name)

        return RDBService.find_by_template(db_schema, table_name, name_template, field_list)

    @classmethod
    def delete_by_name(cls, db_schema, table_name, person_type, name):

        name_template = RDBService.get_name_inputs(person_type, name)

        return RDBService.delete_by_template(db_schema, table_name, name_template)

    @classmethod
    def update_by_name(cls, db_schema, table_name, person_type, name, data):

        name_template = RDBService.get_name_inputs(person_type, name)

        return RDBService.update_by_template(db_schema, table_name, data, name_template)

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        id_keys = ["course_year", "course_sem", "dept", "course_number", "section"]
        course_id = {key: value for key, value in create_data.items() if key in id_keys}
        course_matches = RDBService.find_by_template(db_schema, table_name, course_id)
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

            res = RDBService.run_sql(sql_stmt, args)

            return res
        else:
            return 9
