import os

# Constants
HIGH_ENTROPY_SIZE = 1 * 1024 * 1024  # 1MB
LOW_ENTROPY_SIZE = 5 * 1024 * 1024   # 5MB
OUTPUT_FILE = 'entropy_test_file.bin'

def generate_high_entropy_block(size):
    """Generate a block of random bytes (high entropy)."""
    return os.urandom(size)

def generate_low_entropy_block(size):
    """Generate a block of repeating bytes (low entropy)."""
    pattern = b'\xAA\x55'  # Simple 2-byte pattern
    return (pattern * (size // len(pattern)))[:size]

def create_entropy_test_file(filename):
    with open(filename, 'wb') as f:
        # First 1MB: High entropy
        f.write(generate_high_entropy_block(HIGH_ENTROPY_SIZE))
        # Next 5MB: Low entropy
        f.write(generate_low_entropy_block(LOW_ENTROPY_SIZE))
        # Last 1MB: High entropy
        f.write(generate_high_entropy_block(HIGH_ENTROPY_SIZE))
    print(f"File '{filename}' created with entropy pattern.")

if __name__ == '__main__':
    create_entropy_test_file(OUTPUT_FILE)
