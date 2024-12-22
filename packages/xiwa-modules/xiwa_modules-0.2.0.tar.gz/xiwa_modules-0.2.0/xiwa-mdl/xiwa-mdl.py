import os
import subprocess
import importlib
import colorama
from colorama import Fore, Style, Back

requirements = [
    'b64', 'colorama', 'psutil', 'pillow', 'discord', 'beautifulsoup4',
    'gpt', 'browser-cookie3', 'bcrypt', 'phonenumbers', 'scapy', 'shodan',
    'requests', 'flask', 'paramiko', 'nmap', 'hashlib', 'cryptography',
    'pycryptodome', 'pyfiglet', 'pytest', 'pytest-xdist', 'selenium',
    'aiohttp', 'asyncio', 'sqlalchemy', 'sqlmap', 'openpyxl', 'tabulate',
    'pyftpdlib', 'pexpect', 'pyshark', 'socket', 'urllib3', 'jwt',
    'dnspython', 'pyOpenSSL', 'gevent', 'watchdog', 'progress', 'termcolor',
    'pyinstaller', 'pyzmq', 'click', 'ipaddress', 'logging', 'argparse',
    'pickle', 'subprocess', 'faker', 'yara', 'hashid', 'lz4', 'pyaes',
    'requests_toolbelt', 'httpx', 'websockets', 'h11', 'email-validator',
    'certifi', 'lxml', 'brotli', 'crypten', 'json5', 'pyjwt', 'mypy',
    'zlib', 'pyotp', 'whois', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'networkx', 'pyngrok', 'idna', 'scipy', 'sympy', 'nltk', 'spacy',
    'gensim', 'tensorflow', 'keras', 'torch', 'sklearn', 'opencv-python',
    'dlib', 'pytesseract', 'pymongo', 'redis', 'sqlparse', 'pyyaml',
    'jinja2', 'markupsafe', 'itsdangerous', 'werkzeug', 'gunicorn',
    'uvicorn', 'fastapi', 'starlette', 'pydantic', 'typer', 'rich',
    'loguru', 'tqdm', 'dataclasses', 'attrs', 'marshmallow', 'schematics',
    'pydot', 'graphviz', 'boto3', 'botocore', 's3transfer', 'fabric',
    'ansible', 'salt', 'celery', 'kombu', 'flower', 'rq', 'huey',
    'dramatiq', 'pytest-cov', 'coverage', 'hypothesis', 'tox', 'nox',
    'black', 'isort', 'flake8', 'pylint', 'bandit', 'safety', 'pipenv',
    'poetry', 'virtualenv', 'setuptools', 'wheel', 'twine', 'sphinx',
    'mkdocs', 'pdoc3', 'pygments', 'docutils', 'html5lib', 'bleach',
    'markdown', 'mistune', 'django', 'fastapi', 'bottle', 'cherrypy',
    'tornado', 'web2py', 'pyramid', 'falcon', 'hug', 'dash', 'plotly',
    'bokeh', 'altair', 'pygal', 'ggplot', 'geopandas', 'shapely', 'folium',
    'basemap', 'cartopy', 'imageio', 'scikit-image', 'pywavelets', 
    'pdfminer.six', 'reportlab', 'weasyprint', 'xhtml2pdf', 'fpdf',
    'pypdf2', 'pdfkit', 'docx', 'python-docx', 'xlrd', 'xlsxwriter',
    'pyxlsb', 'statsmodels', 'pymc3', 'theano', 'textblob', 'pattern',
    'pyspellchecker', 'langdetect', 'translate', 'goslate', 'deepl',
    'googletrans', 'speechrecognition', 'pyaudio', 'wave', 'soundfile',
    'librosa', 'audioread', 'pydub', 'pygame', 'pyglet', 'kivy',
    'tkinter', 'wxpython', 'pyqt5', 'pygtk', 'pygobject', 'pycairo',
    'pyopengl', 'pythreejs', 'vtk', 'mayavi', 'blender', 'povray',
    'manim', 'pybullet', 'gym', 'roboschool', 'pyrobot', 'ros',
    'pyserial', 'pyusb', 'pynput', 'keyboard', 'mouse', 'pyscreenshot',
    'pyautogui', 'pynput', 'pywinauto', 'pygetwindow', 'pyperclip',
    'clipboard', 'pystray', 'pywebview', 'eel', 'flaskwebgui',
    'pyqtwebengine', 'cefpython3', 'pywebio', 'streamlit', 'dash',
    'panel', 'voila', 'gradio', 'flask-socketio', 'socketio'
]

def install_and_import(modules):
    installed_modules = []
    for module in modules:
        try:
            importlib.import_module(module)
            installed_modules.append(module)
        except ImportError:
            subprocess.check_call([os.sys.executable, "-m", "pip", "install", module])
            installed_modules.append(module)
    return installed_modules

xiwa_modules = install_and_import(requirements)

imported_modules = {}
for module in xiwa_modules:
    imported_modules[module] = importlib.import_module(module)

blue = Fore.BLUE
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
cyan = Fore.CYAN
magenta = Fore.MAGENTA
white = Fore.WHITE
black = Fore.BLACK
reset = Fore.RESET

bg_blue = Back.BLUE
bg_red = Back.RED
bg_green = Back.GREEN
bg_yellow = Back.YELLOW
bg_cyan = Back.CYAN
bg_magenta = Back.MAGENTA
bg_white = Back.WHITE
bg_black = Back.BLACK
bg_reset = Back.RESET

bold = Style.BRIGHT
reset_style = Style.RESET_ALL

def print_success(message):
    print(f"{green}{bold}SUCCESS: {message}{reset_style}")

def print_error(message):
    print(f"{red}{bold}ERROR: {message}{reset_style}")

def print_info(message):
    print(f"{cyan}{bold}INFO: {message}{reset_style}")

def print_warning(message):
    print(f"{yellow}{bold}WARNING: {message}{reset_style}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_internet_connection():
    try:
        response = subprocess.check_output(["ping", "-c", "1", "google.com"])
        return True
    except subprocess.CalledProcessError:
        return False

def list_requirements():
    for req in requirements:
        print(f"{blue}{req}{reset}")

clear_console()
print_info("Initialisation des modules...")
list_requirements()
print_success("Modules initialisés avec succès!")