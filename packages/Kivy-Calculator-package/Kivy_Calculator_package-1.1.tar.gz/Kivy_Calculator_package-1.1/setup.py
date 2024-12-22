from setuptools import setup, find_packages
setup(
    name="Kivy_Calculator_package",
    version="1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'Kivy_Calculator_package = Kivy_Calculator_package.main:main'
        ]
    },
    package_data={
        '': ['Kivy_Calculator_package/*'],
    },
)