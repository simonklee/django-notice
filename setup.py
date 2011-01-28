import os
from setuptools import setup, find_packages

setup(
    author='Simon Zimmermann',
    author_email='simonz05@gmail.com',
    description='django-notice is an application to send messages.',
    include_package_data=True,
    #install_requires=['simplejson', 'redis'],
    license='GPL',
    long_description=open('README').read(),
    name='django-notice',
    packages=find_packages(),
    url='http://github.com/simonz05/django-notice',
    version='0.1.2',
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
