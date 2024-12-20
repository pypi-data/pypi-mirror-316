from setuptools import setup, find_packages

setup(
    name="minimal_program_tester", 
    version="0.0.3",  
    description="A really minimalistic program tester",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown", 
    author="Dewliak",  
    author_email="veres.z.benedek@gmail.com",  
    packages=find_packages(),  
    python_requires=">=3.10",  
    install_requires=[
        "colorama", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  
    zip_safe=True,  
)
