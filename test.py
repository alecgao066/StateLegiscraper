from statelegiscraper import dashboard_helper

file = "HHS"
# Read in data
if file == "HHS":
    data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//dashboard//nv_hhs_analysis//cleaned_data.json")
elif file == 'FIN':
    data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//dashboard//nv_fin_analysis//cleaned_data.json")
else:
    data_by_date = {}
query = 'shut down'
# Semantic searching
sm_search = dashboard_helper.NVSemanticSearching(data_by_date, query, 5)
if file == "HHS":
    filtered_dict = sm_search.rapid_searching("data//dashboard//nv_hhs_analysis//")
elif file == 'FIN':
    filtered_dict = sm_search.rapid_searching("data//dashboard//nv_fin_analysis//")
else:
    filtered_dict = {}

# Organize the data by the month
data_by_month = {}
for i in filtered_dict.keys():
    month = i[:2]
    if month == '06' or month == '09':
        continue
    if month not in data_by_month:
        data_by_month[month] = filtered_dict[i]
    else:
        data_by_month[month].extend(filtered_dict[i])
dashboard_helper.sentiment_analysis(data_by_month, 'data//dashboard//plots//')

query = 'small business'
# Semantic searching
sm_search = dashboard_helper.NVSemanticSearching(data_by_date, query, 5)
if file == "HHS":
    filtered_dict = sm_search.rapid_searching("data//dashboard//nv_hhs_analysis//")
elif file == 'FIN':
    filtered_dict = sm_search.rapid_searching("data//dashboard//nv_fin_analysis//")
else:
    filtered_dict = {}

# Organize the data by the month
data_by_month = {}
for i in filtered_dict.keys():
    month = i[:2]
    if month == '06' or month == '09':
        continue
    if month not in data_by_month:
        data_by_month[month] = filtered_dict[i]
    else:
        data_by_month[month].extend(filtered_dict[i])
dashboard_helper.sentiment_analysis(data_by_month, 'data//dashboard//plots//')

# Text cleaning
text_preprocessing = dashboard_helper.NVTextProcessing(data_by_month)
text_preprocessing.text_processing()
processed_dict = text_preprocessing.json

# Analysis: word frequency, tf-idf for key word extraction
analysis_freq = dashboard_helper.NVTextAnalysis(processed_dict)
_, word_freq = analysis_freq.word_frequency()
_, word_key = analysis_freq.tf_idf_analysis()
num_div = [2, 4]
# Visualization: save word cloud plots, generate yop key words
month = {'05': 'May', '04': 'April', '03': 'March', '02': 'February', '01': 'January', }
for i in range(num_div[0], num_div[1] + 1):
    dashboard_helper.NVVisualizations.word_cloud(word_freq[str(i).zfill(2)], "data//dashboard//plots//",
                                                 str(i).zfill(2))
results = dashboard_helper.NVVisualizations.key_word_display(word_key, 4)
print('0')