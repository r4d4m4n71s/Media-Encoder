import os
import sys

# Get the directory containing the package
package_dir = os.path.dirname(os.path.abspath(__file__))

# Add media_encoder directory to Python path for internal imports
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# Make all modules available
__all__ = [
    'models',
    'encoder',
    'encoder_cli',
    'utils',
    'config',
    'data_manager',
    'meta_updater'
]

# Clean up namespace
del os, sys, package_dir