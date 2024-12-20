from pathlib import Path
import pathlib
import warnings
import numpy as np

from scipy.interpolate import RegularGridInterpolator


class LampSurface:
    def __init__(self, width, length, depth, units, source_density, intensity_map):
        """
        Represents the emissive surface of a lamp; manages functions
        related to source discretization.
        """
        # source values
        self.width = width
        self.length = length
        self.depth = depth
        self.units = units
        self.surface_points = None
        self.num_points_width = None
        self.num_points_length = None
        self.photometric_distance = None
        self.source_density = 1 if source_density is None else source_density
        self.intensity_map_orig = self._load_intensity_map(intensity_map)
        self.intensity_map = self.intensity_map_orig
        self._update_surface_params()

    def _update_surface_params(self):
        """
        update all emissive surface parameters--surface grid points,
        relative intensity map, and photometric distance
        """
        self.surface_points = self._generate_surface_points()
        self.intensity_map = self._generate_intensity_map()
        if all([self.width, self.length, self.units]):
            self.photometric_distance = max(self.width, self.length) * 10
        else:
            self.photometric_distance = None

    def load_intensity_map(self, intensity_map):
        """external method for loading relative intensity map after lamp object has been instantiated"""
        self.intensity_map_orig = self._load_intensity_map(intensity_map)
        self.intensity_map = self.intensity_map_orig
        self._update_surface_params()

    def _load_intensity_map(self, arg):
        """check filetype and return correct intensity_map as array"""
        if arg is None:
            intensity_map = None
        elif isinstance(arg, (str, pathlib.Path)):
            # check if this is a file
            if Path(arg).is_file():
                intensity_map = np.genfromtxt(Path(arg), delimiter=",")
            else:
                msg = f"File {arg} not found. intensity_map will not be used."
                warnings.warn(msg, stacklevel=3)
                intensity_map = None
        elif isinstance(arg, bytes):
            intensity_map = np.genfromtxt(
                arg.decode("utf-8").splitlines(), delimiter=","
            )
        elif isinstance(arg, (list, np.ndarray)):
            intensity_map = np.array(arg)
        else:
            msg = f"Argument type {type(arg)} for argument intensity_map. intensity_map will not be used."
            warnings.warn(msg, stacklevel=3)
            intensity_map = None
        return intensity_map

    def _get_num_points(self):
        """calculate the number of u and v points"""
        num_points = self.source_density + self.source_density - 1
        num_points_v = max(
            num_points, num_points * int(round(self.width / self.length))
        )
        num_points_u = max(
            num_points, num_points * int(round(self.length / self.width))
        )
        if num_points_u % 2 == 0:
            num_points_u += 1
        if num_points_v % 2 == 0:
            num_points_v += 1

        return num_points_u, num_points_v

    def _generate_raw_points(self, num_points_u, num_points_v):
        """generate the points on the surface of the lamp, prior to transforming them"""

        # spacing = min(self.length, self.width) / num_points
        spacing_v = self.width / num_points_v
        spacing_u = self.length / num_points_u

        # If there's only one point, place it at the center
        if num_points_v == 1:
            v_points = np.array([0])  # Single point at the center of the width
        else:
            startv = -self.width / 2 + spacing_v / 2
            stopv = self.width / 2 - spacing_v / 2
            v_points = np.linspace(startv, stopv, num_points_v)

        if num_points_u == 1:
            u_points = np.array([0])  # Single point at the center of the length
        else:
            startu = -self.length / 2 + spacing_u / 2
            stopu = self.length / 2 - spacing_u / 2
            u_points = np.linspace(startu, stopu, num_points_u)

        return u_points, v_points

    def _generate_surface_points(self):
        """
        generate the points with which the calculations should be performed.
        If the source is approximately square and source_density is 1, only
        one point is generated. If source is more than twice as long as wide,
        (or vice versa), 2 or more points will be generated even if density is 1.
        Total number of points will increase quadratically with density.
        """

        # generate the points

        if all([self.width, self.length, self.source_density]):

            num_points_u, num_points_v = self._get_num_points()
            # points pre-transformation
            u_points, v_points = self._generate_raw_points(num_points_u, num_points_v)

            vv, uu = np.meshgrid(v_points, u_points)
            # get the normal plane to the aim point
            # Normalize the direction vector (normal vector)
            direction = self.position - self.aim_point
            normal = direction / np.linalg.norm(direction)

            # Generate two vectors orthogonal to the normal
            if np.allclose(normal, [1, 0, 0]):
                # if normal is close to x-axis, use y and z to define the plane
                u = np.array([0, 1, 0])
            else:
                u = np.cross(normal, [1, 0, 0])
            u = u / np.linalg.norm(u)  # ensure it's unit length

            # Second vector orthogonal to both the normal and u
            v = np.cross(normal, u)
            v = v / np.linalg.norm(v)  # ensure it's unit length
            # Calculate the 3D coordinates of the points, with an overall shift by the original point
            surface_points = (
                self.position + np.outer(uu.flatten(), u) + np.outer(vv.flatten(), v)
            )
            # reverse so that the 'upper left' point is first
            surface_points = surface_points[::-1]
            self.num_points_width = num_points_v
            self.num_points_length = num_points_u

        else:
            surface_points = self.position
            self.num_points_length = 1
            self.num_points_width = 1

        return surface_points

    def _generate_intensity_map(self):
        """if the relative map is None or ones, generate"""

        if self.intensity_map is None:
            # if no relative intensity map is provided
            intensity_map = np.ones((self.num_points_length, self.num_points_width))
        elif self.intensity_map.shape == (
            self.num_points_length,
            self.num_points_width,
        ):
            # intensity map does not need updating
            intensity_map = self.intensity_map
        else:
            # reshape the provided relative map to the current coordinates
            # make interpolator based on original intensity map
            num_points_u, num_points_v = self.intensity_map_orig.shape
            x_orig, y_orig = self._generate_raw_points(num_points_u, num_points_v)
            interpolator = RegularGridInterpolator(
                (x_orig, y_orig),
                self.intensity_map_orig,
                bounds_error=False,
                fill_value=None,
            )

            x_new, y_new = self._generate_raw_points(
                self.num_points_length, self.num_points_width
            )
            # x_new, y_new = np.unique(self.surface_points.T[0]), np.unique(self.surface_points.T[1])
            x_new_grid, y_new_grid = np.meshgrid(x_new, y_new)
            # Create points for interpolation and extrapolation
            points_new = np.array([x_new_grid.ravel(), y_new_grid.ravel()]).T
            intensity_map = interpolator(points_new).reshape(len(x_new), len(y_new)).T

            # normalize
            intensity_map = intensity_map / intensity_map.mean()

        return intensity_map
