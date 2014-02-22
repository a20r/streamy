
import streamy
import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        streamy.run("localhost", 8080)
    elif len(sys.argv) == 3:
        streamy.run(sys.argv[1], int(sys.argv[2]))
