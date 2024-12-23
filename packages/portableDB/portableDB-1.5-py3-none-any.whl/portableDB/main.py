import os
# try:
#     from colorama import Fore, init
# except ImportError:
#     import subprocess
#     import sys
#     print("colorama is not installed. Installing...")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
#     from colorama import Fore, init  # Спробуємо імпортувати знову після встановлення
from colorama import Fore, init
init()

#e

class DATABASE:
    def __init__(self):
        self.LogS = ""
        self.FileType = "db"

    def LogState(self, State):
        if State == "BASE" or State == "COLORFUL" or State == "NONE":
            self.LogS = State
        else:
            raise Exception(Fore.RED + f"Logs state cannot be: '{Fore.RESET}{Fore.BLUE}{State}{Fore.RESET}{Fore.RED}'. Only '{Fore.RESET}BASE{Fore.RESET}{Fore.RED}', '{Fore.RESET}{Fore.YELLOW}COLORFUL{Fore.RESET}{Fore.RED}' or '{Fore.RESET}{Fore.LIGHTBLACK_EX}NONE{Fore.RESET}{Fore.RED}'") 
            #print(Fore.RED + f"Logs state cannot be: '{Fore.RESET}{Fore.BLUE}{State}{Fore.RESET}{Fore.RED}'. Only '{Fore.RESET}BASE{Fore.RESET}{Fore.RED}', '{Fore.RESET}{Fore.YELLOW}COLORFUL{Fore.RESET}{Fore.RED}' or '{Fore.RESET}{Fore.LIGHTBLACK_EX}NONE{Fore.RESET}{Fore.RED}'") 
            

    def Create_Database(self, filename):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, filename)
        
        if os.path.exists(f"{filename}.{self.FileType}"):
            if self.LogS == 'BASE':
                print(f"Database: '{filename}' exists")
            elif self.LogS == 'COLORFUL':
                print(Fore.GREEN + f"Database: '{Fore.RESET}{Fore.BLUE}{filename}{Fore.RESET}{Fore.GREEN}' exists")
            return file_path
        else:
            f = open(f"{filename}.{self.FileType}", "x")
            if self.LogS == 'BASE':
                print(f"Database: {filename} was created")
                return file_path
            elif self.LogS == 'COLORFUL':
                print(Fore.GREEN + f"Database: '{Fore.RESET}{Fore.BLUE}{filename}{Fore.RESET}{Fore.GREEN}' was created")
                return file_path
            else:
                return file_path
            



    def Write_Database(self, filename, information, case):

        if os.path.exists(f"{filename}.{self.FileType}"):

            information_str = list(map(str,information))
            index = 0
            with open(f"{filename}.{self.FileType}", "r") as f:
                lines = f.readlines()
            with open(f"{filename}.{self.FileType}", "w") as f:

                if self.LogS == 'BASE':
                    print(Fore.RESET + f"Database file '{filename}.{self.FileType}' Writing...")
                elif self.LogS == 'COLORFUL':
                    print(Fore.RED + f"Database file '{filename}.{self.FileType}' Writing... {Fore.RESET}")

                lines = [line for line in lines if not line.startswith(str(case))]

                for cs in information_str:
                    lines.append(f"{str(case)}|{index}|{cs}|{str(case)}|{index}\n")
                    index += 1
                f.writelines(lines)
                index = 0
                
        else:
            self.Create_Database(filename)
            self.Write_Database(filename, information,  case) 





    def Read_Database(self, filename, case, index):
        ret = []
        if os.path.exists(f"{filename}.{self.FileType}"):
            try:
                with open(f"{filename}.{self.FileType}", "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = []

            if index == "ALL":
                for line in lines:
                    indexes = line.split('|')
                    if indexes[0] == str(case):
                        ret.append(indexes[2]) 
                return ret
            else:
                for line in lines:
                    indexes = line.split('|')
                    if indexes[0] == str(case):
                        if indexes[1] == str(index):
                            return indexes[2]
            if self.LogS == 'BASE':
                print(Fore.RESET + f"Database file '{filename}.{self.FileType}' Reading...")
            elif self.LogS == 'COLORFUL':
                print(Fore.RED + f"Database file '{filename}.{self.FileType}' Reading... {Fore.RESET}")
        

        else:
            self.Create_Database(filename)
            return 'DB was not found!'  







    def Delete_Database(self, filename):
        DATABASE_PATH = f"{filename}.{self.FileType}"

        if os.path.exists(DATABASE_PATH): 
            try:
                os.remove(DATABASE_PATH)
                if self.LogS == 'BASE':
                    print(Fore.RESET + f"Deleting database >> {filename}")
                elif self.LogS == 'COLORFUL':
                    print(Fore.RED + f"Deleting database >> {filename}{Fore.RESET}")

            except OSError as e:
                print(f"Error: {e.strerror}")
        else:

            if self.LogS == 'BASE':
                print(Fore.RESET + f"Database file '{filename}.{self.FileType}' was not found!")
            elif self.LogS == 'COLORFUL':
                print(Fore.RED + f"Database file '{filename}.{self.FileType}' was not found! {Fore.RESET}")

    
    def Rename_Database(self, filename1, filename2):

        if os.path.exists(f"{filename1}.{self.FileType}"):
            if not os.path.exists(f"{filename2}.{self.FileType}"):

                if self.LogS == 'BASE':
                    print(Fore.RESET + f"Database file '{filename1}.{self.FileType}' Renaming!!!")
                elif self.LogS == 'COLORFUL':
                    print(Fore.RED + f"Database file '{Fore.GREEN}{filename1}.{self.FileType}{Fore.RED}' Renaming!!! {Fore.RESET}")

                open(f"{filename2}.{self.FileType}", "x")
                f = open(f"{filename1}.{self.FileType}", "r")
                with open(f"{filename2}.{self.FileType}", "w") as dt2:
                    dt2.writelines(f)

                if self.LogS == 'BASE':
                    print(Fore.RESET + f"Database file '{filename1}.{self.FileType}' Renaming completed!!! New name >> {filename2}.{self.FileType}")
                elif self.LogS == 'COLORFUL':
                    print(Fore.RED + f"Database file '{Fore.GREEN}{filename1}.{self.FileType}{Fore.RED}' Renaming completed!!! New name >> {Fore.GREEN}{filename2}.{self.FileType}{Fore.RESET}")

                f.close()
                DATABASE_PATH = f"{filename1}.{self.FileType}"
                os.remove(DATABASE_PATH)
            
            else:
                if self.LogS == 'BASE':
                    print(Fore.RESET + f"Database file >> '{filename2}.{self.FileType}' exists. Deleting...")
                elif self.LogS == 'COLORFUL':
                    print(Fore.RED + f"Database file >> '{Fore.GREEN}{filename2}.{self.FileType}{Fore.RED}' exists. Deleting... {Fore.RESET}")

                DATABASE_PATH = f"{filename2}.{self.FileType}"
                os.remove(DATABASE_PATH)
                self.Rename_Database(filename1, filename2)
        else:
            if self.LogS == 'BASE':
                print(Fore.RESET + f"Database file >> '{filename1}.{self.FileType}' does not exist.")
            elif self.LogS == 'COLORFUL':
                print(Fore.RED + f"Database file >> '{Fore.GREEN}{filename1}.{self.FileType}{Fore.RED}' does not exist. {Fore.RESET}")


    # def Change_File_Type(self, filename, NewfileType):#
        
    #     if NewfileType != self.FileType:
    #         if filename != "":
                
    #             old_file_path = f"{filename}.{self.FileType}"
    #             new_file_path = f"{filename}.{NewfileType}"

    #             if os.path.exists(old_file_path):
    #                 if self.LogS == 'BASE':
    #                     print(Fore.RESET + f"Database file '{old_file_path}' Renaming!!!")
    #                 elif self.LogS == 'COLORFUL':
    #                     print(Fore.RED + f"Database file '{Fore.GREEN}{old_file_path}{Fore.RED}' Renaming!!! {Fore.RESET}")


    #                 with open(old_file_path, "r") as f:
    #                     content = f.read()
    #                 with open(new_file_path, "w") as new_file:
    #                     new_file.write(content)


    #                 os.remove(old_file_path)
    #                 self.FileType = NewfileType
                 

    #                 if self.LogS == 'BASE':
    #                     print(Fore.RESET + f"Database file '{old_file_path}' Renaming complete!!! New name >> {new_file_path}")
    #                 elif self.LogS == 'COLORFUL':
    #                     print(Fore.RED + f"Database file '{Fore.GREEN}{old_file_path}{Fore.RED}' Renaming complete!!! New name >> {Fore.GREEN}{new_file_path}{Fore.RESET}")

                    
    #             else:
    #                 if self.LogS == 'BASE':
    #                     print(Fore.RESET + "The original file does not exist")
    #                 elif self.LogS == 'COLORFUL':
    #                     print(Fore.BLUE + "The original file does not exist")
    #         else:
    #             self.FileType = NewfileType
    #             if self.LogS == 'BASE':
    #                 print(Fore.RESET + "The File is reseted")
    #             elif self.LogS == 'COLORFUL':
    #                 print(Fore.BLUE + "The File is reseted")
    #     else:
    #         if self.LogS == 'BASE':
    #             print(Fore.RESET + "The file type is already the same")
    #         elif self.LogS == 'COLORFUL':
    #             print(Fore.BLUE + "The file type is already the same")