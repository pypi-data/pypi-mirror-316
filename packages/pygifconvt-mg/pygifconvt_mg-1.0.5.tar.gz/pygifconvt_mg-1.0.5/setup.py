from setuptools import setup, find_packages

setup(
    name             = 'pygifconvt_mg',
    version          = '1.0.5',
    description      = 'Test package for distribution',
    author           = 'kmg6522',
    author_email     = 'ddmr0608@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = ['pillow'],     # 내장함수에 해당하는 glob은 필요없음
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['GIFCONVERTER', 'gifconverter'],   # 검색할때 나오는 키워드
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 