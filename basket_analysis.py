"""
Author: Krutarth
        Ashwin
This file generates all the data structures
Happy Programming
"""

import csv
import re
import parameter_parsing
from MS_Apriori import MSAprioriAlgo


def generate_mis_dict(file):
    mis_dict = {}
    for line in file:
        mis_dict[int(line[0])] = line[1]
    return mis_dict


def generate_exclusion_list(file):
    excluded_item_list = []
    for line in file:
        temp_list = line.split(",")
        excluded_item_list.append([int(x) for x in temp_list])
    return excluded_item_list


def generate_musthave_elements(file):
    musthave_list = []
    for line in file:
        musthave_list.append(int(line))
    return musthave_list


def generate_sdc(file):
    for line in file:
        sdc = float(line)
    return sdc


def generate_input(file):
    input_list = []
    for line in file:
        line = line.strip(" ")
        if not line == '\n':
            temp_list = re.findall(r'\{([^{}]+)\}', line)[0].split(",")
            item_list = [int(x) for x in temp_list]
            input_list.append(item_list)
    return input_list


def main():
    # ----------------------------------------------------------------
    # Generate all the temporary files for creation of data structures
    # ----------------------------------------------------------------
    parameter_parsing

    # -----------------------
    # Generate MIS Dictionary
    # -----------------------
    f_mis = open("mis_file.txt", "r")
    mis_file = csv.reader(f_mis)
    mis_dict = generate_mis_dict(mis_file)
    f_mis.close()

    # ------------------------------
    # Generate excluded itemset list
    # ------------------------------
    f_exclusion = open("exclusion_list.txt", "r")
    exclusion_list = generate_exclusion_list(f_exclusion)
    f_exclusion.close()

    # -------------------------------
    # Generate musthave elements list
    # -------------------------------
    f_musthave = open("must_have.txt")
    musthave_list = generate_musthave_elements(f_musthave)
    f_musthave.close()

    # ----------------
    # Generate SDC ~ Ø
    # ----------------
    f_sdc = open("sdc_file.txt", "r")
    sdc = generate_sdc(f_sdc)
    f_sdc.close()

    # -------------------
    # Generate input list
    # -------------------
    input_file = "input-dat-jordan.txt"
    f_input = open(input_file, "r")
    input_list = generate_input(f_input)
    f_input.close()

    # ----------------------------------------------------------------
    # MS Apriori Algorithm
    # ----------------------------------------------------------------
    MSAprioriAlgo(input_list, mis_dict, sdc, exclusion_list, musthave_list)


main()
