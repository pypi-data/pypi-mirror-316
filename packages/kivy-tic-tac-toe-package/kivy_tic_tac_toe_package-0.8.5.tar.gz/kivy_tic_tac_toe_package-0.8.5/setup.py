from setuptools import setup, find_packages
setup(
    name="kivy_tic_tac_toe_package",
    version="0.8.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_tic_tac_toe_package = kivy_tic_tac_toe_package.main:main'
        ]
    },
    package_data={
        '': ['kivy_tic_tac_toe_package/*'],
    },
)
