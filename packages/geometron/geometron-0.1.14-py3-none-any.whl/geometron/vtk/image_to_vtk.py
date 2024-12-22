from geometron.geometries.transforms import shapely_matrix_to_vtk_matrix, rasterio_matrix_to_shapely_matrix
import pyvista as pv
import rasterio as rio
import numpy as np

def geotiff_to_grid(filename, warp=False, scalars_name=None, factor=1.):
    """ Reads a geotiff file and transforms it to a grid

    Parameters
    ----------
    filename: str
        path to the image
    warp: bool, default=False
        if True, the grid is warped by the scalar
    scalars_name: str, default=None
        Name of the scalar point data. if set to None the name will be "Tiff Scalars"
    factor: float

    """
    img = pv.read(filename)
    grid = img.cast_to_structured_grid()
    src = rio.open(filename)
    transform = shapely_matrix_to_vtk_matrix(rasterio_matrix_to_shapely_matrix(src.read_transform()), force_3d=True)
    grid = grid.transform(transform)
    no_data = [n for n, i in enumerate(grid.point_data['Tiff Scalars']) if i in src.nodatavals]
    grid.point_data['Tiff Scalars'][no_data] = np.nan
    grid.set_active_scalars('Tiff Scalars')
    if warp:
        grid = grid.warp_by_scalar('Tiff Scalars', factor=factor)
    if scalars_name is not None:
        grid.rename_array('Tiff Scalars', scalars_name, preference='point')
    return grid
