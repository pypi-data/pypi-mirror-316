from setuptools import setup, find_packages
setup(
    name="Kivy_Stopwatch_package",
    version="1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'Kivy_Stopwatch_package = Kivy_Stopwatch_package.main:main'
        ]
    },
    package_data={
        '': ['Kivy_Stopwatch_package/*'],
    },
)