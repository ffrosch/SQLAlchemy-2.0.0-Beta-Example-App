# SQLAlchemy 2.0.0 Beta

A simple working example of the new **SQLAlchemy** together with the most recent **SQLAlchemy-Utils**.

The `development.dev.txt` containts tools to ensure best coding practices.

A Monkey Patch of `SQLAlchemy.__version__` makes it possible to run SQLAlchemy-Utils with the 2.0Beta version.

## Features

This app uses the new support for `dataclasses` by inheriting from `MappedAsDataclass`.
Note that this is not possible in **Flask-SQLAlchemy**, because its base model already does stuff like creating an `__init__` function.

Furthermore the new typechecking-friendly **SQLAlchemy 2** idiom for ORM class creation with `Mapper` and `mapped_column` is used.

Last but not least `__mapper_args__` supplies a mechanism to automatically update the timestamp of a column.

## Usage

Simply run `python app.py` from your commandline.
This will run the commands in the `if __name__ == "__main__":` section and print out the results.
