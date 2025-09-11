def filtered_to_original_map(original_list):
    """
    Creates a mapping from indices of non-empty strings in the filtered list to their original positions.

    Given a list with potential empty strings, this function generates a dictionary where each key is an index (0-based)
    of a non-empty string in the filtered list, and the corresponding value is the original index (0-based) from the
    `original_list`.

    Args:
        original_list (list of str): The original list containing strings, which may include empty strings.

    Returns:
        tuple:
            dict: A dictionary where keys are indices of non-empty strings in the filtered list (0-based),
                  and values are the corresponding indices of these non-empty strings in the original list (0-based).
            int: The length of the original list.
    """
    filtered_to_original_map = {}
    for i, item in enumerate(original_list):
        if item != "":
            filtered_to_original_map[len(filtered_to_original_map)] = i
    return filtered_to_original_map, len(original_list)


def remap_indices(input_data, filtered_to_original_map, original_length):
    """
    Remaps the indices of input data to match the original list including empty strings.

    Args:
        input_data (list): List of dictionaries with 0-based indices relative to the filtered list.
        filtered_to_original_map (dict): Mapping of filtered indices to original indices.
        original_length (int): Length of the original list.

    Returns:
        list: List of dictionaries with updated indices and values corresponding to the original list.
    """
    # Initialize the output list with empty strings of the same length as the original list
    output_list = [{"index": i} for i in range(original_length)]

    # Update the output list using the mapping
    for item in input_data:
        filtered_index = item["index"]
        original_index = filtered_to_original_map[filtered_index]
        item["index"] = original_index
        output_list[original_index] = item

    # Convert the output list to the desired format
    return output_list
