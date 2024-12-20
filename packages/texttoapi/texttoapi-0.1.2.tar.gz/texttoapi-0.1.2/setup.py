from setuptools import setup, find_packages

setup(
    name="texttoapi",
    version="0.1.2",  
    description="A package for the TextToAPI tool",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,  
    install_requires=[
        "setuptools",
        "python-dotenv",
        "llama-index",
        "llama-index-embeddings-azure-openai",
        "llama-index-llms-azure-openai",
        "openinference-instrumentation-llama-index",
        "opentelemetry-sdk",
        "opentelemetry-exporter-otlp",
        "opentelemetry-proto",
        "rich",
        "Flask",
    ],
    python_requires=">=3.7",
)
