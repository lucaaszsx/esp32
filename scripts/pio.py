import sys

from lib.pio import find_project, pio_call


def main():
    sys.exit(pio_call(find_project(sys.argv[1]), sys.argv[2:]))

if __name__ == "__main__":
    main()
