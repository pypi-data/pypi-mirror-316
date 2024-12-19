import importlib.resources as pkg_resources

from types import SimpleNamespace
from superlimo.base_model import BaseModel
from superlimo.superpoint_open import VGGBlock
import torch
from torch import nn

class SuperLIMo(BaseModel):
    default_conf = {
        "descriptor_dim": 256,
        "nms_radius": 4,
        "max_num_keypoints": None,
        "force_num_keypoints": False,
        "superlimo_min_score": 0.05,
        "remove_borders": 4,
        "descriptor_dim": 256,
        "channels": [64, 64, 128, 128, 256],
        "dense_outputs": None,
    }

    def _init(self, conf):
        self.conf = SimpleNamespace(**conf)
        self.stride = 2 ** (len(self.conf.channels) - 2)
        channels = [2, *self.conf.channels[:-1]]

        backbone = []
        for i, c in enumerate(channels[1:], 1):
            layers = [VGGBlock(channels[i - 1], c, 3), VGGBlock(c, c, 3)]
            if i < len(channels) - 1:
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            backbone.append(nn.Sequential(*layers))
        self.backbone = nn.Sequential(*backbone)

        c = self.conf.channels[-1]
        self.detector = nn.Sequential(
            VGGBlock(channels[-1], c, 3),
            VGGBlock(c, self.stride**2 + 1, 1, relu=False),
        )
        self.descriptor = nn.Sequential(
            VGGBlock(channels[-1], c, 3),
            VGGBlock(c, self.conf.descriptor_dim, 1, relu=False),
        )
        if conf.checkpoint_url in [None, 'default']:
            checkpoint_url = pkg_resources.files('superlimo').joinpath('weights.pth')
        else:
            checkpoint_url = conf.checkpoint_url
        self.load_weights(checkpoint_url, conf.device)

    def load_weights(self, checkpoint_url, device):
        self.load_state_dict(torch.load(
            checkpoint_url,
            map_location=torch.device(device),
            weights_only=True))

    def get_scores_descriptors(self, image):
        if image.shape[1] == 3:  # RGB
            scale = image.new_tensor([0.299, 0.587, 0.114]).view(1, 3, 1, 1)
            image = (image * scale).sum(1, keepdim=True)
        features = self.backbone(image)
        descriptors_dense = torch.nn.functional.normalize(self.descriptor(features), p=2, dim=1)

        # Decode the detection scores
        scores = self.detector(features)
        return scores, descriptors_dense

    def get_keypoint_scores(self, s):
        """ Compute scores and position of keypoints

        Inputs:
            s : CNN output, [B, 65, height / 8, width / 8]
            min_kp_score : score threshold for selecting KPs

        Outputs:
            scores : scores of KPs [n_kps]
            gpi_r, gpi_c : coordinates OF 8x8 windows [n_kps]
            gpi_z        : coordinates IN 8x8 windows [n_kps]
        """

        # s is just an ouput from CNN with values ranging from ~ -10 to 10
        # sm is a probability of having a keypoint in a pixel in a 8x8 sub-window:
        #     softmax: sum of probabilities equal to 1
        #     sm.shape: torch.Size([64, 512, 512])
        #     64 = 8x8: each pixel in 64 values vector represents a pixel in 8x8 window
        sm = torch.nn.functional.softmax(s[0], 0)[:-1]
        # coordinates OF 8x8 windows with score above threshold
        # if min_kp_score == 0: coordinates of ALL 8x8 windows
        gpi_r, gpi_c = torch.where(sm.max(0).values > self.conf.superlimo_min_score)
        # coordinates IN 8x8 windows with maximum score (which pixel in 8x8 window is a KP?)
        gpi_z = sm.max(0).indices[gpi_r, gpi_c]
        # the score of the KP
        scores = sm[gpi_z, gpi_r, gpi_c]
        return scores, gpi_r, gpi_c, gpi_z

    def _forward(self, image):
        scores, descriptors = self.get_scores_descriptors(image)
        kp_scores, gpi_r, gpi_c, gpi_z = self.get_keypoint_scores(scores)
        keypoint_row = gpi_r * self.stride + self.stride/2
        keypoint_col = gpi_c * self.stride + self.stride/2
        keypoints = torch.cat([keypoint_col[None].T, keypoint_row[None].T], 1)
        descriptors = descriptors[0, :, gpi_r, gpi_c]
        return {
            'keypoints': keypoints,
            'scores': kp_scores,
            'descriptors': descriptors
        }

    def loss(self, pred, data):
        raise NotImplementedError

