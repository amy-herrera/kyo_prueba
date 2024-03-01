"""Calculate subLuts for checking..."""

import numpy as np


def hex_to_binary(type, file):
    """Extract the numbers...."""
    # Read hexadecimal numbers from the file and store them in hex_numbers
    hex_numbers = read_hex_numbers_from_file(type, file)

    if type == "PQ":
        max_length = max(len(hex_number) -
                         (2 if hex_number.startswith('0x') else 0)
                         for hex_number in hex_numbers)
        # Pad each hexadecimal number with zeros to have the same length
        padded_hex_numbers = [
            hex_number.ljust(
                max_length + 2,
                '0') for hex_number in hex_numbers]
        # Convert each padded hexadecimal number to binary
        binary_numbers = [format(int(hex_number, 16),
                                 '0' + str(max_length * 4) + 'b')
                          for hex_number in padded_hex_numbers]
        return binary_numbers

    elif type == "MG":
        binary_numbers = []
        for hex_number in hex_numbers:
            # Get the maximum length needed for the binary
            total_length = len(hex_number) * 4
            # Convert the hexadecimal number to binary and remove the '0b'
            # prefix
            binary_representation = bin(int(hex_number, 16))[
                2:].zfill(total_length)
            # Append the binary representation to the list
            binary_numbers.append(binary_representation)
        return binary_numbers


def read_hex_numbers_from_file(type, file):
    """Extract the numbers..."""
    hex_numbers = []
    with open(file, 'r') as file:
        if type == "PQ":
            # Find '0x' if file is "lut_hex"
            for line in file:
                hex_start = line.find('0x')
                if hex_start != -1:
                    hex_number = line[hex_start:].strip()
                    hex_numbers.append(hex_number)
        elif type == "MG":

            for line in file:
                colon_index = line.find(':')
                if colon_index != -1:
                    hex_number = line[colon_index + 1:].strip()
                    hex_numbers.append(hex_number)

    return hex_numbers


def divide_binary_number_into_decimal_values(binary_number):
    """Extract the numbers..."""
    # Divide the number into 7 bits groups
    groups_of_7_bits = [binary_number[i:i + 7]
                        for i in range(0, len(binary_number), 7)]
    # Reverse to have first group in index 0
    groups_of_7_bits.reverse()
    decimal_values = [int(group, 2) for group in groups_of_7_bits]
    return decimal_values


def process_values_c(type, file):
    """Extract the numbers..."""
    output = "output_"
    processed_lines = []
    if type == "PQ":
        with open(file, 'r') as filename:
            for line in filename:
                # Find first 'x'
                equal_sign_index = line.find('x')

                if equal_sign_index != -1:
                    # Get characters 'x'
                    characters = line[equal_sign_index + 1:]

                # Divide into 8 characters and add '0x'
                    grouped_values = ', '.join([
                        '0x' +
                        characters[i:i +
                                   8] if len(characters[i:i +
                                                        8]) == 8 else characters[i:i +
                                                                                 8]
                        for i in range(0, len(characters), 8)])

                # Check if there are groups of 8 characters to add a comma and
                # line break
                    if grouped_values:
                        processed_lines.append(grouped_values)

        # Write in Output file
        output_file = output + file
        with open(output_file, 'w') as output_file:
            output_file.writelines(processed_lines)

    if type == "MG":

        with open(file, 'r') as filename:
            lineas = filename.readlines()

        # Get only numbers and divide them into 7 characters groups
        numbers = []
        for linea in lineas:
            partes = linea.split(':')
            if len(partes) > 1:
                numbers.append(partes[1].strip().split()[
                               0])  # Get only hex number

        numeros_hex = ''.join(numbers)
        new_numbers = [numeros_hex[i:i + 7]
                       for i in range(0, len(numeros_hex), 7)]
        groups_of_7 = [f"0x{numero}" for numero in new_numbers]

        # Write in Output file
        output_file = output + file
        with open(output_file, 'w') as output:
            for i in range(0, len(groups_of_7), 6):
                for grupo in groups_of_7[i:i + 6]:
                    output.write(f"{grupo}, ")
                output.write('\n')


def columns_errors(array_new, var):
    """Extract the numbers..."""
    checkinvalid = 0
    valid_column = True
    for coor_x, array in enumerate(array_new):
        for coor_y, value in enumerate(array[:-1]):
            next_value = array[coor_y + 1]

            # Check if value greater than next_value
            if value > next_value:
                print(
                    f"Errors in coords: ({coor_x}, {coor_y}).")
                checkinvalid = checkinvalid + 1

            # Check if value is less-than coor x
            elif value < coor_x:
                print(
                    f"Errors in coords: ({coor_x}, {coor_y}).")
                checkinvalid = checkinvalid + 1

    if checkinvalid:
        print(f"***ERROR*** SubLUT{var} is invalid")
        valid_column = False

    last_column = array_new[-1]  # Get last column

    # Check every value in last column
    for value in last_column:
        if value != 127:
            print(
                f"Error in last column of SubLUT{var}: The value in column: {coor_x} is not 127.")
            checkinvalid = checkinvalid + 1
            valid_column = False
    return valid_column


def rows_errors(matriz, var):
    """Extract the numbers..."""
    checkinvalid = 0
    valid_rows = True

    for coor_y, array in enumerate(matriz):
        for coor_x, value in enumerate(array[:-1]):
            next_value = array[coor_x + 1]
            if value > next_value:
                print(
                    f"Errors in coordinates: {coor_x}, {coor_y} in SubLUT{var}")
                checkinvalid = checkinvalid + 1
            elif value == next_value == 0:
                checkinvalid == checkinvalid + 1
                print(f"***ERROR*** SubLUT{var} is invalid. ")

    if checkinvalid:
        valid_rows = False
        print(f"***ERROR*** SubLUT_{var} is invalid")

    return valid_rows


def export_LUT(valid_array, num_LUTS):
    """Extract the numbers..."""
    check_exit = False

    while True:
        if check_exit:
            break

        var = int(
            input(f"Enter a value from 0 to {num_LUTS-1} for exporting: "))
        if var >= 0 and var < num_LUTS - 1:
            file_csv = f'SubLUT_{var}.csv'
            spaces_format = ' '.join(['%5d'] * valid_array[var].shape[1])
            # Save
            np.savetxt(file_csv, valid_array[var],
                       delimiter=' ', fmt=spaces_format)
            print("The formed SubLUT has been successfully exported to", file_csv)

        else:
            print("Enter a valid number between range).")

        while True:
            export = input(
                "Would you like to keep exporting SubLUTs? Enter y for yes or n for no: ").lower()
            if export == "y":
                break  # end this bucle to continue

            elif export == "n":
                check_exit = True
                print(f"The SubLUT{var} was not exported.")
                print("Exiting the program...")
                print(
                    "*****************************************************************")
                break


def Lut_creation(array, num_LUTS, type, file, remap, array_input):
    """Extract the numbers..."""
    checkLUT = 0
    valid_array = []

    for variable in range(num_LUTS):
        sub_array = array[variable]
        # Array for groups of 32 values
        groups_of_32 = []

        for i in range(0, len(sub_array), 32):
            group = sub_array[i:i + 32]  # Each group of 32 values
            groups_of_32.append(group)  # Add each group int groups_of_32 array

        # New array to check
        new_array = np.array(groups_of_32)
        # print(f"Checking valid columns SubLUT{variable}") enable this for
        # debbuging
        result_1 = columns_errors(new_array, variable)

        # Newarray from 32x128 to 128x32
        array_reverse = new_array.T
        # print(f"Checking valid rows SubLUT{variable}") enable this for
        # debbuging
        result_2 = rows_errors(array_reverse, variable)

        if result_1 and result_2:
            lut = array_reverse[::-1]
            # Valid LUT into valid_array
            valid_array.append(lut)
            checkLUT = checkLUT + 1

            if checkLUT == num_LUTS:
                process_values_c(type, file)
                print(f"Valid SubLUTs: {num_LUTS}")
                print()

                if type == "PQ":
                    if not array_input:
                        print(
                            "The input is invalid for Burst Absorption checking. Please enter a valid input...")
                    else:
                        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
                        print("Checking Burst Absorption...")
                        print()
                        burstAbsChecking(valid_array, remap, array_input)
                # else:
                    # export_LUT(valid_array, num_LUTS)


def array_creation(type, file, remap, array_input):
    """Extract the numbers..."""
    binary_numbers = hex_to_binary(type, file)

    # Array for 7 bits groups
    array_of_groups = []

    # Process each binary number
    for decimal_value in binary_numbers:
        # Divide each binary number into 7 bits groups to convert it decimal
        # value
        decimal_number = divide_binary_number_into_decimal_values(
            decimal_value)

        # Decimal values into the array
        for i, group in enumerate(decimal_number):
            if len(array_of_groups) <= i:
                array_of_groups.append([])
            array_of_groups[i].append(group)

    num_LUTS = len(array_of_groups)
    print("*****************************************************************")
    print(f"Number of SubLUTs for {file}:", num_LUTS)
    print()
    Lut_creation(array_of_groups, num_LUTS, type, file, remap, array_input)


def burstAbsChecking(valid_array, remap, array_input):
    """Extract the numbers..."""
    for array in array_input:
        print(array)
        var_BA = array[0]
        QG_limit = array[1]
        PQ_limit = array[2]

        remap_value = (PQ_limit / QG_limit) * 127
        remap_value = round(remap_value)
        print(f"Remap value for SubLUT{var_BA}: ", remap_value)
        converted_value = convert_remap(remap_value, remap)

        if converted_value is not None:
            print(
                f"Converted value of remap ({remap_value}): {converted_value}")
        else:
            print("Invalid remap value.")

        arrayBA = valid_array[var_BA]

        checkvalidBA = check_sequence(arrayBA, converted_value)

        if checkvalidBA:
            print(
                f"SubLUT{var_BA} meets the requirements of Burst Absorption.")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            print()

        elif checkvalidBA:
            print(
                f"SubLUT{var_BA} does not meet Burst Absorption requirements.")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            print()


def check_sequence(array, limit):
    """Extract the numbers..."""
    checkvalidBA = False
    if limit <= 0 or limit > len(array):
        return "Limit out of range"
    # Get upper limit
    upper_limit = len(array) - limit

    # Get new array from the upper limit
    sub_array = array[upper_limit:]

    # Checking each row
    for row in sub_array:
        # Check if the next value is greater
        if all(row[i] == i or (i == len(row) - 1 and row[i] == 127)
               for i in range(len(row))):
            checkvalidBA = True
        else:
            print("Invalid row: ", row)

    return checkvalidBA


def convert_remap(remap_value, remap):
    """Extract the numbers..."""
    remapped_values = []
    original_values = []

    with open(remap, 'r') as file:
        for line in file:
            if ':' in line:
                remapped, original = map(int, line.strip().split(':'))
                remapped_values.append(remapped)
                original_values.append(original)

    for j in range(len(original_values) - 1):
        actual_value = original_values[j]
        next_value = original_values[j + 1]

        if 0 <= remap_value <= original_values[0]:
            return remapped_values[0]

        elif actual_value < remap_value <= next_value:
            # print(actual_value)
            # print(next_value)
            return remapped_values[j + 1]
