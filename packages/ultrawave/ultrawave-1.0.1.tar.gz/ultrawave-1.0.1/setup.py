from setuptools import setup, find_packages

setup(
    name='ultrawave',               # Nama paket
    version='1.0.1',                 # Versi paket
    packages=find_packages(),        # Temukan semua paket Python dalam direktori
    test_suite='tests',              # Menentukan lokasi test
    author='Muhammad Thoyfur',
    author_email='ipungg.id@gmail.com',
    description='Lib for read UHF Scanner',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ipungg-junior/ultrawave',  # URL proyek (misalnya GitHub)
    python_requires='>=3.7',          # Versi Python yang didukung
)
