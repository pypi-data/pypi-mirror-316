from cellstitch_cuda.postprocessing_cupy import fill_holes_and_remove_small_masks, filter_nuclei_cells
import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda


img = r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-small\raw.tif"
with tifffile.TiffFile(img) as tif:
    img = tif.asarray()

masks = cellstitch_cuda(img, output_masks=True, verbose=True)

quit()
