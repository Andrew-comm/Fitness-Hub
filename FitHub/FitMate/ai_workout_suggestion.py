# ai_workout_suggestion.py
import joblib
from sklearn.preprocessing import LabelEncoder

def suggest_workout(user_profile):
    # Load the trained model and label encoder
    model = joblib.load('/home/andrea/Projects/Django/Gym/FitHub/FitMate')
    label_encoder = joblib.load('/home/andrea/Projects/Django/Gym/FitHub/FitMate')

    # Preprocess the user's profile data
    features = user_profile_to_features(user_profile, label_encoder)

    # Use the model to predict the suggested workout
    suggested_workout = model.predict(features)[0]

    return suggested_workout

def user_profile_to_features(user_profile, label_encoder):
    # Extract relevant features and encode categorical variables
    features = [user_profile.age, user_profile.height, user_profile.weight,
                user_profile.fitness_level, user_profile.gender]

    # Encode categorical variables
    features[3] = label_encoder.transform([features[3]])[0]
    features[4] = label_encoder.transform([features[4]])[0]

    return [features]