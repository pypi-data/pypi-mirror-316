from setuptools import setup, find_packages

setup(
    name='library_package',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,  # Paket ile ekstra dosyaları dahil etmek için
    package_data={
        'library_package': ['resources/*.txt'],
    },
    install_requires=[],
    description='A sample package',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/my_package',
    #author='Your Name',
    #author_email='your.email@example.com',
    #license='MIT',
)