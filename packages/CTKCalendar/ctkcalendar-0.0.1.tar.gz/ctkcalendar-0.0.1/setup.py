from setuptools import setup, find_packages

setup(
    name='CTKCalendar',
    version='0.0.1',
    packages=find_packages(),
    author='Claudio Morais',
    author_email='jc.morais86@gmail.com',
    description='A customized calendar to facilitate date selection in graphical interfaces.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ClaudioM1386/CTkWidgets',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'customtkinter'  # Inclui a dependência do CTkCalendar, se for um pacote separado
    ],
)
