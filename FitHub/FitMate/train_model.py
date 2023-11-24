# train_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
from models import UserProfile


def preprocess_data(user_profiles, encoder=None):
    # Example: Extract relevant features and encode categorical variables
    features = user_profiles[['age', 'height', 'weight', 'fitness_level', 'gender']]
    
    if encoder is None:
        encoder = LabelEncoder()

    features['fitness_level'] = encoder.fit_transform(features['fitness_level'])
    features['gender'] = encoder.fit_transform(features['gender'])
    
    return features, encoder

def train_model(user_profiles):
    features, label_encoder = preprocess_data(user_profiles)
    target = user_profiles['suggested_workout']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train a RandomForestClassifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save the trained model and label encoder
    joblib.dump(model, 'trained_model.joblib')
    joblib.dump(label_encoder, 'label_encoder.joblib')

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'Model Accuracy: {accuracy}')

    return model

if __name__ == "__main__":
    # Ensure you have user profiles in your database
    user_profiles = UserProfile.objects.all()

    # Train the model using user profiles
    trained_model = train_model(user_profiles)

    print("Training completed. Model saved as 'trained_model.joblib'")
