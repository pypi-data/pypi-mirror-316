import numpy


def load(filename):
    return None


def save(data, headers, metadata, filename):
    pass


if __name__ == "__main__":
    import sys

    data, metadata = load(sys.argv[1])
    save(data, metadata, sys.argv[2])
