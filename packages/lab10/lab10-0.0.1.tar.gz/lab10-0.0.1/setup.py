from setuptools import setup, find_packages
import sys
import subprocess
setup(
    name="lab10",
    version="0.0.1"
)

def main():
    print("Виберіть опцію:")
    print("1. Запустити основний код")
    print("2. Запустити всі тести")

    choice = input("Введіть ваш вибір (1/2): ")

    if choice == "1":
        subprocess.run([sys.executable, "lab10main/lab10.py"])
    elif choice == "2":
        subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"])
    else:
        print("Невірний вибір. Будь ласка, спробуйте ще раз.")
if __name__ == "__main__":
    main()
