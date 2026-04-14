# Layer 3 - Uses formulas from layer2
from formulas import circle_area, falling_time

def main():
    r = 5
    area = circle_area(r)
    t = falling_time(100)
    print(f"Area of circle r={r}: {area}")
    print(f"Time to fall 100m: {t:.2f}s")

if __name__ == "__main__":
    main()
