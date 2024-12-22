from setuptools import setup, find_packages
setup(
    name="kivy_music_player_package",
    version="1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_music_player_package = kivy_music_player_package.main:main'
        ]
    },
    package_data={
        '': ['kivy_music_player_package/*'],
    },
)
