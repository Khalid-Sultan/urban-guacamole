import zipfile, xml.dom.minidom

def extract(path):
    def clean(item, data):
        item = item.strip()
        tag = ''
        value = ''
        last = 0
        for i in range(len(item)):
            if item[i]=='>' and tag=='':
                tag = item[4:i]
                last = i+1
            elif item[i]=='<' and tag!='':
                value = item[last:i]
                break
        data[tag] = value
    # Open the MS Office file to see the XML structure.
    document = zipfile.ZipFile(path)
    
    # Open/read the core.xml (contains the last user and modified date).
    uglyXML = xml.dom.minidom.parseString(document.read('docProps/core.xml')).toprettyxml(indent='  ')

    # Split lines in order to create a list.
    asText = uglyXML.splitlines()

    meta_data = {}
    # loop the list in order to get the value you need. In my case last Modified By and the date.
    for ind in range(2, len(asText)-1):
        item = asText[ind]
        clean(item, meta_data)
    return meta_data