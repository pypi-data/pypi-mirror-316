from __future__ import annotations
import meshlib.mrmeshpy
from meshlib.mrmeshpy import func_bool_from_float
from meshlib.mrmeshpy import int_output
from meshlib.mrmeshpy import std_vector_MeshIntersectionResult
from meshlib.mrmeshpy import std_vector_MeshProjectionResult
from meshlib.mrmeshpy import std_vector_MeshTriPoint
from meshlib.mrmeshpy import std_vector_SkyPatch
from meshlib.mrmeshpy import std_vector_Vector3_float as std_vector_Vector3f
from meshlib.mrmeshpy import std_vector_Vector3_float
from meshlib.mrmeshpy import std_vector_float
import typing
__all__ = ['FastWindingNumber', 'PointsToMeshProjector', 'computeDistanceMap', 'computeDistanceMapHeapBytes', 'computeSkyViewFactor', 'distanceMapFromContours', 'distanceMapFromContoursHeapBytes', 'findSkyRays', 'func_bool_from_float', 'getCudaAvailableMemory', 'int_output', 'isCudaAvailable', 'negatePicture', 'pointsToDistanceVolume', 'std_vector_MeshIntersectionResult', 'std_vector_MeshProjectionResult', 'std_vector_MeshTriPoint', 'std_vector_SkyPatch', 'std_vector_Vector3_float', 'std_vector_Vector3f', 'std_vector_float']
class FastWindingNumber(meshlib.mrmeshpy.IFastWindingNumber):
    """
    Generated from:  MR::Cuda::FastWindingNumber
    
    the class for fast approximate computation of winding number for a mesh (using its AABB tree)
    \\ingroup AABBTreeGroup
    """
    @typing.overload
    def __init__(self, mesh: meshlib.mrmeshpy.Mesh) -> None:
        """
        constructs this from AABB tree of given mesh;
        """
    @typing.overload
    def __init__(self, arg0: FastWindingNumber) -> None:
        """
        Implicit copy constructor.
        """
    def calcFromGrid(self, res: meshlib.mrmeshpy.std_vector_float, dims: meshlib.mrmeshpy.Vector3i, gridToMeshXf: meshlib.mrmeshpy.AffineXf3f, beta: float, cb: meshlib.mrmeshpy.func_bool_from_float) -> None:
        ...
    def calcFromGridWithDistances(self, res: meshlib.mrmeshpy.std_vector_float, dims: meshlib.mrmeshpy.Vector3i, gridToMeshXf: meshlib.mrmeshpy.AffineXf3f, windingNumberThreshold: float, beta: float, maxDistSq: float, minDistSq: float, cb: meshlib.mrmeshpy.func_bool_from_float) -> None:
        ...
    def calcFromVector(self, res: meshlib.mrmeshpy.std_vector_float, points: meshlib.mrmeshpy.std_vector_Vector3_float, beta: float, skipFace: meshlib.mrmeshpy.FaceId = 'MR::FaceId{}') -> None:
        """
        see methods' descriptions in IFastWindingNumber
        """
    def calcSelfIntersections(self, res: meshlib.mrmeshpy.FaceBitSet, beta: float, cb: meshlib.mrmeshpy.func_bool_from_float) -> bool:
        ...
class PointsToMeshProjector(meshlib.mrmeshpy.IPointsToMeshProjector):
    """
    Generated from:  MR::Cuda::PointsToMeshProjector
    
    Computes the closest point on mesh to each of given points on GPU. It caches data that necessary for computing
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: PointsToMeshProjector) -> None:
        """
        Implicit copy constructor.
        """
    def findProjections(self, res: meshlib.mrmeshpy.std_vector_MeshProjectionResult, points: meshlib.mrmeshpy.std_vector_Vector3_float, objXf: meshlib.mrmeshpy.AffineXf3f, refObjXf: meshlib.mrmeshpy.AffineXf3f, upDistLimitSq: float, loDistLimitSq: float) -> None:
        """
        <summary>
        Computes the closest point on mesh to each of given points
        </summary>
        <param name="res">vector pf projections</param>
        <param name="points">vector of points to project</param>
        <param name="objXf">transform applied to points</param>
        <param name="refObjXf">transform applied to referencing mesh</param>
        <param name="upDistLimitSq">maximal squared distance from point to mesh</param>
        <param name="loDistLimitSq">minimal squared distance from point to mesh</param>
        """
    def projectionsHeapBytes(self, numProjections: int) -> int:
        """
        Returns amount of additional memory needed to compute projections
        """
    def updateMeshData(self, mesh: meshlib.mrmeshpy.Mesh) -> None:
        """
        update all data related to the referencing mesh
        """
def computeDistanceMap(mesh: meshlib.mrmeshpy.Mesh, params: meshlib.mrmeshpy.MeshToDistanceMapParams, cb: meshlib.mrmeshpy.func_bool_from_float = 'MR::ProgressCallback{}', outSamples: meshlib.mrmeshpy.std_vector_MeshTriPoint = None) -> meshlib.mrmeshpy.DistanceMap:
    """
    computes distance (height) map for given projection parameters
    using float-precision for finding ray-mesh intersections, which is faster but less reliable
    """
def computeDistanceMapHeapBytes(mesh: meshlib.mrmeshpy.Mesh, params: meshlib.mrmeshpy.MeshToDistanceMapParams, needOutSamples: bool = False) -> int:
    """
    Computes memory consumption of computeDistanceMap function
    """
def computeSkyViewFactor(terrain: meshlib.mrmeshpy.Mesh, samples: meshlib.mrmeshpy.VertCoords, validSamples: meshlib.mrmeshpy.VertBitSet, skyPatches: meshlib.mrmeshpy.std_vector_SkyPatch, outSkyRays: meshlib.mrmeshpy.BitSet = None, outIntersections: meshlib.mrmeshpy.std_vector_MeshIntersectionResult = None) -> meshlib.mrmeshpy.VertScalars:
    """
    computes relative radiation in each valid sample point by emitting rays from that point in the sky:
    the radiation is 1.0f if all rays reach the sky not hitting the terrain;
    the radiation is 0.0f if all rays do not reach the sky because they are intercepted by the terrain;
    \\param outSkyRays - optional output bitset where for every valid sample #i its rays are stored at indices [i*numPatches; (i+1)*numPatches),
                        0s for occluded rays (hitting the terrain) and 1s for the ones which don't hit anything and reach the sky
    \\param outIntersections - optional output vector of MeshIntersectionResult for every valid sample point
    """
def distanceMapFromContours(polyline: meshlib.mrmeshpy.Polyline2, params: meshlib.mrmeshpy.ContourToDistanceMapParams) -> meshlib.mrmeshpy.DistanceMap:
    """
    Computes distance of 2d contours according to ContourToDistanceMapParams (works correctly only when withSign==false)
    """
def distanceMapFromContoursHeapBytes(polyline: meshlib.mrmeshpy.Polyline2, params: meshlib.mrmeshpy.ContourToDistanceMapParams) -> int:
    """
    Computes memory consumption of distanceMapFromContours function
    """
def findSkyRays(terrain: meshlib.mrmeshpy.Mesh, samples: meshlib.mrmeshpy.VertCoords, validSamples: meshlib.mrmeshpy.VertBitSet, skyPatches: meshlib.mrmeshpy.std_vector_SkyPatch, outIntersections: meshlib.mrmeshpy.std_vector_MeshIntersectionResult = None) -> meshlib.mrmeshpy.BitSet:
    """
    In each valid sample point tests the rays from that point in the sky;
    \\return bitset where for every valid sample #i its rays are stored at indices [i*numPatches; (i+1)*numPatches),
            0s for occluded rays (hitting the terrain) and 1s for the ones which don't hit anything and reach the sky
    \\param outIntersections - optional output vector of MeshIntersectionResult for every valid sample point
    """
def getCudaAvailableMemory() -> int:
    """
    Returns available GPU memory in bytes
    """
def isCudaAvailable(driverVersion: meshlib.mrmeshpy.int_output = None, runtimeVersion: meshlib.mrmeshpy.int_output = None, computeMajor: meshlib.mrmeshpy.int_output = None, computeMinor: meshlib.mrmeshpy.int_output = None) -> bool:
    """
    Returns true if Cuda is present on this GPU
    optional out maximum driver supported version
    optional out current runtime version
    optional out compute capability major version
    optional out compute capability minor version
    """
def negatePicture(image: meshlib.mrmeshpy.Image) -> None:
    """
    This function inverts Color value (255 - value in each channel except alpha) 
    """
def pointsToDistanceVolume(cloud: meshlib.mrmeshpy.PointCloud, params: meshlib.mrmeshpy.PointsToDistanceVolumeParams) -> meshlib.mrmeshpy.SimpleVolumeMinMax:
    """
    makes SimpleVolume filled with signed distances to points with normals
    """
