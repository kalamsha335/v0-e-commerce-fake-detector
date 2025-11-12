"""
Model training script for fake product detection.
Trains a RandomForest classifier on labeled listings.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, roc_auc_score
)
import pickle
import json
from pathlib import Path
from features import FeatureExtractor, extract_batch_features

def load_dataset(csv_path: str) -> pd.DataFrame:
    """Load labeled dataset."""
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} samples")
    print(f"Fake: {df['is_fake'].sum()}, Real: {(1 - df['is_fake']).sum()}")
    return df

def train_model(train_df: pd.DataFrame, test_df: pd.DataFrame):
    """Train and evaluate the model."""
    
    # Feature extraction
    print("Extracting features...")
    extractor = FeatureExtractor()
    
    # Fit extractor on training data
    extractor.fit(train_df)
    
    # Extract features
    X_train = extract_batch_features(train_df, extractor)
    X_test = extract_batch_features(test_df, extractor)
    
    y_train = train_df['is_fake'].values
    y_test = test_df['is_fake'].values
    
    print(f"Feature count: {X_train.shape[1]}")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train RandomForest
    print("Training RandomForest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Handle imbalance
    )
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Evaluation
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, zero_division=0)),
        'f1': float(f1_score(y_test, y_pred, zero_division=0)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
    }
    
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n=== Model Evaluation ===")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1 Score: {metrics['f1']:.4f}")
    print(f"ROC AUC: {metrics['roc_auc']:.4f}")
    print(f"\nConfusion Matrix:\n{cm}")
    
    # Feature importance
    feature_importance = {
        name: float(importance)
        for name, importance in zip(X_train.columns, model.feature_importances_)
    }
    feature_importance_sorted = dict(
        sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    )
    
    print("\nTop Features:")
    for i, (name, importance) in enumerate(list(feature_importance_sorted.items())[:10]):
        print(f"  {i+1}. {name}: {importance:.4f}")
    
    return model, scaler, extractor, metrics, feature_importance_sorted, cm, X_test, y_test, y_pred


def save_artifacts(model, scaler, extractor, metrics, feature_importance, output_dir: str = 'ml/models'):
    """Save model and preprocessing artifacts."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save model
    with open(f'{output_dir}/fake_detector_v0.1.pkl', 'wb') as f:
        pickle.dump({
            'model': model,
            'scaler': scaler,
            'extractor': extractor,
        }, f)
    
    # Save metrics
    with open(f'{output_dir}/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save feature importance
    with open(f'{output_dir}/feature_importance.json', 'w') as f:
        json.dump(feature_importance, f, indent=2)
    
    print(f"\nArtifacts saved to {output_dir}/")


if __name__ == '__main__':
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    
    categories = ['electronics', 'clothing', 'jewelry', 'watches', 'books']
    countries = ['US', 'IN', 'CN', 'UK', 'CA']
    
    data = {
        'title': [f'Product {i}' for i in range(n_samples)],
        'description': [f'Description {i}' for i in range(n_samples)],
        'price': np.random.uniform(10, 5000, n_samples),
        'seller': [f'Seller {i % 50}' for i in range(n_samples)],
        'rating': np.random.uniform(1, 5, n_samples),
        'review_count': np.random.randint(0, 10000, n_samples),
        'category': np.random.choice(categories, n_samples),
        'country': np.random.choice(countries, n_samples),
        'images': [[] for _ in range(n_samples)],
        'is_fake': np.random.binomial(1, 0.3, n_samples),  # 30% fake
    }
    
    df = pd.DataFrame(data)
    
    # Split
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['is_fake'])
    
    # Train
    model, scaler, extractor, metrics, feature_importance, cm, X_test, y_test, y_pred = train_model(train_df, test_df)
    
    # Save
    save_artifacts(model, scaler, extractor, metrics, feature_importance)
    
    print("\n=== Training Complete ===")
