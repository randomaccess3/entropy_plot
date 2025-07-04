# Entropy Plot

This project analyses the entropy of a file in 1MB blocks and visualizes it using a line graph. It also includes tools to generate test files with varying entropy patterns.

## Features

- 📊 Plot entropy per block of any file
- 🧪 Generate test files with:
    - High/low entropy regions
    - Periodic entropy spikes

## Install

```bash
pip install -r requirements.txt
```

## Usage

### Generate test files

```bash
python generate_entropy_file.py
```

### Plot Entropy

```bash
python entropy_plot.py path/to/your/file.bin
```

```bash
python entropy_plot.py path/to/your/file.bin --block-size 524288
```