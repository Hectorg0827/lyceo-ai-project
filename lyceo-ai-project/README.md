# Lyceo AI Project

## Overview
The Lyceo AI Project is designed to analyze student data and interactions to enhance educational outcomes. This project includes an API for data handling, an ETL pipeline for data processing, machine learning models for predictions and recommendations, and analysis scripts for engagement metrics.

## Folder Structure
- **api/**: Contains the main application for the API.
  - `app.py`: Entry point for the API, defining routes for student data handling.
  
- **data/**: Holds the datasets used in the project.
  - `sample_student_data.csv`: Sample data for students, including attributes like ID, name, and age.
  - `student_content_interactions.csv`: Records of student interactions with content, including timestamps and content IDs.

- **etl/**: Contains the ETL pipeline for data processing.
  - `etl_pipeline.py`: Functions for extracting, transforming, and loading data.

- **models/**: Implements machine learning models.
  - `student_success_model.py`: Model predicting student success based on various features.
  - `recommendation_engine.py`: Suggests content to students based on interactions.
  - `reinforcement_learning.py`: Implements reinforcement learning algorithms for optimizing engagement.

- **analysis/**: Scripts for analyzing student engagement.
  - `engagement_analysis.py`: Functions for visualizing data and calculating engagement metrics.

- **requirements.txt**: Lists project dependencies for libraries used in data manipulation, machine learning, and web development.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd lyceo-ai-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the API:
   ```
   python api/app.py
   ```

## Usage Guidelines
- Use the API endpoints defined in `app.py` to interact with student data.
- Utilize the ETL pipeline to process and load data for analysis.
- Explore the models to understand predictions and recommendations.
- Analyze engagement metrics using the scripts in the analysis folder.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.