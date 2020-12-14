from zipfile import ZipFile
import tarfile
import pkg_resources
from pathlib import Path


class WheelPackageInfo:
    def __init__(self, filename):
        self.wheel_package = ZipFile(filename)
        self.info = {
            "NAME": "",
            "VERSION": "",
            "REQUIRES-DIST": {},
            "REQUIRES-PYTHON": "",
        }
        self.read_info()

    def read_info(self):
        for file in self.wheel_package.namelist():
            if file.endswith("METADATA"):
                for line in (
                    self.wheel_package.open(file).read().decode("utf-8").split("\n")
                ):
                    if "===" in line:
                        break
                    words = line.split(" ")
                    subkey = words[0].upper().replace(":", "")
                    if subkey in self.info.keys():
                        if self.info[subkey] == "":
                            self.info[subkey] = words[1]
                        else:
                            if words[2].__contains__("("):
                                self.info[subkey].update({words[1]: words[2]})
                            else:
                                self.info[subkey].update({words[1]: ""})

        self.wheel_package.close()

    def is_installed(self):
        try:
            _ = pkg_resources.get_distribution(
                "{}=={}".format(self.get_name(), self.get_version())
            )
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            return False
        else:
            return True

    def has_dependencies(self):
        return self.get_requires_dist().__len__() != 0

    def get_name(self):
        return self.info["NAME"]

    def get_version(self):
        return self.info["VERSION"]

    def get_requires_dist(self):
        return self.info["REQUIRES-DIST"]

    def get_requires_python(self):
        return self.info["REQUIRES-PYTHON"]


class JCK:
    def __init__(self):
        self.filenames = []
        self.jckinfo = ""

    def read_directory(self, path_to_dir):
        entries = Path(path_to_dir)
        for entry in entries.iterdir():
            if entry.is_file():
                self.filenames.append(entry)

    def create_file(self, filename):
        with tarfile.open("{}.jck".format(filename), "w:xz") as file:
            for name in self.filenames:
                file.add(name)

    def read_file(self, filename):
        with tarfile.open("{}.jck".format(filename), "r:xz") as file:
            for name in file.getnames():
                if name == "jckinfo":
                    for line in (
                        file.extractfile(name).read().decode("utf-8").split("\n")
                    ):
                        self.jckinfo += line

    def analize_wheels(self):
        pass

    def log_jckinfo(self, name, version, status):
        with open("jckinfo", "a") as file:
            file.write("{} {} {}".format(name, version, status))

    def list_dir(self):
        print("=====================================")
        print("Files: \n")
        for i in self.filenames:
            print(i)
        print("=====================================")
