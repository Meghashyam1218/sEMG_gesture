import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import pandas as pd
import numpy as np
from tensorflow import keras


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
    ]
]

y = dataset["Gesture"]
# Encode labels using LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)
# Model Architecture
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dropout(0.5),  # Add dropout layer to prevent overfitting
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(np.unique(y_encoded)), activation="softmax"),
    ]
)

# Compile the model with a different learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

# Increase the number of training epochs
model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test))


X_test = test[
    [
        "AVG POT VALUE 1",
        "AVG POT VALUE 2",
        "STD DEV 1",
        "STD DEV 2",
        "MAD 1",
        "MAD 2",
    ]
]

y_test = test["Gesture"]
y_encoded_test = label_encoder.fit_transform(y_test)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_encoded_test)
print(f"Test Accuracy: {test_accuracy}")

# Save the TensorFlow Lite model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("model_finetuned.tflite", "wb") as f:
    f.write(tflite_model)


converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]


# Define a representative dataset for quantization
def representative_data_gen():
    for input_value in (
        tf.data.Dataset.from_tensor_slices(X_train.values).batch(1).take(100)
    ):
        # Quantization requires a representative dataset for calibration
        yield [input_value]


converter.representative_dataset = representative_data_gen
# Ensure that if any ops can't be quantized, the converter throws an error
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
# Set the input and output tensors to uint8 (APIs added in r2.3)
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
tflite_model_quant = converter.convert()

with open("tflite_model.tflite", "wb") as f:
    f.write(tflite_model_quant)
