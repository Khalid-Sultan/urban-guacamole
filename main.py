import os
import hachoir_extractor as hs
import pdf_extractor as pd
import docx_extractor as docx
import exif_extractor as exif
import easygui

hachoir_types = {
    ".bzip2", ".cab", ".gzip", ".mar", ".tar",".zip"
    ".mp3", ".wav", ".sun_next_audio", ".ogg", ".midi", ".aiff", ".aifc", ".ra",
    ".bmp", ".cur", ".emf", ".ico", ".gif", ".jpeg", ".jpg", ".pcx", ".png", ".tga", ".tiff", ".wmf", ".xcf",
    ".torrent",
    ".asf",
    ".wmv", ".avi", ".mkv", ".mov", ".ogg", ".theora", ".rm"
}
legacy_office = {
    ".doc", ".dot", ".wbk",
    ".xls", ".xlt", ".xlm",
    ".ppt", ".pot", ".pps",
    ".mdb", ".mde"
}
current_office = {
    ".docx", ".docm", ".dotx", ".dotm", ".docb",
    ".xlsx", ".xlsm", ".xltx", ".xltm",
    ".xlsb", ".xla", ".xlam", ".xll", ".xlw",
    ".pptx", ".pptm", ".potx", ".potm", ".ppam", ".ppsx", ".ppsm", ".sldx", ".sldm",
    ".accdb", "accde", "accdt", "accdr",
    ".one", ".pub", ".xps"
}

while True:
    path = easygui.fileopenbox()
    if os.path.isdir(path):
        continue
    name, extension = os.path.splitext(path)
    extension = extension.lower()
    print(name)
    if extension in current_office:
        print(docx.extract(path))
    elif extension == '.pdf':
        print(pd.extract(path))
    else:
        try:
            print(hs.extract(path))
        except Exception as err:
            try:
                print(exif.extract(path))
            except Exception as err_2:
                print('Cannot get metadata for ', path)
    