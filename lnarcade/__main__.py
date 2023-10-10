# def main():
#     """ This is the entry point for the application when called from the command line. """
#     from lnarcade.app import App
#     App.get_instance().start()

# This should only be used when trying to run this python module with `python -m lnarcade`
# ...but we are installing it as a package so this should not be used.
if __name__ == '__main__':
    from lnarcade.app import main
    main()
