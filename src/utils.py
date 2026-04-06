from datetime import date

def hr(char="─", width=58):
    print(char * width)

def prompt_date(label, required=True):
    while True:
        val = input(f"  {label} (YYYY-MM-DD){'' if required else ' [Enter to skip]'}: ").strip()
        if not val and not required:
            return None
        try:
            return date.fromisoformat(val)
        except ValueError:
            print("    ✗ Invalid date. Use YYYY-MM-DD.")

def prompt_int(label, required=True):
    while True:
        val = input(f"  {label}: ").strip()
        if not val and not required:
            return None
        try:
            return int(val)
        except ValueError:
            print("    ✗ Please enter a valid number.")

def pause():
    input("\n  Press Enter to continue...")
