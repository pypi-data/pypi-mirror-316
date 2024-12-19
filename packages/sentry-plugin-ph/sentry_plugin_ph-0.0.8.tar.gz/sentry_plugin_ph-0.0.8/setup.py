#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="sentry-plugin-ph",
    version='0.0.8',
    author='p',
    description='ph notification plugin for Sentry',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sentry>=9.0.0',
        'markdown>=3.0.0',
    ],
    entry_points={
        'sentry.plugins': [
            'dingtalk = sentry_plugin_ph.plugin:DingtalkPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ]
)
