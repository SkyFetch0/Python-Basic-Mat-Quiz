import stat
import tkinter as tk
from quiz_app import MathQuizApp
from config import APP_SETTINGS
import requests
from colorama import Fore,Back,Style
import git
import shutil
import os
import sys
import gc
def check_libraries():
    required_libraries = {
        'tkinter': 'GUI için temel kütüphane',
        'random': 'Rastgele sayı üretimi için',
        'threading': 'Zamanlayıcı için',
        'json': 'JSON dosyası okuma için',
        'operator': 'Matematik operatörleri için',
        'math': 'Matematik fonksiyonları için',
        'requests': "Güncelleme Ve Get istekler için"
    }

    missing_libraries = []
    installed_libraries = []

    print(Fore.GREEN + "Kütüphane Kontrol Ediliyor...")
    print("-" * 50)

    for library, description in required_libraries.items():
        try:
            __import__(library)
            installed_libraries.append(f"✓ {library}: {description}")
        except ImportError:
            missing_libraries.append(f"✗ {library}: {description}")

    print("Yüklü Kütüphaneler:")
    for lib in installed_libraries:
        print(Fore.YELLOW + lib)

    if missing_libraries:
        print(Fore.RED+"\nEksik Kütüphaneler:")
        for lib in missing_libraries:
            print(lib)
        print("\nEksik kütüphaneleri yüklemek için:")
        for lib in missing_libraries:
            lib_name = lib.split(':')[0].replace('✗ ', '')
            print(f"pip install {lib_name}")
    else:

        print(Fore.GREEN + "\nTüm gerekli kütüphaneler yüklü!")
        return True

def remove_readonly(func, path, _):
    """Salt okunur özelliğini kaldır ve işlemi tekrar dene"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def safe_remove_directory(directory):
    """Güvenli bir şekilde dizini sil"""
    if os.path.exists(directory):
        shutil.rmtree(directory, onerror=remove_readonly)

def update_system():
    try:
        print(Fore.YELLOW + "Sistem Güncelleniyor..." + Fore.RESET)
        path = os.path.dirname(__file__) + "/"
        backup_folder = path + "backup/"
        update_folder = path + "update/"

        os.makedirs(backup_folder, exist_ok=True)

        for file in os.listdir(path):
            if file.endswith('.py'):
                shutil.copy2(os.path.join(path, file), backup_folder)

        safe_remove_directory(update_folder)
        os.makedirs(update_folder, exist_ok=True)

        repo_url = "https://github.com/SkyFetch0/Python-Basic-Mat-Quiz"
        repo = git.Repo.clone_from(repo_url, update_folder)
        print(f"Güncel Dosyalar indi konum: {update_folder}")

        for item in os.listdir(update_folder):
            source = os.path.join(update_folder, item)
            destination = os.path.join(path, item)
            if item == '.git':
                continue
                
            try:
                if os.path.isdir(source):
                    if os.path.exists(destination):
                        safe_remove_directory(destination)
                    shutil.copytree(source, destination)
                else:
                    if os.path.exists(destination):
                        os.remove(destination)
                    shutil.copy2(source, destination)
            except Exception as copy_error:
                print(f"Dosya kopyalama hatası ({item}): {str(copy_error)}")

        safe_remove_directory(update_folder)
        print(Fore.GREEN + "Başarıyla Güncelleme Yapıldı! Uygulama Yeniden Başlatılıyor!" + Fore.RESET)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except Exception as e:
        print(Fore.RED + f"Güncelleme sırasında hata oluştu: {str(e)}" + Fore.RESET)
        try:
            for file in os.listdir(backup_folder):
                backup_file = os.path.join(backup_folder, file)
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, path + file)
            print(Fore.YELLOW + "Yedekler geri yüklendi." + Fore.RESET)
        except Exception as restore_error:
            print(Fore.RED + f"Yedek geri yükleme hatası: {str(restore_error)}" + Fore.RESET)


def check_update():

    response = requests.get(APP_SETTINGS['UPDATE_SERVER'])
    data = response.json()
    version = data['version']
    if APP_SETTINGS['APP_VERSION'] != version and APP_SETTINGS['APP_VERSION'] < version:
        print(Fore.RED + "Versiyon Güncel Değil!")
        update_system()
    else:
        print(Fore.GREEN + "Versiyon Güncel!")

    print(Fore.RESET + "Versiyon: " + Fore.YELLOW+ str(APP_SETTINGS['APP_VERSION']) + Fore.RESET)



def main():
    check = check_libraries()
    check_update()


if __name__ == "__main__":
    main()