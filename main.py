import os
import hachoir_extractor as hs
import pdf_extractor as pd
import docx_extractor as docx
import exif_extractor as exif
import easygui

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
def convertResults(res,path):
    def pretty(l, d, indent=0):
        for key, value in d.items():
            l.append('\t' * indent + str(key).upper())
            if isinstance(value, dict):
                pretty(l, value, indent+1)
            else:
                l[-1] += ('\n' + ('\t' * (indent+1)) + str(value))
    l = [path]
    if res:
        pretty(l, res)
    else:
        l[-1]+='\n' + '\t' + 'Cannot Extract metadata for this file.'
    return '\n\n'.join(l)

while True:
    path = easygui.fileopenbox()
    if os.path.isdir(path):
        continue
    name, extension = os.path.splitext(path)
    extension = extension.lower()
    res = None
    if extension in current_office:
        res = docx.extract(path)
    elif extension == '.pdf':
        res = pd.extract(path)
    else:
        try:
            res = hs.extract(path)
        except Exception as err:
            try:
                res = exif.extract(path)
            except Exception as err_2:
                pass
    res = convertResults(res, path)
    easygui.msgbox( res, 'Results')
    option = easygui.ynbox('Do you want to extract the metadata for another file?', 'Continue?', ('Yes', 'No'))
    if option==0:
        break