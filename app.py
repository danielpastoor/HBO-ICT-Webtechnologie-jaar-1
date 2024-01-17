"""
When running the tool you can use the command line or press a button
to start the program. When using the command line use:
python3 app.py
There is also a profiler option. If you want to use it, input the following
in the command line:
python3 app.py --profile
"""

from src.main import run


def main():
    """
    Here the whole code for the website is ran.
    """
    run()


if __name__ == "__main__":
    main()
