def extract_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def transform_data(student_data, interaction_data):
    # Example transformation: merging datasets on student ID
    merged_data = pd.merge(student_data, interaction_data, on='student_id', how='inner')
    return merged_data

def load_data(transformed_data, database_connection):
    # Example loading function (pseudo-code)
    transformed_data.to_sql('student_engagement', con=database_connection, if_exists='replace', index=False)

def run_etl_pipeline(student_data_path, interaction_data_path, database_connection):
    student_data = extract_data(student_data_path)
    interaction_data = extract_data(interaction_data_path)
    transformed_data = transform_data(student_data, interaction_data)
    load_data(transformed_data, database_connection)

# Example usage
if __name__ == "__main__":
    student_data_path = '../data/sample_student_data.csv'
    interaction_data_path = '../data/student_content_interactions.csv'
    database_connection = None  # Replace with actual database connection
    run_etl_pipeline(student_data_path, interaction_data_path, database_connection)