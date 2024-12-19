import argparse

import numpy as np
from omegaconf import OmegaConf
import torch

from superlimo.lib import get_n, get_destimation_domain, warp, clip_and_pad_images, keypoints2position, get_pm_grids, pattern_matching, apply_pm_corrections
from superlimo.superlimo import SuperLIMo
from superlimo.matcher import Matcher

def parse_args():
    parser = argparse.ArgumentParser(description='Derive drift from two SAR images')
    parser.add_argument('config', type=str, help='The config file')
    parser.add_argument('file0', type=str, help='The first SAR image')
    parser.add_argument('file1', type=str, help='The second SAR image')
    parser.add_argument('output', type=str, help='The output file')
    return parser.parse_args()

def main():
    args = parse_args()
    conf = OmegaConf.load(args.config)

    # load data from input images
    n0 = get_n(args.file0)
    n1 = get_n(args.file1)

    # prepare destimation Domain
    dst_dom = get_destimation_domain(conf.proj4, conf.extent, conf.sar_resolution)
    image_time_delta = (n1.time_coverage_start - n0.time_coverage_start).total_seconds()

    # reproject SAR images
    d = {}
    d['hh0'] = warp(n0, n0[1], dst_dom)
    d['hh1'] = warp(n1, n1[1], dst_dom)
    d['hv0'] = warp(n0, n0[2], dst_dom)
    d['hv1'] = warp(n1, n1[2], dst_dom)
    d = clip_and_pad_images(d, conf.min_sar_signal, conf.plim)

    # prepare Tensors
    img0 = torch.tensor(np.stack([d['hh0'], d['hv0']], 0))[None].float()
    img1 = torch.tensor(np.stack([d['hh1'], d['hv1']], 0))[None].float()
    img0[img0.isnan()] = 0
    img1[img1.isnan()] = 0

    # create CNN and apply
    superlimo = SuperLIMo(conf)
    with torch.no_grad():
        pre0 = superlimo(img0)
        pre1 = superlimo(img1)
    pos0 = keypoints2position(pre0['keypoints'], dst_dom)
    pos1 = keypoints2position(pre1['keypoints'], dst_dom)

    # Match keypoints from CNN
    matcher = Matcher(plot=False, time_delta=image_time_delta, **conf)
    idx0, idx1, model = matcher.match(pos0, pos1, pre0['descriptors'].numpy().T, pre1['descriptors'].numpy().T)
    c0pm, r0pm, x0pm, y0pm, c1pmfg, r1pmfg, gpi_pm = get_pm_grids(model, dst_dom, conf.pm_step, conf.pm_template_size, conf.pm_border, conf.proj4)

    # Apply pattern matching corrections
    corrections = pattern_matching(d, c0pm, r0pm, c1pmfg, r1pmfg, gpi_pm, conf.pm_template_size, conf.pm_border, conf.pm_pol)
    x1pm, y1pm, c1pm, r1pm, mccpm = apply_pm_corrections(corrections, c1pmfg, r1pmfg, gpi_pm, dst_dom)

    # Save results
    if not args.output.endswith('.npz'):
        args.output += '.npz'
    np.savez(args.output, x0=x0pm, y0=y0pm, x1=x1pm, y1=y1pm, mcc=mccpm)

if __name__ == '__main__':
    main()
