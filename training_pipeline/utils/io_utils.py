import os
import torch
import argparse
from datetime import datetime


def get_runtime_str():
    """Getting datetime as a string"""

    runtime_str = (
        datetime.now().isoformat().replace(":", "").replace("-", "").replace("T", "-").split(".")[0]
    )
    return runtime_str


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_name",
        default="mnist",
        required=False,  # it should be true by default and no default value
        type=str,
        help="name of the config to be uses",
    )
    args = parser.parse_args()

    return args.config_name


def save_model(cfg, model, runtime_str):
    project_name = cfg.project_name
    save_dir = cfg.training.save_dir

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{project_name}_{runtime_str}.pth")
    torch.save(obj=model, f=save_path)

    return None