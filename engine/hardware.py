"""
Hardware detection and configuration for CUDA/CPU optimization
"""

import torch
import platform
from typing import Dict, Any


def detect_hardware() -> Dict[str, Any]:
    """
    Detect available hardware and return optimal configuration.
    
    Returns:
        Dict containing device type, compute type, and device index
    """
    cuda_available = torch.cuda.is_available()
    
    hardware_info = {
        "device": "cuda" if cuda_available else "cpu",
        "cuda_available": cuda_available,
        "device_name": None,
        "compute_type": None,
    }
    
    if cuda_available:
        hardware_info["device_name"] = torch.cuda.get_device_name(0)
        hardware_info["compute_type"] = "float16"  # Use FP16 for GPU
        print(f"✓ CUDA GPU detected: {hardware_info['device_name']}")
        print(f"  Using compute type: {hardware_info['compute_type']}")
    else:
        hardware_info["device_name"] = "CPU"

        # Use int8 for CPU performance unless on macOS where float32 is needed for stability
        if platform.system() == "Darwin":
            hardware_info["compute_type"] = "float32"
            print(f"⚠ macOS detected. Using CPU with float32 (for stability)")
        else:
            hardware_info["compute_type"] = "int8"
            print(f"⚠ No CUDA GPU detected. Using CPU with int8 (quantized)")

        print(f"  Note: CPU processing will be slower than GPU")
    
    return hardware_info


def get_device_config() -> tuple[str, str]:
    """
    Get device and compute type configuration for faster-whisper.
    
    Returns:
        Tuple of (device, compute_type)
    """
    info = detect_hardware()
    return info["device"], info["compute_type"]


if __name__ == "__main__":
    # Test hardware detection
    print("Testing hardware detection...")
    print("-" * 50)
    hardware = detect_hardware()
    print("-" * 50)
    print(f"\nConfiguration: {hardware}")
