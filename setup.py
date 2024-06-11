import setuptools

with open('./requirements.txt') as requirements_file:
    install_requires = requirements_file.readlines()

scripts = ['./macdonalds_menu/menu_parser/scripts/parse_menu.py']

setuptools.setup(
    name='mac-fullmenu',
    version='0.1.0',
    python_requires='>=3.10',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points='''
    [console_scripts]
    parse_menu=macdonalds_menu.menu_parser.scripts.parse_menu:parse_menu_cli
    run-flask-app=macdonalds_menu.app:main

    ''',
    scripts=scripts
)
