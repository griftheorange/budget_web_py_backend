Init Framework for budgeting application using pandas/flask backend and temporary React Frontend. Python classes and method should be formatted to favor refactoring into an electron app later on.

Code flow works like this: router always routes to data_handler for data manip, but if router needs to return a json format, it routes to data_handler *through* json_parser. The loader controller is exclusively used by the data_handlers class to save files, and load file into dataframes for further manip. Dataframes are returned to data_handler, manipulation is done and will be output where necessary.

Note to self:
- run 'budget' to execute both commands below in one step
- run 'bback' to open and start flask server
- run 'bfront' to open and start react frontend development mode
