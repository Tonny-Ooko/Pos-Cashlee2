from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_mysql_host',
    'database': 'your_database_name',
    'port': 'your_port_number',
}

# Connect to the database
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def daily_report():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        employee_id = request.form['employee_id']
        department = request.form['department']
        position = request.form['position']
        contact_info = request.form['contact_info']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        break_times = request.form['break_times']
        tasks = request.form['tasks']
        incidents = request.form['incidents']
        equipment_used = request.form['equipment_used']
        compliance_checklist = request.form['compliance_checklist']
        quality_control = request.form['quality_control']
        comments = request.form['comments']
        employee_signature = request.form['employee_signature']
        supervisor_signature = request.form['supervisor_signature']

        # Capture date and time
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate total hours worked
        total_hours_worked = calculate_total_hours(start_time, end_time, break_times)

        # Insert data into the database
        insert_query = """INSERT INTO daily_reports (name, employee_id, department, position, contact_info,
                            date_time, start_time, end_time, break_times, total_hours_worked, tasks, incidents, 
                            equipment_used, compliance_checklist, quality_control, comments, employee_signature,
                            supervisor_signature) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (name, employee_id, department, position, contact_info, date_time, start_time, end_time, break_times,
                total_hours_worked, tasks, incidents, equipment_used, compliance_checklist, quality_control, comments,
                employee_signature, supervisor_signature)
        cursor.execute(insert_query, data)
        db.commit()

        return "Daily report submitted successfully!"

    return render_template('daily_report_form.html')

def calculate_total_hours(start_time, end_time, break_times):
    # Convert start and end times to datetime objects
    start_datetime = datetime.strptime(start_time, "%H:%M")
    end_datetime = datetime.strptime(end_time, "%H:%M")

    # Calculate total work hours
    total_hours = (end_datetime - start_datetime).seconds / 3600

    # Deduct break times from total hours
    if break_times:
        breaks = [int(b.strip()) for b in break_times.split(',')]
        total_hours -= sum(breaks)

    return total_hours

if __name__ == '__main__':
    app.run(debug=True)
