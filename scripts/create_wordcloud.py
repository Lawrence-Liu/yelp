from wordcloud import WordCloud
import pandas as pd

reviews = pd.read_csv('/Users/lawrence/PycharmProjects/yelp/data/reviews.csv')

restaurant_id = 'hot-n-juicy-crawfish-washington'
text = ' '.join(reviews.loc[reviews.id == restaurant_id, 'review_text'].tolist())
word_cloud = WordCloud().generate(text)
word_cloud.to_image().save('/Users/lawrence/PycharmProjects/yelp/data/wordcloud/' + restaurant_id + '.jpg')