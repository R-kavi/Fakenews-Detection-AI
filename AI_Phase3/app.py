import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Load the datasets
true_data = pd.read_csv('True.csv')
false_data = pd.read_csv('Fake.csv')

# Add a 'label' column to indicate real news (0) and fake news (1)
true_data['label'] = 0
false_data['label'] = 1

# Concatenate the two datasets
df = pd.concat([true_data, false_data])

# Shuffle the data
df = df.sample(frac=1).reset_index(drop=True)

# Data cleaning and preprocessing
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

def preprocess_text(text):
    # Add your text preprocessing steps here (e.g., lowercasing, removing stopwords)
    words = text.split()
    words = [word.lower() for word in words if word.lower() not in stop_words]
    return ' '.join(words)

df['text'] = df['text'].apply(preprocess_text)

# Split the dataset into training and testing
X = df['text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train a classifier (e.g., Naive Bayes)
clf = MultinomialNB()
clf.fit(X_train_tfidf, y_train)

# Evaluate the model
y_pred = clf.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))
