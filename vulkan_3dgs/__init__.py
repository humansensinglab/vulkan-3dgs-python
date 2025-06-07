import os
import platform

if platform.system() == "Darwin":  # macOS
    os.environ["MVK_CONFIG_USE_METAL_ARGUMENT_BUFFERS"] = "0"

from .vulkan_3dgs_py import run as _run

def run(path, width=None, height=None):
    shader_dir = os.path.join(os.path.dirname(__file__))+"/"
    return _run(path, shader_dir, width, height)

__all__ = ["run"]