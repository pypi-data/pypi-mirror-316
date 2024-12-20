from scipy.ndimage import find_objects, binary_fill_holes
from joblib import Parallel, delayed


def process_slice(i, slc, masks, min_size):
    if slc is not None:
        msk = masks[slc] == (i + 1)
        npix = msk.sum()
        if min_size > 0 and npix < min_size:
            masks[slc][msk] = 0
        elif npix > 0:
            if msk.ndim == 3:
                for k in range(msk.shape[0]):
                    msk[k] = binary_fill_holes(msk[k])
            else:
                msk = binary_fill_holes(msk)
            return slc, msk
    return None


def fill_holes_and_remove_small_masks(masks, min_size=15, n_jobs=-1):
    """Fills holes in masks (2D/3D) and discards masks smaller than min_size.

    This function fills holes in each mask using scipy.ndimage.morphology.binary_fill_holes.
    It also removes masks that are smaller than the specified min_size.

    Adapted from CellPose: https://github.com/MouseLand/cellpose
        https://doi.org/10.1038/s41592-020-01018-x: Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021).
        Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106.
        Copyright © 2023 Howard Hughes Medical Institute, Authored by Carsen Stringer and Marius Pachitariu.

    Parameters:
    masks (ndarray): Int, 2D or 3D array of labelled masks.
        0 represents no mask, while positive integers represent mask labels.
        The size can be [Ly x Lx] or [Lz x Ly x Lx].
    min_size (int, optional): Minimum number of pixels per mask.
        Masks smaller than min_size will be removed.
        Set to -1 to turn off this functionality. Default is 15.
    n_jobs (int): Parallel processing cores to use. Default is -1.

    Returns:
    ndarray: Int, 2D or 3D array of masks with holes filled and small masks removed.
        0 represents no mask, while positive integers represent mask labels.
        The size is [Ly x Lx] or [Lz x Ly x Lx].
    """

    if masks.ndim > 3 or masks.ndim < 2:
        raise ValueError(
            "masks_to_outlines takes 2D or 3D array, not %dD array" % masks.ndim
        )

    slices = find_objects(masks)
    results = Parallel(n_jobs=n_jobs)(delayed(process_slice)(i, slc, masks, min_size) for i, slc in enumerate(slices))

    j = 0
    for result in results:
        if result is not None:
            slc, msk = result
            masks[slc][msk] = (j + 1)
            j += 1
    return masks
