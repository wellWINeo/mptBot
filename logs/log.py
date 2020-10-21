
# here will be funcs for logs
class log():
    
    #TODO in future lenght will be obtained from config file
    def __init__(self, file_name, lenght = 10):
        self.max_lenght = lenght
        
        self.log_handle = open(file_name, "rt")
        self.file_name = file_name

        if self.__get_lines_count() >= lenght:
            self.log_handle.close()
            self.log_handle = open(self.file_name, "wt")
            self.log_handle.write("")

    def __change_mode(self, mode):
        if self.log_handle.mode != mode:
            self.log_handle.close()
            self.log_handle = open(self.file_name, mode)


    def __get_lines_count(self):
        count = 0
        if "r" not in self.log_handle.mode:
            self.__change_mode("rt")

        for line in self.log_handle:
            count+= 1
        
        return count
        
    def write(self, text):
        print(text)
        if self.log_handle.mode != "a":
            self.log_handle.close()
            self.log_handle = open(self.file_name, "a")
        self.log_handle.write(text + "\n")

    def __del__(self):
        self.log_handle.close()


if __name__ == "__main__":
    log = log("sys_logs.txt")
    log.write("[test] Test log")

