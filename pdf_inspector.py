import argparse, csv, hashlib, os, re, shlex, shutil
from datetime import datetime
from functools import partial
from shutil import copyfile
from subprocess import Popen, PIPE

class BinaryPdfForensics:

    def __init__(self, 
                 file_path):
        """Inits class object with attributes"""
        self.file_path = file_path
        self.temp_path = '.tmp/temp.pdf'

    def pdf_magic(self):
        try:
            with open(self.file_path, 'rb') as raw_file:
                read_file = raw_file.read()
                magic_val = read_file[0:4].decode()
                pdf_version = read_file[1:8].decode()
                if magic_val == '%PDF':
                    return (True, pdf_version)
                else:
                    return (False, 'Non-PDF File')
        except UnicodeDecodeError:
            return (False, 'Non-PDF File')
        except IsADirectoryError:
            return (False, 'Directory')
        except FileNotFoundError:
            return (False, 'File Not Found') 

    def copy_file(self):
        if os.path.isfile(self.temp_path):
            os.remove(self.temp_path)
        if not os.path.isdir('.tmp/'):
            os.mkdir('.tmp/')
        # copy file into temporary directory
        copyfile(self.file_path, self.temp_path)
        # calculate return value
        if os.path.isfile(self.temp_path):
            return True
        else:
            return False

    def temp_clean(self):
        try:
            shutil.rmtree('.tmp/')
            return True
        except Exception:
            return False

    def get_info_ref(self):
        with open(self.temp_path, 'rb') as raw_file:
            read_file = raw_file.read()
            regex = b'[/]Info[\s0-9]*?R'
            pattern = re.compile(regex, re.DOTALL)
            info_ref = re.findall(pattern, read_file)
            info_ref = de_dupe_list(info_ref)
            if len(info_ref) == 0:
                info_ref_exists = False
            else:
                info_ref_exists = True
            return (info_ref_exists, info_ref)

    def get_xmp_ref(self):
        with open(self.temp_path, 'rb') as raw_file:
            read_file = raw_file.read()
            regex = b'[/]Metadata[\s0-9]*?R'
            pattern = re.compile(regex, re.DOTALL)
            xmp_ref = re.findall(pattern, read_file)
            xmp_ref = de_dupe_list(xmp_ref)
            if len(xmp_ref) == 0:
                xmp_ref_exists = False
            else:
                xmp_ref_exists = True
            return (xmp_ref_exists, xmp_ref)

    def get_info_obj(self):
        with open(self.temp_path, 'rb') as raw_file:
            read_file = raw_file.read()
            info_ref_tuple = BinaryPdfForensics.get_info_ref(self)
            info_obj_dict = {}
            for ref in info_ref_tuple[1]:
                info_ref = ref.decode()
                info_ref = info_ref.replace('/Info ', '') \
                                   .replace(' R', '')
                info_ref = str.encode(info_ref)
                regex = b'[^0-9]' + info_ref + b'[ ]obj.*?endobj'
                pattern = re.compile(regex, re.DOTALL)
                info_obj = re.findall(pattern, read_file)
                info_obj = de_dupe_list(info_obj)
                if len(info_obj) > 0:
                    for obj in info_obj:
                        info_obj_dict[ref] = obj
            if len(info_obj_dict) == 0:
                info_obj_exists = False
            else:
                info_obj_exists = True
            return (info_obj_exists, info_obj_dict)

    def get_xmp_obj(self):
        with open(self.temp_path, 'rb') as raw_file:
            read_file = raw_file.read()
            xmp_ref_tuple = BinaryPdfForensics.get_xmp_ref(self)
            xmp_obj_dict = {}
            for ref in xmp_ref_tuple[1]:
                xmp_ref = ref.decode()
                xmp_ref = xmp_ref.replace('/Metadata ', '') \
                                 .replace(' R', '')
                xmp_ref = str.encode(xmp_ref)
                regex = b'[^0-9]' + xmp_ref + b'[ ]obj.*?endobj'
                pattern = re.compile(regex, re.DOTALL)
                xmp_obj = re.findall(pattern, read_file)
                xmp_obj = de_dupe_list(xmp_obj)
                if len(xmp_obj) > 0:
                    for obj in xmp_obj:
                        xmp_obj_dict[ref] = obj
            if len(xmp_obj_dict) == 0:
                xmp_obj_exists = False
            else:
                xmp_obj_exists = True
            return (xmp_obj_exists, xmp_obj_dict)

    def file_stats(self):
        stats = os.stat(self.file_path)
        file_abspath = os.path.abspath(self.file_path)
        # calculate file size in bytes
        byte_size = stats[6]
        if byte_size < 1000:
            human_size = str(byte_size) + ' bytes'
        # calculate file size in KBs
        elif byte_size < 1000000:
            human_size = '{0} KB ({1} bytes)'.format(
                str(byte_size / 1000.0),
                str(byte_size)
                )
        # calculate file size in MBs
        elif byte_size < 1000000000:
            human_size = '{0} MB ({1} bytes)'.format(
                str(byte_size / 1000000.0),
                str(byte_size)
                )
        # calculate file size in GBs
        elif byte_size < 1000000000000:
            human_size = '{0} GB ({1} bytes)'.format(
                str(byte_size / 1000000000.0),
                str(byte_size)
                )
        # calculate file size in TBs
        elif byte_size < 1000000000000000:
            human_size = '{0} TB ({1} bytes)'.format(
                str(byte_size / 1000000000000.0),
                str(byte_size)
                )
        # calculate file access time
        atime = datetime.utcfromtimestamp(int(stats[7])). \
            strftime('%Y-%m-%d %H:%M:%S')
        # calculate file modification time
        mtime = datetime.utcfromtimestamp(int(stats[8])). \
            strftime('%Y-%m-%d %H:%M:%S')
        # calculate file change time
        ctime = datetime.utcfromtimestamp(int(stats[9])). \
            strftime('%Y-%m-%d %H:%M:%S')
        file_sys_meta = [
            file_abspath, 
            human_size,
            atime,
            mtime,
            ctime
            ]
        return file_sys_meta

    def file_hashes(self):
        with open(self.file_path, 'rb') as f:
            # initiate hashing algorithms
            d_md5 = hashlib.md5()
            d_sha1 = hashlib.sha1()
            d_sha224 = hashlib.sha224()
            d_sha256 = hashlib.sha256()
            d_sha384 = hashlib.sha384()
            d_sha512 = hashlib.sha512()
            # update hashing with partial byte stream buffer
            for buf in iter(partial(f.read, 128), b''):
                d_md5.update(buf)
                d_sha1.update(buf)
                d_sha224.update(buf)
                d_sha256.update(buf)
                d_sha384.update(buf)
                d_sha512.update(buf)
        # calculate digest for each hash
        md5_hash = d_md5.hexdigest()
        sha1_hash = d_sha1.hexdigest()
        sha224_hash = d_sha224.hexdigest()
        sha256_hash = d_sha256.hexdigest()
        sha384_hash = d_sha384.hexdigest()
        sha512_hash = d_sha512.hexdigest()
        # store hashes for return
        hash_list = [
            md5_hash, 
            sha1_hash, 
            sha224_hash,
            sha256_hash,
            sha384_hash,
            sha512_hash
            ]
        return hash_list

    def gen_report(self):
        # get file system metadata values
        file_sys_meta = BinaryPdfForensics.file_stats(self)
        hash_list = BinaryPdfForensics.file_hashes(self)
        version = BinaryPdfForensics.pdf_magic(self)
        # get encryption status
        crypt_ref = BinaryPdfForensics.get_crypt_ref(self)
        crypt_count = len(crypt_ref[1])

        info_ref = BinaryPdfForensics.get_info_ref(self)
        info_count = len(info_ref[1])
        info_obj = BinaryPdfForensics.get_info_obj(self)
        info_obj_count = len(info_obj[1])
        # get /Metadata references and objects
        xmp_ref = BinaryPdfForensics.get_xmp_ref(self)
        xmp_count = len(xmp_ref[1])
        xmp_obj = BinaryPdfForensics.get_xmp_obj(self)
        xmp_obj_count = len(xmp_obj[1])
        
        d = {
            file_sys_meta,
            hash_list,
            version,
            crypt_ref,
            crypt_count,
            info_count,
            info_ref,
            info_obj_count,
            str(xmp_count),
            str(xmp_obj_count)
        }
        for obj in info_obj[1]:
            d.add(binary_string(info_obj[1][obj]))

        for obj in xmp_obj[1]:
            d.add(binary_string(xmp_obj[1][obj]))


def de_dupe_list(list_var):
    new_list = []
    for element in list_var:
        if element not in new_list:
            new_list.append(element)
    return new_list

def binary_string(binary_obj):
    chr_list = []
    for byte in binary_obj:
        if byte not in [0]:
            try:
                chr_list.append(chr(byte))
            except Exception:
                pass
    chr_string = ''.join(chr_list) \
                   .strip() \
                   .replace('þÿ', '')
    clean_string = re.sub(
        r'xmpmeta>[\s]*<[?]xpacket',
        'xmpmeta>\n<?xpacket',
        chr_string
        )
    return clean_string

def clean_up_msg(clean_up):
    if clean_up is True:
        print("[+] Temporary directory removed: './tmp'\n")
    elif clean_up is False:
        print("[-] Temporary directory not removed: './tmp'\n")

def read_csv(input_file):
    csv_data = []
    try:
        with open(input_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, 
                                    delimiter=',', 
                                    quotechar='"')
            row_num = 0
            for row in csv_reader:
                row_length = len(row)
                if row_length == 3:
                    csv_check = True
                    row_num = row_num + 1
                    csv_data.append(row)
                elif row_length == 2:
                    csv_check = True
                    row_num = row_num + 1
                    row.append('')
                    csv_data.append(row)
                else:
                    csv_check = False
                    break
    except FileNotFoundError:
        print("[-] '{0}' cannot be found\n".format(input_file))
        raise SystemExit(3)
    except UnicodeDecodeError:
        print("[-] Error reading file, does not appear to be "
              "a CSV")
        raise SystemExit(6)
    if csv_check is False:
        print("[-] Error reading CSV, "
              "row {0} has {1} column(s)"
              .format(row_num, row_length))
        raise SystemExit(5)
    return (csv_check, csv_data)

def input_main(path):
    new_file = BinaryPdfForensics(path)

    # test for magic number in PDF file
    magic = new_file.pdf_magic()
    if magic[0] is True:
        print("[+] '{0}' is a valid file type: {1}". format(path, magic[1]))
    else: 
        raise SystemExit(3)

    # generate PDF metadata report
    new_file.gen_report()
    try:        
        new_file.gen_report()
        print('Report generated')
        clean_up = new_file.temp_clean()
        clean_up_msg(clean_up)
    except Exception as e:
        print("[-] Error generating report: {0}".format(str(e)))
        clean_up = new_file.temp_clean()
        clean_up_msg(clean_up)
        raise SystemExit(4)


def single_input(path):
    input_main(path)

def extract(path):
    single_input(path)