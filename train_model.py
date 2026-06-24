import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Dataset Load
data = pd.read_csv("defects.csv")

# Input Features
X = data[['size', 'complexity', 'experience']]

# Output
y = data['defect']

# Model Create
model = DecisionTreeClassifier()

# Train Model
model.fit(X, y)

# Save Model
pickle.dump(model, open("model.pkl", "wb"))

print("Model Trained Successfully!")