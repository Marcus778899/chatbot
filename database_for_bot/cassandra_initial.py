'''
connect cassandra database
'''
import logging
from pathlib import Path
from cassandra.cluster import Cluster
import json

WORK_DIR = Path(__file__).parent.parent
class CassandraDB:
    def __init__(self) -> None:
        self.ip = []
        with open(f"{WORK_DIR}/login_info/cassandra_cluster.txt") as file:
            for row in file.readlines():
                self.ip.append(row.strip())
        self.cluster = Cluster(self.ip)
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

    def close_driver(self):
        self.session.shutdown()
        self.cluster.shutdown()

if __name__ == "__main__":
    action = CassandraDB()
    session = action.session
    with open(f"{WORK_DIR}/login_info/customer_test.json","r") as file:
        example = json.load(file)
    try:
        action.insert_into_customer_data(example)
        # print(rows.current_rows)
    finally:
        action.close_driver()

