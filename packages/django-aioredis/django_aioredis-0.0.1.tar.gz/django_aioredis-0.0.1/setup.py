from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='django-aioredis',
      version='0.1',
      description='This package provides a custom cache backend for Django that integrates with the asynchronous capabilities of the aioredis library.',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.13',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
      ],
      keywords='django redis async aioredis',
      url='https://github.com/Alireza-Tabatabaeian/django-aioredis',
      author='Alireza Tabatabaeian',
      author_email='alireza.tabatabaeian@gmail.com',
      license='MIT',
      packages=['django-aioredis'],
      install_requires=[
          'django',
          'aioredis',
      ],
      include_package_data=True,
      zip_safe=False)
