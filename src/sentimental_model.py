from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def sentimental_model_pipeline():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    sentiment_pipeline = pipeline("sentiment-analysis", model = model, tokenizer=tokenizer)
    return sentiment_pipeline

# Get sentiments
def get_sentiments(input_dict, variable_text, sentiment_pipeline):
    possible_sentiments = ['negative', 'neutral', 'positive']
    for item_ in input_dict:
        sentiment = sentiment_pipeline(item_[variable_text])
        for item in sentiment:
            for shade in possible_sentiments:
                if item['label'] == shade:
                    item_[shade] = item['score']
                else:
                    item_[shade] = 0
    return input_dict
