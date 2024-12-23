from setuptools import setup, find_packages

setup(
    name='portableDB',
    version='1.4',
    author='DoubleSquad',
    description="This library is an easyest way to use local database!",
    long_description="""
    Here is an example:

    from portableDB import DATABASE

    DTB = DATABASE()
    DTB.LogState('COLORFUL') #'BASE' - just normal cmd, 'NONE' - no comments when working
    DTB.Create_Database('Database') #'Database' - name

    DTB.Write_Database('Database',['String value1', 32], 1) #'Database' - name, [] - here should be your values, 1 - index (can be only positive number)

    print(DTB.Read_Database('Database', 1, 'ALL')) #'Database' - name, 1 - index, 'ALL' - index of array ('ALL' or any index of value in array)

    DTB.Rename_Database('Database','DB') #'Database' - current name, 'DB' - new name

    DTB.Change_File_Type('','db') #'' - idk why it should be here, but without it, it will never work (:, 'db' - should be like current type, ALWAYS
    DTB.Change_File_Type('DB','txt') #'DB' - name, 'txt' - new format (can be any except some not text formats (like mp4 LOL) and ALWAYS preverous line should be like in this example)


    DTB.Delete_Database('Database') #No comments
    """,
    packages=find_packages(),
    install_requires=[
        'colorama>=0.4.6'
    ],
)