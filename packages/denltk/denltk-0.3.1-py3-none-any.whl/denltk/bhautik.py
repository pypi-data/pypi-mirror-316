def func1():
    '''
        question1: Given a preprocessed dataset of movie reviews, 
        implement a Support Vector Machine (SVM) classifier to predict the sentiment of a review (positive or negative).
    '''

    print(r'''
        import pandas as pd
        import re
        import string
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import WordNetLemmatizer
        import nltk

        # Download NLTK resources
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        # Load the dataset
        df = pd.read_csv(r"C:\Users\bhautik\Downloads\archive (17)\IMDB Dataset.csv")


        # Define a lemmatizer and stop words
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))

        # Preprocessing function
        def preprocess_text(text):
            text = text.lower()  # Lowercase
            text = re.sub(r'#\S+', '', text)  # Remove hashtags
            text = re.sub(r'\d+', '', text)  # Remove numbers
            text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
            text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
            tokens = word_tokenize(text)  # Tokenize
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]  # Remove stop words & lemmatize
            return ' '.join(tokens)

        # Apply preprocessing to the reviews column
        df['cleaned_review'] = df['review'].apply(preprocess_text)

        print(df[['review', 'cleaned_review']].head())

                
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.svm import SVC
        from sklearn.metrics import classification_report, accuracy_score
                

        vectorizer = TfidfVectorizer(max_features=5000)  # Limit to top 5000 features for simplicity
        X = vectorizer.fit_transform(df['review'])  # Transform reviews into TF-IDF features
        y = df['sentiment'].apply(lambda x: 1 if x == 'positive' else 0)  # Convert sentiment to binary (1 for positive, 0 for negative)
                
        print(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = SVC(kernel='linear', random_state=42)
        model.fit(X_train, y_train)


        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        # Display results
        print(f"Accuracy: {accuracy:.2f}")
        print("\nClassification Report:\n")
        print(report)

    ''')





def func2():
    '''que2:Given a preprocessed
      dataset of news articles, implement a Logistic
     Regression model to classify news articles into different categories (e.g., politics, sports, technology).
    
    '''
    print(r'''


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import re

# Load the dataset
df = pd.read_csv( r"C:\Users\bhautik\Downloads\archive (19)\Articles.csv",encoding='latin1')

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.lower().strip()  # Convert to lowercase and strip whitespace
    return text

# Apply preprocessing
df['Article'] = df['Article'].apply(preprocess_text)
 
# Feature and target
X = df['Article']
y = df['NewsType']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=5000)  # You can adjust the max_features as needed
X_train_tfidf = tfidf.fit_transform(X_train)  # Fit and transform on training data
X_test_tfidf = tfidf.transform(X_test)  # Transform the test data

# Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Predictions and evaluation
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


''')
    


def func3():
    '''
    que3:
        Given a preprocessed dataset of social media posts, 
        implement a Random Forest classifier to predict the sentiment of a post (positive, negative, or neutral).

    '''
    print(r'''

    print(df.columns)  # Check column names

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

    # Step 1: Load the dataset 
    df = pd.read_csv(r"C:\Users\bhautik\Downloads\archive (20)\Social_Media_Advertising.csv")

    # Display first few rows to understand the structure
    print(df.head())


    # Convert 'Duration' to numeric (extract days)
    df['Duration'] = df['Duration'].str.extract(r'(\d+)').astype(float)

    # Clean and convert specified columns to numeric
    columns_to_clean = ['Acquisition_Cost', 'Conversion_Rate', 'ROI', 'Clicks', 'Impressions', 'Engagement_Score']
    df[columns_to_clean] = df[columns_to_clean].replace({'\$': '', ',': ''}, regex=True).astype(float)

    df.drop(columns=['Date'], inplace=True)

    # Label encode categorical columns
    categorical_columns = ['Target_Audience', 'Campaign_Goal', 'Channel_Used', 'Location', 'Language', 'Customer_Segment', 'Company']
    df[categorical_columns] = df[categorical_columns].apply(LabelEncoder().fit_transform)


    # Step 3: Feature Selection and Splitting Data
    X = df.drop('Target_Audience', axis=1)  # Drop the target column from features
    y = df['Target_Audience']  # Target column

    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 4: Model Training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 5: Model Evaluation
    y_pred = model.predict(X_test)

    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

''')
    





def func4():
    '''
    que4:Given a preprocessed dataset of customer service chat logs, implement a Neural Network
      model to classify customer queries into different intents (e.g., product inquiry, technical support, complaint).
    '''
    print(r'''

    import pandas as pd
    import numpy as np
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import classification_report

    # Load dataset
    df = pd.read_excel(r"C:\Users\bhautik\Downloads\archive (21)\Chat_Team_CaseStudy FINAL.xlsx", engine='openpyxl')

    # Preprocess data
    texts = df['Text'].astype(str).values
    labels = df['Customer Comment'].astype(str).values

    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)

    # Tokenize and pad sequences
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences(texts), maxlen=100)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, encoded_labels, test_size=0.2, random_state=42)

    # Build model
    model = Sequential([
        Embedding(input_dim=10000, output_dim=128, input_length=100),
        LSTM(128, dropout=0.2, recurrent_dropout=0.2),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(len(np.unique(encoded_labels)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=2, batch_size=32)

    # Evaluate model
    y_pred = model.predict(X_test).argmax(axis=1)
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

''')
    


def func5():
    '''
    Given a preprocessed dataset
      of scientific articles, implement a Text Summarization model to generate concise summaries of the articles.
    '''    
    print(r'''

    import pandas as pd
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer

    # Load dataset
    data_path = r"C:\Users\bhautik\Downloads\archive (22)\train_tm\train.csv"
    df = pd.read_csv(data_path)

    # Summarization function
    def summarize_text(text, sentences=2):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        return " ".join(str(s) for s in LsaSummarizer()(parser.document, sentences))

    # Generate summaries for the 'ABSTRACT' column
    df['Generated Summary'] = df['ABSTRACT'].astype(str).apply(summarize_text)
    df['Generated Summary']
    # # Save output
    # df.to_csv(r"C:\Users\bhautik\Downloads\archive (22)\train_tm\generated_summaries.csv", index=False)
    # print("Summaries saved!")





''')
    

def func7():
    '''
    que7:Given a preprocessed dataset of historical
      documents, implement a Named Entity Recognition 
      (NER) model to identify and classify named entities (e.g., persons, organizations, locations) in the text.'''
    print(r'''

    import spacy

    # Load the pretrained SpaCy NER model
    nlp = spacy.load("en_core_web_sm")

    # Sample text
    text = "Barack Obama was born in Honolulu, Hawaii and was the President of the United States."

    # Apply the model to the text
    doc = nlp(text)

    # Extract entities
    for ent in doc.ents:
        print(f"{ent.text} ({ent.label_})")

    ''')


def func8():
    '''Given a preprocessed dataset of text documents, implement a 
    Text Clustering algorithm to group similar documents together.'''
print(r'''

    import pandas as pd
    import numpy as np
    import re
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score, calinski_harabasz_score
    from sklearn.model_selection import train_test_split
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    import nltk
    import string

    # Download required NLTK data files
    nltk.download('stopwords')
    nltk.download('wordnet')

    # Step 1: Data Preprocessing

    # Sample text data (replace with your dataset)
    import pandas as pd

    # Dictionary of documents
    documents = {
        1: "Data science is an inter-disciplinary field.",
        2: "Machine learning is a branch of artificial intelligence.",
        3: "Artificial intelligence includes machine learning techniques.",
        4: "Data analysis involves inspecting and cleaning data.",
        5: "Natural language processing is a field in AI."
    }

    # Creating a DataFrame
    df = pd.DataFrame(list(documents.items()), columns=['Document_ID', 'Text'])

    print(df)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # Preprocessing function
    def preprocess_text(text):
        text = text.lower()  # Lowercase
        text = re.sub(r'#\S+', '', text)  # Remove hashtags
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        tokens = word_tokenize(text)  # Tokenize
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]  # Remove stop words & lemmatize
        return ' '.join(tokens)
    df['cleaned_text'] = df['Text'].apply(preprocess_text)

    print(df[['Text', 'cleaned_text']].head())



    vectorizer = TfidfVectorizer(max_features=100) # Adjust number of features as needed
    X = vectorizer.fit_transform(df['cleaned_text'])

    num_clusters = 2
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    labels = kmeans.labels_
    silhouette_avg = silhouette_score(X, labels)
    print(f"Silhouette Score: {silhouette_avg:.2f}")

    calinski_harabasz_avg = calinski_harabasz_score(X.toarray(), labels)
    print(f"Calinski-Harabasz Index: {calinski_harabasz_avg:.2f}")

    ''')