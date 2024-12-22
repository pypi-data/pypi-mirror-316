from setuptools import setup, find_packages
setup(
    name="kivy_snake_package",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_snake = kivy_snake.__main__:main'
        ]
    },
    package_data={
        '': ['kivy_snake_package/*'],
    },
)
