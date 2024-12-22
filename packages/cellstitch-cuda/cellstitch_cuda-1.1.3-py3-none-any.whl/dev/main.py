from cellstitch_cuda.postprocessing_cupy import fill_holes_and_remove_small_masks, filter_nuclei_cells
import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda


img = r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-deep\_masks.tif"
img2 = r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-deep\nuclei_masks.tif"
masks = tifffile.imread(img)
nuclei = tifffile.imread(img2)

import time
time_start = time.time()

masks = filter_nuclei_cells(volumetric_masks=masks, nuclei_masks=nuclei)

print("Time to filter nuclei:", time.time()-time_start)

tifffile.imwrite(r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-deep\cellstitch_masks2.tif", masks)

quit()

masks = cellstitch_cuda(img, output_masks=True, verbose=True)
