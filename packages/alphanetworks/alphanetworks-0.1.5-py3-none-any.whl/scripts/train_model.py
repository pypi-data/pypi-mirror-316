import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from alphanetworks import alphanet  # Import your model from the package
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import argparse  # Importing argparse for command-line argument parsing

def plot_training_history(history):
    epochs = range(1, len(history.history['accuracy']) + 1)
    train_acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(12, 5))

    # Plot Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_acc, label="Training Accuracy", marker='o')
    plt.plot(epochs, val_acc, label="Validation Accuracy", marker='o')
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()

    # Plot Loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_loss, label="Training Loss", marker='o')
    plt.plot(epochs, val_loss, label="Validation Loss", marker='o')
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()

    plt.tight_layout()
    plt.show()

def save_classification_report_and_confusion_matrix(model, val_generator, output_dir):
    # Get true labels and predictions
    y_true = val_generator.classes
    y_pred_probs = model.predict(val_generator)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # Classification report
    class_report = classification_report(y_true, y_pred, target_names=list(val_generator.class_indices.keys()))
    report_path = os.path.join(output_dir, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(class_report)
    print(f"Classification report saved to {report_path}")

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=val_generator.class_indices.keys(), yticklabels=val_generator.class_indices.keys())
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")

    # Save confusion matrix plot
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()
    print(f"Confusion matrix saved to {cm_path}")

def main():
    parser = argparse.ArgumentParser(description="Train AlphaNET model for image classification")
    parser.add_argument("--train", type=str, required=True, help="Path to the training dataset")
    parser.add_argument("--val", type=str, required=True, help="Path to the validation dataset")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for training and validation")
    parser.add_argument("--lr", type=float, default=1e-4, help="Initial learning rate for Adam optimizer")
    parser.add_argument("--output_dir", type=str, default="./", help="Directory to save model weights and reports")
    parser.add_argument("--nc", type=int, required=True, help="Number of target classes for classification")
    args = parser.parse_args()

    # Build the model with the specified number of classes
    model = alphanet(num_classes=args.nc)

    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=args.lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()

    # Data generators for training and validation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        args.train,
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=True
    )
    val_generator = val_datagen.flow_from_directory(
        args.val,
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=False
    )

    # Define callbacks
    early_stopping = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1)
    lr_reduction = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6, verbose=1)

    # Train the model
    history = model.fit(
        train_generator,
        epochs=args.epochs,
        validation_data=val_generator,
        callbacks=[early_stopping, lr_reduction],
        verbose=1
    )

    # Save model weights
    os.makedirs(args.output_dir, exist_ok=True)
    model.save(os.path.join(args.output_dir, "model_weights.keras"))
    print(f"Model weights saved to {os.path.join(args.output_dir, 'model_weights.keras')}")

    # Plot training and validation metrics
    plot_training_history(history)

    # Save classification report and confusion matrix
    save_classification_report_and_confusion_matrix(model, val_generator, args.output_dir)

if __name__ == "__main__":
    main()
