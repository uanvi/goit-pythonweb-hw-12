import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Contacts API'
copyright = '2025, Your Name'
author = 'Your Name'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Mock imports для залежностей які важко імпортувати
autodoc_mock_imports = [
    'fastapi', 'sqlalchemy', 'pydantic', 'jose', 'passlib', 
    'cloudinary', 'fastapi_mail', 'redis', 'slowapi'
]