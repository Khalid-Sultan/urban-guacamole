import os
import hachoir_extractor as hs

path = input()
name, extension = os.path.splitext(path)
hachoir_types = {
    ".bzip2", ".cab", ".gzip", ".mar", ".tar",".zip"
    ".mp3", ".wav", ".sun_next_audio", ".ogg", ".midi", ".aiff", ".aifc", ".ra",
    ".bmp", ".cur", ".emf", ".ico", ".gif", ".jpeg", ".pcx", ".png", ".tga", ".tiff", ".wmf", ".xcf",
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
# if extension in hachoir_types:
print(hs.extract(path))
