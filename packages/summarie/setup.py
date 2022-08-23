import setuptools

with open("./requirements.txt", "r") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="summarie",
    version="0.0.1",
    author="k4rim",
    install_requires=required,
    author_email="xk4rim@gmail.com",
    packages=setuptools.find_packages(),
)
