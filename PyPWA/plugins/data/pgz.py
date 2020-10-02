#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import getpass
import hashlib
import io
import json
import os
import pickle
import tarfile
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd

from PyPWA import ParticlePool, Particle
from PyPWA.libs import common
from PyPWA.libs.file.processor import templates, DataType


class _PGzPlugin(templates.IDataPlugin):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    def plugin_name(self):
        return "PyPWA builtin compressed Data Format"

    def get_memory_parser(self):
        return TarMemory()

    def get_reader(self, file_location, use_pandas):
        pass

    def get_writer(self, file_location):
        pass

    def get_read_test(self):
        return TarTest()

    @property
    def supported_extensions(self):
        return [".pgz"]

    @property
    def supported_data_types(self):
        return [DataType.STRUCTURED, DataType.TREE_VECTOR]

    @property
    def use_caching(self) -> bool:
        return False

    @property
    def supports_iterators(self) -> bool:
        return False


metadata = _PGzPlugin()


class TarTest(templates.IReadTest):

    def can_read(self, filename: Path) -> bool:
        try:
            with tarfile.open(filename, "r:gz") as tar:
                # check for cache file
                tar.getmember("data.cache")

                meta = json.load(tar.extractfile("metadata.json"))
                for file in meta["files"]:
                    tar.getmember(file)
            return True
        except Exception:
            return False


class TarMemory(templates.IMemory):

    def parse(self, filename: Path) -> np.ndarray:
        return TarParser.parse(filename)

    def write(self, filename: Path, data: Union[pd.DataFrame, np.ndarray]):
        TarWriter.write(filename, data)


class TarParser:

    @classmethod
    def parse(cls, file_path: Path):
        with tarfile.open(file_path, "r:gz") as tar:
            meta = cls._load_metadata(tar)

            # If the pickle doesn't even load, we can fall back
            # to just parsing the data directly.
            try:
                cache = pickle.load(tar.extractfile("data.cache"))
            except Exception:
                return cls._load_data_directly(meta, tar)

            # If the cache isn't valid, just load the data directly
            valid = cls._verify_cache(cache, meta, tar)
            if valid:
                return cache["data"]
            return cls._load_data_directly(meta, tar)

    @staticmethod
    def _load_metadata(tar_obj):
        metadata_obj = tar_obj.extractfile("metadata.json")
        return json.load(metadata_obj)

    @classmethod
    def _verify_cache(cls, cache, meta, tar_obj):
        for file in meta["files"]:
            cache_hash, _ = cls._get_cache_hash_and_byte_length(
                tar_obj.extractfile(file)
            )
            if cache["md5"][file] != cache_hash:
                return False
        return True

    @staticmethod
    def _get_cache_hash_and_byte_length(obj):
        obj.seek(0)
        obj_hash = hashlib.md5()
        for chunk in iter(lambda: obj.read(40960), b""):
            obj_hash.update(chunk)

        obj_hash = obj_hash.hexdigest()
        length = obj.tell()
        obj.seek(0)

        return obj_hash, length

    @classmethod
    def _load_data_directly(cls, meta, tar):
        if meta["type"] == "flat":
            data_obj = tar.extractfile(meta["files"][0])
            return np.loadtxt(data_obj)
        elif meta["type"] == "structured":
            return common.pandas_to_numpy(
                pd.read_csv(tar.extractfile(meta["files"][0]))
            )
        elif meta["type"] == "particles":
            return cls._pgz_to_particle_pool(meta, tar)

    @staticmethod
    def _pgz_to_particle_pool(meta, tar):
        particle_list = []
        for particle_file in sorted(meta["files"]):
            data = pd.read_csv(tar.extractfile(particle_file))
            particle_id = int(particle_file.split("_")[1].strip(".csv"))
            particle_list.append(Particle(particle_id, data))
        return ParticlePool(particle_list)


class TarWriter:

    @classmethod
    def write(cls, file_path, data):
        meta = cls._make_metadata(data)
        json_io, json_info = cls._json_data(meta)
        file_data = cls._data_to_bytes(meta, data)
        cache_io, cache_info = cls._make_cache_io(meta, data)

        with tarfile.open(file_path, "w:gz") as tar:
            tar.addfile(json_info, json_io)
            tar.addfile(cache_info, cache_io)
            for data_io, data_info in file_data:
                tar.addfile(data_info, data_io)

    @staticmethod
    def _make_metadata(data):
        meta = {"version": 0.1, "files": []}
        if isinstance(data, ParticlePool):
            meta["type"] = "particles"
            for index, particle in enumerate(data.iter_particles()):
                meta["files"].append(f"{index}_{particle.id}.csv")
        elif (isinstance(data, np.ndarray) and data.dtype.names) or \
                isinstance(data, pd.DataFrame):
            meta["type"] = "structured"
            meta["files"] = ["data.csv"]
        elif isinstance(data, (pd.Series, np.ndarray)):
            meta["type"] = "flat"
            meta["files"] = ["data.txt"]
        else:
            raise ValueError(f"Unknown data type: {type(data)}")
        return meta

    @classmethod
    def _json_data(cls, meta):
        json_data = io.BytesIO(json.dumps(meta).encode("utf-8"))
        tar_info, _ = cls._make_tar_info(json_data, "metadata.json")
        return json_data, tar_info

    @classmethod
    def _data_to_bytes(cls, meta, data):
        meta["md5"] = dict()

        if meta["type"] == "flat":
            raw_data = io.BytesIO()
            np.savetxt(raw_data, data)
            name = "data.txt"
        elif meta["type"] == "structured":
            raw_data = io.BytesIO(
                pd.DataFrame(data).to_csv(index=False).encode("utf-8")
            )
            name = "data.csv"
        else:
            return cls._particles_to_bytes(meta, data)

        data_info, obj_hash = cls._make_tar_info(raw_data, name)
        meta["md5"][name] = obj_hash
        return [(raw_data, data_info)]

    @classmethod
    def _particles_to_bytes(cls, meta, data: ParticlePool):
        data_list = []
        for file, particle in zip(meta["files"], data.iter_particles()):
            raw_data = io.BytesIO(
                particle.dataframe.to_csv(index=False).encode("utf-8")
            )

            info, raw_hash = cls._make_tar_info(raw_data, file)
            meta["md5"][file] = raw_hash
            data_list.append((raw_data, info))

        return data_list

    @classmethod
    def _make_cache_io(cls, meta, data):
        meta["data"] = data
        pickle_io = io.BytesIO(pickle.dumps(meta))
        info, _ = cls._make_tar_info(pickle_io, "data.cache")
        return pickle_io, info

    @classmethod
    def _make_tar_info(cls, obj, name):
        obj_hash, length = cls._get_hash_and_length(obj)

        info = tarfile.TarInfo(name)
        info.size = length
        # info.chksum = obj_hash
        # info.type = b"0"
        info.uid = os.geteuid()
        info.gid = os.getegid()
        info.uname = getpass.getuser()

        obj.seek(0)
        return info, obj_hash

    @staticmethod
    def _get_hash_and_length(obj):
        obj.seek(0)
        obj_hash = hashlib.md5()
        for chunk in iter(lambda: obj.read(40960), b""):
            obj_hash.update(chunk)

        length = obj.tell()
        obj.seek(0)

        return obj_hash.hexdigest(), length
