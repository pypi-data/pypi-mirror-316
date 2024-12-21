import os
from importlib import resources
from sandlersteam.util import data_path

def test_data_location():
    with resources.as_file(resources.files('sandlersteam')) as src_root:
        inst_root=src_root.parent.parent
        dp=data_path()
        assert dp==os.path.join(inst_root,'data')