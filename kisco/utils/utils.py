class Utils():
    def __init__(self):
        pass

    def set_sesstion(self,request):
        return

    def change_list_to_dict(self,data_list):
        dict_list = []
        for data in data_list:
            key = data[0]
            value = data[1]
            temp = [key, value]
            dict_list.append(temp)

        return dict_list
