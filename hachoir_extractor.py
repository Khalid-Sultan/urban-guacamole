from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from sys import argv, stderr, exit

def extract(path):
    parser = createParser(path)
    if path == None:
        print("usage: %s filename" % argv[0], file=stderr)
        return []
    if not parser:
        print("Unable to parse file", file=stderr)
        return []

    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            metadata = None
    if not metadata:
        print("Unable to extract metadata")
        return []
    return metadata.exportPlaintext()

