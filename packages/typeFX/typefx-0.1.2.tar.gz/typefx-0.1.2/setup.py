from setuptools import setup, find_packages

setup(
    name='typeFX',  # The name of your package
    version='0.1.2',  # The version of your package
    description='A package with a typing effect and sound',  # Short description
    long_description='A Python package that creates a typing effect with sound. It uses Pygame to play a sound effect each time a key is typed.',
    long_description_content_type='text/markdown', # The type of content in the long description
    author='Diego Escalante',  # Add your name or your organization's name
    author_email='3dpr1nt3rb0y@gmail.com',  # Add your email for contact
    url='https://github.com/Blend3r/typeFX',  # URL to your GitHub repository
    packages=find_packages(),  # Automatically find packages in your project
    include_package_data=True,  # Include non-Python files specified in package_data
    package_data={
        'typeFX': ['sounds/spacebar-click-keyboard-199448-[AudioTrimmer.com].mp3'],  # Make sure this path is correct
    },
    classifiers=[
        'Programming Language :: Python :: 3',  # Python version
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # OS compatibility
    ],
    install_requires=['pygame'],  # Add any dependencies your package needs
    python_requires='>=3.13',  # Minimum required Python version
)
