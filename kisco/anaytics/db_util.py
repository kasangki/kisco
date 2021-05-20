class DBUtil():
    def __init__(self):
        pass

    ## 변수 타입별 변수 목록 조회
    def get_var_name_list(self, var_type, all_var_name_df):
        # 선택변수 목록
        select_var_name_df = all_var_name_df[all_var_name_df['var_type'] == var_type]

        select_var_name_list = list(select_var_name_df['var_name'])
        select_var_code_list = list(select_var_name_df['var_code'])
        select_var_list = []
        for i in range(len(select_var_code_list)):
            temp = [select_var_code_list[i], select_var_name_list[i]]
            select_var_list.append(temp)
        return select_var_list    ## 변수 타입별 변수 목록 조회


    def set_y_final_value_list(self, var_type, all_var_name_df,y_final_result_dict,var_name_list):
        # 선택변수 목록
        select_var_name_df = all_var_name_df[all_var_name_df['var_type'] == var_type]

        select_var_name_list = list(select_var_name_df['var_name'])
        select_var_code_list = list(select_var_name_df['var_code'])
        select_var_list = []
        for i in range(len(select_var_code_list)):
            var_code = select_var_code_list[i]
            var_name = select_var_name_list[i]

            # 입력변수 존재 여부 체크
            if(var_code in var_name_list) :
                is_in = 'Y'
            else :
                is_in = 'N'
            # 코드, 코드명, 값
            temp = [var_code, var_name,y_final_result_dict[var_code],is_in]
            select_var_list.append(temp)
        return select_var_list


    def set_y_final_all_value_list(self, var_type, all_var_name_df,y_final_result_dict,var_name_list):
        # 선택변수 목록
        select_var_name_df = all_var_name_df[all_var_name_df['var_type'] == var_type]

        select_var_name_list = list(select_var_name_df['var_name'])
        select_var_code_list = list(select_var_name_df['var_code'])
        select_var_list = []
        for i in range(len(select_var_code_list)):
            var_code = select_var_code_list[i]
            var_name = select_var_name_list[i]

            temp = [var_code, var_name,y_final_result_dict[var_code],'N']
            select_var_list.append(temp)
        return select_var_list

