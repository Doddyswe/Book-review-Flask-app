from setuptools import setup, find_packages

setup(
    name="Bookr",
    version="1.0",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "psycopg2",
        "Flask",
        "Flask-Session",
        "SQLAlchemy",
        "python-dotenv",
        "xmltodict",
        "requests"
        ]
)