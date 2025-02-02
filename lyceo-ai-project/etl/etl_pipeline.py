from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the pre-trained student success model.
student_success_model = joblib.load('models/student_success_model.pkl')
# Load the recommendation model (if needed).
recommendation_model = joblib.load('models/recommendation_engine.pkl')

# Risk computation functions (mirroring ETL logic)
def compute_adhd_risk(engagement_score, content_interaction, time_spent):
    return 1 if engagement_score < 0.5 and content_interaction < 5 and time_spent < 60 else 0

def compute_dyslexia_risk(engagement_score, time_spent):
    return 1 if engagement_score < 0.55 and time_spent < 80 else 0

def compute_dysgraphia_risk(content_interaction):
    return 1 if content_interaction < 6 else 0

def compute_anxiety_depression_risk(engagement_score, time_spent):
    return 1 if engagement_score < 0.4 and time_spent < 60 else 0

def compute_asd_risk(engagement_score, content_interaction):
    return 1 if 0.5 <= engagement_score <= 0.7 and content_interaction < 8 else 0

@app.route('/predict_student_success', methods=['POST'])
def predict_student_success():
    """
    Expects a JSON payload with:
      - engagement_score (float)
      - content_interaction (int)
      - time_spent (float)
    Returns the predicted success outcome and computed risk indicators.
    """
    data = request.get_json()
    try:
        engagement_score = float(data.get('engagement_score'))
        content_interaction = int(data.get('content_interaction'))
        time_spent = float(data.get('time_spent'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input. Please provide numeric values for engagement_score, content_interaction, and time_spent.'}), 400

    # Prepare input for the success model.
    features = pd.DataFrame({
        'engagement_score': [engagement_score],
        'content_interaction': [content_interaction],
        'time_spent': [time_spent]
    })
    
    # Predict student success (1 = success, 0 = at-risk).
    success_prediction = int(student_success_model.predict(features)[0])
    
    # Compute additional risk flags.
    adhd_risk = compute_adhd_risk(engagement_score, content_interaction, time_spent)
    dyslexia_risk = compute_dyslexia_risk(engagement_score, time_spent)
    dysgraphia_risk = compute_dysgraphia_risk(content_interaction)
    anxiety_depression_risk = compute_anxiety_depression_risk(engagement_score, time_spent)
    asd_risk = compute_asd_risk(engagement_score, content_interaction)
    
    response = {
        'predicted_success': success_prediction,
        'adhd_risk': adhd_risk,
        'dyslexia_risk': dyslexia_risk,
        'dysgraphia_risk': dysgraphia_risk,
        'anxiety_depression_risk': anxiety_depression_risk,
        'asd_risk': asd_risk
    }
    return jsonify(response)

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    """
    Provide a personalized content recommendation.
    Expects a JSON payload with:
      - user_id (string)
      - (optional) content_history
    Returns a recommended content ID and its estimated rating.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required.'}), 400

    candidate_contents = ['C001', 'C002', 'C003', 'C004', 'C005', 'C006']
    best_rating = -np.inf
    best_content = None

    for content_id in candidate_contents:
        pred = recommendation_model.predict(user_id, content_id)
        if pred.est > best_rating:
            best_rating = pred.est
            best_content = content_id

    response = {
        'recommended_content': best_content,
        'estimated_rating': best_rating
    }
    return jsonify(response)

def plot_engagement_trends(csv_path):
    df = pd.read_csv(csv_path)
    # Ensure the timestamp column is in datetime format.
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='timestamp', y='engagement_score', marker='o')
    plt.title('Student Engagement Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Engagement Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def extract_data(file_path):
    """Extract data from CSV file"""
    logger.info(f"Extracting data from {file_path}")
    return pd.read_csv(file_path)

def transform_data(student_data, interaction_data):
    """Transform and merge student data with interactions"""
    logger.info("Transforming data")
    merged_data = pd.merge(student_data, interaction_data, on='student_id', how='inner')
    return merged_data

def load_data(transformed_data, database_connection):
    """Load transformed data into database"""
    logger.info("Loading data into database")
    transformed_data.to_sql('student_engagement', con=database_connection, if_exists='replace', index=False)

def run_etl_pipeline(student_data_path, interaction_data_path, database_connection):
    """Main ETL pipeline function"""
    try:
        student_data = extract_data(student_data_path)
        interaction_data = extract_data(interaction_data_path)
        transformed_data = transform_data(student_data, interaction_data)
        load_data(transformed_data, database_connection)
        logger.info("ETL pipeline completed successfully")
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    student_data_path = 'data/sample_student_data.csv'
    interaction_data_path = 'data/student_content_interactions.csv'
    database_connection = None  # Replace with actual database connection
    run_etl_pipeline(student_data_path, interaction_data_path, database_connection)

if __name__ == '__main__':
    csv_path = 'data/clean_student_data.csv'
    plot_engagement_trends(csv_path)
    app.run(debug=True, port=5000)

