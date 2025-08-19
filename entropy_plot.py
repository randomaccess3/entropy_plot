import argparse
import math
import os
import matplotlib.pyplot as plt
from progress.bar import Bar

# Default block size: 1MB
BLOCK_SIZE = 1024 * 1024

def parse_size(value: str) -> int:
    """Parse a size string with optional K/M/G suffix (B and iB accepted) into bytes."""
    s = value.strip().lower()
    multipliers = {
        'k': 1024,
        'm': 1024 ** 2,
        'g': 1024 ** 3,
    }

    # Try suffixes like kib/mb/gb, kb/mb/gb, k/m/g
    for key, mult in multipliers.items():
        for suf in (key + 'ib', key + 'b', key):
            if s.endswith(suf):
                num = s[:-len(suf)].strip()
                try:
                    return int(float(num) * mult)
                except ValueError:
                    raise argparse.ArgumentTypeError(f"Invalid size number: {value}")
    # No suffix => plain bytes
    try:
        return int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid size: {value}")

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

def process_file(file_path: str, block_size: int, max_bytes: int | None = None, show_progress: bool = True):
    """Read the file in blocks and compute entropy for each block up to max_bytes, showing a progress bar."""
    entropies = []
    file_size = os.path.getsize(file_path)
    total = min(file_size, max_bytes) if max_bytes is not None else file_size

    bar = None
    if show_progress and total > 0:
        # rate is steps/sec; since we step by bytes, it shows bytes/sec.
        bar = Bar(
            'Processing',
            max=total,
            suffix='%(percent).1f%% - %(index)d/%(max)d bytes - %(rate)s B/s - ETA %(eta)s'
        )

    try:
        with open(file_path, 'rb') as f:
            processed = 0
            while True:
                if processed >= total:
                    break
                to_read = min(block_size, total - processed)
                block = f.read(to_read)
                if not block:
                    break
                entropy = calculate_entropy(block)
                entropies.append(entropy)
                processed += len(block)
                if bar:
                    bar.next(len(block))
    finally:
        if bar:
            bar.finish()

    return entropies

# def process_file(file_path: str, block_size: int, max_bytes: int | None = None):
#     """Read the file in blocks and compute entropy for each block up to max_bytes."""
#     entropies = []
#     with open(file_path, 'rb') as f:
#         processed = 0
#         while True:
#             if max_bytes is not None:
#                 remaining = max_bytes - processed
#                 if remaining <= 0:
#                     break
#                 to_read = min(block_size, remaining)
#             else:
#                 to_read = block_size

#             block = f.read(to_read)
#             if not block:
#                 break

#             entropy = calculate_entropy(block)
#             entropies.append(entropy)
#             processed += len(block)
#     return entropies

def plot_entropy(entropies, block_size):
    """Plot entropy values as a line graph."""
    x = [i for i in range(len(entropies))]
    plt.figure(figsize=(12, 6))
    plt.plot(x, entropies, marker='o', linestyle='-', color='blue')
    # This title shows block size in MB if it's at least 1MB; otherwise just bytes.
    title_bs = f"{block_size // (1024 * 1024)}MB" if block_size % (1024 * 1024) == 0 and block_size >= 1024 * 1024 else f"{block_size} bytes"
    plt.title(f'Entropy per {title_bs} Block')
    plt.xlabel('Block Index')
    plt.ylabel('Entropy (bits)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot entropy of each block in a file.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('--block-size', type=parse_size, default=BLOCK_SIZE,
                        help='Block size to process  (e.g., 10M, 512K, 1G). Default: 1MB')
    parser.add_argument('--max-bytes', '-s', type=parse_size, default=None,
                        help='Maximum number of bytes to process (e.g., 10M, 512K, 1G). If omitted, process entire file.')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        return

    entropies = process_file(args.input_file, args.block_size, args.max_bytes)
    plot_entropy(entropies, args.block_size)

if __name__ == '__main__':
    main()