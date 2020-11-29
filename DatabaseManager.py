import pymysql.cursors
from Constants import *


class DatabaseManager:
    def __init__(self):
        self.connection = pymysql.connect(host=DB_HOST,
                                          user=DB_USER,
                                          password=DB_PASSWORD,
                                          db=DB_NAME,
                                          cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.connection.close()

    def add_pc_to_db(self, pc_name):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                statement = "INSERT INTO " + PC_TABLE + " (`name`) VALUES (%s)"
                cursor.execute(statement, pc_name)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print('Something went wrong while adding pc to the database:', e)

    def add_benchmark_result(self, pc_id, benchmark_id, exec_time, spec_ratio):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                statement = "INSERT INTO " + PC_RESULTS_TABLE + "(`pc_id`, `benchmark_id`, `execution_time`, " \
                                                                "`SPEC_RATIO`) VALUES (%s,%s,%s,%s) "
                cursor.execute(statement, (pc_id, benchmark_id, exec_time, spec_ratio))
            self.connection.commit()
        except Exception as e:
            print('Something went wrong while adding benchmark result to the database:', e)

    def update_avg_spec_ratio(self, pc_id, ratio):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                statement = "UPDATE " + PC_TABLE + " SET `AVG_SPEC_RATIO` = %s WHERE `id` = %s"
                cursor.execute(statement, (ratio, pc_id))
            self.connection.commit()
        except Exception as e:
            print('Something went wrong while updating average spec ratio:', e)

    def get_reference_times(self):
        try:
            with self.connection.cursor() as cursor:
                statement = "SELECT `benchmark_id`, `execution_time` FROM " + PC_RESULTS_TABLE + " WHERE `pc_id`=1"
                cursor.execute(statement)
                result = cursor.fetchall()
            return result
        except Exception as e:
            print('Something went wrong while getting reference times:', e)

    def get_pc_ranking(self, pc_id):
        try:
            with self.connection.cursor() as cursor:
                statement = "SELECT rank, AVG_SPEC_RATIO FROM" \
                            " (SELECT id, name, AVG_SPEC_RATIO, @curRank := @curRank + 1 AS rank" \
                            " FROM " + PC_TABLE + ", (SELECT @curRank := 0) r ORDER BY AVG_SPEC_RATIO DESC) AS T" \
                            " WHERE id = %s;"
                cursor.execute(statement, (str(pc_id)))
                result = cursor.fetchone()
            return {'rank': result['rank'], 'avg': result['AVG_SPEC_RATIO']}
        except Exception as e:
            print('Something went wrong while getting your ranking and average spec ratio:', e)

    def get_total_pc_count(self):
        try:
            with self.connection.cursor() as cursor:
                statement = "SELECT COUNT(id) as total FROM " + PC_TABLE
                cursor.execute(statement)
                result = cursor.fetchone()
            return result['total']
        except Exception as e:
            print('Something went wrong while fetching total number of pcs:', e)
