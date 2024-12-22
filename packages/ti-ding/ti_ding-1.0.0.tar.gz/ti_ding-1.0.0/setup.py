from setuptools import setup, find_packages

setup(
    name="ti-ding",
    version="1.0.0",
    description="A CLI tool to notify you with sound when a terminal process completes.",
    author="Anand Chourasia",
    author_email="anandchourasia007@gmail.com",
    packages=find_packages(),
    install_requires=[
        "playsound",
    ],
    entry_points={
        "console_scripts": [
            "notify=src.cli:run_command_with_notification",
        ],
    },
    python_requires=">=3.6",
)
