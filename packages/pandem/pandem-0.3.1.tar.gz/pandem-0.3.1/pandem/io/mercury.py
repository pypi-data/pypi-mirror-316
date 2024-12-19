import numpy
import csv
import pandem.io.utils as utils

metadata_fields = ["N", "Time", "XMin", "YMin", "ZMin", "XMax", "YMax", "ZMax"]
data_fields = ["x", "y", "z", "vx", "vy", "vz", "radius", "q1", "q2", "q3", "ox", "oy", "oz", "species"]


def load(filename):
    # First line: N, Time, XMin, YMin, ZMin, XMax, YMax, ZMax
    # Np lines: x, y, z, vx, vy, vz, rad, q1, q2, q3, ox, oy, oz, species
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=" ")
        nparticles = 0
        frame = 0
        line_count = sum(1 for row in reader)

        f.seek(0)
        for i, row in enumerate(reader):
            if i == 0:
                nparticles = int(row[0])
                nframes = line_count // (nparticles + 1)
                metadata = [
                    {
                        "N": int(row[0]),
                        "Time": float(row[1]),
                        "XMin": float(row[2]),
                        "YMin": float(row[3]),
                        "ZMin": float(row[4]),
                        "XMax": float(row[5]),
                        "YMax": float(row[6]),
                        "ZMax": float(row[7]),
                    }
                ]
                data = numpy.zeros((nframes, nparticles, 14))
            elif i % (nparticles + 1) == 0:
                frame += 1
                metadata.append(
                    {
                        "N": int(row[0]),
                        "Time": float(row[1]),
                        "XMin": float(row[2]),
                        "YMin": float(row[3]),
                        "ZMin": float(row[4]),
                        "XMax": float(row[5]),
                        "YMax": float(row[6]),
                        "ZMax": float(row[7]),
                    }
                )
            else:
                particle = i % (nparticles + 1) - 1
                data[frame, particle, :] = [float(x) for x in row]

    return data, data_fields, metadata


def save(data, headers, metadata, filename):
    with open(filename, "w") as f:
        data = utils.get_correct_data(data, headers, data_fields)

        for i in range(data.shape[0]):
            frame = data[i]
            metadata[i] = utils.get_correct_metadata(metadata[i], metadata_fields)

            f.write(
                f"{metadata[i]['N']} {metadata[i]['Time']} {metadata[i]['XMin']} {metadata[i]['YMin']} {metadata[i]['ZMin']} {metadata[i]['XMax']} {metadata[i]['YMax']} {metadata[i]['ZMax']}\n"
            )
            for particle in frame:
                f.write(
                    f"{particle[0]} {particle[1]} {particle[2]} {particle[3]} {particle[4]} {particle[5]} {particle[6]} {particle[7]} {particle[8]} {particle[9]} {particle[10]} {particle[11]} {particle[12]} {particle[13]}\n"
                )


if __name__ == "__main__":
    import sys

    data, metadata = load(sys.argv[1])
    save(data, metadata, sys.argv[2])
