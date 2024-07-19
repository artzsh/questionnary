from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="123"
    )
    return conn

@app.route('/question')
def question():
    return render_template("quest.html")
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    institution_data = {
        "location": data.get('location'),
        "name": data.get('name'),
        "type": data.get('type'),
        "staff_shortage": 'staff_shortage' in data
    }

    employees_data = []
    for i in range(len(data.getlist('specialty[]'))):
        employee = {
            "specialty": data.getlist('specialty[]')[i],
            "age": data.getlist('age[]')[i],
            "education": data.getlist('education[]')[i],
            "education_location": data.getlist('education_location[]')[i],
            "education_year": data.getlist('education_year[]')[i],
            "additional_specialty_education": data.getlist('additional_specialty_education[]')[i],
            "additional_position_education": data.getlist('additional_position_education[]')[i]
        }
        employees_data.append(employee)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO questionnary.institutions (location, name, type, staff_shortage) VALUES (%s, %s, %s, %s) RETURNING id",
        (institution_data['location'], institution_data['name'], institution_data['type'], institution_data['staff_shortage'])
    )
    institution_id = cur.fetchone()[0]
    
    for employee in employees_data:
        cur.execute(
            "INSERT INTO questionnary.employees (institution_id, specialty, age, education, education_location, education_year, additional_specialty_education, additional_position_education) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (institution_id, employee['specialty'], employee['age'], employee['education'], employee['education_location'], employee['education_year'], employee['additional_specialty_education'], employee['additional_position_education'])
        )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)