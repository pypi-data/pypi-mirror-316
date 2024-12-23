from setuptools import setup, find_packages

setup(
    name="streamlit-colab",
    version="0.1.5",
    description="Run Streamlit apps on Google Colab with ease",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Wuhp",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/streamlit-colab",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.0.0",
        "pyngrok>=5.0.0"
    ],
    entry_points={
        "console_scripts": [
            "stc=streamlit_colab.core:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
