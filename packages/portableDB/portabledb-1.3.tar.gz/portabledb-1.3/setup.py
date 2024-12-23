from setuptools import setup, find_packages

setup(
    name='portableDB',
    version='1.3',
    author='DoubleSquad',
    description="This library is an easyest way to use local database!",
    long_description="""
    Here is an example:

    from portableDB import DATABASE

    DTB = DATABASE()
    DTB.LogState('COLORFUL')
    DTB.Create_Database('TXT')

    DTB.Write_Database('TXT',['hello worleed', 'loeel', 'poefen', 'poefsdadsen', 'poefasdasfqweren', 'poe42742fen', 'poe42745274862fen', 'poe42742y84fe4564676754n'], 1)

    mass = ['1','2','3']
    DTB.Write_Database('TXT',mass, 1)

    print(DTB.Read_Database('TXT', 1, '2'))

    DTB.Rename_Database('TXT','DB')

    DTB.Change_File_Type('','db')    # txt
    DTB.Change_File_Type('DB','txt') # db


    DTB.Delete_Database('TXT')
    """,
    packages=find_packages(),
    install_requires=[
        'colorama>=0.4.6'
    ],
)