from tifffile import imsave
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import time as Time
import scipy.stats
from scipy import stats
from scipy.ndimage import label
from skimage.filters import threshold_otsu
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
from scipy import stats
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr
import random as rd 
from scipy.signal import fftconvolve
from scipy import ndimage
from rasterio.transform import from_origin
from pyproj import Proj, transform
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import rasterio
from rasterio.transform import from_bounds
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import confusion_matrix
from scipy.ndimage import label, distance_transform_edt, sobel
from scipy.special import expit  # Pour la fonction logistique
from scipy.ndimage import binary_dilation
from scipy.spatial import ConvexHull
from skimage.draw import polygon
import matplotlib.pyplot as plt
from collections import Counter
import random
from shapely.geometry import Point
from rasterio.features import rasterize

def reassign_non_continuous_regions(arrayp):
    array=arrayp.copy()
    unique_labels = np.unique(array)
    current_max_label = np.nanmax(unique_labels)
    
    for label_value in unique_labels:
        if label_value is None:
            continue
        
        # Create a binary mask for the current label
        mask = array == label_value
        
        # Label connected components in the mask
        labeled_mask, num_features = label(mask)
        
        if num_features > 1:
            for i in range(2, num_features + 1):
                current_max_label += 1
                #print(current_max_label)
                array[labeled_mask == i] = current_max_label
                
    return array        


# get a 2D array from a shpfile and reproject it using a ref file
def project_shpfile(reftifpath,shpfile):
    # Chemin vers le fichier TIFF
    tiff_path = reftifpath
    with rasterio.open(tiff_path) as src:
        reference_crs = src.crs
        reference_transform = src.transform
        width = src.width
        height = src.height
        bounds = src.bounds
    ecoregions = gpd.read_file(shpfile)
    ecoregions = ecoregions.to_crs(reference_crs)
    # Créer une liste de (geometry, value) pour chaque écorégion
    shapes = [(geom, float(i + 1)) for i, geom in enumerate(ecoregions.geometry)]
    # Définir la taille du raster
    out_shape = (height, width)
    # Rasteriser les géométries du shapefile
    raster = rasterize(shapes, out_shape=out_shape, transform=reference_transform, fill=0.0, dtype='float32')
    return raster



# save a tif file from a 2D array taking as a reference a reference file tif
def saveTIF(reffile,array,outputfile):
    # Load reference metadata
    ref_file = reffile  # Path to your reference file
    new_file = outputfile    # Path where new file will be saved

    # Load the reference dataset
    with rasterio.open(ref_file) as ref:
        meta = ref.meta.copy()  # Copy the metadata
        transform = ref.transform  # Get transform (extent, resolution, etc.)
        crs = ref.crs  # Get projection
        ref.close()

    # Your 2D numpy array (data to be saved)
    import numpy as np
    data=array.copy()

    # Update metadata
    meta.update({
        "driver": "GTiff",
        "height": data.shape[0],
        "width": data.shape[1],
        "transform": transform,
        "crs": crs,
    })

    # Save the numpy array to a new TIFF file
    with rasterio.open(new_file, 'w', **meta) as dst:
        dst.write(data, 1)  # Write data to the first band


def gkern(sig=1.,hole=False):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    l=int(8*sig + 1)
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    if hole==True:
        kernel[kernel==np.max(kernel)]=0
    return kernel / np.sum(kernel)

def circkernel(A):
    R=(A/np.pi)**(1/2)
    K=np.zeros((2*int(R)+1,2*int(R)+1))
    Ks=K.shape[0]
    mid=Ks//2
    for x in range(Ks):
        for y in range(Ks):
            if ((x-mid)**2 + (y-mid)**2)**(1/2) <= R:
                K[x,y]=1
    return K

# def applykernel(Map,Kernel): 
#     imax,jmax = Map.shape
#     ks=Kernel.shape[0]
#     lx,ly = np.where(Map==1)
#     newMap=np.zeros((imax,jmax))
#     for x,y in zip(lx,ly):
#         x1=max(x-ks//2,0) ; x2 = min(x+ks//2+1,imax) # ça c'est bon
#         y1=max(y-ks//2,0) ; y2 = min(y+ks//2+1,jmax) # ça c'est bon
#         s1=ifelse(x-ks//2<0,abs(x-ks//2),0) ; s2 = ifelse(x+ks//2 >imax-1, (ks)-(x+ks//2-imax+1),ks)
#         r1=ifelse(y-ks//2<0,abs(y-ks//2),0) ; r2 = ifelse(y+ks//2 >jmax-1,(ks)-(y+ks//2-jmax+1),ks)
#         newMap[x1:x2,y1:y2] += Kernel[s1:s2,r1:r2] # concerned kernel part
#     return newMap


def cosgkern(sig=1.,hole=False):
    K=np.zeros((8*int(sig)+1,8*int(sig)+1))
    ks = K.shape[0]
    mid = ks//2
    for x in range(ks):
        for y in range(ks):
            d= ((x-mid)**2 + (y-mid)**2)**(1/2)
            K[x,y] = d
    K = np.cos(K*np.pi/(4*sig))*np.exp(-K**2/(2*sig**2))
    return K


def applykernel_pr(Map,Kernel): 
        imax,jmax = Map.shape
        ks=Kernel.shape[0]
        lx,ly = np.where(Map==1)
        newMap=np.zeros((imax,jmax))
        for x,y in zip(lx,ly):
            x1=max(x-ks//2,0) ; x2 = min(x+ks//2+1,imax) # ça c'est bon
            y1=max(y-ks//2,0) ; y2 = min(y+ks//2+1,jmax) # ça c'est bon
            s1=ifelse(x-ks//2<0,abs(x-ks//2),0) ; s2 = ifelse(x+ks//2 >imax-1, (ks)-(x+ks//2-imax+1),ks)
            r1=ifelse(y-ks//2<0,abs(y-ks//2),0) ; r2 = ifelse(y+ks//2 >jmax-1,(ks)-(y+ks//2-jmax+1),ks)
            newMap[x1:x2,y1:y2] += Kernel[s1:s2,r1:r2] # concerned kernel part
        return newMap





def Beta2(x,mu,var):
    alpha=((mu*(1-mu))/var-1)*mu
    beta=((mu*(1-mu))/var-1)*(1-mu)
    dist = scipy.stats.beta(alpha, beta)
    return dist.pdf(x)

# generate an exponential kernel based on Mean Dispersal Distance, return a 2D exponential kernel generated from an exponential
# distance distribution with mean =MDD, hole paramter remove the centered pixel and its neighbors, sizecoeff is the parameter  
# that control the size of the generated kernel, higher values for sizecoeff means generation of a larger part of the kernel

def ifelse(condition,resultif,resultelse):
    if condition == True:
        return resultif
    else:
        return resultelse

def gaussian_kernel(sig):
    size = int(8*sig + 1)
    K=np.zeros((size,size))
    mid=K.shape[0]//2
    for x in range(0,size):
        for y in range(0,size):
            K[x,y]=np.exp(-(((x-mid)**2)/(2*sig**2)+((y-mid)**2)/(2*sig**2)))
    K[mid,mid]=0
    return K/np.nansum(K)

def generate_exponential_kernel(MDD,hole=True,sizecoeff=10,size=None):
    if size is None:
        size = 2*(int(MDD*sizecoeff//2)) +1 # value 20 is high but we need to compute a large area to not having jump on the map due to lack of border calculation
    mid=size // 2
    X = np.arange(size)
    Y = np.arange(size)
    kernel=np.zeros((size,size))
    for x in X:
        for y in Y:
            distance_squared = (x-mid)**2 + (y-mid)**2
            kernel[x,y] = np.exp(-np.sqrt(distance_squared) * (1 / MDD))
    if hole==True:
        kernel[mid-1:mid+2,mid-1:mid+2]=0
    return kernel

# Estar algorithm permits to produce a ExpoScore Map based on observations and IUCN
IUCNalone=False


# Function to find the bin index for a given number
def get_bin_index(number, bin_edges):
    """
    Given a number and bin edges, returns the index of the bin the number falls into.
    If the number is outside the range, returns None.
    """
    if number < bin_edges[0] or number > bin_edges[-1]:
        return None
    # np.digitize returns bins in 1-based index, so we subtract 1
    bin_index = np.digitize(number, bin_edges) - 1
    # Handle the edge case where the number is exactly equal to the maximum edge
    if bin_index == len(bin_edges) - 1:
        bin_index -= 1
    return bin_index

# Function to get the relative frequency of the bin a number falls into
def get_relative_frequency(number, bin_edges, relative_frequencies):
    bin_index = get_bin_index(number, bin_edges)
    if bin_index is None:
        return 0  # Number is outside the range
    return relative_frequencies[bin_index]


def genhist(L,num_bins=10):
    # Compute histogram
    counts, bin_edges = np.histogram(L, bins=num_bins, range=(min(L), max(L)), density=False)
    # Calculate relative frequencies
    total_count = len(L)
    relative_frequencies = counts / total_count
    return bin_edges,relative_frequencies
 
def applykernel(Map,Kernel,NanMap=None,WeightMap=None): 
    imax,jmax = Map.shape
    ks=Kernel.shape[0]
    lx,ly = np.where(Map==1)
    newMap=np.zeros((imax,jmax))
    if NanMap is not None:  
        continuous_regions=1-NanMap
        iD_continuous_regions = label(continuous_regions, structure=np.ones((3, 3)))[0]
    else:
        iD_continuous_regions = np.ones_like(Map)
    
    inhabited_regions = np.unique(iD_continuous_regions[np.where(Map==1)])
    print("list of inhabited continuous regions iD",inhabited_regions)
    print("applying kernels...")
    nb_points_done =0 
    nb_points = len(lx)
    t0=Time.time()
    for region in inhabited_regions:
        if Time.time()-t0 > 5:
            print(nb_points_done ,"/", nb_points, " points done")
            t0 = Time.time()
        Mask_accessible_region = iD_continuous_regions==region
        xs,ys = np.where(Map*Mask_accessible_region)
        for x,y in zip(xs,ys):
            if WeightMap is not None:
                weight = WeightMap[x,y]
            else:
                weight = 1
            x1=max(x-ks//2,0) ; x2 = min(x+ks//2+1,imax) # ça c'est bon
            y1=max(y-ks//2,0) ; y2 = min(y+ks//2+1,jmax) # ça c'est bon
            s1=ifelse(x-ks//2<0,abs(x-ks//2),0) ; s2 = ifelse(x+ks//2 >imax-1, (ks)-(x+ks//2-imax+1),ks)
            r1=ifelse(y-ks//2<0,abs(y-ks//2),0) ; r2 = ifelse(y+ks//2 >jmax-1,(ks)-(y+ks//2-jmax+1),ks)
            newMap[x1:x2,y1:y2] += Kernel[s1:s2,r1:r2]*Mask_accessible_region[x1:x2,y1:y2]*weight # concerned kernel part
            nb_points_done +=1
    return newMap


print("utilitary tools imported")