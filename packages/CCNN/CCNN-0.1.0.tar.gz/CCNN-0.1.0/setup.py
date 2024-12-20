import setuptools

setuptools.setup(
    name='CCNN',
    version='0.1.0',
    author='Hamza Mehyedden',
    description='Q Network Implementation',
    long_description='This package implements a Q-Network for reinforcement learning applications.',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add your package dependencies here, e.g.,
        'tensorflow>=1.15.0,<2.0',  # Example: TensorFlow for Q-network
        'numpy',                    # Example: NumPy for numerical operations
    ],
)
