# Resize Photos

Resize Photos is an application that consumes images from an external
endpoint and generate three different photo formats for each one, they are:
small (320x240), medium (384x288) and large (640x480).

# Run App

Before running the app, make sure you have both Python 3
and `pip` installed on your system.

## Dependencies

This application depends on external libraries to be fully
operational, in order to download all of them type the
following commands on your terminal:

    $ cd resizephotos
    $ pip install -r requirements.txt

Now that you downloaded all project requirements,
you can run the application by typing on your terminal:

    $ cd resizephotos
    $ python app.py

# Run Tests

If you want to run all unit tests of this application simply
type the following commands:

    $ cd resizephotos
    $ python -m unittest discover

The `discover` option above will find the `tests` package,
and execute all tests existing in this package.
