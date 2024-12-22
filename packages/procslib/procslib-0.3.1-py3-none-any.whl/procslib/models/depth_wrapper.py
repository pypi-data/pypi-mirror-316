import os
from typing import List

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import DPTForDepthEstimation, DPTImageProcessor

# Assume that these are defined elsewhere or adapt as needed:
from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class DepthEstimationInference(BaseImageInference):
    """Depth inference class using DPTForDepthEstimation and DPTImageProcessor.
    Computes a depthness score based on percentile differences.
    Optionally saves depth maps if output_dir is provided.

    Args:
        device (str): Device to run on.
        batch_size (int): Batch size for inference.
        lower_percentile (int): Lower percentile for depthness calculation.
        upper_percentile (int): Upper percentile for depthness calculation.
        output_dir (str): Directory to save depth images (as webp). If None, no saving is done.
    """

    def __init__(
        self,
        device="cuda",
        batch_size=32,
        lower_percentile=15,
        upper_percentile=95,
        # output_dir=None
    ):
        super().__init__(device=device, batch_size=batch_size)
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        # self.output_dir = output_dir
        # if self.output_dir:
        #     os.makedirs(self.output_dir, exist_ok=True)
        self._load_model(None)

    def _load_model(self, checkpoint_path: str = None):
        self.feature_extractor = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
        self.model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas").to(self.device)
        self.model.eval()

    def _preprocess_image(self, pil_image: Image.Image):
        inputs = self.feature_extractor(images=pil_image, return_tensors="pt")
        return inputs.pixel_values.squeeze(0)

    def _postprocess_output(self, depth_map: torch.Tensor):
        # depth_map shape: [B, H, W] or [B, 1, H, W] from model (check model output)
        # The model returns predicted_depth: [B, H, W]
        # Add a channel dimension if missing
        if depth_map.ndim == 3:
            depth_map = depth_map.unsqueeze(1)

        # Resize/normalize depth map to a fixed resolution (1024x1024)
        depth_map = F.interpolate(
            depth_map,
            size=(1024, 1024),
            mode="bicubic",
            align_corners=False,
        )

        # Normalize depth values between 0 and 1
        depth_min = torch.amin(depth_map, dim=[1, 2, 3], keepdim=True)
        depth_max = torch.amax(depth_map, dim=[1, 2, 3], keepdim=True)
        depth_map_norm = (depth_map - depth_min) / (depth_max - depth_min + 1e-8)

        results = []
        for i in range(depth_map_norm.size(0)):
            dm = depth_map_norm[i].squeeze().cpu().numpy()
            depth_values = dm.flatten()
            p_low = np.percentile(depth_values, self.lower_percentile)
            p_high = np.percentile(depth_values, self.upper_percentile)
            depthness_score = float(p_high - p_low)

            # Create depth image
            # depth_image_np = (dm * 255.0).clip(0, 255).astype(np.uint8)
            # depth_image_pil = Image.fromarray(depth_image_np)

            results.append(
                {
                    "depth_score": depthness_score,
                    # "depth_image": depth_image_pil,
                },
            )
        return results

    def infer_many(self, image_paths: List[str]):
        # Same approach as BaseImageInference, but after we get predictions,
        # we also save depth images if output_dir is not None.
        dataset = ImagePathDataset(image_paths, preprocess_fn=self._preprocess_image)
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=0,  # Avoid dynamic transform pickling issues
            pin_memory=True,
            collate_fn=custom_collate,
        )

        self.model.eval()
        results = []
        with torch.no_grad(), torch.autocast(self.device if "cuda" in self.device else "cpu"):
            for batch in tqdm(dataloader, desc="Inferring paths"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device)
                output = self.model(images)
                batch_results = self._postprocess_output(output.predicted_depth)

                for path, res in zip(paths, batch_results):
                    filename = os.path.basename(path)
                    res["filename"] = filename

                    # Save depth image if output_dir is provided
                    # if self.output_dir is not None:
                    #     base_name = Path(path).stem
                    #     depth_image_path = Path(self.output_dir) / f"{base_name}.depth.webp"
                    #     res["depth_image"].save(depth_image_path)
                    # del res["depth_image"]  # Remove PIL image from final results

                    results.append(res)

        return pd.DataFrame(results)


import glob


# Demo usage
def demo_depth_wrapper():
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")
    inference = DepthEstimationInference(
        device="cuda",
        batch_size=24,
        lower_percentile=15,
        upper_percentile=95,
    )

    # Many images (parallelized with ProcessPoolExecutor)
    df = inference.infer_many(image_paths)
    df.to_csv("depth_scores.csv", index=False)
    print("Inference completed. Results saved to 'depth_scores.csv'.")


if __name__ == "__main__":
    demo_depth_wrapper()
