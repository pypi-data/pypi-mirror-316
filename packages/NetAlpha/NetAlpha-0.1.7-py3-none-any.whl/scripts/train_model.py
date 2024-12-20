import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from netalpha import build_model  # Import your model from the package
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

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
    parser = argparse.ArgumentParser(description="AlphaNET Developed By Ihtesham Jahangir at Alpha Networks")
    parser.add_argument("--train_dir", type=str, required=True, help="Training directory path")
    parser.add_argument("--val_dir", type=str, required=True, help="Validation directory path")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    parser.add_argument("--initial_lr", type=float, default=1e-4, help="Initial learning rate")
    parser.add_argument("--output_dir", type=str, default="./", help="Output directory for saving model weights")
    parser.add_argument("--num_classes", type=int, required=True, help="Number of classes for the model")
    args = parser.parse_args()

    # Call to your model build function with the specified number of classes
    model = build_model(num_classes=args.num_classes)

    # Compile the model before training
    model.compile(
        optimizer=Adam(learning_rate=args.initial_lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()

    # Implement data generators with augmentation
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

    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        args.train_dir,
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=True
    )
    val_generator = val_datagen.flow_from_directory(
        args.val_dir,
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=False
    )

    # Callbacks for early stopping and learning rate reduction
    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    lr_reduction = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )

    # Training the model
    history = model.fit(
        train_generator,
        epochs=args.epochs,
        validation_data=val_generator,
        callbacks=[early_stopping, lr_reduction],
        verbose=1
    )

    # Save the trained model weights
    os.makedirs(args.output_dir, exist_ok=True)
    model.save(os.path.join(args.output_dir, "model_weights.keras"))
    print(f"Model weights saved to {os.path.join(args.output_dir, 'model_weights.keras')}")

    # Plot training history
    plot_training_history(history)

    # Save classification report and confusion matrix
    save_classification_report_and_confusion_matrix(model, val_generator, args.output_dir)

if __name__ == "__main__":
    main()
