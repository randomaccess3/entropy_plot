import os
import random

# Configuration
BLOCK_SIZE = 1024 * 1024  # 1MB
TOTAL_BLOCKS = 20         # Total number of blocks in the file
SPIKE_INTERVAL = 5        # Every N blocks will be a high-entropy spike
OUTPUT_FILE = 'spiky_entropy_file.bin'

def generate_medium_entropy_block(size):
    """Generate a block with medium entropy using a biased random pattern."""
    # Use a limited set of bytes to reduce entropy slightly
    byte_pool = bytes([random.randint(0, 255) for _ in range(32)])
    return bytes(random.choice(byte_pool) for _ in range(size))

def generate_high_entropy_block(size):
    """Generate a block of pure random bytes (high entropy)."""
    return os.urandom(size)

def create_spiky_entropy_file(filename):
    with open(filename, 'wb') as f:
        for i in range(TOTAL_BLOCKS):
            if i % SPIKE_INTERVAL == 0:
                block = generate_high_entropy_block(BLOCK_SIZE)
                print(f"Block {i}: HIGH entropy")
            else:
                block = generate_medium_entropy_block(BLOCK_SIZE)
                print(f"Block {i}: medium entropy")
            f.write(block)
    print(f"\nFile '{filename}' created with periodic entropy spikes.")

if __name__ == '__main__':
    create_spiky_entropy_file(OUTPUT_FILE)
