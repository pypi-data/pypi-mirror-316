from setuptools import setup, find_packages


setup(
    name="my_socket_library",
    version="0.1.0",
    author="Anonymous",  # Можно оставить пустым или указать "Unknown"
    author_email="anonymous@example.com",  # Можно оставить пустым или указать "unknown@example.com"
    description="Библиотека для клиент-серверного взаимодействия через сокеты",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",  # Можно оставить пустым, если нет репозитория
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'my_socket_cli=my_socket_library.cli:main',
        ],
    },
)
