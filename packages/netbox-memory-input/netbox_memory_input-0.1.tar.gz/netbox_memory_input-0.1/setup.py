from setuptools import find_packages, setup

setup(
    name='netbox_memory_input',
    version='0.1',
    description='Input VM memory in GB instead of MB in NetBox.',
    url='https://itandtel.at',
    author='jannis',
    license='AGPLv3',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

