Features
========

The goal of czml3 is to make the process of writing CZML files in Python.

Type Checking
-------------

czml3 is built upon Pydantic. Therefore, all classes enforces type checking on the inputs. This ensures that the data is in the correct format before it is written to the CZML file.

Cooercion of Data
-----------------

Again, czml3 is build upon Pydantic. Therefore, czml3 is able to `coerce data to their right type <https://docs.pydantic.dev/latest/why/#json-schema>`_. See Example 2 in  :ref:`examples-label`.

Minimal CZML File Creation
--------------------------

czml3 will remove all fields that are not set (i.e. ``None``). This ensures that the CZML file is as small as possible.
