import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='file_sorter.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class FileSorter:
    def __init__(self):
        # Расширенный словарь для сопоставления расширений файлов с категориями
        self.extensions = {
            'documents': [
                '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.tex', '.md', '.epub', '.csv', '.xls', '.xlsx', '.ppt', '.pptx', 
                '.chm', '.xps', '.odp', '.ods', '.rtf', '.pages', '.odm', '.wpd', '.wps', '.html', '.epub', '.mobi', '.azw', '.azw3'
            ],
            'images': [
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico', '.raw', '.psd', '.ai', '.eps', '.webp', 
                '.heif', '.heic', '.indd', '.xcf', '.pdf', '.tga', '.ppm', '.dng', '.pgn', '.cmx', '.jpe', '.pbm', '.pgm', '.pcx'
            ],
            'videos': [
                '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.mpeg', '.3gp', '.m2ts', '.ogv', '.rm', '.rmvb', 
                '.vob', '.ts', '.swf', '.f4v', '.asf', '.divx', '.h264', '.xvid', '.mjpeg'
            ],
            'audio': [
                '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.aiff', '.alac', '.amr', '.midi', '.pcm', '.wma', 
                '.mka', '.webm', '.au', '.ape', '.dts', '.tta', '.sng', '.mid', '.vob', '.cue'
            ],
            'archives': [
                '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.tar.gz', '.tar.bz2', '.tar.xz', '.dmg', '.cab', '.pkg', 
                '.tar.lzma', '.tar.Z', '.lz', '.tgz', '.zpaq', '.ace', '.uue', '.xxe', '.bin', '.mdf', '.nrg', '.img'
            ],
            'code': [
                '.py', '.js', '.html', '.css', '.cpp', '.c', '.java', '.php', '.swift', '.go', '.rs', '.rb', '.ts', '.h', '.cs', 
                '.vb', '.pl', '.lua', '.m', '.scala', '.clj', '.r', '.sql', '.sh', '.bash', '.ps1', '.json', '.yml', '.yaml', '.xml', 
                '.ini', '.toml', '.asp', '.jsp', '.swift', '.perl', '.actionscript', '.typescript', '.vhdl', '.asm', '.vhd', '.matlab'
            ],
            'executables': [
                '.exe', '.msi', '.app', '.dmg', '.sh', '.bat', '.cmd', '.jar', '.deb', '.rpm', '.apk', '.bin', '.pkg', '.pl', '.wsf'
            ],
            'fonts': [
                '.ttf', '.otf', '.woff', '.woff2', '.eot', '.fnt', '.fon', '.bdf', '.pcf', '.svg', '.ttc', '.dfont', '.bitmap'
            ],
            'ebooks': [
                '.epub', '.mobi', '.azw', '.azw3', '.lit', '.pdb', '.cbz', '.cbr', '.fb2', '.pdf', '.djvu', '.epub3', '.ibooks', '.prc'
            ],
            'data': [
                '.json', '.xml', '.yaml', '.sql', '.db', '.sqlite', '.csv', '.tsv', '.parquet', '.avro', '.pickle', '.log', '.dat', 
                '.log', '.ini', '.yml', '.dbf', '.ods', '.db3', '.pdb', '.sqlite3', '.dbf', '.mdb', '.accdb', '.dat', '.bdb', '.txt'
            ],
            'designs': [
                '.ai', '.psd', '.xd', '.sketch', '.fig', '.pdf', '.eps', '.svg', '.cdr', '.indd', '.pub', '.afdesign', '.grd', '.pat', 
                '.brush', '.ai', '.bpg', '.luts', '.otl', '.3ds', '.blend', '.max', '.dwg', '.fbx', '.obj', '.stl', '.gltf', '.dae'
            ],
            '3d_models': [
                '.obj', '.stl', '.fbx', '.blend', '.dae', '.3ds', '.max', '.gltf', '.ply', '.skp', '.step', '.x3d', '.ifc', '.3mf', 
                '.acis', '.igs', '.gcode', '.xaml'
            ],
            'virtual_machines': [
                '.vdi', '.vmdk', '.ova', '.vhd', '.qcow2', '.img', '.vhdx', '.iso', '.raw', '.vmdk', '.bak', '.hdd'
            ],
            'scripts': [
                '.sh', '.bat', '.ps1', '.cmd', '.zsh', '.fish', '.ksh', '.bash', '.csh', '.tcsh', '.dash', '.tcsh', '.awk', '.sed', 
                '.perl', '.python', '.lua', '.ruby', '.bash_profile', '.bashrc', '.zprofile'
            ],
            'spreadsheets': [
                '.xls', '.xlsx', '.ods', '.csv', '.tsv', '.xlsm', '.xlsb', '.fods', '.sxc', '.dbf'
            ],
            'databases': [
                '.db', '.sqlite', '.mdb', '.accdb', '.sql', '.sqlite3', '.dbf', '.parquet', '.avro'
            ]
        }

    def sort_files(self, directory, sort_by='extension'):
        # Проверяем существование директории
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Директория {directory} не существует.")
        
        # Проходим по всем файлам в директории и подкаталогах
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_ext = os.path.splitext(filename)[1].lower()

                # Определяем категорию файла
                file_category = None
                for category, exts in self.extensions.items():
                    if file_ext in exts:
                        file_category = category
                        break
                
                if file_category is None:
                    file_category = 'other'

                # Логика сортировки по дате или размеру
                if sort_by == 'date':
                    file_category = f'{file_category}_{datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d")}'
                elif sort_by == 'size':
                    file_size = os.path.getsize(file_path)
                    size_category = 'small' if file_size < 100 * 1024 else 'large'  # Размеры: меньше 100KB - маленькие
                    file_category = f'{file_category}_{size_category}'
                
                # Создаем папку для категории, если она еще не существует
                category_path = os.path.join(directory, file_category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)

                # Перемещаем файл в соответствующую папку
                destination = os.path.join(category_path, filename)
                try:
                    shutil.move(file_path, destination)
                    logging.info(f"Перемещен файл {filename} в папку {file_category}")
                except Exception as e:
                    logging.error(f"Ошибка при перемещении файла {filename}: {str(e)}")
                    print(f"Ошибка при перемещении файла {filename}: {str(e)}")

        print("Сортировка файлов завершена.")
