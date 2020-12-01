#!/usr/bin/python3

# text2magic.py
#
# Read a text file from standard input
# and write out the text as a array of magic cells.
#
# Paul Schulz <paul@mawsonlakes.org>
import getopt
import sys
import os.path
import pprint

# Options
options, remainder = getopt.getopt(sys.argv[1:],
                                   'c:v:h',
                                   ['cellname',
                                    'verbose',
                                    'help',
                                   ])

def usage():
    sys.stderr.write("text2magic.py <options>\n")
    sys.stderr.write("  Use as filter.\n")
    sys.stderr.write("  Text on stdin is converted to magic tcl on stdout\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Options:\n")
    sys.stderr.write("    [-c|--cellname] - Required. Cell name to use.\n")
    sys.stderr.write("    [-v|--verbose]  - Verbose output\n")
    sys.stderr.write("    [-h|--help]     - Display these details\n")

cellname = '-'
for opt, arg in options:
    if opt in ('-c', '--cellname'):
        cellname = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt in ('-h', '--help'):
        usage()
        exit()
    else:
        usage()
        exit()

if cellname == '-':
    usage()
    sys.stderr.write("\n")
    sys.stderr.write("*** cellname required\n")
    exit()

debug = 0
# Used to locate character data files
path = "libraries/sky130_pschulz_xx_hd/mag/"
# scale = 2

# Covert character id to cellname
# Accepts character UTF-8 encodings
def get_cellname (ch):
    """Return name of cell used to store character data"""

    prefix = "font_"

    if (ord(ch) < 0x100):
        cellname = "{:02X}".format(ord(ch))
    elif (ord(ch) < 0x10000):
        cellname = "{:04X}".format(ord(ch))
    elif (ord(ch) < 0x1000000):
        cellname = "{:06X}".format(ord(ch))
    else:
        cellname = "{:X}".format(ord(ch))

    return prefix+cellname

# Convert character id to filename
def get_filename(ch):
    filename = get_cellname(ch)+".mag"
    return filename

# Check that character data exists
def check_file_status (ch):
    """Check character has file"""

    # Handle whitespace
    if (ch == "\n" or ch == "\t"):
        ch = ' ';

    filename = get_filename(ch)
    if (os.path.isfile(path+filename)):
        result = 1
    else:
        result = 0

    return result

##############################################################################
# Read character data

def read_character_cell (character):
    """Read character details from file"""
    filename = get_filename(character)
    file1 = open(path+filename, 'r')
    Lines = file1.readlines()

    count = 0
    mode = "top"
    data = {}
    for line in Lines:
        line = line.strip()
        count = count+1
        linedata = line.split()

        if debug:
            print("Line{}: {}".format(count, line))

        if linedata[0] =="<<":
            if linedata[1] == "metal1":
                mode = "metal1"
            if linedata[1] == "properties":
                mode = "properties"
            if linedata[1] == "end":
                mode = "end"

        if mode == "top":
            if linedata[0] == "magic":
                data["filetype"] = "magic"
            elif linedata[0] == "tech":
                data["tech"] = linedata[1]
            elif linedata[0] == "timestamp":
                data["timestamp"] = linedata[1]

        if mode == "metal1":
            if linedata[0] == "rect":
                if "left" in data:
                    if int(linedata[1]) < data["left"]:
                        data["left"] = int(linedata[1])
                else:
                    data["left"] = int(linedata[1])

                if "right" in data:
                    if int(linedata[3]) > data["right"]:
                        data["right"] = int(linedata[3])
                else:
                    data["right"] = int(linedata[3])

                if "bottom" in data:
                    if int(linedata[2]) < data["bottom"]:
                        data["bottom"] = int(linedata[2])
                else:
                    data["bottom"] = int(linedata[2])

                if "top" in data:
                    if int(linedata[4]) < data["top"]:
                        data["top"] = int(linedata[4])
                else:
                    data["top"] = int(linedata[4])

        if mode == "properties":
           if linedata[0] == "string" and linedata[1] == "FIXED_BBOX":
               data["FIXED_BBOX"] = [linedata[2],linedata[3],linedata[4],linedata[5]]

    # Calculate bounding box size
    if "FIXED_BBOX" in data:
        data["bbox-width"]  = int(data["FIXED_BBOX"][2]) - int(data["FIXED_BBOX"][0])
        data["bbox-height"] = int(data["FIXED_BBOX"][3]) - int(data["FIXED_BBOX"][1])
    else:
        data["bbox-width"]  = data["right"] - data["left"]
        data["bbox-height"] = data["top"] - data["bottom"]

    # Calculate character skip
    # If bounding box present, use that (regular character with FIXED_BBOX)
    # otherwise use furthest paint (something without a bounding box)
    # else zero skip,
    if "FIXED_BBOX" in data:
        data["skip"] = int(data["FIXED_BBOX"][2])
    elif "right" in data:
        data["skip"] = data["right"]
    else:
        data["skip"] = 0
    data["skip"] = data["skip"]*2
    return data

def print_cell_data (data):
    """Display the cell data stored in 'data'"""
    print(data)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

def write_character (character,metrics):
    """Write a character, and use character metrics to move to cursor to next
character location.
    """
    print("# "+character)
    print("pushbox")
    print("getcell "+get_cellname(character)+" child 0 0")
    print("popbox")
    print("box move r "+str(metrics["skip"]))
    print()

def write_text (message):
    x = 0
    y = 0
    baselineskip = 400
    metrics = {}

    print("path .:libraries/sky130_pschulz_xx_hd/mag")
    print()
    print("select top cell")
    print("snap int")
    print("box position {} {}".format(x,y))
    print()

    for char in message:
        if char != "\n":
            if check_file_status(char):
                metrics[char] = read_character_cell(char)
            else:
                metrics[char] = read_character_cell("?")
            write_character(char,metrics[char])
        else:
            x = 0
            y = y - baselineskip
            print("box position {} {}".format(x,y))
            print()

    print("")
    print("gds write gds/{}.gds".format(cellname))
    print("quit")

##############################################################################
# Configuration
# print("path: ", path)

# Test
# font_status(characters)

# for a in text:
#    print('{:s} 0x{:02x}'.format(a,ord(a)))

# write_text("Test...!!?")
# f = open("demofile.txt", "r")
# print(f.read())

message = ""
for line in sys.stdin:
    message=message+line

write_text(message)
# print("Counted", len(message))
