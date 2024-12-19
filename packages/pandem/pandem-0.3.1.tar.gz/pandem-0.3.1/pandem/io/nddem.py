import numpy
import pandem.io.utils as utils

data_fields = ["x", "y", "z", "radius", "PBCFlags", "Vmag", "Omegamag"]
metadata_fields = []


def load(filename):
    # NDDEM uses a single csv file for each frame
    # First line: x0,x1,x2,R,PBCFlags,Vmag,Omegamag

    data = numpy.loadtxt(filename, delimiter=",", skiprows=1)
    data = numpy.expand_dims(data, axis=0)
    metadata = [{"N": len(data)}]

    return data, data_fields, metadata


def save(data, headers, metadata, filename):
    filename = filename.rstrip(".csv")
    data = utils.get_correct_data(data, headers, data_fields)
    print(data.shape)

    for i in range(data.shape[0]):
        frame = data[i]

        numpy.savetxt(
            f"{filename}_{i:06d}.csv",
            frame,
            delimiter=",",
            header="x0,x1,x2,R,PBCFlags,Vmag,Omegamag",
            comments="",
        )


if __name__ == "__main__":
    import sys

    data, metadata = load(sys.argv[1])
    save(data, metadata, sys.argv[2])
