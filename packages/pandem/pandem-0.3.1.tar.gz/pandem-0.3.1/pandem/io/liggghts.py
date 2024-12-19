import csv
import numpy
from pandem.io import utils

metadata_fields = ["Timestep", "N", "XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax"]


def load(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=" ")
        data = []
        metadata = []
        for row in reader:
            if row == ["ITEM:", "TIMESTEP"]:
                timestep = int(next(reader)[0])
                metadata.append({})
                metadata[-1]["Timestep"] = timestep
            elif row == ["ITEM:", "NUMBER", "OF", "ATOMS"]:
                nparticles = int(next(reader)[0])
                metadata[-1]["N"] = nparticles
            elif row == ["ITEM:", "BOX", "BOUNDS", "pp", "pp", "pp"]:
                bounds = [next(reader) for _ in range(3)]
                metadata[-1].update(
                    {
                        "XMin": float(bounds[0][0]),
                        "XMax": float(bounds[0][1]),
                        "YMin": float(bounds[1][0]),
                        "YMax": float(bounds[1][1]),
                        "ZMin": float(bounds[2][0]),
                        "ZMax": float(bounds[2][1]),
                    }
                )
            elif row[:2] == ["ITEM:", "ATOMS"]:
                if row[-1] == "":
                    row = row[:-1]
                num_fields = len(row) - 2
                data_fields = row[2:]
                frame = numpy.zeros((nparticles, num_fields))
                for j in range(nparticles):
                    row = next(reader)
                    if row[-1] == "":
                        row = row[:-1]
                    frame[j] = [float(x) for x in row]
                data.append(frame)

    data = numpy.array(data)

    return data, data_fields, metadata


def save(data, headers, metadata, filename):
    with open(filename, "w") as f:
        for i, frame in enumerate(data):
            metadata[i] = utils.get_correct_metadata(metadata[i], metadata_fields)
            f.write("ITEM: TIMESTEP\n")
            f.write(f"{metadata[i]['Timestep']}\n")
            f.write("ITEM: NUMBER OF ATOMS\n")
            f.write(f"{metadata[i]['N']}\n")
            f.write("ITEM: BOX BOUNDS pp pp pp\n")
            f.write(
                f"{metadata[i]['XMin']} {metadata[i]['XMax']}\n"
                f"{metadata[i]['YMin']} {metadata[i]['YMax']}\n"
                f"{metadata[i]['ZMin']} {metadata[i]['ZMax']}\n"
            )
            f.write("ITEM: ATOMS ")
            f.write(" ".join(headers))
            f.write("\n")
            for particle in frame:
                f.write(" ".join(str(x) for x in particle))
                f.write("\n")


if __name__ == "__main__":
    import sys

    data, metadata = load(sys.argv[1])
    save(data, metadata, sys.argv[2])
