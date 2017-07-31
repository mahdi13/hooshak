from hooshak.amazon.importer import AmazonImporter

"""
We will predict the user's votes and compare it with reality to find out error.
The goal is to finding the algorithm with minimum error.

"""


if __name__ == '__main__':

    for useruid, entityuid, value, timestamp in AmazonImporter.seek_file():
        pass
