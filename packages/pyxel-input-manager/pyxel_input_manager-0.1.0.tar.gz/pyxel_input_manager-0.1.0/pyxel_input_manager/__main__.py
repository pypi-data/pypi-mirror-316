import sys
from . import demo, demo_analog

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Available commands:")
        print("  demo    - Run the input manager demo")
        print("  demo_analog    - Run the analog input demo")
        return

    command = sys.argv[1]
    if command == "demo":
        demo.main()
    elif command == "demo_analog":
        demo_analog.main()
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        print("  demo    - Run the input manager demo")

if __name__ == "__main__":
    main()
