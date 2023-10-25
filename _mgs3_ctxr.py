import struct
import os
from array import array
import argparse

def process_ctxr_file(input_folder, filename):
    # Open the .ctxr file in binary mode for reading
    input_path = os.path.join(input_folder, filename)
    with open(input_path, 'rb') as ctxr_file:
        # Reading data from a .ctxr file
        data = ctxr_file.read()
        print("File name: "+filename)

        # Reading 2 bytes in Big Endian from offset 0x8
        value1 = struct.unpack('>h', data[0x8:0xA])[0]
        print("width: "+str(value1))

        # Reading 2 bytes into Big Endian from offset 0xA
        value2 = struct.unpack('>h', data[0xA:0xC])[0]
        print("height: "+str(value2))

        # Reading 4 bytes in Big Endian from offset 0x80
        value3 = struct.unpack('>i', data[0x80:0x84])[0]
        print("size: "+str(value3))

        # Read bytes after offset 0x80 in the amount specified in value3
        additional_data = data[0x84:0x84 + value3]

        # Create a byte array to record the DDS header
        #dds_header = array('B', [0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x0F, 0x10, 0x02, 0x00, 0x52, 0x00, 0x00, 0x00, 0x40, 0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        dds_header = array('B', [0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x0F, 0x10, 0x02, 0x00, 0x52, 0x00, 0x00, 0x00, 
                                 0x40, 0x01, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 
                                 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 
                                 0x00, 0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 
                                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        
        # Replace the twelfth byte in the DDS header with value2 in Signed Int format
        dds_header[12:16] = array('B', struct.pack('<i', value2))

        # Replace the sixteenth byte in the DDS header with value1 in Signed Int format
        dds_header[16:20] = array('B', struct.pack('<i', value1))

        # Create a new file with the extension .DDS and write data to it
        output_filename = os.path.splitext(filename)[0] + '.DDS'
        output_path = os.path.join(input_folder, output_filename)
        with open(output_path, 'wb') as dds_file:
            dds_file.write(dds_header)
            dds_file.write(additional_data)

def process_ctxr_files_in_directory(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".ctxr"):
                process_ctxr_file(root, filename)

def process_dds_file(input_folder, filename):
    # Открываем файл .ctxr в бинарном режиме для чтения
    input_path = os.path.join(input_folder, filename)
    with open(input_path, 'rb') as dds_file:
        # Читаем данные из .ctxr файла
        data = dds_file.read()
        print("File name: "+filename)

        # Reading 4 bytes in Little Endian from offset 0xC
        value1 = struct.unpack('<i', data[0xC:0x10])[0]
        print("width: "+str(value1))

        # Reading 4 bytes into Little Endian from offset 0x10
        value2 = struct.unpack('<i', data[0x10:0x14])[0]
        print("height: "+str(value2))

        # Read all bytes after offset 0x80
        additional_data = data[0x80:]

        output_filename = os.path.splitext(filename)[0] + '.ctxr'
        output_path = os.path.join(input_folder, output_filename)
        with open(output_path, 'rb+') as ctxr_file:
            #data = ctxr_file.read()
            #print("File name: "+output_filename)
            #header_data = data[0x0:84]
            ctxr_file.seek(132)
            ctxr_file.write(additional_data)
     

def process_dds_files_in_directory(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".DDS"):
                process_dds_file(root, filename)

def main():
    print("MGS 3 Export|Import ctxr textures by Giza(tr1ton)")
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", action="store_true", help="Process .ctxr files")
    parser.add_argument("-i", action="store_true", help="Process .dds files")
    parser.add_argument("folder", help="Folder containing .ctxr\.dds files")
    args = parser.parse_args()

    input_folder = args.folder
    if args.e:
        process_ctxr_files_in_directory(input_folder)
    elif args.i:
        process_dds_files_in_directory(input_folder)

if __name__ == '__main__':
    main()
