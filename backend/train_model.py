"""
Train and evaluate ML models for Vehicle Insurance Fraud Detection (Tasks 1-5).
Produces model.joblib, model_metadata.json, and regression_metadata.json.
"""

import os
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

CLEANED_DATA_PATH = os.path.join(PROJECT_DIR, "cleaned_data.csv")
RAW_DATA_PATH = os.path.join(PROJECT_DIR, "insurance_fraud_data.csv")
TASK3_DATA_PATH = os.path.join(PROJECT_DIR, "Classification_Task3_Data.csv")

MODEL_OUT_PATH = os.path.join(BASE_DIR, "model.joblib")
META_OUT_PATH = os.path.join(BASE_DIR, "model_metadata.json")
REG_OUT_PATH = os.path.join(BASE_DIR, "regression_metadata.json")
EDA_OUT_PATH = os.path.join(BASE_DIR, "eda_metadata.json")


def train_classification_model():
    print("Loading cleaned dataset from:", CLEANED_DATA_PATH)
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Target and features
    X = df.drop(columns=['fraud_reported_Y', 'claim_number', 'claim_date'], errors='ignore').copy()
    y = df['fraud_reported_Y'].astype(int)
    
    # Ensure boolean columns are numeric 0/1
    for col in X.columns:
        if X[col].dtype == 'bool':
            X[col] = X[col].astype(int)
    
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    feature_names = list(X.columns)
    
    # 80/20 Stratified Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Models from Task 5
    models = {
        'Logistic Regression': Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(max_iter=2000, random_state=42))
        ]),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=6),
        'Random Forest': RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42, n_jobs=-1),
        'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    }
    
    model_evaluations = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    best_model_name = "Gradient Boosting"
    best_model_obj = None
    best_f1 = -1.0
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        train_acc = float(accuracy_score(y_train, train_pred))
        test_acc = float(accuracy_score(y_test, test_pred))
        precision = float(precision_score(y_test, test_pred, zero_division=0))
        recall = float(recall_score(y_test, test_pred, zero_division=0))
        f1 = float(f1_score(y_test, test_pred, zero_division=0))
        
        diff = train_acc - test_acc
        if diff > 0.10:
            fit_status = "Overfitting"
        elif train_acc < 0.60 and test_acc < 0.60:
            fit_status = "Underfitting"
        else:
            fit_status = "Good fit"
            
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='f1', n_jobs=-1)
        cv_f1_mean = float(cv_scores.mean())
        cv_f1_std = float(cv_scores.std())
        
        model_evaluations[name] = {
            "train_accuracy": round(train_acc, 4),
            "test_accuracy": round(test_acc, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "fit_status": fit_status,
            "cv_f1_mean": round(cv_f1_mean, 4),
            "cv_f1_std": round(cv_f1_std, 4)
        }
        
        # We select model with best test F1 or best balance
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model
            
    # Default best model: Gradient Boosting (or Random Forest)
    if best_model_obj is None:
        best_model_name = 'Gradient Boosting'
        best_model_obj = models['Gradient Boosting']
        
    print(f"Best model selected: {best_model_name} (F1={best_f1:.4f})")
    
    # Save best model
    joblib.dump(best_model_obj, MODEL_OUT_PATH)
    print(f"Saved best model to: {MODEL_OUT_PATH}")
    
    # Get feature importances if tree-based
    feature_importances = {}
    if hasattr(best_model_obj, "feature_importances_"):
        importances = best_model_obj.feature_importances_
        sorted_indices = np.argsort(importances)[::-1]
        for idx in sorted_indices[:15]:
            feature_importances[feature_names[idx]] = round(float(importances[idx]), 4)
            
    # Final confusion matrix for best model
    best_pred = best_model_obj.predict(X_test)
    cm = confusion_matrix(y_test, best_pred).tolist()
    
    metadata = {
        "best_model": best_model_name,
        "feature_names": feature_names,
        "evaluations": model_evaluations,
        "feature_importances": feature_importances,
        "confusion_matrix": cm,
        "train_samples": int(X_train.shape[0]),
        "test_samples": int(X_test.shape[0]),
        "total_samples": int(df.shape[0]),
        "total_features": int(len(feature_names)),
        "class_distribution": {
            "not_fraud": int((y == 0).sum()),
            "fraud": int((y == 1).sum())
        }
    }
    
    with open(META_OUT_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved model metadata to: {META_OUT_PATH}")


def train_regression_task3():
    print("Running Task 3 Linear Regression and Gradient Descent...")
    if not os.path.exists(TASK3_DATA_PATH):
        print("Task 3 data not found at", TASK3_DATA_PATH)
        return
        
    df = pd.read_csv(TASK3_DATA_PATH)
    X = df[['Age']]
    y = df['Income']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Part A: Sklearn
    model = LinearRegression()
    model.fit(X_train, y_train)
    sklearn_slope = float(model.coef_[0])
    sklearn_intercept = float(model.intercept_)
    sklearn_r2 = float(model.score(X_test, y_test))
    
    # Predict for Age 30
    pred_30_sklearn = float(model.predict(pd.DataFrame({'Age': [30]}))[0])
    
    # Part B: Gradient Descent from Scratch
    X_tr = X_train.values.flatten().astype(float)
    y_tr = y_train.values.astype(float)
    X_te = X_test.values.flatten().astype(float)
    y_te = y_test.values.astype(float)
    
    n = len(X_tr)
    m = 0.0
    c = 0.0
    lr = 0.0001
    epochs = 20000
    
    loss_history = []
    for _ in range(epochs):
        y_pred = m * X_tr + c
        error = y_pred - y_tr
        m_grad = (2 / n) * np.sum(error * X_tr)
        c_grad = (2 / n) * np.sum(error)
        m = m - lr * m_grad
        c = c - lr * c_grad
        
    y_pred_te = m * X_te + c
    gd_mse = float(np.mean((y_te - y_pred_te) ** 2))
    pred_30_gd = float(m * 30 + c)
    
    reg_meta = {
        "dataset_shape": list(df.shape),
        "sklearn": {
            "slope": round(sklearn_slope, 4),
            "intercept": round(sklearn_intercept, 4),
            "r2_score": round(sklearn_r2, 4),
            "predicted_income_age_30": round(pred_30_sklearn, 2)
        },
        "gradient_descent": {
            "slope": round(m, 4),
            "intercept": round(c, 4),
            "mse": round(gd_mse, 4),
            "predicted_income_age_30": round(pred_30_gd, 2),
            "epochs": epochs,
            "learning_rate": lr
        }
    }
    
    with open(REG_OUT_PATH, "w") as f:
        json.dump(reg_meta, f, indent=2)
    print(f"Saved Task 3 regression metadata to: {REG_OUT_PATH}")


def generate_eda_metadata():
    print("Generating Task 1 EDA metadata...")
    if not os.path.exists(RAW_DATA_PATH):
        return
    df = pd.read_csv(RAW_DATA_PATH)
    
    stats = {}
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols[:10]:
        stats[col] = {
            "mean": round(float(df[col].mean()), 2),
            "std": round(float(df[col].std()), 2),
            "min": round(float(df[col].min()), 2),
            "max": round(float(df[col].max()), 2)
        }
        
    eda_meta = {
        "total_records": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "missing_values": {k: int(v) for k, v in df.isnull().sum().items() if v > 0},
        "summary_statistics": stats,
        "fraud_distribution": {str(k): int(v) for k, v in df['fraud reported'].value_counts().items()} if 'fraud reported' in df.columns else {}
    }
    
    with open(EDA_OUT_PATH, "w") as f:
        json.dump(eda_meta, f, indent=2)
    print(f"Saved Task 1 EDA metadata to: {EDA_OUT_PATH}")


if __name__ == "__main__":
    train_classification_model()
    train_regression_task3()
    generate_eda_metadata()
    print("All ML training and metadata generation tasks completed successfully!")
