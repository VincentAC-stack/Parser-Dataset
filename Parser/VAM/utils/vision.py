"""Utility functions related to vision"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import torch
import torchvision.utils as vutils


def plot_images(batch: torch.Tensor, title: str):
    """Plot a batch of images

    Args:
        batch: (torch.Tensor) a batch of images with dimensions (batch, channels, height, width)
        title: (str) title of the plot and saved file
    """
    n_samples = batch.size(0)
    plt.figure(figsize=(n_samples // 2, n_samples // 2))
    plt.axis("off")
    plt.title(title)
    plt.imshow(
        np.transpose(vutils.make_grid(batch, padding=2, normalize=True), (1, 2, 0))
    )
    plt.savefig(f"{title}.png")


def draw_on_image(img, true_actions, action, gt=True):
    """Draw text on the image

    Args:
        img: (torch.Tensor) frame
        measurements: (dict) ground truth actions
        action: (torch.Tensor) predicted actions
        gt: whether to draw true action or not
    """
    # if measurements:
    linear_gt = true_actions[0].item()
    angular_gt = true_actions[1].item()

    linear = action[0].item()
    angular = action[1].item()

    upsampler = torch.nn.Upsample(scale_factor=8, mode='bilinear')
    if len(img.shape) < 4:
        img.unsqueeze_(0)
    img = upsampler(img).squeeze(0).permute(1, 2, 0).numpy()
    img_width = img.shape[1] // 2
    img = Image.fromarray(
        (((img - img.min()) / (-img.min() + img.max())) * 255).astype(np.uint8)
    )
    draw = ImageDraw.Draw(img)
    # load font
    fnt_path = Path(__file__).parent.parent / "misc_files/FUTURAM.ttf"
    fnt = ImageFont.truetype(str(fnt_path), 18)
    draw.text((5, 30), f"Linear_Vel: {linear:.3f}", fill="red", font=fnt)
    draw.text((5, 60), f"Angular_Vel: {angular:.3f}", fill="red", font=fnt)

    if gt:
        draw.text(
            (img_width * 2 - 200, 30), f"Linear_Vel: {linear_gt:.3f}", fill="green", font=fnt
        )
        draw.text(
            (img_width * 2 - 200, 60), f"Angular_Vel: {angular_gt:.3f}", fill="green", font=fnt
        )

    return np.array(img)


if __name__ == "__main__":
    img = torch.from_numpy(plt.imread('34.jpg')).permute(2, 0, 1)
    img = draw_on_image(img, torch.tensor([2, 4], dtype=torch.float), torch.tensor([6, 8], dtype=torch.float))
    plt.imshow(img)
    plt.show()
