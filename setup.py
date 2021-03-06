from setuptools import setup, find_packages
from os import path

setup(name='audio_effects',
      packages=find_packages(),
      version='0.22',
      license='LGPLv2.1',
      description=
      'Some audio effects such as delay, speed changes implemented in python',
      author='Rainbow-Dreamer',
      author_email='1036889495@qq.com',
      url='https://github.com/Rainbow-Dreamer/audio_effects',
      download_url=
      'https://github.com/Rainbow-Dreamer/audio_effects/archive/0.22.tar.gz',
      keywords=['python', 'audio', 'effects'],
      install_requires=['pydub', 'numpy'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
      long_description=open('README.md', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      include_package_data=True)
