# fixme: performance
from setuptools import setup, find_packages

setup(
    name="claudemcp",
    version="0.1.0",
    description="MCP plugins for Claude Desktop",
    author="chu2bard",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.0",
        "requests>=2.31",
        "pydantic>=2.0",
    ],
)
