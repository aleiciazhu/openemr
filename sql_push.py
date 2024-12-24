import mysql.connector
import logging
from mysql.connector import Error
from datetime import datetime, date

logging.basicConfig(level=logging.DEBUG)
def connect_to_database():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='localhost',         # Replace with your database host
            port=8320,
            user='openemr',     # Replace with your MariaDB username
            password='openemr', # Replace with your MariaDB password
            database='openemr',  # Replace with your database name
            collation="utf8mb4_general_ci",
            charset='utf8mb4'
        )

        if connection.is_connected():
            print("Connected to MariaDB")

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            cursor.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';")

            # Push a SOAP form
            subjective = """Patient reports fluctuating energy levels and inconsistent blood sugar readings, with higher levels noted 3-4 times a week, especially in the mornings and occasionally post-dinner.
                Increased stress at work and reduced exercise.
                Diet mostly adherent to the meal plan but includes dining out twice weekly with occasional high-carb choices."""
            objective = """Blood glucose logbook reviewed: fasting glucose elevated on multiple days, post-dinner glucose spikes noted.
                Patient denies increased thirst, frequent urination, or blurred vision."""
            assessment = """Suboptimal glucose control likely due to stress, dietary choices, and reduced physical activity.
                Possible overnight hepatic glucose production contributing to elevated fasting sugars."""
            plan = """Dietary Adjustments:
                Add a protein-based bedtime snack to stabilize overnight glucose.
                Reduce portions of starchy foods at dinner; focus on vegetables and lean protein.
                Physical Activity:
                Incorporate a 10-15 minute post-dinner walk.
                Stress Management:
                Begin using relaxation apps for deep breathing or meditation.
                Consider counseling if stress persists.
                Medications:
                Continue metformin as prescribed. Evaluate potential dosage adjustment after lab results.
                Labs Ordered:
                A1C, kidney function, cholesterol panel.
                Follow-up:
                Schedule in two weeks to discuss lab results and reassess glucose management."""
            soap_id = 2
            patient_id = 1
            create_soap = push_soap(patient_id, soap_id, subjective, objective, assessment, plan)
            cursor.execute(create_soap)
            connection.commit()

            form_add = f"""INSERT INTO `forms` (`id`, `date`, `encounter`, `form_name`, `form_id`, `pid`, `user`, 
            `groupname`, `authorized`, `deleted`, `formdir`) 
            VALUES (2, '{date.today()}', 2, 'SOAP', 2, '{patient_id}', 'physician', 'Default', 1, 0, 'soap');"""
            cursor.execute(form_add)
            connection.commit()
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")

def execute_query(query):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug("Query executed successfully")
        # Fetch and display results
        results = cursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as err:
        logging.error(f"Error executing query: {err}")
    finally:
        cursor.close()
        connection.close()
        print("Connection closed.")

def push_soap(patient_id, form_id, s, o, a, p):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"""INSERT INTO `form_soap` (`id`, `date`, `pid`, `user`, `groupname`, `authorized`, 
        `activity`, `subjective`, `objective`, `assessment`, `plan`) 
        VALUES ('{form_id}', '{formatted_date}', '{patient_id}', 'physician', 'Default', 0, 1, '{s}', '{o}', '{a}', '{p}');"""



if __name__ == "__main__":
    connect_to_database()
    print("Connected to MariaDB")

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            cursor.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';")

            # Push a SOAP form
            subjective = """Patient reports fluctuating energy levels and inconsistent blood sugar readings, with higher levels noted 3-4 times a week, especially in the mornings and occasionally post-dinner.
                Increased stress at work and reduced exercise.
                Diet mostly adherent to the meal plan but includes dining out twice weekly with occasional high-carb choices."""
            objective = """Blood glucose logbook reviewed: fasting glucose elevated on multiple days, post-dinner glucose spikes noted.
                Patient denies increased thirst, frequent urination, or blurred vision."""
            assessment = """Suboptimal glucose control likely due to stress, dietary choices, and reduced physical activity.
                Possible overnight hepatic glucose production contributing to elevated fasting sugars."""
            plan = """Dietary Adjustments:
                Add a protein-based bedtime snack to stabilize overnight glucose.
                Reduce portions of starchy foods at dinner; focus on vegetables and lean protein.
                Physical Activity:
                Incorporate a 10-15 minute post-dinner walk.
                Stress Management:
                Begin using relaxation apps for deep breathing or meditation.
                Consider counseling if stress persists.
                Medications:
                Continue metformin as prescribed. Evaluate potential dosage adjustment after lab results.
                Labs Ordered:
                A1C, kidney function, cholesterol panel.
                Follow-up:
                Schedule in two weeks to discuss lab results and reassess glucose management."""
            soap_id = 2
            patient_id = 1
            create_soap = push_soap(patient_id, soap_id, subjective, objective, assessment, plan)
            cursor.execute(create_soap)
            connection.commit()

            form_add = f"""INSERT INTO `forms` (`id`, `date`, `encounter`, `form_name`, `form_id`, `pid`, `user`, 
            `groupname`, `authorized`, `deleted`, `formdir`) 
            VALUES (2, '{date.today()}', 2, 'SOAP', 2, '{patient_id}', 'physician', 'Default', 1, 0, 'soap');"""
            cursor.execute(form_add)
            connection.commit()