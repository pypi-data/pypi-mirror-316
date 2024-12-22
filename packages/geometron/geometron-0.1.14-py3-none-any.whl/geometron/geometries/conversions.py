import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import numpy as np


def features_to_gdf(features, **kwargs):
    """ Creates a geodataframe from features

    Parameters
    ----------
    features: object
        iterable of features, where each element must be a feature dictionary or implement the __geo_interface__,
        or feature collection, where the ‘features’ key contains an iterable of features or an Object holding a feature
        collection that implements the __geo_interface__.

    Returns
    -------
        geopandas.GeoDataFrame

    """

    profiles_coll = {"type": "FeatureCollection", "features": features}
    return gpd.GeoDataFrame.from_features(profiles_coll, **kwargs)


def gdf_to_points_gdf(gdf, columns=None):
    """ Creates a geodataframe with the vertices of the geometries of the input geodataframe as geometries

    Parameters
    ----------
    gdf: geopandas.GeoDataFrame
        the input geodataframe
    columns: list, default=None
        the column to copy in the output geodataframe

    Returns
    -------
        geopandas.GeoDataFrame

    """
    if columns is None:
        columns = []
    geo_interface = {"type": "FeatureCollection"}
    features = []
    bbox = (gdf.iloc[:]['geometry'].bounds.minx.min(), gdf.iloc[:]['geometry'].bounds.maxx.max(),
            gdf.iloc[:]['geometry'].bounds.miny.min(), gdf.iloc[:]['geometry'].bounds.maxy.max())
    geo_interface["bbox"] = bbox
    point_id = 0
    for idx, row in gdf.iterrows():
        if isinstance(row['geometry'], Polygon):
            polygon = row['geometry']
            vertices = np.array(polygon.exterior.coords[:])
            for j in range(vertices.shape[0]):
                properties = {p: row[p] for p in columns}
                pt = {"id": f'{point_id}', "type": "Feature", "properties": properties,
                      "geometry": {"type": "Point", "coordinates": tuple(vertices[j, :])}
                      }
                features.append(pt)
                point_id += 1
        elif isinstance(row['geometry'], LineString):
            linestring = row['geometry']
            vertices = np.array(linestring.coords[:])
            for j in range(vertices.shape[0]):
                properties = {p: row[p] for p in columns}
                pt = {"id": f'{point_id}', "type": "Feature", "properties": properties,
                      "geometry": {"type": "Point", "coordinates": tuple(vertices[j, :])}
                      }
                features.append(pt)
                point_id += 1
        elif isinstance(row['geometry'], Point):
            point = row['geometry']
            properties = {p: row[p] for p in columns}
            pt = {"id": f'{point_id}', "type": "Feature", "properties": properties,
                  "geometry": {"type": "Point", "coordinates": tuple(point.coords[:])}
                  }
            features.append(pt)
            point_id += 1
        else:
            print(f'Warning: gdf_to_points_gdf cannot process {type(row["geometry"])} geometries. '
                  f'These geometries will be ignored.')
    geo_interface["features"] = features

    return gpd.GeoDataFrame.from_features(geo_interface, crs=gdf.crs)
