import pandas as pd
from argparse import ArgumentParser

# read the processed file
RE_processed_df = pd.read_csv("D://Self Project//RE_processed_data.csv")

# creating a dictionary and RE_site (key) - RE_enzyme (value) pair
RE_dict = {}
for i in range(len(RE_processed_df.Enzymes)):
    RE_dict.setdefault(RE_processed_df.Recognition_Sequence[i], [])
    RE_dict[RE_processed_df.Recognition_Sequence[i]].append(RE_processed_df.Enzymes[i])


# creating a function which fetch the path of the sequence file and return the RE enzymes which site is present in the
# given sequences
def restriction_site_finder(path):
    with open(path) as file:
        header = None
        sequences = []  # single or multiple fasta sequences are append into this list in list of lists manner
        temp_sequence = ''
        for line in file.readlines():
            if line.startswith('>'):
                if header is not None:
                    sequences.append(temp_sequence)
                    temp_sequence = ''
                header = line.strip('\n')
            else:
                temp_sequence += line.strip('\n')
        sequences.append(temp_sequence)

    available_recognition_site = []
    for RE_site in RE_dict:
        if RE_site in sequences[0]:
            temp_tuple = f'Position:{sequences[0].index(RE_site)}, Cut site:{RE_site}, RE:{RE_dict.get(RE_site)}'
            available_recognition_site.append(temp_tuple)
    return '\n'.join(available_recognition_site)


print(restriction_site_finder("D://Self Project//test sequence.txt"))

# creating a CLI
parser = ArgumentParser(prog='Restriction Site Finder',
                        description='It helps to find the restriction site and the respective RE enzyme with '
                                    'specified position',
                        epilog='Thanks for using Restriction Site Finder tool')

parser.add_argument('test_seq', help='finding restriction site', type=str)
parser.add_argument('-v', '--verbose', help='description', action='store_true')

args = parser.parse_args()

if args.verbose:
    print(f'Restriction enzymes are {restriction_site_finder(args.test_seq)}')
else:
    print(restriction_site_finder(args.test_seq))
