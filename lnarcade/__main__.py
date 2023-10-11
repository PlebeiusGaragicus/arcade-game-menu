# This should only be used when trying to run this python module with `python -m lnarcade`
# ...but we are installing it as a package so this should not be used.
if __name__ == '__main__':
    from lnarcade.app import App
    App.get_instance().start()

# print("This should not be used.  Please install with `pip install .` and run 'lnarcade' instead.")
# exit(1)
