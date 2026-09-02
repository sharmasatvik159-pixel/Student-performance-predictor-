import pandas as pd
import numpy as np
import os

def generate_data(num_samples=1000):
    np.random.seed(42)
    
    study_hours = np.random.uniform(0, 15, num_samples)
    attendance = np.random.uniform(50, 100, num_samples)
    previous_scores = np.random.uniform(40, 100, num_samples)
    
    parental_education = np.random.choice(["High School", "Bachelor's", "Master's"], num_samples)
    test_preparation = np.random.choice(['None', 'Completed'], num_samples)
    
    # Calculate base performance
    performance = (
        study_hours * 2 + 
        (attendance / 100) * 30 + 
        (previous_scores / 100) * 40
    )
    
    # Add categorical effects
    perf_adj = []
    for edu, prep in zip(parental_education, test_preparation):
        adj = 0
        if edu == "Bachelor's":
            adj += 5
        elif edu == "Master's":
            adj += 10
            
        if prep == 'Completed':
            adj += 8
        perf_adj.append(adj)
        
    performance += np.array(perf_adj)
    
    # Add noise
    performance += np.random.normal(0, 3, num_samples)
    
    # Clip to 0-100
    performance = np.clip(performance, 0, 100)
    
    data = {
        'Study_Hours': np.round(study_hours, 1),
        'Attendance': np.round(attendance, 1),
        'Previous_Score': np.round(previous_scores, 1),
        'Parental_Education': parental_education,
        'Test_Preparation': test_preparation,
        'Final_Score': np.round(performance, 1)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/student_data.csv', index=False)
    print(f"Data generated and saved to data/student_data.csv with {num_samples} records.")

if __name__ == '__main__':
    generate_data()
