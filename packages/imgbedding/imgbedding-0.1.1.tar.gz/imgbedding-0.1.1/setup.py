from setuptools import setup

setup(
    name="imgbedding",
    packages=["imgbedding"],  # this must be the same as the name above
    version="0.1.1",
    description="A Python package to generate image embeddings with CLIP without PyTorch/TensorFlow (UPDATED)",
    # long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Malay Damani",
    author_email="damanimalay@gmail.com",
    keywords=[
        "ai",
        "transformers",
        "onnx",
        "images",
        "image-processing",
        "embeddings",
        "clip",
    ],
    classifiers=[],
    license="MIT",
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        "transformers>=4.17.0",
        "onnxruntime>=1.10.0",
        "Pillow",
        "tqdm",
        "scikit-learn",
    ],
)