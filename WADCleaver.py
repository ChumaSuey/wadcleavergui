import os
import argparse

"""
WADCleaver
    Chops up a WAD file into several WAD files based on texture names
    Run with -h for usage help
2023 nickster
nickster6660@hotmail.com
"""

__version__ = 1.0


UNKNOWN_TOKEN = 'unknown'

SHORT = 2
LONG = 4

DIR_ENTRY_LEN = 32
TEX_NAME_LEN = 16
WAD_HEADER_LEN = 12

HEADER_INDEX = 0
TCOUNT_INDEX = 4
DIRLOC_INDEX = 8

TEX_WSIZE_OFFS = 4
TEX_SIZE_OFFS = 8
TEX_IDENT_OFFS = 12
TEX_COMP_OFFS = 13
TEX_NAME_OFFS = 16


def ba_to_int(byte_arr):
    return int.from_bytes(byte_arr, byteorder='little')


def int_to_ba(num, bytes=LONG):
    return bytearray(num.to_bytes(bytes, byteorder='little'))


def ba_to_str(byte_arr):
    return str(byte_arr).split("'")[1].split('\\')[0]


def str_to_ba(string, padto=TEX_NAME_LEN):
    bval = bytearray()
    bval.extend(map(ord, string))
    while (len(bval) < padto):
        bval.extend(b'\x00')
    return bval


class Texture():
    def __init__(self, wad_data, dir_offs):
        self.Start = ba_to_int(wad_data[dir_offs:dir_offs+LONG])
        self.Name = ba_to_str(wad_data[dir_offs+TEX_NAME_OFFS:dir_offs+TEX_NAME_OFFS+TEX_NAME_LEN])
        self.Size = ba_to_int(wad_data[dir_offs+TEX_SIZE_OFFS:dir_offs+TEX_SIZE_OFFS+LONG])
        self.Wsize = ba_to_int(wad_data[dir_offs+TEX_WSIZE_OFFS:dir_offs+TEX_WSIZE_OFFS+LONG])
        self.Comp = wad_data[dir_offs+TEX_COMP_OFFS]
        self.Ident = wad_data[dir_offs+TEX_IDENT_OFFS]

        self.Data = wad_data[self.Start:self.Start+self.Wsize]

    def rename(self, new_name):
        self.Name = new_name
        #unfortunately the name is also stored in the texture data
        self.Data = str_to_ba(self.Name) + self.Data[TEX_NAME_LEN:len(self.Data)-1]

    def get_directory_bytes(self):
        data = bytearray()
        data += int_to_ba(self.Start)
        data += int_to_ba(self.Wsize)
        data += int_to_ba(self.Size)
        data += int_to_ba(self.Ident, bytes=1)
        data += int_to_ba(self.Comp, bytes=1)
        data += int_to_ba(0, bytes=SHORT)
        data += str_to_ba(self.Name)

        return data


class WadFile():
    def __init__(self, wad_path=None):
        self.Header = 'WAD2'
        self.TextureCount = 0
        self.DirOffset = 0

        self.Textures = []

        if wad_path:
            self._loadWadFile(wad_path)

    def _loadWadFile(self, wad_path):
        with open(wad_path, 'rb') as wad_file:
            wad_bytes = bytearray(wad_file.read())

            self.Header = ba_to_str(wad_bytes[HEADER_INDEX:HEADER_INDEX+LONG])
            self.TextureCount = ba_to_int(wad_bytes[TCOUNT_INDEX:TCOUNT_INDEX+LONG])
            self.DirOffset = ba_to_int(wad_bytes[DIRLOC_INDEX:DIRLOC_INDEX+LONG])

            wad_dir_bytes = wad_bytes[self.DirOffset:len(wad_bytes)-1]

            tind = 0
            while tind < len(wad_dir_bytes):
                newtex = Texture(wad_bytes, self.DirOffset+tind)
                self.add_texture(newtex)
                tind += DIR_ENTRY_LEN

    def _get_header_bytes(self):
        data = bytearray()
        data += str_to_ba(self.Header, padto=4)
        data += int_to_ba(self.TextureCount)
        data += int_to_ba(self.DirOffset)

        return data

    def _get_texturedata_bytes(self):
        data = bytearray()
        for t in self.Textures:
            t.Start = WAD_HEADER_LEN + len(data)
            data += t.Data

        self.DirOffset = WAD_HEADER_LEN + len(data)

        return data

    def _get_directory_bytes(self):
        data = bytearray()
        for t in self.Textures:
            data += t.get_directory_bytes()
            
        return data

    def add_texture(self, texture):
        self.Textures += [texture]
        self.TextureCount = len(self.Textures)

    def write_file(self, wad_path):
        wad_tdata = self._get_texturedata_bytes()
        wad_dir = self._get_directory_bytes()
        wad_header = self._get_header_bytes()

        with open(wad_path, 'wb') as wad_file:
            wad_file.write(wad_header + wad_tdata + wad_dir)


def main():
    parser = argparse.ArgumentParser(description='Chops up a WAD file into several WAD files based on texture names')
    parser.add_argument('input_wad', 
                        help='WAD file to read textures from')
    parser.add_argument('output_dir', 
                        help='Path to write the new chopped-up WAD files')
    parser.add_argument('--delim', default='_', 
                        help='Delimiter character string used to break up texture names (default _)')
    parser.add_argument('--token', type=int, default=-1, 
                        help='Token index to match on after the texture name is split up; use negative numbers to count from the right (default -1)')
    parser.add_argument('--skipshort', action='store_true', 
                        help='If the token is a single character, try to use the next token')
    args = parser.parse_args()

    print(f'Splitting {args.input_wad}...')

    input_wad = WadFile(args.input_wad)

    # group textures into dict by naming convention
    texture_groups = {}
    for t in input_wad.Textures:
        try:
            mytoken = t.Name.split(args.delim)[args.token]
            if args.skipshort and len(mytoken) == 1:
                mytoken = t.Name.split(args.delim)[args.token + (1 if args.token >= 0 else -1)]
        except IndexError:
            print(f'    Not enough tokens in {t.Name}, adding to group {UNKNOWN_TOKEN}')
            mytoken = UNKNOWN_TOKEN
        try:
            texture_groups[mytoken] += [t]
        except KeyError:
            texture_groups[mytoken] = [t]
        
        print(f'  Added {t.Name} to group {mytoken}')

    # prep output
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    wad_root_name = os.path.splitext(os.path.basename(args.input_wad))[0]

    print(f'Generating new WADs...')

    # build individual WADs and write to disk
    for group in texture_groups.keys():
        new_wad_path = os.path.join(args.output_dir, f'{wad_root_name}_{group}.wad')
        print(f'  Writing {new_wad_path}')

        new_wad = WadFile()

        for t in texture_groups[group]:
            new_wad.add_texture(t)

        new_wad.write_file(new_wad_path)

    print('Done.')


if __name__ == "__main__":
    main()