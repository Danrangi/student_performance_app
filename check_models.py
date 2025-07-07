"""
Check if models are properly loaded and working
"""

import os
import joblib
import pandas as pd

def check_models():
    print("🔍 Checking model files...")
    
    # Check if model files exist
    model_files = [
        'models/student_performance_model.joblib',
        'models/label_encoders.joblib', 
        'models/feature_names.joblib'
    ]
    
    missing_files = []
    for file_path in model_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing {len(missing_files)} model files!")
        print("Please ensure you have the following files in the models directory:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    # Try to load models
    try:
        print("\n🔄 Loading models...")
        model = joblib.load('models/student_performance_model.joblib')
        label_encoders = joblib.load('models/label_encoders.joblib')
        feature_names = joblib.load('models/feature_names.joblib')
        
        print(f"✅ Model type: {type(model).__name__}")
        print(f"✅ Number of features: {len(feature_names)}")
        print(f"✅ Number of encoders: {len(label_encoders)}")
        
        # Test prediction with sample data
        print("\n🧪 Testing prediction...")
        sample_data = {
            'school': ['GP'], 'sex': ['F'], 'age': [18], 'address': ['U'], 'famsize': ['GT3'],
            'Pstatus': ['A'], 'Medu': [4], 'Fedu': [4], 'Mjob': ['at_home'], 'Fjob': ['teacher'],
            'reason': ['course'], 'guardian': ['mother'], 'traveltime': [2], 'studytime': [2],
            'failures': [0], 'schoolsup': ['yes'], 'famsup': ['no'], 'paid': ['no'],
            'activities': ['no'], 'nursery': ['yes'], 'higher': ['yes'], 'internet': ['no'],
            'romantic': ['no'], 'famrel': [4], 'freetime': [3], 'goout': [4], 'Dalc': [1],
            'Walc': [1], 'health': [3], 'absences': [6], 'G1': [5], 'G2': [6]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Preprocess data
        processed_df = df.copy()
        for column, encoder in label_encoders.items():
            if column in processed_df.columns:
                processed_df[column] = processed_df[column].astype(str)
                known_categories = set(encoder.classes_)
                processed_df[column] = processed_df[column].apply(
                    lambda x: x if x in known_categories else encoder.classes_[0]
                )
                processed_df[column] = encoder.transform(processed_df[column])
        
        for feature in feature_names:
            if feature not in processed_df.columns:
                processed_df[feature] = 0
        
        processed_df = processed_df[feature_names]
        
        # Make prediction
        prediction = model.predict(processed_df)[0]
        prediction_proba = model.predict_proba(processed_df)[0]
        confidence = max(prediction_proba)
        
        print(f"✅ Sample prediction: {'Good Performance' if prediction == 1 else 'Needs Support'}")
        print(f"✅ Confidence: {confidence:.1%}")
        
        print("\n🎉 All models are working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error loading models: {str(e)}")
        return False

def check_data_files():
    print("\n📁 Checking data files...")
    
    data_files = [
        'data/test_students.csv',
        'data/sample_student_data.csv'
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
            try:
                df = pd.read_csv(file_path)
                print(f"   📊 Shape: {df.shape}")
            except Exception as e:
                print(f"   ❌ Error reading file: {str(e)}")
        else:
            print(f"⚠️ Missing: {file_path}")

if __name__ == "__main__":
    print("🎓 Student Performance Prediction System - Model Check")
    print("=" * 60)
    
    models_ok = check_models()
    check_data_files()
    
    print("\n" + "=" * 60)
    if models_ok:
        print("✅ System is ready! You can now run the web application.")
        print("\nTo start the web app, run:")
        print("streamlit run web_app.py")
    else:
        print("❌ Please fix the issues above before running the application.")
