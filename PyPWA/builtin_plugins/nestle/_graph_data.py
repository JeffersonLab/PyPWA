#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil

import numpy

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _Handler(object):

    __data = None  # type: numpy.ndarray

    def __init__(self, data):
        self.__process_data(data)

    def __process_data(self, data):
        list_of_points = self._find_points(data)
        array_of_points = self.__convert_list_to_numpy(list_of_points)
        self.__data = array_of_points

    @staticmethod
    def _find_points(data):
        raise NotImplementedError
    
    @staticmethod
    def __convert_list_to_numpy(list_of_points):
        return numpy.array(list_of_points)

    def save_data(self, file_location):
        numpy.save(file_location, self.__data)


class _EllipsoidHandler(_Handler):

    @staticmethod
    def _find_points(ellipsoids):
        list_of_centers = [[],[]]
        for ellipsoid in ellipsoids:
            center = ellipsoid.ctr
            list_of_centers[0].append(center[0])
            list_of_centers[1].append(center[1])
        return list_of_centers


class _PointsHandler(_Handler):

    @staticmethod
    def _find_points(points):
        xs_and_ys = [[],[]]
        for point in points:
            xs_and_ys[0].append(point[0])
            xs_and_ys[1].append(point[1])
        return xs_and_ys
        

class SaveData(object):

    __DATA_FOLDER = "saved_data"

    __basic_data = None  # type: List[double]
    __root_save_name = None  # type: str

    def __init__(self, folder_name):
        self.__create_empty_basic_data()
        self.__handle_directories()

    def __set_folder_name(self, folder):
        self.__DATA_FOLDER = folder

    def __create_empty_basic_data(self):
        self.__basic_data = []
        
    def __handle_directories(self):
        if os.path.isdir(self.__DATA_FOLDER):
            self.__clear_directory()
        self.__create_directory()

    def __clear_directory(self):
        shutil.rmtree(self.__DATA_FOLDER)

    def __create_directory(self):
        os.mkdir(self.__DATA_FOLDER)

    def process_callback(self, info):
        self.__set_root_save_name(info["it"])
        self.__process_ellipsoids(info["sampler"].ells)
        self.__process_active_points(info["active_u"])
        self.__append_basic_data(info["logz"])

    def __set_root_save_name(self, iteration):
        self.__root_save_name = self.__DATA_FOLDER + "/"
        self.__root_save_name += str(iteration) + "_"
        
    def __process_ellipsoids(self, ells):
        handler = _EllipsoidHandler(ells)
        save_location = self.__root_save_name + "ellipsoids.npy"
        handler.save_data(save_location)

    def __process_active_points(self, points):
        handler = _PointsHandler(points)
        save_location = self.__root_save_name + "points.npy"
        handler.save_data(save_location)

    def __append_basic_data(self, logz):
        self.__basic_data.append(logz)

    def save_final_data(self):
        final_data = self.__converted_basic_data()
        self.__write_data(final_data)

    def __converted_basic_data(self):
        return numpy.array(self.__basic_data)

    def __write_data(self, data):
        numpy.save(self.__DATA_FOLDER + "/logz.npy", data)
