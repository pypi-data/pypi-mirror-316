import sys
from sintaxis.utils import (
    test,
    submit,
    create,
)
import asyncio


def main():
    command = sys.argv[1]

    match command:
        case 'test':
            test()
        case 'submit':
            asyncio.run(submit())
        case 'create':
            if len(sys.argv) < 4:
                print('Uso: codigo create <project_type> <user_uuid>')
                exit(1)

            command = sys.argv[2]
            user_uuid = sys.argv[3]
            create(command, user_uuid)
        case _:
            print('Invalid command', end='')
            exit(1)  

if __name__ == '__main__':
    main()