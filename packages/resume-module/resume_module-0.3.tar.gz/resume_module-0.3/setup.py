# setup.py
from setuptools import setup, find_packages

setup(
    name="resume_module", 
    version="0.3",  
    description="A module to generate and save professional resumes as PDFs using OpenAI",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author_email="string2025@gmail.com",  
    url="https://github.com/ibrahim-string/resume_module", 
    packages=find_packages(), 
    install_requires=[ 
        "openai",  
        "fpdf",  
        "python-dotenv",  
    ],
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
