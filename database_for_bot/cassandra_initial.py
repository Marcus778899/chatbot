'''
connect cassandra database
'''
import logging
from pathlib import Path
from cassandra.cluster import Cluster,DCAwareRoundRobinPolicy
import json

WORK_DIR = Path(__file__).parent.parent
class CassandraDB:
    def __init__(self) -> None:
        self.ip = []
        with open(f"{WORK_DIR}/login_info/cassandra_cluster.txt") as file:
            for row in file.readlines():
                self.ip.append(row.strip())
        self.cluster = Cluster(
            contact_points=self.ip,
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
            protocol_version=4,
        )
        self.session = self.cluster.connect(keyspace="telegram")

    def insert_into_customer_data(self, data: dict):
        query_prefix = f"INSERT INTO telegram.customer ("
        query_suffix = ") VALUES ("
        for key, value in data.items():
            query_prefix += (key + ", ")
            query_suffix += (f"'{value}'" + ", ")
        query = query_prefix[:-2] + query_suffix[:-2] + ");"
        print(query)
        try:
            self.session.execute(query)
            logging.info("create customer basic information")
        except Exception as e:
            logging.error(e)
    
    def check_the_username_exist(self, username: str) -> bool:
        query = f"SELECT username FROM telegram.customer WHERE username = '{username}'"
        rows = self.session.execute(query)
        if rows.current_rows:
            return True
        
    def check_the_account(self, login: dict) -> bool:
        show_column = ['username', 'password']
        query = f"SELECT {','.join(show_column)} FROM telegram.customer WHERE username = '{login['username']}'"
        rows = self.session.execute(query)
        if rows.current_rows and  rows.current_rows[0].password == login['password']:
            return True
        return False

    def selet_account_data(self,username:str):
        show_column = ['username','email', 'phone', 'level']
        query = f"SELECT {','.join(show_column)} FROM telegram.customer WHERE username = '{username}';"
        rows = self.session.execute(query)
        return rows.current_rows
    
    def select_price_data(self, level: str):
        query = f"SELECT price FROM telegram.level_payment WHERE level ='{level}';"
        price = self.session.execute(query).current_rows[0].price
        return price

    def close_driver(self):
        self.session.shutdown()
        self.cluster.shutdown()

if __name__ == "__main__":
    action = CassandraDB()
    session = action.session
    # with open(f"{WORK_DIR}/login_info/customer_test.json","r") as file:
    #     example = json.load(file)
    try:
        # if action.check_the_username_exist(username = 'Marcus'):
        #     print("exist")
        # else:
        #     print("not exist")
        # print(rows.current_rows)
        action.select_price_data(level='basic')
    finally:
        action.close_driver()

