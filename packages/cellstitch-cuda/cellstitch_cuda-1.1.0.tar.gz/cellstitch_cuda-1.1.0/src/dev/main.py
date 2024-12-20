from cellstitch_cuda.pipeline import cellstitch_cuda


img = r"E:\Tom\raw.tif"

masks = cellstitch_cuda(img, output_masks=True, verbose=True)
