from municipality import Municipality
class Municipality_List:
    """description of class"""
    def __init__(self):
        mun_file_handle = open("mun.txt", "r")
        mun_dir = ""
        mun_name = ""
        mun_fname = ""
        mun_id = ""
        mun_shp_id = ""
        self.mun_dict = {}
        for line in mun_file_handle:
            if "==" in line:
                continue
            if "munFolder" in line:
                mun_dir = line.split("=")[1].strip()
                continue
            if "munName" in line:
                mun_name = line.split("=")[1].strip()
                continue
            if "munFullName" in line:
                mun_fname = line.split("=")[1].strip()
                continue
            if "munID" in line:
                mun_id = line.split("=")[1].strip()
                continue
            if "shpMunID" in line:
                mun_shp_id = line.split("=")[1].strip()
                # build the Muncipality object
                mun = Municipality(mun_dir, mun_name, mun_fname, mun_id, mun_shp_id)
                self.mun_dict.update({mun_id:mun})
                continue
        mun_file_handle.close()

    def to_string(self):
        for mun in self.mun_dict.keys():
            self.mun_dict[mun].to_string("aFile.txt")
    def to_json(self):
        json_file_handle = open("municipalities.json", "a")
        json_file_handle.write("{\n\t")
        numkeys = len(self.mun_dict.keys())
        count = 0
        for mun in self.mun_dict.keys():
            if count < numkeys - 1:
                json_file_handle.write(self.mun_dict[mun].to_json() + ",\n\t")
            else: 
                json_file_handle.write(self.mun_dict[mun].to_json())
            count+=1
        json_file_handle.write("\n}")
        json_file_handle.close()