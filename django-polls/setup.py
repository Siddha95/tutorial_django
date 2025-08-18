import os
from pathlib import Path
from setuptools import find_packages, setup

BASE_DIR = Path(__file__).resolve().parent
README = (BASE_DIR / 'README.rst').read_text(encoding='utf-8')

# Allow running from any path
os.chdir(str(BASE_DIR))

setup(
    name='django-polls',
    version='0.1.1',  # bumped version
    packages=find_packages(exclude=('tests', 'tests.*')),  # exclude standalone test dirs if any
    include_package_data=True,
    license='BSD-3-Clause',  # clearer SPDX style label
    description='A simple reusable Django app to conduct web-based polls.',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://example.com/django-polls',
    project_urls={
        'Source': 'https://example.com/django-polls',
        'Tracker': 'https://example.com/django-polls/issues',
    },
    author='Your Name',
    author_email='yourname@example.com',
    python_requires='>=3.6',  # adjust if you only target newer
    install_requires=[
        'Django>=1.11,<2.0',  # code uses url() patterns; tighten upper bound
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='django polls app example tutorial',
)