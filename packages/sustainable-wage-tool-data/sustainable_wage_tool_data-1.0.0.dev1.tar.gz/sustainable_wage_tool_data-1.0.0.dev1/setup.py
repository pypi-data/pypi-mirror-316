from setuptools import setup

# read the contents of your README file as GitHub-flavored Markdown
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sustainable_wage_tool_data',
    version='1.0.0.dev1',
    packages=['sustainable_wage_tool_data'],
    install_requires=[  
        'beautifulsoup4==4.12.3',
        'pdfplumber==0.11.4',
        'polars==1.9.0',
        'Requests==2.32.3',
        'selenium==4.25.0',
        'XlsxWriter==3.2.0',
        'fastexcel',
        'argparse'
    ],
    author='Angel Febles'
)