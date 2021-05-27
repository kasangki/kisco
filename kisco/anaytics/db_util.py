from django.db import connection


class DBUtil():
    def __init__(self):
        self.cursor = connection.cursor()


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

    def convert_to_dict(self, results):
        """
        This method converts the resultset from postgres to dictionary
        interates the data and maps the columns to the values in result set and converts to dictionary
        :param columns: List - column names return when query is executed
        :param results: List / Tupple - result set from when query is executed
        :return: list of dictionary- mapped with table column name and to its values
        """
        columns = self.cursor.description
        allResults = []

        columns = [col.name for col in columns]
        if type(results) is list:
            for value in results:
                allResults.append(dict(zip(columns, value)))
            return allResults
        elif type(results) is tuple:
            allResults.append(dict(zip(columns, results)))
            return allResults

    # smartop_sum 데이터 조회 flag : all 전체, single : 한건
    def get_smartop_sum_list(self,op_num,flag):

        query = '''select 
                        A.* ,
                        B.first_heavy_scrap_a ,
                        B.first_heavy_scrap_b ,
                        B.first_light_scrap_a ,
                        B.first_light_scrap_b ,
                        B.first_gsa ,
                        B.first_gsb ,
                        B.first_gss ,
                        B.first_mb ,
                        B.first_lathe_a ,
                        B.first_lathe_b ,
                        B.first_heavy_scrap_a + B.first_heavy_scrap_b + 
	                    B.first_light_scrap_a + B.first_light_scrap_b + 
	                    B.first_gsa + B.first_gsb + B.first_gss +
	                    B.first_mb + B.first_lathe_b  as first_scrap_metal_usage,

                        B.second_heavy_scrap_a ,
                        B.second_heavy_scrap_b ,
                        B.second_light_scrap_a ,
                        B.second_light_scrap_b ,
                        B.second_gsa ,
                        B.second_gsb ,
                        B.second_gss ,
                        B.second_mb ,
                        B.second_lathe_a ,
                        B.second_lathe_b ,
                        B.second_heavy_scrap_a + B.second_heavy_scrap_b + 
	                    B.second_light_scrap_a + B.second_light_scrap_b + 
	                    B.second_gsa + B.second_gsb + B.second_gss +
	                    B.second_mb + B.second_lathe_b  as second_scrap_metal_usage
                    from tb_smartop_sum  A ,
                    (SELECT DISTINCT op_num, 
                        sum(first_heavy_scrap_a) as first_heavy_scrap_a,
                        sum(first_heavy_scrap_b) as first_heavy_scrap_b,
                        sum(first_light_scrap_a) as first_light_scrap_a,
                        sum(first_light_scrap_b) as first_light_scrap_b,
                        sum(first_gsa) as first_gsa,
                        sum(first_gsb) as first_gsb,
                        sum(first_gss) as first_gss,
                        sum(first_mb) as first_mb,
                        sum(first_lathe_a) as first_lathe_a,
                        sum(first_lathe_b) as first_lathe_b,

                        sum(second_heavy_scrap_a) as second_heavy_scrap_a,
                        sum(second_heavy_scrap_b) as second_heavy_scrap_b,
                        sum(second_light_scrap_a) as second_light_scrap_a,
                        sum(second_light_scrap_b) as second_light_scrap_b,
                        sum(second_gsa) as second_gsa,
                        sum(second_gsb) as second_gsb,
                        sum(second_gss) as second_gss,
                        sum(second_mb) as second_mb,
                        sum(second_lathe_a) as second_lathe_a,
                        sum(second_lathe_b) as second_lathe_b
                        

                        FROM (
                            SELECT DISTINCT op_num,
                                case when order_num = 1 then heavy_scrap_a else 0 end as first_heavy_scrap_a ,
                                case when order_num = 1 then heavy_scrap_b else 0 end as first_heavy_scrap_b ,
                                case when order_num = 1 then light_scrap_a else 0 end as first_light_scrap_a ,
                                case when order_num = 1 then light_scrap_b else 0 end as first_light_scrap_b ,
                                case when order_num = 1 then gsa else 0 end as first_gsa ,
                                case when order_num = 1 then gsb else 0 end as first_gsb , 
                                case when order_num = 1 then gss else 0 end as first_gss ,
                                case when order_num = 1 then mb else 0 end as first_mb , 
                                case when order_num = 1 then lathe_a else 0 end as first_lathe_a , 
                                case when order_num = 1 then lathe_b else 0 end as first_lathe_b ,

                                case when order_num = 2 then heavy_scrap_a else 0 end as second_heavy_scrap_a ,
                                case when order_num = 2 then heavy_scrap_b else 0 end as second_heavy_scrap_b ,
                                case when order_num = 2 then light_scrap_a else 0 end as second_light_scrap_a ,
                                case when order_num = 2 then light_scrap_b else 0 end as second_light_scrap_b ,
                                case when order_num = 2 then gsa else 0 end as second_gsa ,
                                case when order_num = 2 then gsb else 0 end as second_gsb , 
                                case when order_num = 2 then gss else 0 end as second_gss ,
                                case when order_num = 2 then mb else 0 end as second_mb , 
                                case when order_num = 2 then lathe_a else 0 end as second_lathe_a , 
                                case when order_num = 2 then lathe_b else 0 end as second_lathe_b 
                            FROM tb_scrap_history
                        ) C_2_1
                        GROUP BY op_num
                        order by op_num
                    ) B			
                    where A.op_num = B.op_num '''
        if flag == 'single' :
            query = query + ''' and  A.op_num =%s '''
            self.cursor.execute(query, [op_num])
            smartop_sum_list = self.cursor.fetchall()
            return smartop_sum_list
        else :
            self.cursor.execute(query)
            smartop_sum_list = self.cursor.fetchall()
            return smartop_sum_list

        #cursor = connection.cursor()



