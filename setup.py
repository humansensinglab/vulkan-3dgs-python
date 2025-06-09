import os
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

def download_sample_data():
    """Download sample 3DGS data"""
    import requests
    data_dir = Path("vulkan_3dgs/data")
    data_dir.mkdir(exist_ok=True)
    
    sample_file = data_dir / "bonsai.ply"
    
    if not sample_file.exists():
        print("Downloading sample 3DGS data...")
        url = "https://huggingface.co/datasets/dylanebert/3dgs/resolve/main/bonsai/point_cloud/iteration_30000/point_cloud.ply?download=true"
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(sample_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded sample data to {sample_file}")
        except Exception as e:
            print(f"Failed to download sample data: {e}")
    else:
        print(f"Sample data already exists at {sample_file}")

def build_cmake():
    """Build CMake project with Python bindings"""
    cmake_source_dir = Path("vulkan_3dgs/csrc/3dgs-vulkan-cpp")
    build_dir = cmake_source_dir / "build"
    build_dir.mkdir(exist_ok=True)
    
    print("Running CMake build...")
    
    subprocess.check_call([
        "cmake", 
        "-DBUILD_PYTHON_BINDING=ON",
        ".."
    ], cwd=build_dir)

    subprocess.check_call([
        "cmake", 
        "--build", 
        ".",
        "--config", 
        "Release",
    ], cwd=build_dir)

    import glob
    import platform

    if platform.system() in ["Darwin", "Linux"]:  # macOS and Linux
        built_modules = glob.glob(str(build_dir / "vulkan-3dgs" / "vulkan_3dgs_py.*"))
    else:  # Windows
        built_modules = glob.glob(str(build_dir / "vulkan-3dgs" / "*" / "vulkan_3dgs_py.*"))

    if built_modules:
        import shutil
        dest = Path("vulkan_3dgs") / Path(built_modules[0]).name
        python_modules = [f for f in built_modules if f.endswith(('.pyd', '.so'))]
        if python_modules:
            shutil.copy2(python_modules[0], dest)

    shutil.copytree("vulkan_3dgs/csrc/3dgs-vulkan-cpp/vulkan-3dgs/src/Shaders", 
               "vulkan_3dgs/Shaders", dirs_exist_ok=True)

class CustomInstall(install):
    def run(self):
        download_sample_data()
        build_cmake()
        super().run()

class CustomDevelop(develop):
    def run(self):
        download_sample_data()
        build_cmake()
        super().run()

class CustomBuild(build_py):
    def run(self):
        download_sample_data()
        build_cmake()
        super().run()

setup(
    name="vulkan-3dgs",  
    cmdclass={
        "build_py": CustomBuild, 
        "install": CustomInstall,
        "develop": CustomDevelop  
    }
)
