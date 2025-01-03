import pandas as pd


def calculate_nutrition_from_excel(file_path, food_data_path, apiece_weight):
    # 读取 Excel 文件
    df_input = pd.read_excel(file_path)
    input_weight_dict = dict(zip(df_input.iloc[:, 0], df_input.iloc[:, 1]))

    print(input_weight_dict)
    print("===================================================================")

    df_nutrition = pd.read_excel(food_data_path)
    #print(df_nutrition.columns)
    nutrition_data = df_nutrition.loc[:, '瘦肉':].to_dict(orient='list')
    print(df_nutrition)
    print("===================================================================")
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
        if ingredient not in df_nutrition.columns:
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
    for key, data in zip(columns,apiece_values):
      result_dict[key] = data
    result_dict2 = {}
    for key, data in zip(columns,normalized_values):
      result_dict2[key] = data
    #print(result_dict)    
    df_result1 = pd.DataFrame(result_dict.items(), columns=["配料", "每份"])
    #print(df_result)    
    df_result2 = pd.DataFrame(result_dict2.items(), columns=["配料", "每100g"])
    return df_result1, df_result2
# 使用示例
# 假设输入的 Excel 文件包含两列："配料" 和 "重量 (g)"
file_path = "/home/c95hcw/下載/配方123.xlsx"
food_data_path = "/home/c95hcw/下載/all_data.xlsx"
apiece_weight = 25 # 每份含量 25 g
df_result1, df_result2 = calculate_nutrition_from_excel(file_path, food_data_path, apiece_weight)
print("==============================================================================")
print(f"每份 (含量{apiece_weight}g) 營養標示")
print(df_result1)
print("==============================================================================")
print(f"100 g 營養標示")
print(df_result2)
print("==============================================================================")