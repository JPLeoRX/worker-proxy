from setuptools import setup, find_packages


setup_args = dict(
    name='worker-proxy-utils',
    version='0.1',
    description='',
    keywords=[],
    long_description='',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author="Leo Ertuna",
    author_email="leo.ertuna@gmail.com",
)


install_requires = [
    'injectable'
]


if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
