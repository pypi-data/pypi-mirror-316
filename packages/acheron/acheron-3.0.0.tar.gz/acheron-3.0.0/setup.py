import setuptools
import sys


class BinaryDistribution(setuptools.Distribution):
    def has_ext_modules(self):
        return True


try:
    from wheel.bdist_wheel import bdist_wheel

    class CustomBdistWheel(bdist_wheel):
        def run(self):
            clean = self.reinitialize_command('clean')
            clean.all = True
            self.run_command('clean')
            bdist_wheel.run(self)

        def get_tag(self):
            rv = bdist_wheel.get_tag(self)
            l = [self.python_tag, 'none']
            l.extend(rv[2:])
            return tuple(l)

        def finalize_options(self):
            bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    CustomBdistWheel = None  # type: ignore

package_data = {"acheron": ["html/*"]}

if sys.platform == "win32":
    is_64bit = sys.maxsize > (2 ** 32)
    if is_64bit:
        package_data['acheron'].append('7zip_64bit/*')
    else:
        package_data['acheron'].append('7zip_32bit/*')
        raise NotImplementedError("32-bit builds no longer supported!")
    distclass = BinaryDistribution
    cmdclass = {'bdist_wheel': CustomBdistWheel}
else:
    distclass = setuptools.Distribution
    cmdclass = {}


def no_local_develop_scheme(version):
    if version.branch == "develop" and not version.dirty:
        return ""
    else:
        from setuptools_scm.version import get_local_node_and_date
        return get_local_node_and_date(version)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="acheron",
    use_scm_version={'write_to': 'acheron/version.py',
                     'local_scheme': no_local_develop_scheme},
    setup_requires=['setuptools_scm<7.0'],
    author="Suprock Technologies, LLC",
    author_email="inquiries@suprocktech.com",
    description="Plotting and recording program for Asphodel devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/suprocktech/acheron",
    packages=setuptools.find_packages(exclude=["test", "test.*"]),
    keywords="asphodel suprock apd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.10",
    install_requires=[
        "asphodel",
        "boto3",
        "croniter",
        "diskcache",
        "hyperborea",
        "intervaltree",
        "numpy",
        "packaging",
        "psutil",
        "pydantic",
        "pymodbus>=2.5.3,<3",
        "pyqtgraph",
        "pyserial",
        "PySide6-Essentials",
        "requests",
        "setproctitle",
    ],
    entry_points={
        'gui_scripts': [
            'acheron = acheron.gui.__main__:main',
        ],
        'console_scripts': [
            'acheron-cli = acheron.core.__main__:main',
        ],
    },
    package_data=package_data,
    distclass=distclass,
    cmdclass=cmdclass,
)
