from setuptools import setup, find_packages

setup(
    name="PredictorNachiket",  # Your library's name
    version="0.2",     # Initial version
    description="A Python library for making predictions using a pre-trained model.",
    author="Nachiket", # Your name
    author_email="nachiketshinde2004@gmail.com",  # Replace with your email
    url="https://github.com/Nachiket858",   # Link to your repository
    packages=find_packages(),              # Automatically find package folders
    install_requires=[
        "numpy",
        "requests",
        "scikit-learn"  # Required for predictions
    ],
    python_requires=">=3.6",               # Minimum Python version required
)
