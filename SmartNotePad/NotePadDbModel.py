import cx_Oracle
import traceback
from cx_Oracle import *

class Db_Model:
    def __init__(self):
        self.file_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("mojo/mojo@127.0.0.1/xe")
            print("Connected successfully to the DB")
            self.cur = self.conn.cursor()
        except DatabaseError:
            self.db_status = False
            print("DBError:",traceback.format_exc())

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor closed")
        if self.conn is not None:
            self.conn.close()
            print("Connection closed")

    def add_file(self, file_name, file_path, file_owner, file_pwd):
        self.file_dict[file_name] = (file_path, file_owner, file_pwd)
        print("file added:", self.file_dict[file_name])

    def get_file_path(self, file_name):
        return self.file_dict[file_name][0]

    def add_file_to_db(self, file_name, file_path, file_owner, file_pwd):
        self.cur.execute("select max(file_id) from myfiles")
        last_file_id = self.cur.fetchone()[0]
        next_file_id = 1
        if last_file_id is not None:
            next_file_id = last_file_id + 1
        self.cur.execute("insert into myfiles values(:1,:2,:3,:4,:5)",(next_file_id, file_name, file_path, file_owner, file_pwd))
        self.conn.commit()
        return "file successfully added to your Database"

    def load_files_from_db(self):
        self.cur.execute("select file_name,file_path,file_owner,file_pwd from myfiles")
        file_present = False
        for file_name, file_path, file_owner, file_pwd in self.cur:
            self.file_dict[file_name] = (file_path, file_owner, file_pwd)
            file_present = True
        if file_present:
            return "files populated from DB"
        else:
            return "No files present in your DB"

    def remove_file_from_db(self, file_name):
        self.cur.execute("delete from myfiles where file_name=:1", (file_name,))
        count = self.cur.rowcount
        if count == 0:
            return "file not presant in your DB"
        else:
            self.file_dict.pop(file_name)
            self.conn.commit()
            return "file deleted from your DB"

    def is_secure_file(self, file_name):
        if file_name in self.file_dict:
            return True
        else:
            return False

    def get_file_pwd(self, file_name):
        return self.file_dict[file_name][2]

    def get_file_count(self):
        return len(self.file_dict)


e1=Db_Model()