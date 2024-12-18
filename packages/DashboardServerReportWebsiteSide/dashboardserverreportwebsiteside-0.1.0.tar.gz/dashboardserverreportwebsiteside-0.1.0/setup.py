from setuptools import setup, find_packages

setup(
    name='DashboardServerReportWebsiteSide',
    version='0.1.0',
    author='Unknown',
    author_email='unknown@example.com',
    description='A website monitoring tool for performance, security, SEO, and UI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/DashboardServerReportWebsiteSide',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
