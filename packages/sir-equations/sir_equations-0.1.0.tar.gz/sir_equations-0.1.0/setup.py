from setuptools import setup, find_packages

setup(
    name="sir-equations",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
    ],
    author="Sai Ganesh Kolan",
    author_email="vgreddy0128@gmail.com",
    description="Advanced epidemiological model combining SIR dynamics with social-psychological behavior patterns",
)