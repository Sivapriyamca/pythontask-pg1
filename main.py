import pandas as pd
from flask import Flask
from flask_restful import Api, Resource
data = pd.read_excel("C:\Users\HP\PycharmProjects\pythonProject3\production_data.xls")
annual_data = data.groupby("API WELL NUMBER")[["OIL (BBL)", "GAS (MCF)", "BRINE (BBL)"]].sum().reset_index()
import sqlite3
conn = sqlite3.connect("C:\Users\HP\PycharmProjects\pythonProject3\sqlite_3.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS annual_data (API_WELL_NUMBER TEXT, OIL INTEGER, GAS INTEGER, BRINE INTEGER)")
for _, row in annual_data.iterrows():
    cursor.execute("INSERT INTO annual_data VALUES (?, ?, ?, ?)", row)
conn.commit()
conn.close()

app = Flask(__name__)
api = Api(app)


class DataResource(Resource):
    def get(self):
        api_well_number = "34059242540000"
        conn = sqlite3.connect("C:\Users\HP\PycharmProjects\pythonProject3\sqlite_3.db")
        cursor = conn.cursor()
        cursor.execute("SELECT OIL, GAS, BRINE FROM annual_data WHERE API_WELL_NUMBER = ?", (api_well_number,))
        result = cursor.fetchone()
        conn.close()

        if result:
            oil, gas, brine = result
            return {"oil": oil, "gas": gas, "brine": brine}
        else:
            return {"error": "Well number not found."}, 404


api.add_resource(DataResource, "/data")

if __name__ == "__main__":

    app.run(port=8080)
