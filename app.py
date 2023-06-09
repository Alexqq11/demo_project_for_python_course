from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] =f"postgresql://{os.environ['PG_USER']}:{os.environ['PG_PASSWORD']}@{os.environ['PG_HOST']}:5432/{os.environ['PG_DB']}"
#'postgresql://myuser:mypassword@45.131.40.79:5432/employees'#80.249.146.63:5432
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))

    def __init__(self, name, position):
        self.name = name
        self.position = position


with app.app_context():
    db.create_all()

@app.route('/employees')
def get_employees():
    try:
        employees = Employee.query.all()
        result = []
        for employee in employees:
            data = {
                        'id': employee.id,
                        'name': employee.name,
                        'position': employee.position
                    }
            result.append(data)
        return jsonify(result)
    except SQLAlchemyError as e:
        error = str(__dict__.get('orig', e))
        return jsonify({'error': error}), 500

@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        name = request.json['name']
        position = request.json['position']
        employee = Employee(name=name, position=position)
        db.session.add(employee)
        db.session.commit()
        return jsonify({'message': 'Employee added successfully'})
    except SQLAlchemyError as e:
        error = str(e)
        return jsonify({'error': error}), 500


@app.route('/get_employee/<int:id>')
def get_employee(id):
    try:
        employee = Employee.query.get(id)
        if employee:
            return jsonify({
                'id': employee.id,
                'name': employee.name,
                'position': employee.position
            })
        else:
            return {'error': 'Employee not found'}
    except SQLAlchemyError as e:
        error = str(e)
        return jsonify({'error': error}), 500

@app.route('/update_employee/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        name = request.json.get('name', employee.name)
        position = request.json.get('position', employee.position)
        employee.name = name
        employee.position = position
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'})
    except SQLAlchemyError as e:
        error = str(e)
        return jsonify({'error': error}), 500


@app.route('/delete_employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})
    except SQLAlchemyError as e:
        error = str(e)
        return jsonify({'error': error}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
