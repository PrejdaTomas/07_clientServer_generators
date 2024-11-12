from .A001_ReprObject import ReprObject, Self
import pickle

class Picklable(ReprObject):
    _pickleSuffix: str = ".PICK"
    def storeBitCopy(self, path: str) -> str:
        """Stores the instance copy to a path without a suffix, which is added to the path string.

        Args:
            path (str): path to the stored file without a suffix, with just the filename the working directory is used.

        Returns:
            str: absolute path to the stored file with a suffix
        """
        path = path + self.__class__._pickleSuffix
        with open(path, "wb") as writePort:
            pickle.dump(self, writePort)
        return path
    
    @classmethod
    def loadBitCopy(cls, path: str) -> Self:
        """Loads the instance copy from a path without a suffix, which is added to the path string.

        Args:
            path (str): path to the stored file without a suffix, with just the filename the working directory is used.

        Returns:
            Self: the reconstructed Self.__class__ instance
        """
        path = path + cls.__class__._pickleSuffix
        with open(path, "wb") as readPort:
            nuInstance: Self = pickle.load(readPort)
        return nuInstance