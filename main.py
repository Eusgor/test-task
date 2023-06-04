from compare import compare
import argparse


def main():
    parser = argparse.ArgumentParser(description='Compare binary packages between two branches')
    parser.add_argument('branch1', help='First branch to compare')
    parser.add_argument('branch2', help='Second branch to compare')
    args = parser.parse_args()

    compare(args.branch1, args.branch2)


if __name__ == '__main__':
    main()
