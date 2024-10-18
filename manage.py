import argparse
from commands.createuser import create_user

def main():
    parser = argparse.ArgumentParser(description='Command management tool')

    subparsers = parser.add_subparsers(dest='command')

    # Command for run createuser
    createuser_parser = subparsers.add_parser('createuser', help='Create a regular user')

    args = parser.parse_args()

    if args.command == 'createuser':
        create_user()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
