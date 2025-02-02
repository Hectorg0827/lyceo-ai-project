from flask import Flask, jsonify, request # type: ignore
import pandas as pd

app = Flask(__name__)

# Load student data
student_data = pd.read_csv('data/sample_student_data.csv')
content_interactions = pd.read_csv('data/student_content_interactions.csv')

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(student_data.to_dict(orient='records'))

@app.route('/interactions', methods=['GET'])
def get_interactions():
    return jsonify(content_interactions.to_dict(orient='records'))

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = student_data[student_data['student_id'] == student_id]
    if student.empty:
        return jsonify({'error': 'Student not found'}), 404
    else:
        # Return the first matching record
        return jsonify(student.iloc[0].to_dict())

@app.route('/interactions/<int:student_id>', methods=['GET'])
def get_student_interactions(student_id):
    interactions = content_interactions[content_interactions['student_id'] == student_id]
    return jsonify(interactions.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)