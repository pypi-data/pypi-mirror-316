from .constants import FieldNameMap
import random

def rand_instance(n: int) -> str:
    digits = "0123456789"
    d2 = "123456789"  # d2 used for the first digit to avoid 0 at the start

    if n <= 1:
        return str(random.randint(0, 9))  # Return a single random digit

    # Generate the string with n characters
    result = [random.choice(digits) for _ in range(n)]

    # Ensure the first digit is from d2 (i.e., 1-9)
    result[0] = random.choice(d2)

    return ''.join(result)


def convert_data_keys(data):
    # Loop through each entry in the data
    converted_data = []

    for entry in data:
        # Convert each entry by renaming keys
        converted_entry = {}
        for key, value in entry.items():
            # Check if the key exists in the FieldNameMap
            if int(key) in FieldNameMap:
                # Map the key to the corresponding name
                converted_entry[FieldNameMap[int(key)]] = value
            else:
                # If no mapping exists, keep the original key
                converted_entry[int(key)] = value
        converted_data.append(converted_entry)

    return converted_data
