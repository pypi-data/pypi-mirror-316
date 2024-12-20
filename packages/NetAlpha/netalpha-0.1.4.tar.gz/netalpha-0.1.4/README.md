
# NetAlpha

[![PyPI Version](https://img.shields.io/pypi/v/netalpha.svg)](https://pypi.org/project/netalpha/)
[![Python Versions](https://img.shields.io/pypi/pyversions/netalpha.svg)](https://pypi.org/project/netalpha/)
[![License](https://img.shields.io/pypi/l/netalpha.svg)](https://github.com/ihtesham-jahangir/netalpha/blob/main/LICENSE)

**NetAlpha** is a Python package designed to train a multi-branch Convolutional Neural Network (CNN) model that integrates **ResNet50V2** and **DenseNet169** architectures for superior image classification tasks.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation via Pip](#installation-via-pip)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
    - [Basic Usage](#basic-usage)
    - [Options](#options)
    - [Help](#help)
  - [Examples](#examples)
  - [Data Preparation](#data-preparation)
- [Programmatic Usage](#programmatic-usage)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
  - [Reporting Issues](#reporting-issues)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## Introduction

**NetAlpha** offers a hybrid architecture combining the strengths of ResNet50V2 and DenseNet169 for high-performance image classification. By integrating these architectures, **NetAlpha** provides robust feature extraction and better generalization for diverse datasets.

---

## Features

- **Hybrid Architecture**: Combines ResNet50V2 and DenseNet169 for enhanced feature extraction.
- **Data Augmentation**: Advanced augmentation techniques to improve model robustness.
- **Early Stopping & Learning Rate Scheduling**: Built-in callbacks for better training control.
- **Command-Line Interface (CLI)**: Simplified training and configuration through CLI commands.
- **Customizable Hyperparameters**: Fine-tune learning rate, batch size, and more.
- **Training Visualization**: Plot training and validation metrics for better insights.

---

## Installation

### Prerequisites

- **Python**: Version 3.6 or higher.
- **TensorFlow**: Version 2.x or later.
- **pip**: Latest version recommended.

### Installation via Pip

Install **NetAlpha** directly from PyPI:

```bash
pip install netalpha
```

---

## Usage

### Command-Line Interface

Once installed, you can use the `netalpha_train` command.

#### Basic Usage

```bash
netalpha_train --train_dir PATH_TO_TRAIN_DIR --val_dir PATH_TO_VAL_DIR [OPTIONS]
```

#### Options

- `--train_dir`: **(Required)** Path to the training data directory.
- `--val_dir`: **(Required)** Path to the validation data directory.
- `--epochs`: Number of epochs (default: 50).
- `--batch_size`: Batch size (default: 8).
- `--initial_lr`: Initial learning rate (default: 1e-4).
- `--output_dir`: Directory to save model outputs (default: `./`).
- `--plot`: Add this flag to generate training plots.

#### Help

To see a detailed list of options, run:

```bash
netalpha_train --help
```

---

### Examples

#### Example 1: Basic Training

```bash
netalpha_train   --train_dir ./data/train   --val_dir ./data/val   --epochs 30   --batch_size 16
```

#### Example 2: Training with Custom Parameters

```bash
netalpha_train   --train_dir ./data/train   --val_dir ./data/val   --epochs 40   --batch_size 32   --initial_lr 5e-5   --output_dir ./outputs   --plot
```

---

### Data Preparation

Organize your dataset as follows:

```
dataset/
├── train/
│   ├── class1/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── class2/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
└── val/
    ├── class1/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── class2/
        ├── image1.jpg
        ├── image2.jpg
        └── ...
```

---

## Programmatic Usage

NetAlpha can also be used in Python scripts:

```python
from netalpha import build_model

# Build the model
model = build_model(input_shape=(224, 224, 3), num_classes=2)

# Compile the model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train or evaluate as needed
```

---

## Project Structure

```
netalpha/
├── netalpha/
│   ├── __init__.py
│   ├── model.py
│   └── utils.py
├── scripts/
│   └── train_model.py
├── setup.py
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Documentation

For detailed documentation, visit the [GitHub repository](https://github.com/ihtesham-jahangir/netalpha).

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/netalpha.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```
4. Commit your changes:
   ```bash
   git commit -am "Add new feature"
   ```
5. Push the branch:
   ```bash
   git push origin feature/new-feature
   ```
6. Open a pull request.

### Reporting Issues

If you encounter any issues, please [open an issue](https://github.com/yourusername/netalpha/issues).

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Contact

- **Author**: Ihtesham Jahangir
- **Email**: [ihteshamjahangir21@gmail.com](mailto:ihteshamjahangir21@gmail.com)
- **GitHub**: [ihtesham-jahangir](https://github.com/ihtesham-jahangir)

---

## Acknowledgments

- **TensorFlow and Keras Teams**: For their excellent frameworks.
- **Researchers**: Behind ResNet and DenseNet architectures.
- **Open Source Community**: For fostering innovation and collaboration.

---

*This README provides detailed information about NetAlpha, making it easy for users to install, use, and contribute to the project.*
