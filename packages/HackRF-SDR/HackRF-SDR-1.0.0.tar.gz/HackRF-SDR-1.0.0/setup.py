from setuptools import setup
setup(
    name="HackRF-SDR",
    version="1.0.0",
    author="Enbuging",
    author_email="electricfan@yeah.net",
    license="MIT",
    description="A wrapper for libhackrf.dll, which can be used to access the HackRF, a software defined radio peripheral, by programs on Microsoft Windows platform.",
    keywords=["radio","SDR","HackRF","libhackrf.dll","hackrf.dll"],
    platforms=["Windows"],
    package_data={
        "hackrf":["config.json"]
    },
    install_requires=["numpy>=1.21"],
    packages=["hackrf"]
)