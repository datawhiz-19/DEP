import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting background of plot as white
sns.set_style("whitegrid")

#Loading the data-set
file_path = r"C:\Users\SCS\Practice\heart+disease\processed.cleveland.data"
column_names = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
heart_diseases_df = pd.read_csv(file_path, header=None, names=column_names)
heart_diseases_df.head()     

#Data Exploration
print(f"Data set contains {heart_diseases_df.shape[0]} rows(patients) and {heart_diseases_df.shape[1]} columns(features).")
heart_diseases_df.describe(include='all')
heart_diseases_df.isnull().sum()

#Data Cleaning
heart_diseases_df.replace("?", pd.NA, inplace=True)
heart_diseases_df['ca'] = pd.to_numeric(heart_diseases_df['ca'], errors='coerce')
heart_diseases_df['thal'] = pd.to_numeric(heart_diseases_df['thal'], errors='coerce')
heart_diseases_df.fillna(heart_diseases_df.median(), inplace=True)
heart_diseases_df.isnull().sum()

# Data Analysis and visualization

    # Distribution by age and gender
plt.figure(figsize=(10,6))
sns.histplot(heart_diseases_df['age'], bins=20, kde=True, color='blue')
plt.title('Age Distribution of patients')
plt.xlabel('Age')
plt.ylabel('Number of patients')
plt.show()
sns.countplot(x='sex', hue='sex', data=heart_diseases_df, palette='coolwarm')
plt.xlabel('Sex(0=Female, 1=Male)')
plt.title('Gender Distribution of Patients')
plt.xlabel('Sex (0 = Female, 1 = Male)')
plt.ylabel('Number of Patients')
plt.show()

    # Risk factor by heart disease status
heart_diseases_df['heart_disease'] = heart_diseases_df['target'].apply(lambda x:1 if x>0 else 0)
sns.boxplot(x='heart_disease', y='chol', hue='heart_disease',data=heart_diseases_df, palette='Set2')
plt.title('Cholestrol levels by heart disease status')
plt.xlabel('Heart Disease (0=No, 1=Yes)')
plt.ylabel('Cholestrol level')
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(x='heart_disease', y='trestbps', hue='heart_disease', data=heart_diseases_df, palette='Set3')
plt.title('Resting blood pressure by heart diseass status')
plt.xlabel('Heart Disease (0=No, 1=Yes)')
plt.ylabel('Resting Blood Pressure')
plt.show()
 
    # Correlation Heatmap
corr_matrix = heart_diseases_df.corr()
plt.figure(figsize=(12,8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation matrix')
plt.show()

#Saving data
heart_diseases_df.to_csv('cleaned_heart_diseases_data.csv', index=False)


# In[ ]:





# In[ ]:




