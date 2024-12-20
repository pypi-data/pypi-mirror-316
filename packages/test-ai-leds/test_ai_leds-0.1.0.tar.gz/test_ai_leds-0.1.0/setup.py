from setuptools import setup, find_packages

setup(
    name="test_ai_leds",
    version="0.1.0",
    author="LEDS",
    author_email="gabrieldpbrunetti@gmail.com",
    description="AI automated test generation" ,
    packages=find_packages(include=['testailib']),
    include_package_data=True,
    requires=[
        "crewai",
        "crewai_tools",
        "google_generativeai",
        "pyaml"
    ],
    entry_points={
        "console_scripts": [
            "testai=testailib.main:main",  # Executável que chama a função main
        ]
    }
)