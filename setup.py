from setuptools import setup

setup(
    name='clean_folder',
    version='1',
    description='Sort all files and clear',
    url='https://github.com/VladimirKuharets/Cleaner',
    author='Volodymyr Kukharets',
    author_email='vladimir.kuharets.kiev@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    },
)
