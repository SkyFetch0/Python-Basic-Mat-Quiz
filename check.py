class Check:
    def __init__(self):
        self.required_libraries = {
            'tkinter': 'GUI için temel kütüphane',
            'random': 'Rastgele sayı üretimi için',
            'threading': 'Zamanlayıcı için',
            'json': 'JSON dosyası okuma için',
            'operator': 'Matematik operatörleri için',
            'math': 'Matematik fonksiyonları için'
        }
        self.missing_libraries = []
        self.installed_libraries = []

    def check_libraries(self):
        print("Kütüphane Kontrol Ediliyor...")
        print("-" * 50)

        for library, description in self.required_libraries.items():
            try:
                __import__(library)
                self.installed_libraries.append(f"✓ {library}: {description}")
            except ImportError:
                self.missing_libraries.append(f"✗ {library}: {description}")

        print("Yüklü Kütüphaneler:")
        for lib in self.installed_libraries:
            print(lib)

        if self.missing_libraries:
            print("\nEksik Kütüphaneler:")
            for lib in self.missing_libraries:
                print(lib)
            print("\nEksik kütüphaneleri yüklemek için:")
            for lib in self.missing_libraries:
                lib_name = lib.split(':')[0].replace('✗ ', '')
                print(f"pip install {lib_name}")
            return False
        else:
            print("\nTüm gerekli kütüphaneler yüklü!")
            return True