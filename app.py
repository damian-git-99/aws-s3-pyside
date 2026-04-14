# Layer 3 - Top layer, uses both
from base import PI
from processor import process_nothing

def main():
    result = process_nothing()
    print(f"Result: {result}")
    print(f"PI is still {PI}")

if __name__ == "__main__":
    main()
