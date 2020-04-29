import json
class Municipality:
    """description of class"""
    def __init__(self, mun_folder, mun_name, mun_full_name, mun_id, shape_mun_id):
        self.mun_folder = mun_folder
        self.mun_name = mun_name
        self.mun_full_name = mun_full_name
        self.mun_id = mun_id
        self.shape_mun_id = shape_mun_id
    def to_string(self, file = None):
        if file == None:
            return self.mun_folder + "," + self.mun_name + "," + self.mun_full_name + "," + self.mun_id + "," + self.shape_mun_id + "\n"
        else:
            file_handle = open(file, "a")
            file_handle.write(self.mun_folder + "," + self.mun_name + "," + self.mun_full_name + "," + self.mun_id + "," + self.shape_mun_id + "\n")
            file_handle.close()
            return "Municipality appended to file " + file + "."
    def to_json(self, file = None):

        if file == None:
            return  self.mun_id + ': {\n\t\t"munFolder":"' + self.mun_folder + '",\n\t\t"munName":' + self.mun_name + ',\n\t\t"munFullName":' + self.mun_full_name + ',\n\t\t"munID":' + self.mun_id + ',\n\t\t"shpMunID":' + \
                    self.shape_mun_id + '\n\t\t}'
        else:
            return "no file writing allowed"
