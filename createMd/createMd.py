import sys
class state () :
    def __init__(self):
       self.state = 'stop'

    def start_record (self) :
        if self.state == 'stop':
            self.state = 'start'

    def stop_warning (self) :
        if self.state == 'start':
            self.state = 'warning'

    def stop_record(self):
        if self.state == 'warning':
            self.state = 'stop'

    def status (self):
        return self.state

class parser () :
    def __init__ (self, state_mc, file_name, write_file) :
        self.__last_line__ = None
        self.__parser__ = state_mc
        self.__file_name__ = file_name
        self.__write_file_name = write_file 
        self.__write_file__ = None 

    def __print_list_line__(self) :
        if self.__last_line__ != None :
           self.__write_file__.write(self.__last_line__)
           self.__last_line__ = None

    def parse (self) :
        self.__write_file__ = open(self.__write_file_name, 'w') 
        with open(self.__file_name__,'r') as file:
            for line in file:
                for word in line.split():
                    if word == 'def':
                        self.__parser__.start_record()
                    if word == '"""':
                        if self.__parser__.status() == 'start':
                            self.__parser__.stop_warning()
                        elif self.__parser__.status() == 'warning':
                            self.__parser__.stop_record()
                            self.__last_line__ = line

                if self.__parser__.status() != 'stop':
                    if (line != '\n'):
                        self.__write_file__.write(line)
                else :
                   self.__print_list_line__()

    def complete(self):   
        self.__write_file__.close()
 
    def __process_def__(self, line) :
        words = line.split('(')
        header = words[0].replace('_', ' ')
        header = header.replace('def', '')
        header = "# " + header.upper()
        return (header)

    def generate_readme (self):
        file_id = open('README.md', 'w')         
        with open(self.__write_file_name, 'r') as file:
            for line in file :
                if 'def' in line.split():
                    header = self.__process_def__(line)
                    file_id.write(header + '\n')
                    file_id.write(line)
                elif '"""' in  line.split():
                    file_id.write('```\n')
                else:
                    file_id.write(line)
        file_id.close()
             

def main (argv, argc) :
    # Phase 1
    a = state()
    l = parser(a, argv, "readme.tmp.txt")
    l.parse()
    l.complete()
    # Phase 2
    l.generate_readme()

if __name__ == "__main__":
   argv = sys.argv[1] 
   argc = len(sys.argv)
   main (argv, argc)


