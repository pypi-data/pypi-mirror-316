from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='flet_navigator',
    version='3.8.5',
    author='Evan',
    author_email='name1not1found.com@gmail.com',
    description='⚡⚓ Minimalistic, fast, and powerful navigation library for Flet applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xzripper/flet_navigator',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers'],
    keywords=['navigator', 'router', 'utility', 'flet'],
    packages=['flet_navigator'],
    python_requires='>=3.9',
)
