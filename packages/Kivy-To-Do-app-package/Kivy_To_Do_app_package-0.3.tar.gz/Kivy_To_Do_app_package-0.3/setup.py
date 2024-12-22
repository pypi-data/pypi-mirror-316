from setuptools import setup, find_packages
setup(
    name="Kivy_To_Do_app_package",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Kivy",
    ],
    entry_points={
        'console_scripts': [
            'Kivy_To_Do_app_package = Kivy_To_Do_app_package.main:main'
        ]
    },
    package_data={
        '': ['Kivy_To_Do_app_package/*'],
    },
)