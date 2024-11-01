# blog/__init__.py

# You can define the version of your app
__version__ = '1.0.0'

# You can also import specific classes or functions if needed
# from .models import Post  # Example of importing a model

# Example of a simple initialization function
def ready():
    """
    App ready function that can be used to perform any startup tasks.
    """
    print("Blog app is ready!")