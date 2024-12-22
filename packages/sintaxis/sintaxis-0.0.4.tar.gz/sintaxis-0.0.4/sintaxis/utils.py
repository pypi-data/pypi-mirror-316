import os
from typing import Literal
import subprocess
import shutil
import stat
import sys
import os
import urllib.error
import socketio
import importlib
import traceback
import json
import urllib.request
from typing import TypedDict
from sintaxis.challenges.python_functions.tests.clb3jv5hb0000z7m9v74n3u5u import test_task
from sintaxis.ascii import print_codigo_line, show_codigo_ascii
import io

sio = socketio.AsyncSimpleClient()
API_URL = 'http://localhost:5000'

tasks = {
    'clb3jv5hb0000z7m9v74n3u5u': {
        'test_function': test_task,
        'function_name': 'sum',
    },
}

def test_load_function():
    print(os.getcwd())
    print(os.path.abspath(os.path.join(os.getcwd(), '..')))
    print(sys.path)
    print(os.path.dirname(__file__))

def get_prints(func: callable) -> list[str]:
    buffer = io.StringIO()
    original_stdout = sys.stdout

    try:
        sys.stdout = buffer
        task_uuid, user_uuid, passed = func()
    finally:
        sys.stdout = original_stdout
        print(buffer.getvalue())
    
    return buffer.getvalue(), task_uuid, user_uuid, passed

def load_function(module_name: str, function_name):
    try:
        sys.path.append(os.path.abspath(os.getcwd()))
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        return func
    except Exception as e:
        print(f"No se pudo cargar la funcion: {e}")
        exit(1)

def get_challenge_user_uuid() -> tuple[str, str]:
    file_dir = os.path.join(os.getcwd(), '.svn', 'project_info', 'project.txt')

    with open(file_dir, 'r') as f:
        content = f.read()
        challenge_uuid = content.split('\n')[2]
        user_uuid = content.split('\n')[0]
        return challenge_uuid, user_uuid

def test():
    try:
        show_codigo_ascii()
        challenge_uuid, user_uuid = get_challenge_user_uuid()
        current_task = get_user_challenge_progress(challenge_uuid, user_uuid)
        task_uuid = current_task['uuid']

        test_function = tasks[task_uuid]['test_function']
        user_function = load_function('app', tasks[task_uuid]['function_name'])
        passed, total = test_function(user_function)
        
        print_codigo_line(f'Total: {total}')
        print_codigo_line(f'Passed: {passed}')
        print_codigo_line(f'Failed: {total - passed}')
        return task_uuid, user_uuid, passed == total

    except TypeError as e:
        print(f'Error: {e}')
        exit(1)
    except Exception as e:
        print(f'{e}')
        exit(1)

async def submit():
    try:
        stdout, task_uuid, user_uuid, passed = get_prints(test)
        await sio.connect(API_URL, transports=['websocket'])

        room = f'{task_uuid}/{user_uuid}'
        
        await sio.emit('test-stdout', {
            'room': room,
            'stdout': stdout,
            'passed': passed,
        })

        if passed == True:
            task_reponse = complete_task(task_uuid, user_uuid)
            
            if task_reponse == False:
                print_codigo_line('No se pudo actualizar challenge, intente nuevamente')
                exit(1)

    except Exception as e:
        print(f"Error submitting: {e}")
    finally:
        await sio.disconnect()

def create(project_type: Literal['python_functions'], user_uuid: str):
    if project_type not in ['python_functions']:
        print('Tipo de proyecto no especificado') 
        exit(1)

    if user_uuid == '':
        print('UUID del usuario no especificado')
        exit(1)

    show_codigo_ascii()
    handle_create_project(project_type, user_uuid)

def handle_create_project(challenge_uuid: str, user_uuid: str):
    project_root = os.path.join(challenge_uuid)
    app_file = os.path.join(project_root, 'app.py')
    current_dir = os.path.dirname(__file__)
    template_dir = os.path.join(current_dir, 'challenges', challenge_uuid, 'template.py')

    try:
        os.makedirs(project_root)

        with open(template_dir, 'r') as template_file:
            main_content = template_file.read()

        with open(app_file, 'w') as app_file:
            app_file.write(main_content)

        create_user_info_dir(challenge_uuid, user_uuid)

        current_task = get_user_challenge_progress(challenge_uuid, user_uuid)
        task_uuid = current_task['uuid']
        task_response = complete_task(task_uuid, user_uuid)

        if task_response == False:
            shutil.rmtree(project_root, onerror=handle_remove_readonly)
            print('No se pudo actualizar el estado del challenge')
            exit(1)
    
        print_codigo_line('Proyecto creado exitosamente\n')
        print_codigo_line('Para abrir el proyecto, ejecuta el siguiente comando:')
        print_codigo_line(f'  - cd {challenge_uuid}')
        print_codigo_line('  - python -m app\n')
    except Exception as e:
        print(f'Ha ocurrido un error al crear el proyecto: {e}')
        exit(1)

class CurrentTaskJson(TypedDict):
    id: int
    uuid: str
    name: str
    order: int
    step_id: int

def get_user_challenge_progress(challenge_uuid: str, user_uuid: str) -> CurrentTaskJson:
    try:
        url = f'{API_URL}/api/v1/challenges/{challenge_uuid}/{user_uuid}/progress'
        headers = {
            'Content-Type': 'application/json',
        }
        request = urllib.request.Request(
            url,
            headers=headers,
            method='GET'
        )
        with urllib.request.urlopen(request) as response:
            response_data = response.read().decode('utf-8')
        json_data = json.loads(response_data)
        return json_data.get('data')
    except urllib.error.HTTPError as e:
        print(f'Error al obtener el paso del reto: {e}')
        exit(1)
    except urllib.error.URLError as e:
        print(f'La ruta solicitada no existe: {e}')
        exit(1)
    except Exception as e:
        print(f'Error al obtener el paso del reto: {e}')
        exit(1)

def complete_task(task_uuid: str, user_uuid: str) -> bool:
    try:
        url = f'{API_URL}/api/v1/tasks/{task_uuid}/{user_uuid}/complete'
        headers = {
            'Content-Type': 'application/json'
        }
        request = urllib.request.Request(
            url,
            headers=headers,
            method='GET'
        )
        with urllib.request.urlopen(request) as response:
            status_code = response.status

        return status_code == 200
    except urllib.error.HTTPError as e:
        print(f'Error al completar la tarea: {e}')
        exit(1)
    except urllib.error.URLError as e:
        print(f'La ruta solicitada no existe: {e}')
        exit(1)
    except Exception as e:
        print(f'Error al completar la tarea: {e}')
        exit(1)

def create_user_info_dir(challenge_uuid: str, user_uuid: str):
    user_info_dir = os.path.join(challenge_uuid, '.svn', 'project_info')
    os.makedirs(user_info_dir)
    user_file_dir = os.path.join(user_info_dir, 'project.txt')

    with open(user_file_dir, 'w') as f:
        f.write(f'{user_uuid}\n{os.path.getmtime(os.getcwd())}\n{challenge_uuid}')

    subprocess.call(['attrib', '+h', user_info_dir])

def handle_remove_readonly(func: callable, path: str, exc: Exception) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)
        
def clone_repo(repo: str):
    try:
        result = subprocess.run(
            ['git', 'clone', repo],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        print('Repository cloned successfully')
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f'Error cloning repository: {e.stderr}')
        return
    except Exception as e:
        print(f'Error cloning repository: {e}')
        return


    git_dir = os.path.join('react-chat-app', '.git')
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, onerror=handle_remove_readonly)
    else:
        print('No .git directory found')

    user_info_dir = os.path.join('react-chat-app', '.user_info')
    os.mkdir(user_info_dir)
    user_id = 'nhb51h131o23401'
    with open(os.path.join(user_info_dir, 'user_id.txt'), 'w') as f:
        f.write(f'User: {user_id}\nDate: {os.path.getmtime(os.getcwd())}')
        
    subprocess.call(['attrib', '+h', user_info_dir])

def handle_error() -> str:
    pass