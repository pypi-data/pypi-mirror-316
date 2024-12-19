from vtkmodules.vtkIOLegacy import vtkPolyDataReader, vtkPolyDataWriter
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonCore import vtkPoints, vtkFloatArray
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import numpy
import pandem.io.utils as utils

# data_fields = ["x", "y", "z", "radius", "PBCFlags", "Vmag", "Omegamag"]
# metadata_fields = []


def load(filename):
    # Create the reader for legacy VTK files
    reader = vtkPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()

    # Get the output as vtkPolyData
    polydata = reader.GetOutput()

    # Access point information
    points = vtk_to_numpy(polydata.GetPoints().GetData())
    scalars = vtk_to_numpy(polydata.GetPointData().GetScalars())
    data = numpy.hstack([points, scalars[:, None]])
    data = numpy.expand_dims(data, axis=0)

    scalars = polydata.GetPointData().GetScalars()
    scalar_name = scalars.GetName()
    
    data_fields = ["x", "y", "z", scalar_name]
    metadata = [{"N": len(data)}]

    return data, data_fields, metadata
    # return None, None


def save(data, headers, metadata, filename):
    filename = ".".join(filename.split(".")[:-1])
    data = utils.get_correct_data(data, headers, data_fields)
    print(data.shape)

    for i in range(data.shape[0]):
        frame = data[i]
        points = vtkPoints()
        points.SetData(numpy_to_vtk(frame[:, :3]))

        # Create polydata
        polydata = vtkPolyData()
        polydata.SetPoints(points)

        for j in range(2, frame.shape[1]):
            arr = numpy_to_vtk(frame[:, j])
            arr.SetName(headers[j])
            polydata.GetPointData().AddArray(arr)

        # Write out to a VTK file
        print(filename)
        print(f"{filename}_{i:06d}.vtk")
        writer = vtkPolyDataWriter()
        writer.SetFileName(f"{filename}_{i:06d}.vtk")
        writer.SetInputData(polydata)
        writer.SetFileTypeToASCII()  # optional: to save as ASCII
        writer.Write()


if __name__ == "__main__":
    import sys

    data, data_fields, metadata = load(sys.argv[1])
    save(data, data_fields, metadata, sys.argv[2])
