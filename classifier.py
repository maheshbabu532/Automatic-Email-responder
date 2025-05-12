from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load training data (manual samples of urgent, general, spam)
training_data = [
    ("URGENT: Server is down!", "Urgent"),
    ("Can you update me on the project status?", "General"),
    ("You won a lottery! Claim now!", "Spam"),
]

texts, labels = zip(*training_data)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X_train, labels)

# Save Model
pickle.dump((vectorizer, model), open("email_classifier.pkl", "wb"))

def classify_email(subject, body):
    vectorizer, model = pickle.load(open("email_classifier.pkl", "rb"))
    text_features = vectorizer.transform([subject + " " + body])
    return model.predict(text_features)[0]
