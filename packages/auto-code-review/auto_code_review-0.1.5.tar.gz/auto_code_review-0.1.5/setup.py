from setuptools import setup, find_packages
from pathlib import Path

# Чтение содержимого README.md
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="auto-code-review",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "openai>=0.27",
        "jinja2>=3.0,<4.0",
        "PyYAML>=6.0",
        "requests>=2.26.0",
    ],
    description="Auto code review for PR in GitHub",
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    author="Dmitry Geyvandov",
    author_email="geyvandovdd@gmail.com",
    url="https://github.com/yosuke-yuikimatsu/auto-code-review",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'auto-code-review = auto_code_review.cli:main',
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "auto_code_review": ["prompts/*.jinja2"], 
    },
)
