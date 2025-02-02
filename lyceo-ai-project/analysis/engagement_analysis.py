import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path)

def analyze_engagement(interaction_data):
    engagement_metrics = {
        'total_interactions': len(interaction_data),
        'unique_students': interaction_data['student_id'].nunique(),
        'average_interactions_per_student': interaction_data['student_id'].value_counts().mean()
    }
    return engagement_metrics

def visualize_engagement(interaction_data):
    interaction_counts = interaction_data['student_id'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.hist(interaction_counts, bins=30, alpha=0.7, color='blue')
    plt.title('Distribution of Interactions per Student')
    plt.xlabel('Number of Interactions')
    plt.ylabel('Number of Students')
    plt.grid(axis='y')
    plt.show()

if __name__ == "__main__":
    interaction_data = load_data('../data/student_content_interactions.csv')
    metrics = analyze_engagement(interaction_data)
    print(metrics)
    visualize_engagement(interaction_data)