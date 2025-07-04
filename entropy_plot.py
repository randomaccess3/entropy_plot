import argparse
import math
import os
import matplotlib.pyplot as plt

# Default block size: 1MB
BLOCK_SIZE = 1024 * 1024

def calculate_entropy(data: bytes) -> float:
    """Calculate the Shannon entropy of a byte sequence."""
    if not data:
        return 0.0
    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1
    entropy = 0.0
    for count in byte_counts:
        if count == 0:
            continue
        p = count / len(data)
        entropy -= p * math.log2(p)
    return entropy

def process_file(file_path: str, block_size: int):
    """Read the file in blocks and compute entropy for each block."""
    entropies = []
    with open(file_path, 'rb') as f:
        block_index = 0
        while True:
            block = f.read(block_size)
            if not block:
                break
            entropy = calculate_entropy(block)
            entropies.append(entropy)
            block_index += 1
    return entropies

def plot_entropy(entropies, block_size):
    """Plot entropy values as a line graph."""
    x = [i for i in range(len(entropies))]
    plt.figure(figsize=(12, 6))
    plt.plot(x, entropies, marker='o', linestyle='-', color='blue')
    plt.title(f'Entropy per {block_size // (1024 * 1024)}MB Block')
    plt.xlabel('Block Index')
    plt.ylabel('Entropy (bits)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot entropy of each block in a file.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('--block-size', type=int, default=BLOCK_SIZE,
                        help='Block size in bytes (default: 1MB)')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        return

    entropies = process_file(args.input_file, args.block_size)
    plot_entropy(entropies, args.block_size)

if __name__ == '__main__':
    main()
