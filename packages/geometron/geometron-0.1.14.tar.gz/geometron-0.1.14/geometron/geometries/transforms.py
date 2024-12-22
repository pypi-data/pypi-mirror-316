import geopandas
import numpy as np
import shapely
from shapely.ops import transform
from shapely.affinity import affine_transform
from shapely.geometry import Point, LineString, Polygon
from . import vectors as ggv
import rasterio

# Note:
# The projective_transform could also be performed using the scikit-image package like this:
#
# ``` python
# import skimage
# proj_transf = skimage.transform.ProjectiveTransform()
# proj_transf.estimate(origin_coords, destination_coords)
# def projective_transform(x, y, z=1.):
#     p = proj_transf(np.asarray([x,y]).T)
#     return tuple(p[0])
# ```

def affine_transform_matrix(origin_coords, destination_coords, rcond=-1, shapely_format=True):
    """ Computes a transform matrix to use on shapely or vtk objects from control points coordinates

    origin_coords : list, numpy.ndarray
        2D or 3D coordinates of the control points in the origin space
    destination_coords : list, numpy.ndarray
        2D or 3D coordinates of the control points in the destination space
    rcond : float, default: -1
        Cut-off ratio for small singular values used by numpy.linalg.lstsq
    shapely_format : bool, default: True
        If True, returns a transform matrix in the shapely format otherwise returns a 3x3 or 4x4 transform matrix

    Returns
    -------
    matrix : numpy.ndarray, list
        The transform matrix (in list form if shapely_format is True)
    residuals : numpy.ndarray
        The residuals of the least-squares fitting of the parameters of the transform from the control points coordinate
         pairs
    rank : int
        Rank of matrix a
    singular: (min(M, N),) ndarray
        Singular values of a

    Example
    -------
    >>> # This example shows how to use this function to compute the affine transform matrix from 2D control points.
    >>> import numpy as np
    >>> import geometron.geometries.transforms as ggt
    >>> origin_coords = [np.array([0.,0.]), np.array([0.,1.]), np.array([1.,0.]), np.array([1.,1.2])]
    >>> destination_coords = [np.array([2.5,1.5]), np.array([2.,2.]), np.array([3.,2.]), np.array([2.5,3.])]
    >>> transform_matrix, residuals, rank, singular = ggt.affine_transform_matrix(origin_coords, destination_coords)
    >>> transform_matrix
    [0.5450819672131152, -0.4508196721311477, 0.6803278688524602,
    0.6967213114754098, 2.4754098360655745, 1.401639344262296]

    """
    if isinstance(origin_coords, list):
        if hasattr(origin_coords[0], '__geo_interface__'):
            origin_coords = [np.array(i.__geo_interface__['geometry']['coordinates']) 
                             if 'geometry' in i.__geo_interface__.keys() 
                             else np.array(i.__geo_interface__['coordinates']) for i in origin_coords]
        origin_coords = np.array(origin_coords)
    if isinstance(destination_coords, list):
        if hasattr(destination_coords[0], '__geo_interface__'):
            destination_coords = [np.array(i.__geo_interface__['geometry']['coordinates']) 
                             if 'geometry' in i.__geo_interface__.keys() 
                             else np.array(i.__geo_interface__['coordinates']) for i in destination_coords]
        destination_coords = np.array(destination_coords)

    n_pts, dim = origin_coords.shape
    assert destination_coords.shape[0] == n_pts
    assert destination_coords.shape[1] == dim

    a = np.vstack([origin_coords.T, np.ones([1, n_pts])]).T
    b = destination_coords
    transform_matrix, residuals, rank, singular = np.linalg.lstsq(a, b, rcond=rcond)
    transform_matrix = np.vstack([transform_matrix.swapaxes(0, 1), np.hstack([np.zeros([1, dim]), np.ones([1, 1])])])
    if shapely_format:
        transform_matrix = vtk_matrix_to_shapely_matrix(transform_matrix)
    return transform_matrix, residuals, rank, singular


def projective_transform_matrix(origin_coords, destination_coords, rcond=-1):
    """ Computes a projective transform matrix from control points coordinates

    origin_coords : list, numpy.ndarray
        2D coordinates of the control points in the origin space
    destination_coords : list, numpy.ndarray
        2D coordinates of the control points in the destination space
    rcond : float, default: -1
        Cut-off ratio for small singular values used by numpy.linalg.lstsq

    Returns
    -------
    matrix : numpy.ndarray, list
        The transform matrix

    Example
    -------
    >>> # This example shows how to use this function to compute the projective transform matrix from 2D control points.
    >>> import numpy as np
    >>> import geometron.geometries.transforms as ggt
    >>> origin_coords = [np.array([0.,0.]), np.array([0.,1.]), np.array([1.,0.]), np.array([1.,1.2])]
    >>> destination_coords = [np.array([2.5,1.5]), np.array([2.,2.]), np.array([3.,2.]), np.array([2.5,3.])]
    >>> transform_matrix, residuals, rank, singular = ggt.projective_transform_matrix(origin_coords, destination_coords)
    >>> transform_matrix
    [0.5450819672131152, -0.4508196721311477, 0.6803278688524602,
    0.6967213114754098, 2.4754098360655745, 1.401639344262296]

    """
    if isinstance(origin_coords, list):
        if hasattr(origin_coords[0], '__geo_interface__'):
            origin_coords = [np.array(i.__geo_interface__['geometry']['coordinates']) 
                             if 'geometry' in i.__geo_interface__.keys() 
                             else np.array(i.__geo_interface__['coordinates']) for i in origin_coords]
        origin_coords = np.array(origin_coords)
    if isinstance(destination_coords, list):
        if hasattr(destination_coords[0], '__geo_interface__'):
            destination_coords = [np.array(i.__geo_interface__['geometry']['coordinates'])
                             if 'geometry' in i.__geo_interface__.keys()
                             else np.array(i.__geo_interface__['coordinates']) for i in destination_coords]
        destination_coords = np.array(destination_coords)

    n_pts, dim = origin_coords.shape
    assert destination_coords.shape[0] == n_pts
    assert destination_coords.shape[1] == dim

    a = np.zeros([2 * n_pts, 8])
    b = np.zeros(2 * n_pts)
    for i in range(n_pts):
        a[2 * i, :] = [origin_coords[i, 0], origin_coords[i, 1], 1., 0., 0., 0.,
                       -origin_coords[i, 0] * destination_coords[i, 0], -origin_coords[i, 1] * destination_coords[i, 0]]
        a[2 * i + 1, :] = [0., 0., 0., origin_coords[i, 0], origin_coords[i, 1], 1.,
                           -origin_coords[i, 0] * destination_coords[i, 1],
                           -origin_coords[i, 1] * destination_coords[i, 1]]
        b[2 * i] = destination_coords[i, 0]
        b[2 * i + 1] = destination_coords[i, 1]

    transform_matrix_coefs, residuals, rank, singular = np.linalg.lstsq(a, b, rcond=rcond)

    transform_matrix = np.hstack([transform_matrix_coefs, np.array([1.])]).reshape([3, 3])
    return transform_matrix, residuals, rank, singular

def vtk_matrix_to_shapely_matrix(transform_matrix):
    """ Translates shapely affine transform array into a vtk 3x3 or 4x4 transform matrix
    Parameters
    ----------
    transform_matrix : numpy.ndarray
        a 3x3 or 4x4 affine transform matrix

    Returns
    -------
        np.ndarray
    """
    if transform_matrix.shape==(4,4):
        return np.array([transform_matrix[0,0], transform_matrix[0,1], transform_matrix[0,2],
                         transform_matrix[1,0], transform_matrix[1,1], transform_matrix[1,2],
                         transform_matrix[2,0], transform_matrix[2,1], transform_matrix[2,2],
                         transform_matrix[0,3], transform_matrix[1,3], transform_matrix[2,3]])
    elif transform_matrix.shape==(3,3):
        return np.array([transform_matrix[0,0], transform_matrix[0,1],
                         transform_matrix[1,0], transform_matrix[1,1],
                         transform_matrix[0,2], transform_matrix[1,2]])
    else:
        raise ValueError('Error: matrix should 3x3 or 4x4')


def shapely_matrix_to_vtk_matrix(transform_matrix, force_3d=False):
    """ Translates a vtk 3x3 or 4x3 transform matrix into a shapely affine transform array
    Parameters
    ----------
    transform_matrix : list or numpy.ndarray
        a 6 ot 12 elements affine transform matrix in the shapely format
    force_3d : bool
        if True, forces vtk_matrix to be 4x4 even if the shapely matrix has only 6 elements, in this case the third coordinate is not modified by the transform

    Returns
    -------
        np.ndarray
    """
    if len(transform_matrix)==12:
        return np.array([[transform_matrix[0], transform_matrix[1], transform_matrix[2], transform_matrix[9]],
                        [transform_matrix[3], transform_matrix[4],transform_matrix[5], transform_matrix[10]],
                        [transform_matrix[6], transform_matrix[7], transform_matrix[8], transform_matrix[11]],
                        [0., 0., 0., 1.]])
    elif len(transform_matrix)==6:
        if force_3d:
            return np.array([[transform_matrix[0], transform_matrix[1], 0., transform_matrix[4]],
                             [transform_matrix[2], transform_matrix[3], 0., transform_matrix[5]],
                             [0., 0., 1., 0.],
                             [0., 0., 0., 1.]])
        else:
            return np.array([[transform_matrix[0], transform_matrix[1], transform_matrix[4]],
                             [transform_matrix[2], transform_matrix[3], transform_matrix[5]],
                             [0., 0., 1.]])
    else:
        raise ValueError('Error: shapely matrix should have 6 (2D) or 12 (3D) elements')

def rasterio_matrix_to_shapely_matrix(transform_matrix):
    """ Translates a rasterio Affine transform matrix into a shapely affine transform array
    Parameters
    ----------
    transform_matrix : rasterio.Affine
        a rasterio Affine transform

    Returns
    -------
        np.ndarray
    """

    transform_matrix = np.array(transform_matrix)
    return np.array([transform_matrix[1], transform_matrix[2],
                     transform_matrix[4], transform_matrix[5],
                     transform_matrix[0], transform_matrix[3]])

def projective_transform(geometry, transform_matrix):
    """

    Parameters
    ----------
    geometry : shapely.geometry
        geometry to transform
    transform_matrix: numpy.ndarray
        the transform matrix
    Returns
    -------
        transform geometries
    """
    def t(x, y, z=1.):
        n = np.asarray([[x,y,z]], dtype='object')
        p = n @ transform_matrix.T
        p[p[:, 2] == 0, 2] = np.finfo(float).eps
        p[:, :2] /= p[:, 2:3]
        return tuple(p[0, :2])

    return transform(t, geometry)

def flatten_geometry(geom):
    """ Takes a 3D geometry and returns a 2D geometry discarding the third coordinate
    Parameters
    ----------
    geom : shapely.geometry
        a 3D geometry to flatten

    Returns
    -------
    shapely.geometry
        a 2D geometry
    """

    return shapely.wkb.loads(shapely.wkb.dumps(geom, output_dimension=2))

def projection_on_plane(plane):
    """ Define a 3d transform corresponding to the projection on a plane

    Parameters
    ----------

    Returns
    -------

    Example
    -------
    >>> # This example shows how to use this function.
    >>> plane = {'origin': (20,0,0), 'normal': (1, 3, 3), 'first_unit_vector' : (0,1,0)}
    >>> project_coords_on_plane((1,0,0), plane = plane)

    """

    t = np.asarray(plane['origin'])
    e1 = ggv.unit_vector(plane['first_unit_vector'])
    e3 = ggv.unit_vector(plane['normal'])
    e2 = ggv.unit_vector(-np.cross(e1, e3))
    return affine_transform_matrix(origin_coords=[ggv.null, ggv.ux, ggv.uy, ggv.uz],
                                                           destination_coords=[t, t+e1, t+e2, t+e3])

def project_coords_on_plane(coords, **kwargs):
    # TODO: add docstring
        coords = np.asarray(coords)
        if 'plane' in kwargs.keys():
            plane = kwargs.pop('plane')
            if plane == 'xy':
                return (coords[0], coords[1])
            elif plane == 'xz':
                return (coords[0], coords[2])
            elif plane == 'yz':
                return (coords[1], coords[2])
            elif isinstance(plane, dict) and ('origin' in plane.keys()) and ('normal' in plane.keys()) and (
                    'first_unit_vector' in plane.keys()):
                transform = projection_on_plane(plane)
                return np.array([i for i in affine_transform(Point(coords), transform[0]).coords])
        elif 'transform' in kwargs.keys():
            transform = kwargs.pop('transform')
            return np.array([i for i in affine_transform(Point(coords), transform[0]).coords])
        else:
            print('Warning: unable to project on plane due to unknown arguments')
            return None

def raise_geometry(obj, elevation=0.):
    """ Turns a 2d geometry or 2d geometries of a geodataframe in 3d geometry(ies) with the given constant elevation,
    if obj is a geodataframe, the transform is done in place.

    Parameters
    ----------
    obj : shapely.geometry or geopandas.GeoDataFrame
        the geometry
    elevation : float
        elevation to which obj will be raised

    Returns
    -------
    shapely.geometry or geopandas.GeoDataFrame
        modified geometry(ies)

    Examples
    --------
    >>> # This example shows how to raise a 2D Point to a 3D point with elevation set to 100.
    >>> from shapely.geometry import Point
    >>> from geometron.geometries.transforms import raise_geometry
    >>> p = Point([1., 3.])
    >>> p = raise_geometry(p, 100.)
    >>> print(p)
    POINT Z (1 3 100)
    """

    if isinstance(obj, geopandas.GeoDataFrame):
        for idx, row in obj.iterrows():
            g = row['geometry']
            if g.geom_type == 'Point':
                coords = [(i[0], i[1], elevation) for i in row['geometry'].coords]
                obj.loc[idx, 'geometry'] = Point(coords)
            elif g.geom_type == 'LineString':
                coords = [(i[0], i[1], elevation) for i in row['geometry'].coords]
                obj.loc[idx, 'geometry'] = LineString(coords)
            elif g.geom_type == 'Polygon':
                # exterior ring
                exterior = [(i[0], i[1], elevation) for i in g.exterior.coords]
                # interior rings (a.k.a. holes)
                interiors = [[(j[0], j[1], elevation) for j in i.coords] for i in g.interiors]
                obj.loc[idx, 'geometry'] = Polygon(exterior, interiors)
    elif obj.geom_type == 'Point':
        coords = [(i[0], i[1], elevation) for i in obj.coords]
        obj = Point(coords)
    elif obj.geom_type == 'LineString':
        coords = [(i[0], i[1], elevation) for i in obj.coords]
        obj = LineString(coords)
    elif obj.geom_type == 'Polygon':
        # exterior ring
        exterior = [(i[0], i[1], elevation) for i in obj.exterior.coords]
        # interior rings (a.k.a. holes)
        interiors = [[(j[0], j[1], elevation) for j in i.coords] for i in obj.interiors]
        obj = Polygon(exterior, interiors)
    return obj


def rotate_around_vector(vector, angle, degrees=False, affine_4x4=False):
    """Returns the matrix associated to a rotation by a given angle around a given vector using Rodrigues formula

    Parameters
    ----------
    vector : numpy.array
        vector around which the rotation matrix will be computed
    angle : float
        amplitude of rotation given following the right-hand-side rule
    degrees : bool, default: False
        set to True if angle is given in degrees rather than in radians
    affine_4x4 : bool, default: False
        set to True to return a 4x4 affine transform matrix

    Returns
    -------
    numpy.array
        transform matrix

    Example
    -------
    >>> # This example shows how to use this function to rotate by 90° a given vector a around vector v.
    >>> import numpy as np
    >>> import geometron.geometries.transforms as ggt
    >>> a = np.array([0., 0., 1.])
    >>> v = np.array([3., 0., 0.])
    >>> angle = np.pi/2
    >>> r = ggt.rotate_around_vector(v, angle)
    >>> np.dot(r, a)
    array([ 0.00000000e+00, -1.00000000e+00,  1.11022302e-16])
    For more info. see https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula#Matrix_notation
    """

    vector = np.array(vector)  # convert array-like (list, tuple) into a numpy array
    vector = vector/np.linalg.norm(vector)  # normalize the vector
    if degrees:
        # convert degrees to radians
        angle = angle * np.pi / 180.
    c = np.array([[0., -vector[2], vector[1]], [vector[2], 0., -vector[0]], [-vector[1], vector[0], 0.]])
    r = np.eye(3) + c * np.sin(angle) + np.matmul(c, c) * (1 - np.cos(angle))
    if affine_4x4:
        r = np.vstack([r, np.array([0., 0., 0.])])
        r = np.hstack([r, np.array([[0., 0., 0., 1.]]).T])
    return r
