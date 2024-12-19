import numpy

synonyms = [
    ["Timestep", "Time"],
    ["N", "NParticles"],
    ["ox", "omegax"],
    ["oy", "omegay"],
    ["oz", "omegaz"],
    ["R", "radius", "RadiusProjected"],
]



def get_correct_metadata(metadata, required_fields):
    """
    Updates the metadata dictionary by setting fields that are in fields_out but not in fields_in to NaN.

    Parameters:
    metadata (dict): The metadata dictionary to be updated.
    fields_in (list): A list of fields that are present.
    fields_out (list): A list of fields that should be checked and potentially set to NaN.

    Returns:
    dict: The updated metadata dictionary.
    """
    for field in required_fields:
        if field not in metadata:
            for syn in synonyms:
                if field in syn:
                    for s in syn:
                        if s in metadata:
                            metadata[field] = metadata[s]
                            break
        if field not in metadata:
            metadata[field] = numpy.nan

    return metadata


def get_correct_data(data, headers_in, headers_out):
    """
    Transforms the input data to match the specified output headers.

    Parameters:
    data (numpy.ndarray): The input data array with shape (n_samples, n_features, n_channels).
    headers_in (list of str): The list of headers corresponding to the channels in the input data.
    headers_out (list of str): The list of headers that the output data should conform to.

    Returns:
    numpy.ndarray: The transformed data array with shape (n_samples, n_features, len(headers_out)),
                   where each channel corresponds to the headers in headers_out. If a header in
                   headers_out is not found in headers_in, the corresponding channel in the output
                   data will be filled with NaNs.
    """
    data_out = numpy.nan*numpy.ones((data.shape[0], data.shape[1], len(headers_out)))
    for i, header in enumerate(headers_out):
        if header in headers_in:
            data_out[:, :, i] = data[:, :, headers_in.index(header)]
        else:
            for syn in synonyms:
                if header in syn:
                    for s in syn:
                        if s in headers_in:
                            data_out[:, :, i] = data[:, :, headers_in.index(s)]
                            break
    return data_out
