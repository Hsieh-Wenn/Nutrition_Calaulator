import pandas as pd
import streamlit as st

class NutrtionDataCalculator:
    def __init__(self, file_path, food_data_path):
        self._initial_gui_setting()
        self.df_input = pd.read_excel(file_path)
        self.df_nutrition = pd.read_excel(food_data_path)


    def main_calculator(self, ):
        st.title("八大營養標示計算器")
        st.info("此為營養標示計算器，請輸入配方與每份含量克數後點擊計算按鈕，即可顯示八大營養標示結果。（食材營養成份資料預設值來源於all_data2.xlsx檔案）")



        # 假设第一行为列名，重新设置列名
        self.df_nutrition.columns = self.df_nutrition.iloc[0]
        self.df_nutrition = self.df_nutrition[1:].reset_index(drop=True)

        # 转换数值列的数据类型，跳过第一个列（假设为名称）
        for col in self.df_nutrition.columns[1:]:
            self.df_nutrition[col] = pd.to_numeric(self.df_nutrition[col], errors='coerce')

        st.header("食材營養成份：")
        st.write("請輸入食材名稱以及對應的營養成份（單位為g）。")

        # 在 Streamlit 中显示编辑器
        nutrition_df = st.data_editor(self.df_nutrition, num_rows="dynamic")
        

        st.header("配方：")
        st.write("請輸入配料名稱以及對應的重量（單位為g）。")
        #nutrition_df = st.data_editor(self.df_nutrition, num_rows="dynamic")

        edited_df = st.data_editor(self.df_input, num_rows="dynamic",use_container_width=True)

        apiece_weight = int(st.text_input("請輸入每份含量（g）",25))
        calculate_button = st.button("計算")
        if calculate_button:
            df_result1, df_result2 = self.calculate_nutrition_from_excel(edited_df, nutrition_df, apiece_weight)
            header1, hesder2 = st.columns(2)
            header1.subheader(f"每份 (含量{apiece_weight}g) 營養標示")
            hesder2.subheader("100 g 營養標示")
            h1, h2 = st.columns(2)
            h1.write()
            h1.dataframe(df_result1, use_container_width=True, hide_index=True)
            h2.dataframe(df_result2, use_container_width=True, hide_index=True)



    @staticmethod
    def calculate_nutrition_from_excel(df_input, df_nutrition, apiece_weight):
        # 读取 Excel 文件
        #df_input = pd.read_excel(file_path)
        input_weight_dict = dict(zip(df_input.iloc[:, 0], df_input.iloc[:, 1]))

        print(input_weight_dict)
        print("===================================================================")

        #df_nutrition = pd.read_excel(food_data_path)
        #print(df_nutrition.columns)
        nutrition_data = df_nutrition.set_index("成分").T.to_dict(orient="list")
        # nutrition_data = df_nutrition.loc[:, '瘦肉':].to_dict(orient='list')
        print(df_nutrition)
        print("===================================================================")
        nurtition_columns = df_nutrition.columns.tolist()[1:]
        columns = df_nutrition['成分'].tolist()
        #print(columns)
        #ingredient_nutrition_per100 = {key: [] for key in input_weight_dict.keys()}
        #print(ingredient_nutrition_per100)

        ingredient_nutrition_per100 = dict()

        #print(nutrition_data["脂肪"])
        #ttt = [(nutrition_value / 100) * input_weight_dict["蛋"] for nutrition_value in nutrition_data["脂肪"]]
        #print(f"ttt:{ttt}")
        # 验证输入表格包含的配料
        for ingredient in df_input['配料']:
            if ingredient not in columns:
                raise ValueError(f"配料 '{ingredient}' 不再成分營養資料中，請確認輸入。")
            
            nutrition_values = [(nutrition_value / 100) * input_weight_dict[ingredient] for nutrition_value in nutrition_data[ingredient]]
            #print(ingredient)
            #print(nutrition_values)
            ingredient_nutrition_per100[ingredient] = nutrition_values
        #print(ingredient_nutrition_per100) 

        summed_values = [sum(values) for values in zip(*ingredient_nutrition_per100.values())]
        #print(f"summed_values:{summed_values}")
        # 熱量 (kcal)=(蛋白質 (g)×4)+(脂肪 (g)×9)+(碳水化合物 (g)×4)
        summed_values[0] = (summed_values[1]*4) + (summed_values[2]*9) + (summed_values[3]*4)
        #print(f"summed_values_new:{summed_values}")
        total_weight = sum(df_input['重量'].tolist())
        print(total_weight)

        normalized_values = [(s_value / total_weight)*100 for s_value in summed_values]
        #print(normalized_values)
        apiece_values = [(s_value / total_weight)*apiece_weight for s_value in summed_values]
        result_dict = {}
        for key, data in zip(nurtition_columns,apiece_values):
            result_dict[key] = data
        result_dict2 = {}
        for key, data in zip(nurtition_columns,normalized_values):
            result_dict2[key] = data
        #print(result_dict)    
        df_result1 = pd.DataFrame(result_dict.items(), columns=["配料", "每份"])
        #print(df_result)    
        df_result2 = pd.DataFrame(result_dict2.items(), columns=["配料", "每100g"])
        return df_result1, df_result2




    @staticmethod
    def _initial_gui_setting():
        # DESIGN implement changes to the standard streamlit UI/UX
        st.set_page_config(page_title="Nutrtion_Data_Calculator")
        # Design move app further up and remove top padding
        st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
        # Design change st.Audio to fixed height of 45 pixels
        st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
        # Design change hyperlink href link color
        st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
        st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode


if __name__ == '__main__':
    file_path = "配方456.xlsx"
    food_data_path = "all_data2.xlsx"
    infer_tool = NutrtionDataCalculator(file_path, food_data_path)
    infer_tool.main_calculator()
