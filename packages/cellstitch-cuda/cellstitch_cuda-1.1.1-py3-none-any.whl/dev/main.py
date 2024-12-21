from cellstitch_cuda.pipeline import cellstitch_cuda


img = r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-deep\raw.tif"

masks = cellstitch_cuda(img, output_masks=True, verbose=True)
