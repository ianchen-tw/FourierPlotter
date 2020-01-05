import setuptools
setuptools.setup(
  name = "fourierplotter",
  version="0.0.1",
  author="Ian Chen",
  author_email="ianre657@gmail.com",
  description="Use complex Fourier Analysis to draw svg images",
  # long_description=long_descriptio,
  # long_description_content_type="text/markdown",
  url="https://github.com/ianre657/FourierPlotter",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  entry_points={
    'console_scripts': ['fourierplotter=fourierplotter.__main__:fourier_plotter']
  }
)