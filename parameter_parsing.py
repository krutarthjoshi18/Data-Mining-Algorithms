"""
Author: Krutarth
        Ashwin
The file generates the temporary intermediate files that are then used as input in MS-Apriori Algorithm
Happy Programming
"""

import re
import csv


def generate_mis_scores(par_file):
    file = open(par_file, "r")
    f = open("mis_file.txt", "w")
    csv_write = csv.writer(f, lineterminator='')
    for line in file:
        if re.search("MIS", line):
            temp_key = re.findall(r'\(([^]]*)\)', line)
            temp_value = line.split("=")
            csv_write.writerow([int(temp_key[0]), float(temp_value[-1])])
            csv_write.writerow('\n')
        else:
            continue
    f.close()
    file.close()


def generate_sdc(par_file):
    file = open(par_file, "r")
    f = open("sdc_file.txt", "w")
    csv_write = csv.writer(f, lineterminator='')
    for line in file:
        if not re.search("SDC", line):
            continue
        else:
            sdc = line.split("=")[-1].strip()
            csv_write.writerow([float(sdc)])
            csv_write.writerow('\n')
            break
    f.close()
    file.close()


def generate_excluded_sets(par_file):
    file = open(par_file, "r")
    f = open("exclusion_list.txt", "w")
    csv_write = csv.writer(f, lineterminator='')
    for line in file:
        if not re.search("cannot_be_together", line):
            continue
        else:
            temp_set = line.split(":")[-1]
            temp_key = re.findall(r'\{([^{}]+)\}', temp_set)
    for line in temp_key:
        temp_list = line.split(",")
        exclusion_list = []
        for element in temp_list:
            exclusion_list.append(int(element))
        csv_write.writerow(exclusion_list)
        csv_write.writerow('\n')
    permute_exclusive_sets(temp_key)
    file.close()


def permute_exclusive_sets(element_list):
    f = open("pairwise_exclusion.txt", "w")
    csv_write = csv.writer(f, lineterminator='')
    for element in element_list:
        curr_list = element.split(",")
        for i in range(0, len(curr_list)):
            for j in range(i + 1, len(curr_list)):
                csv_write.writerow([int(curr_list[i]), int(curr_list[j])])
                csv_write.writerow('\n')
    f.close()


def generate_musthave_elements(par_file):
    file = open(par_file, "r")
    f = open("must_have.txt", "w")
    for line in file:
        if not re.search("must-have", line):
            continue
        else:
            elements = line.split(":")[-1].strip()
            nums = elements.split("or")
    for num in nums:
        f.write(num.strip())
        f.write("\n")
    f.close()
    file.close()


def main():
    parameter_file = "parameter-file_jordan.txt"
    generate_mis_scores(parameter_file)
    generate_sdc(parameter_file)
    generate_excluded_sets(parameter_file)
    generate_musthave_elements(parameter_file)


main()
