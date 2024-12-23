from cellstitch_cuda.postprocessing_cupy import fill_holes_and_remove_small_masks, filter_nuclei_cells
import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda


img = r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\unmixed\unmixed.tif"

masks = cellstitch_cuda(img, output_masks=True, verbose=True)
