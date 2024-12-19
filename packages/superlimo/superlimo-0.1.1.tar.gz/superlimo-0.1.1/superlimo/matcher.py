import cv2
from skimage.measure import ransac
import skimage.transform as sckitran
import matplotlib.pyplot as plt
import numpy as np


class Matcher:
    def __init__(self,
                 norm=cv2.NORM_L2,
                 max_distance=0.8,
                 max_drift=0.2,
                 ransac_model=sckitran.AffineTransform,
                 ransac_ratio=0.2,
                 ransac_threshold=0.03,
                 lowe_ratio=0.9,
                 plot=False,
                 use_ransac=True,
                 time_delta=1,
                 **kwargs):
        if isinstance(norm, str): norm = eval(f'cv2.{norm}')
        self.norm = norm
        self.max_distance = max_distance
        self.max_drift = max_drift * time_delta
        if isinstance(ransac_model, str): norm = eval(f'sckitran.{ransac_model}')
        self.ransac_model = ransac_model
        self.ransac_ratio = ransac_ratio
        self.ransac_threshold = ransac_threshold * time_delta
        self.lowe_ratio = lowe_ratio
        self.plot = plot
        self.use_ransac = use_ransac

    def plot_quiver(self, pos0, pos1, dist):
        u = pos1[:, 0] - pos0[:, 0]
        v = pos1[:, 1] - pos0[:, 1]
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        scat = axs[0].scatter(u, v, c=dist, cmap='jet', clim=np.percentile(dist, [1, 99]))
        axs[1].quiver(
            pos0[:, 0],
            pos0[:, 1],
            pos1[:, 0] - pos0[:, 0],
            pos1[:, 1] - pos0[:, 1],
            dist,
            cmap='jet',
            clim=np.percentile(dist, [1, 99]),
            angles='xy',
            scale_units='xy',
            scale=1)
        plt.colorbar(scat, ax=axs[0], shrink=0.5)
        plt.show()

    def match(self, pos0, pos1, x0, x1):
        matches = self.match_with_crosscheck(x0, x1)
        rc_idx0, rc_idx1, residuals, model = self.filter(matches, pos0, pos1)
        if rc_idx0.size / pos0.shape[0] < 0.1:
            matches = self.match_with_lowe_ratio(x0, x1)
            rc_idx0_lowe, rc_idx1_lowe, residuals_lowe, model_lowe = self.filter(matches, pos0, pos1)
            if residuals_lowe.mean() < residuals.mean():
                rc_idx0, rc_idx1, model = rc_idx0_lowe, rc_idx1_lowe, model_lowe
        return rc_idx0, rc_idx1, model

    def match_with_crosscheck(self, x0, x1):
        bf = cv2.BFMatcher(self.norm, crossCheck=True)
        matches = bf.match(x0, x1)
        return matches

    def match_with_lowe_ratio(self, x0, x1):
        bf = cv2.BFMatcher(self.norm, crossCheck=False)
        all_matches = bf.knnMatch(x0, x1, k=2)
        matches = []
        for m,n in all_matches:
            if m.distance < self.lowe_ratio*n.distance:
                matches.append(m)
        return matches

    def filter(self, matches, pos0, pos1):
        descriptor_distance = np.array([m.distance for m in matches])
        bf_idx0 = np.array([m.queryIdx for m in matches])
        bf_idx1 = np.array([m.trainIdx for m in matches])
        if self.plot: self.plot_quiver(pos0[bf_idx0], pos1[bf_idx1], descriptor_distance)

        gpi0 = np.nonzero(descriptor_distance < self.max_distance)
        dd_idx0 = bf_idx0[gpi0]
        dd_idx1 = bf_idx1[gpi0]
        if self.plot: self.plot_quiver(pos0[dd_idx0], pos1[dd_idx1], descriptor_distance[gpi0])

        gpi1 = np.hypot(pos1[dd_idx1, 0] - pos0[dd_idx0, 0], pos1[dd_idx1, 1] - pos0[dd_idx0, 1]) < self.max_drift
        md_idx0 = dd_idx0[gpi1]
        md_idx1 = dd_idx1[gpi1]
        if self.plot: self.plot_quiver(pos0[md_idx0], pos1[md_idx1], descriptor_distance[gpi0][gpi1])
        if not self.use_ransac: return md_idx0, md_idx1

        min_samples = int(self.ransac_ratio * md_idx0.size)
        model, inliers = ransac((pos0[md_idx0], pos1[md_idx1]), self.ransac_model, min_samples, self.ransac_threshold)
        gpi2 = np.nonzero(inliers)[0]
        rc_idx0 = md_idx0[gpi2]
        rc_idx1 = md_idx1[gpi2]
        residuals = model.residuals(pos0[rc_idx0], pos1[rc_idx1])
        if self.plot: self.plot_quiver(pos0[rc_idx0], pos1[rc_idx1], residuals)
        return rc_idx0, rc_idx1, residuals, model