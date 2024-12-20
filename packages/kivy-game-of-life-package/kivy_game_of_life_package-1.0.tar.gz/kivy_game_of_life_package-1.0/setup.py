from setuptools import setup, find_packages
setup(
    name="kivy_game_of_life_package",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_game_of_life = kivy_game_of_life.__main__:main'
        ]
    },
    package_data={
        '': ['kivy_game_of_life_package/*'],
    },
)
