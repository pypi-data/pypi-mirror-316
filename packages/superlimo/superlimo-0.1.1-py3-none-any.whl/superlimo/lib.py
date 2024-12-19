from nansat import Nansat, Domain, NSR
import numpy as np
from scipy import ndimage as ndi
from scipy.interpolate import LinearNDInterpolator
from scipy.ndimage import map_coordinates
import cv2
import pyproj

def get_n(filename, pols=('HH', 'HV')):
    """Open S1 file with Nansat and add calibrated, downsampled, uint8 HH and HV bands."""
    n = Nansat(filename)
    bb = []
    for pol in pols:
        # Read digital numbers
        b = n[f'DN_{pol}'].astype(float)
        # Read and average calibration
        cal_avg = n.vrt.band_vrts[f'sigmaNought_{pol}'].vrt.dataset.ReadAsArray().mean()
        # Create filter for subsampling and calibration
        filter = np.ones((2, 2)) / 4. / cal_avg
        bf = ndi.convolve(b, filter)[::2, ::2]
        bb.append(bf)
    # Resize Nansat so that reprojection of coordinates is correct
    n.resize(0.5)
    # Adjust bands shapes
    bb = [b[:n.shape()[0], :n.shape()[1]] for b in bb]
    # Add bands to Nansat with name s0_HH or s0_HV
    parameters = [{'name': f's0_{pol}'} for pol in pols]
    d = Nansat.from_domain(n)
    d.set_metadata(n.get_metadata())
    d.add_bands(bb, parameters=parameters)
    # Improve geolocation accuracy
    d.reproject_gcps()
    d.vrt.tps = True
    return d

def get_destimation_domain(proj4str, extent, resolution):
    dst_srs = NSR(proj4str)
    dst_dom = Domain(dst_srs, f'-te {extent} -tr {resolution} {resolution}')
    return dst_dom

def get_dst_rows_cols(dst_dom):
    """ Create grids with row, column coordinates of the destination domain """
    rows2, cols2 = np.meshgrid(
        np.arange(0, dst_dom.shape()[0]),
        np.arange(0, dst_dom.shape()[1]),
        indexing='ij',
    )
    return rows2, cols2

def warp_with_rowcol(src_dom, src_img, c1, r1, c2, r2, dst_dom):
    """ Train interpolators of coordinates and apply to full resolution coordinates to computed a warped image """
    interp_r1 = LinearNDInterpolator(list(zip(r2, c2)), r1)
    interp_c1 = LinearNDInterpolator(list(zip(r2, c2)), c1)
    rows2, cols2 = get_dst_rows_cols(dst_dom)
    r1a = np.clip(interp_r1((rows2, cols2)), 0, src_dom.shape()[0])
    c1a = np.clip(interp_c1((rows2, cols2)), 0, src_dom.shape()[1])
    dst_img = map_coordinates(src_img, (r1a, c1a), order=0)
    return dst_img

def warp_with_lonlat(src_dom, src_img, lon1, lat1, lon2, lat2, dst_dom):
    """ Warp input image on destination domain if vectors of lon,lat source and destination points are knwown """
    c1, r1 = src_dom.transform_points(lon1.flatten(), lat1.flatten(), DstToSrc=1)
    c2, r2 = dst_dom.transform_points(lon2.flatten(), lat2.flatten(), DstToSrc=1)
    dst_img = warp_with_rowcol(src_dom, src_img, c1, r1, c2, r2, dst_dom)
    return dst_img

def warp(src_dom, src_img, dst_dom, step=None):
    """ Warp input image on destination domain (without drift compensation) """
    if step is None:
        step = int(src_dom.shape()[0]/100)
    src_lon, src_lat = src_dom.get_geolocation_grids(step)
    dst_img = warp_with_lonlat(src_dom, src_img, src_lon, src_lat, src_lon, src_lat, dst_dom)
    return dst_img

def pad_to_divisible_by_8(arr):
    new_shape = ((arr.shape[0] + 7) // 8 * 8, (arr.shape[1] + 7) // 8 * 8)
    padded_arr = np.zeros(new_shape)
    padded_arr[:arr.shape[0], :arr.shape[1]] = arr
    return padded_arr

def clip(img, plim=(1,99)):
    """ Clip values in input image to 0 - 1 range. Plim: - [high, low] percentiles to keep """
    vmin, vmax = np.nanpercentile(img, plim)
    return np.clip((img - vmin) / (vmax - vmin), 0, 1)

def clip_and_pad_images(d, min_signal=0.005, plim=(1,99)):
    dd = {}
    for key in d:
        d[key][d[key] < min_signal] = min_signal
        d[key] = pad_to_divisible_by_8(d[key])
        dd[key] = clip(np.log10(d[key]), plim).astype(np.float32)
    return dd

def keypoints2position(keypoints, domain):
    x, y = domain.transform_points(*keypoints.T, DstToSrc=0, dst_srs=NSR(domain.vrt.get_projection()[0]))
    return np.column_stack([x, y])

def get_pm_grids(model, dst_dom, pm_step, template_size, border, proj4str):
    img_size = template_size + border * 2
    dst_shape = dst_dom.shape()

    c0pm_vec = np.arange(0, dst_shape[1], pm_step)
    r0pm_vec = np.arange(0, dst_shape[0], pm_step)
    c0pm, r0pm = np.meshgrid(c0pm_vec, r0pm_vec)
    x0pm, y0pm = dst_dom.transform_points(c0pm.ravel(), r0pm.ravel(), DstToSrc=0, dst_srs=NSR(dst_dom.vrt.get_projection()[0]))
    x1pmfg, y1pmfg = model(np.column_stack([x0pm, y0pm])).T
    lon1pmfg, lat1pmfg = pyproj.Proj(proj4str)(x1pmfg, y1pmfg, inverse=True)
    c1pmfg, r1pmfg = dst_dom.transform_points(lon1pmfg, lat1pmfg, DstToSrc=1)

    x0pm, y0pm, c1pmfg, r1pmfg = [iii.reshape(r0pm.shape) for iii in [x0pm, y0pm, c1pmfg, r1pmfg]]

    gpi_pm = (
        (c0pm > template_size) *
        (c0pm < dst_shape[1] - template_size) *
        (r0pm > template_size) *
        (r0pm < dst_shape[0] - template_size) *
        (c1pmfg > img_size) *
        (c1pmfg < dst_shape[1] - img_size) *
        (r1pmfg > img_size) *
        (r1pmfg < dst_shape[0] - img_size)
        )
    return c0pm, r0pm, x0pm, y0pm, c1pmfg, r1pmfg, gpi_pm

def pattern_matching(d, c0pm, r0pm, c1pmfg, r1pmfg, gpi_pm, template_size, border, pm_pol):
    hs = template_size // 2
    corrections = []
    for c0, r0, c1, r1 in zip(c0pm[gpi_pm], r0pm[gpi_pm], c1pmfg[gpi_pm], r1pmfg[gpi_pm]):
        template = d[f'{pm_pol}0'][r0-hs:r0+hs+1, c0-hs:c0+hs+1]
        image2 = d[f'{pm_pol}1'][int(r1-hs-border):int(r1+hs+1+border), int(c1-hs-border):int(c1+hs+1+border)]
        result = cv2.matchTemplate(image2, template, cv2.TM_CCOEFF_NORMED)
        mccr, mccc = np.unravel_index(result.argmax(), result.shape)
        dr, dc = mccr - border, mccc - border
        mcc = result[mccr, mccc]
        corrections.append([dc, dr, mcc])
    corrections = np.array(corrections)
    return corrections

def apply_pm_corrections(corrections, c1pmfg, r1pmfg, gpi_pm, dst_dom):
    c1pm = np.array(c1pmfg)
    r1pm = np.array(r1pmfg)
    c1pm[gpi_pm] += corrections[:, 0].astype(int)
    r1pm[gpi_pm] += corrections[:, 1].astype(int)
    mccpm = np.zeros(c1pm.shape) + np.nan
    mccpm[gpi_pm] = corrections[:, 2]
    x1pm, y1pm = dst_dom.transform_points(c1pm.ravel(), r1pm.ravel(), DstToSrc=0, dst_srs=NSR(dst_dom.vrt.get_projection()[0]))
    x1pm, y1pm = [iii.reshape(c1pm.shape) for iii in [x1pm, y1pm]]
    return x1pm, y1pm, c1pm, r1pm, mccpm