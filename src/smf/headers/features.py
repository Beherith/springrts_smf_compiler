from struct import Struct
from .root import SMFRootHeader


class SMFFeatureHeader(SMFRootHeader):
    """
        Python representation for MapFeatureHeader struct. Maps to the following:

        int numFeatureType;
        int numFeatures;
    """

    feature_type: int

    feature_count: int

    __struct_def: Struct = Struct('< i i')

    def pack(self):
        return self.__struct_def.pack(
            self.feature_type,
            self.feature_count
        )


class SMFFeatureInstanceHeader(SMFRootHeader):
    """
        Python representation for MapFeature struct. Maps to the following:

        int featureType;
        float xPos;
        float yPos;
        float zPos;
        float rotation;
        float scale;
    """

    feature_type: int

    x_pos: float
    y_pos: float
    z_pos: float
    rotation: float
    scale: float

    __struct_def: Struct = Struct('< i f f f f f')

    def pack(self):
        return self.__struct_def.pack(
            self.feature_type,
            self.x_pos,
            self.y_pos,
            self.z_pos,
            self.rotation,
            self.scale
        )
