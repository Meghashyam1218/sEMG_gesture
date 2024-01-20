import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import pandas as pd
import numpy as np


dataset = pd.read_csv("output.csv")
test = pd.read_csv("toutput.csv")
# Create a dataframe with only the features and target variable
X = dataset[
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
# X = dataset[
#     [

#         "STD DEV 1",
#         "STD DEV 2",
        
#     ]
# ]
y = dataset["Gesture"]
# Encode labels using LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# scaler = MinMaxScaler()
# X_train_normalized = scaler.fit_transform(X_train)
# X_test_normalized = scaler.transform(X_test)

# Define a simple neural network model using TensorFlow
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(
            64, activation="relu", input_shape=(X_train.shape[1],)
        ),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(len(np.unique(y_encoded)), activation="softmax"),
    ]
)

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

X_test = test[
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
# X_test = test[
#     [

#         "STD DEV 1",
#         "STD DEV 2",
        
#     ]
# ]
y_test = test["Gesture"]
y_encoded_test = label_encoder.fit_transform(y_test)
# X_test_normalized = scaler.fit_transform(X_test)
# y_test_normalized = scaler.transform(y_test)
# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_encoded_test)
print(f"Test Accuracy: {test_accuracy}")

# Save the TensorFlow Lite model
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()

# with open("model.tflite", "wb") as f:
#     f.write(tflite_model)
