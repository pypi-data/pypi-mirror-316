from setuptools import setup, find_packages

setup(
    name="sqliteorm_py",
    version="0.0.5",
    description="A lightweight SQLite ORM framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Behzad Jalili",
    author_email="jalilibhzad21@gmail.com",
    url="https://github.com/jaliliB21/sqlorm/",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "sqliteorm_py": ["templates/*.py"],
    },
    entry_points={
        "console_scripts": [
            "sqliteorm-admin = sqliteorm_py.cli:main",
        ]
    },
    install_requires=[],
    license="GPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
