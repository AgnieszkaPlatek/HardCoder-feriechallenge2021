"""
Napisz program, który w wybranej lokalizacji odczyta wszystkie pliki graficzne (w określonych formatach,
np. jpg, png, bmp itp.), następnie zmniejszy ich rozdzielczość o 50% i zapisze je w podkatalogu “smaller”
z odpowiednimi nazwami. Wykorzystaj pillow lub inną bibliotekę do pracy z obrazami.
Propozycja rozszerzenia: Oblicz ile miejsca na dysku można oszczędzić po kompresji (odczytaj rozmiar plików
w pierwotnym folderze oraz "smaller" i porównaj obie wartości - bezwzględnie i w %)
"""

import os

from PIL import Image


def resize_images(dir_path, perc):
    """
    Finds image files and reduces their size by given percent, saving in new 'smaller' subdirectory.
    :param dir_path: string path to directory with images
    :param perc: percent of reducing resolution
    :return: None
    """
    dir_size = 0
    new_dir_size = 0
    sm_path = os.path.join(dir_path, 'smaller')
    os.makedirs(sm_path, exist_ok=True)
    for filename in os.listdir(dir_path):
        if os.path.splitext(filename)[1] in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            file_path = os.path.join(dir_path, filename)
            try:
                with Image.open(file_path) as im:
                    dir_size += os.path.getsize(file_path)/1024
                    width, height = im.size
                    im.thumbnail((int(width * perc / 100), int(height * perc / 100)))
                    filename = filename.partition('.')[0] + '_sm.' + filename.partition('.')[2]
                    new_path = os.path.join(sm_path, filename)
                    im.save(new_path, 'JPEG')
                    new_dir_size += os.path.getsize(new_path)/1024
            except OSError:
                pass

    saved = dir_size - new_dir_size
    print('The images have been resized.')
    print(f'You saved {saved:.2f} KB, which is {saved/dir_size*100:.2f}%. Well done!')


def main():
    dir_path = 'Absolute path to your directory with images'
    percent = 50  # Change it if you wish
    resize_images(dir_path, percent)


if __name__ == "__main__":
    main()
