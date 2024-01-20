# prompt: Using dataframe dataset: create a model to identify the gesture by new iteration time series
#The imports cell
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

dataset = pd.read_csv('output2.csv')
test=pd.read_csv('toutput2.csv')
# Create a dataframe with only the features and target variable
features = dataset[
    [
        "AVG POT VALUE 1",
        "AVG POT VALUE 2",
        "STD DEV 1",
        "STD DEV 2",
        "MAD 1",
        "MAD 2",
        "DELTA AVG POT VALUE 1",
        "DELTA AVG POT VALUE 2",
        "DELTA STD DEV 1",
        "DELTA STD DEV 2",
        "DELTA MAD 1",
        "DELTA MAD 2",
    ]
]
target = dataset['Gesture']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.30)

# Create a Random Forest classifier
# model = RandomForestClassifier()
model = DecisionTreeClassifier(random_state=42)

# Train
# Train the model
model.fit(X_train, y_train)

X_test=test[
    [
        "AVG POT VALUE 1",
        "AVG POT VALUE 2",
        "STD DEV 1",
        "STD DEV 2",
        "MAD 1",
        "MAD 2",
        "DELTA AVG POT VALUE 1",
        "DELTA AVG POT VALUE 2",
        "DELTA STD DEV 1",
        "DELTA STD DEV 2",
        "DELTA MAD 1",
        "DELTA MAD 2",
    ]
]
y_test=test['Gesture']
# Make predictions
print(X_test)
predictions = model.predict(X_test)
print(predictions)
# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")