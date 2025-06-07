import os
from .vulkan_3dgs_py import run as _run

def run(path, width=None, height=None):
    shader_dir = os.path.join(os.path.dirname(__file__))+"/"
    return _run(path, shader_dir, width, height)

__all__ = ["run"]