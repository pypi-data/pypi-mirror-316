from constants import FieldNameMap


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
