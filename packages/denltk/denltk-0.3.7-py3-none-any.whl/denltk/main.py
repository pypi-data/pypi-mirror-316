class Bhim:
    def func1(self):
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





    def func2(self):
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
        


    def func3(self):
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
        





    def func4(self):
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
        


    def func5(self):
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
        

    def func7(self):
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


    def func8(self):
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


class Ram:
    def menu(self):
           print(r'''1:Preprocessing \n2:Naive_Bayes \n3:Word2vec_gensim \n4:sentiment \n5:newsclassification \n6:social_sentiment \n7:customer_class \n8:NER \n9:summary \n10:cluster \n10:NN''')
           
           
    def Preprocessing (self):
        print(r'''

        import re
        import string
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import WordNetLemmatizer
        from nltk import download

        # Download NLTK data (required once)
        download('punkt')
        download('stopwords')
        download('wordnet')

        def preprocess_text(text):
            # Initialize the WordNetLemmatizer
            lemmatizer = WordNetLemmatizer()

            # a) Remove punctuation
            text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)

            # b) Remove stop words
            stop_words = set(stopwords.words('english'))
            tokens = word_tokenize(text)
            tokens = [word for word in tokens if word.lower() not in stop_words]

            # c) Convert text to lowercase
            tokens = [word.lower() for word in tokens]

            # d) Tokenization (already done in the stop words removal step)

            # e) Apply lemmatization (text normalization)
            tokens = [lemmatizer.lemmatize(word) for word in tokens]

            # f) Remove extra spaces and special characters
            text = " ".join(tokens)
            text = re.sub(r"\\s+", " ", text).strip()

            # g) Remove numbers
            text = re.sub(r"\\d+", "", text)

            # h) Remove hashtags
            text = re.sub(r"#\\w+", "", text)

            return text

        # Example usage
        sample_text = """
            The movie was absolutely fantastic! #MustWatch
            However, it did have a few slow parts, and the runtime (2.5 hours) was a bit long.
            Overall, I'd rate it 8/10. A true masterpiece of storytelling.
        """

        preprocessed_text = preprocess_text(sample_text)
        print("Original Text:", sample_text)
        print("Preprocessed Text:", preprocessed_text)

            ''')


    def Naive_Bayes(self):
        print(r'''from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import accuracy_score
        import nltk
        from nltk.corpus import movie_reviews

        # nltk.download('movie_reviews')

        # Load dataset
        documents = [(list(movie_reviews.words(fileid)), category)
                    for category in movie_reviews.categories()
                    for fileid in movie_reviews.fileids(category)]

        # Split into text and labels
        texts = [" ".join(words) for words, label in documents]
        labels = [label for words, label in documents]

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

        # Vectorize text
        vectorizer = CountVectorizer()
        X_train_vect = vectorizer.fit_transform(X_train)
        X_test_vect = vectorizer.transform(X_test)

        # Train Naive Bayes classifier
        classifier = MultinomialNB()
        classifier.fit(X_train_vect, y_train)

        # Predict and evaluate
        y_pred = classifier.predict(X_test_vect)
        print("Naive Bayes Accuracy:", accuracy_score(y_test, y_pred))''')

    def Word2vec_gensim(self):
        print(r'''from gensim.models import Word2Vec
        from nltk.tokenize import word_tokenize

        # Sample text corpus
        text_corpus = [
            "The movie was fantastic and thrilling.",
            "I didn't enjoy the movie at all, it was boring.",
            "What a great performance by the actors!",
        ]

        # Tokenize sentences
        tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in text_corpus]

        # Train Word2Vec model
        word2vec_model = Word2Vec(sentences=tokenized_corpus, vector_size=100, window=5, min_count=1, workers=4)
        word2vec_model.save("word2vec.model")

        # Example: Get vector for a word
        word_vector = word2vec_model.wv['movie']
        print("Vector for 'movie':", word_vector)''')
        
        
    def sentiment(self):
        print(r'''import nltk
        from nltk.corpus import movie_reviews
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

        # Download the dataset
        nltk.download('movie_reviews')

        # Load data
        documents = [(list(movie_reviews.words(fileid)), category)
                    for category in movie_reviews.categories()
                    for fileid in movie_reviews.fileids(category)]

        # Separate the data and labels
        texts = [" ".join(words) for words, label in documents]
        labels = [label for _, label in documents]

        # Split into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42)

        # Feature extraction: Use TF-IDF Vectorizer
        vectorizer = TfidfVectorizer(max_features=5000)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Train a Logistic Regression model
        model = LogisticRegression()
        model.fit(X_train_vec, y_train)

        # Make predictions
        y_pred = model.predict(X_test_vec)

        # Evaluation
        print("Model Performance on Test Set:")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Precision:", precision_score(y_test, y_pred, pos_label="pos"))
        print("Recall:", recall_score(y_test, y_pred, pos_label="pos"))
        print("F1 Score:", f1_score(y_test, y_pred, pos_label="pos"))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))

        # Test the model with user input
        def classify_review(review):
            review_vec = vectorizer.transform([review])  # Vectorize the input
            prediction = model.predict(review_vec)[0]  # Predict the sentiment
            return "Positive" if prediction == "pos" else "Negative"

        # Test example
        print("\n--- Test the Model ---")
        user_review = input("Enter a movie review: ")
        print(f"The review sentiment is: {classify_review(user_review)}")
        ''')

    def newsclassification(self):
        print(r'''from sklearn.datasets import fetch_20newsgroups
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.svm import LinearSVC
        from sklearn.metrics import classification_report
        from sklearn.model_selection import train_test_split

        # Load the 20 newsgroups dataset
        newsgroups = fetch_20newsgroups(subset='all')
        X, y = newsgroups.data, newsgroups.target

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Convert text to TF-IDF features
        vectorizer = TfidfVectorizer(max_features=10000)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        # Train an SVM classifier
        classifier = LinearSVC()
        classifier.fit(X_train_tfidf, y_train)

        # Predict and evaluate
        y_pred = classifier.predict(X_test_tfidf)
        print("Classification Report:\n", classification_report(y_test, y_pred, target_names=newsgroups.target_names))

        example_review = ["naredra modi won election "]
        example_vector = vectorizer.transform(example_review).toarray()
        example_prediction=classifier.predict(example_vector)

        print(f"class of news: {newsgroups.target_names[example_prediction[0]]}")
        # print(f"class of news: {newsgroups.target_names[example_prediction[0]]}")
        ''')

    def social_sentiment(self):
        print(r'''import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import classification_report, accuracy_score

        # Sample dataset
        data = {
            'post': [
                "I love this product, it's amazing!",
                "Terrible service, I am so disappointed.",
                "Not great, not terrible, just okay.",
                "Fantastic experience, highly recommend!",
                "Worst product ever, will never buy again.",
                "It's alright, nothing special."
            ],
            'sentiment': ['positive', 'negative', 'neutral', 'positive', 'negative', 'neutral']
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Step 1: Split data into training and testing sets
        X = df['post']
        y = df['sentiment']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Step 2: Feature extraction using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(max_features=500)
        X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
        X_test_tfidf = tfidf_vectorizer.transform(X_test)

        # Step 3: Train a Logistic Regression classifier
        classifier = LogisticRegression()
        classifier.fit(X_train_tfidf, y_train)

        # Step 4: Evaluate the model
        y_pred = classifier.predict(X_test_tfidf)

        # Print evaluation metrics
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Step 5: Predict sentiment for a new post
        new_post = ["I am so happy with this purchase!"]
        new_post_tfidf = tfidf_vectorizer.transform(new_post)
        new_prediction = classifier.predict(new_post_tfidf)

        print(f"\nSentiment of the new post: {new_prediction[0]}")
        ''')

    def customer_class(self):
        print(r'''import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import classification_report, accuracy_score

        # Sample dataset
        data = {
            'chat_log': [
                "Can you tell me the price of this product?",
                "I need help setting up the device.",
                "This product is defective, I want a refund.",
                "What is the warranty period for this item?",
                "My internet is not working, please assist.",
                "I am unhappy with the quality of this product."
            ],
            'intent': [
                "product inquiry",
                "technical support",
                "complaint",
                "product inquiry",
                "technical support",
                "complaint"
            ]
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Step 1: Split data into training and testing sets
        X = df['chat_log']
        y = df['intent']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Step 2: Feature extraction using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(max_features=500)
        X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
        X_test_tfidf = tfidf_vectorizer.transform(X_test)

        # Step 3: Train a Logistic Regression classifier
        classifier = LogisticRegression()
        classifier.fit(X_train_tfidf, y_train)

        # Step 4: Evaluate the model
        y_pred = classifier.predict(X_test_tfidf)

        # Print evaluation metrics
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Step 5: Predict the intent of a new chat log
        new_chat = ["I need assistance with my account settings."]
        new_chat_tfidf = tfidf_vectorizer.transform(new_chat)
        new_prediction = classifier.predict(new_chat_tfidf)

        print(f"\nPredicted intent for the new chat: {new_prediction[0]}")

        ''')
    def summary(self):
        print(r'''import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import sent_tokenize, word_tokenize
        from nltk.probability import FreqDist
        from nltk.corpus import stopwords
        import heapq

        # Ensure necessary NLTK data is available
        nltk.download('punkt')
        nltk.download('stopwords')

        # Sample article (replace with actual data)
        article = """Deep learning is a subset of machine learning, which is a branch of artificial intelligence (AI).
        It aims to learn from large amounts of data and make decisions autonomously.
        Deep learning has been applied to numerous fields such as image recognition, natural language processing, and more."""

        # Tokenize the article into sentences
        sentences = sent_tokenize(article)

        # Tokenize the article into words and remove stopwords
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(article.lower())
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

        # Get frequency distribution of the words
        fdist = FreqDist(filtered_words)

        # Score the sentences based on word frequency
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            score = sum(fdist[word] for word in sentence_words if word in fdist)
            sentence_scores[sentence] = score

        # Get the top N sentences
        top_sentences = heapq.nlargest(2, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(top_sentences)
        print("Summary:", summary)
        ''')

    def cluster(self):
        print(r'''import nltk
        import matplotlib.pyplot as plt
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from nltk.corpus import reuters
        from sklearn.decomposition import PCA
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from collections import defaultdict

        # Download the dataset (if not already downloaded)
        nltk.download("reuters")
        nltk.download("punkt")
        nltk.download("stopwords")

        # Step 1: Load a subset of the Reuters dataset
        categories = ['coffee', 'gold']  # Select specific categories for simplicity
        document_ids = reuters.fileids(categories)

        # Split into training and test datasets (if needed)
        documents = [reuters.raw(doc_id) for doc_id in document_ids]

        # Step 2: Preprocess the text (tokenization and stopword removal)
        stop_words = set(stopwords.words("english"))

        def preprocess(text):
            tokens = word_tokenize(text.lower())  # Tokenize and lowercase
            tokens = [word for word in tokens if word.isalpha()]  # Remove non-alphabetic tokens
            tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
            return " ".join(tokens)

        processed_documents = [preprocess(doc) for doc in documents]

        # Step 3: Convert text to numeric features using TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(processed_documents)

        # Step 4: Apply K-Means clustering
        k = 2  # Assume we want 2 clusters
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)

        # Step 5: Evaluate clustering
        labels = kmeans.labels_
        sil_score = silhouette_score(X, labels)
        print(f"Silhouette Score: {sil_score:.2f}")

        # Step 6: Display results
        # print("Document Clusters:")
        # for i, label in enumerate(labels):
        #     print(f"Document {i+1}: Cluster {label}")

        # Optional: Group documents by cluster
        cluster_groups = defaultdict(list)
        for i, label in enumerate(labels):
            cluster_groups[label].append(documents[i])

        print("Grouped Documents:")
        for cluster, docs in cluster_groups.items():
            print(f"Cluster {cluster}: {docs[:2]}...")  # Show only the first 2 docs for brevity

        # Step 7: Reduce dimensions for visualization using PCA
        pca = PCA(n_components=2)
        reduced_X = pca.fit_transform(X.toarray())

        # Step 8: Plot the clustering results
        plt.figure(figsize=(8, 6))
        plt.scatter(reduced_X[:, 0], reduced_X[:, 1], c=labels, cmap='viridis', marker='o')
        plt.title('K-Means Clustering of Reuters Articles')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.colorbar(label='Cluster')
        plt.show()

        ''')

    def NER(self):
        print(r'''# Install spaCy and download the model first:
        # !pip install spacy
        # !python -m spacy download en_core_web_sm

        # Import spaCy
        import spacy

        # Load the small English model for Named Entity Recognition
        nlp = spacy.load("en_core_web_sm")

        # Sample preprocessed dataset of historical documents
        documents = [
            "In 1492, Christopher Columbus discovered the Americas.",
            "Queen Isabella and King Ferdinand of Spain funded Columbus's expedition.",
            "The Magna Carta was signed in 1215 by King John of England."
        ]

        # Process each document to find named entities
        for text in documents:
            doc = nlp(text)
            print(f"\nText: {text}")
            print("Entities found:")
            for entity in doc.ents:
                print(f" - {entity.text}: {entity.label_}")
        ''')

    def NN(self):
        print(r'''import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder
        from tensorflow.keras.preprocessing.text import Tokenizer
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
        from tensorflow.keras.utils import to_categorical
        from sklearn.metrics import classification_report

        # Load the dataset (assuming the dataset has 'text' and 'intent' columns)
        data = pd.read_csv('/content/Bitext_Sample_Customer_Service_Training_Dataset.csv')

        # Encode the target labels
        label_encoder = LabelEncoder()
        data['intent'] = label_encoder.fit_transform(data['intent'])

        # Tokenize and pad the input text
        max_words = 10000  # Adjust vocabulary size as needed
        max_len = 100       # Adjust maximum sequence length as needed
        tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
        tokenizer.fit_on_texts(data['utterance'])
        X = tokenizer.texts_to_sequences(data['utterance'])
        X = pad_sequences(X, maxlen=max_len)
        y = to_categorical(data['intent'])

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Build the Neural Network model
        model = Sequential([
            Embedding(input_dim=max_words, output_dim=128, input_length=max_len),
            LSTM(128, return_sequences=False),
            Dropout(0.5),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(y.shape[1], activation='softmax')
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

        # Evaluate the model
        y_pred = np.argmax(model.predict(X_test), axis=1)
        y_true = np.argmax(y_test, axis=1)

        # Generate classification report
        report = classification_report(y_true, y_pred, target_names=label_encoder.classes_)
        print("\nClassification Report:\n", report)
        ''')






class Old:

    def hello1(self):
        print('''
            import nltk
    from nltk.tag import hmm

    # Create a small custom corpus (word, POS tag pairs)
    train_data = [
        [('The', 'DT'), ('cat', 'NN'), ('sat', 'VBD')],
        [('A', 'DT'), ('dog', 'NN'), ('barked', 'VBD')],
        [('The', 'DT'), ('dog', 'NN'), ('runs', 'VBZ')],
        [('She', 'PRP'), ('loves', 'VBZ'), ('dogs', 'NNS')]
    ]

    # Create the HMM tagger
    trainer = hmm.HiddenMarkovModelTrainer()

    # Train the HMM POS tagger
    tagger = trainer.train(train_data)

    # Test sentence
    test_sentence = "The dog runs".split()

    # Tag the test sentence
    tagged_sentence = tagger.tag(test_sentence)

    # Print the tagged sentence
    print(tagged_sentence)
    ''')
        
        
        
    def hello2(self):
        print('''
    # Program 2: Text Classification using Naive Bayes
    # Implement a Naive Bayes classifier for text classification using the 20 Newsgroups dataset.

    from sklearn.datasets import fetch_20newsgroups
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    from sklearn import metrics

    # Load the 20 Newsgroups dataset
    newsgroups = fetch_20newsgroups(subset='all')

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(newsgroups.data, newsgroups.target, test_size=0.2, random_state=42)

    # Convert text data into feature vectors using CountVectorizer
    vectorizer = CountVectorizer(stop_words='english')
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Train the Naive Bayes classifier
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vectorized, y_train)

    # Make predictions
    y_pred = nb_classifier.predict(X_test_vectorized)

    # Evaluate the model
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Classification Report:\n", metrics.classification_report(y_test, y_pred))

    ''')
        
    def hello3(self):
        print('''
    # Program 3: Dependency Parsing using CKY Algorithm
    # Implement the CKY algorithm for dependency parsing using a context-free grammar.

    import nltk
    from nltk import CFG

    # Define a simple context-free grammar (CFG)
    grammar = CFG.fromstring("""
    S -> NP VP
    VP -> V NP
    NP -> Det N
    Det -> 'a' | 'the'
    N -> 'dog' | 'cat'
    V -> 'chases' | 'sees'
    """)

    # Input sentence (as a list of words)
    sentence = ['the', 'dog', 'chases', 'a', 'cat']

    # Create a parser using the CKY algorithm
    parser = nltk.ChartParser(grammar)

    # Parse the sentence
    for tree in parser.parse(sentence):
        tree.pretty_print()
            ''')
        
    def hello4(self):
        print('''
    # Program 4: Word Embeddings using Word2vec 
    # Implement Word2vec using the Gensim library and train it on a given text corpus.
    from gensim.models import Word2Vec
    from nltk.tokenize import word_tokenize
    import nltk

    # Download NLTK data (if necessary)
    # nltk.download('punkt')

    # Sample corpus (a list of sentences)
    corpus = [
        "I love machine learning",
        "Word embeddings are useful in NLP",
        "Word2Vec is a popular algorithm",
        "Machine learning is fun"
    ]

    # Tokenize the corpus (split into words)
    tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]

    # Train Word2Vec model
    model = Word2Vec(tokenized_corpus, vector_size=50, window=3, min_count=1, sg=0)
    # model
    # # Example: Get the vector for a word
    word_vector = model.wv['machine']

    # Output the word vector
    print("Vector for 'machine':", word_vector)

    # Example: Find most similar words to 'machine'
    similar_words = model.wv.most_similar('machine', topn=3)
    print("Most similar words to 'machine':", similar_words)

            ''')
        

    def hello5(self):
        print('''
    # Program 5: Text Summarization using Extractive Summarization
    # Implement an extractive summarization algorithm using Textrank

    import spacy
    import pytextrank

    # Load a pre-trained spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Add the TextRank component to the spaCy pipeline
    nlp.add_pipe("textrank")

    # Sample text to summarize
    text = """
    Text summarization is the process of creating a concise and coherent version of a longer text document. 
    There are two main types of text summarization techniques: extractive and abstractive. 
    Extractive summarization selects key sentences directly from the text, while abstractive summarization generates new sentences.
    """

    # Process the text
    doc = nlp(text)

    # Extractive summarization: Get top sentences based on TextRank
    summary = [sent.text for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=2)]

    # Print the summary
    print("Summary:", " ".join(summary))

            ''')
        

    def hello6(self):
        print('''
    # Program 6: Named Entity Recognition using HMM
    # Implement a Hidden Markov Model (HMM) for Named Entity Recognition (NER).

    import nltk
    from nltk.tag import hmm
    from nltk.corpus import conll2002

    # Download necessary NLTK datasets
    # nltk.download('conll2002')

    # Train a Hidden Markov Model (HMM) for NER using the conll2002 dataset
    train_sents = conll2002.iob_sents('esp.train')  # Training data
    test_sents = conll2002.iob_sents('esp.testb')  # Test data

    # Train the HMM model
    trainer = hmm.HiddenMarkovModelTrainer()
    ner_model = trainer.train(train_sents)

    # Test the model on a sentence
    test_sentence = [("John", "NP"), ("Doe", "NP"), ("is", "VB"), ("a", "DT"), ("doctor", "NN")]
    ner_tags = ner_model.tag_sents([test_sentence])

    # Print the NER results
    print(ner_tags)
            ''')
        

    def hello7(self):
        print('''
    # Program 7: Sentiment Analysis using Supervised Learning
    # Implement a supervised learning model for sentiment analysis using the IMDB dataset.

    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import accuracy_score
    from sklearn.datasets import load_files

    # Load the IMDB dataset (reviews labeled with sentiment: positive/negative)
    # You can download the IMDB dataset from sklearn or other sources, here it is assumed to be pre-loaded
    # If using an external dataset, you can load it as follows:
    # imdb = load_files("path_to_imdb_data", categories=["pos", "neg"])

    # For simplicity, we use a smaller example dataset with predefined labels
    data = {
        'data': ["I love this movie", "This was a terrible movie", "Amazing film!", "I hate this film", "Great performance", "Not good at all"],
        'target': [1, 0, 1, 0, 1, 0]
    }

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'], test_size=0.3, random_state=42)

    # Convert text to numerical features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train a Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test_tfidf)

    # Evaluate the model
    print("Accuracy:", accuracy_score(y_test, y_pred))

            ''')
        
        
    def hello8(self):
        print('''
    # Program 8: Semantic Similarity Measure using WordNet
    # Implement a semantic similarity measure using WordNet.

    from nltk.corpus import wordnet as wn

    # Download necessary NLTK data
    import nltk
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')

    # Define two words
    word1 = "dog"
    word2 = "cat"

    # Get WordNet synsets for each word
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    # Calculate similarity between the first synset of both words
    similarity = synsets1[0].wup_similarity(synsets2[0])

    # Output the similarity score
    print(f"Semantic similarity between '{word1}' and '{word2}': {similarity}")

    ''')
        
        
    def hello9(self):
        print('''
    # Program 9: Character-to-Sentence Embeddings using CNN
    # Implement character-to-sentence embeddings using a Convolutional Neural Network (CNN).

    import numpy as np
    from keras.models import Sequential
    from keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense
    from keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.preprocessing.text import Tokenizer

    # Sample sentences (a small example for simplicity)
    sentences = ["I love machine learning", "Deep learning is amazing", "Natural language processing is fun"]

    # Tokenize the sentences by characters
    tokenizer = Tokenizer(char_level=True)
    tokenizer.fit_on_texts(sentences)
    sequences = tokenizer.texts_to_sequences(sentences)

    # Pad the sequences to have equal length
    X = pad_sequences(sequences, padding='post')

    # Define the model
    model = Sequential()
    model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=50, input_length=X.shape[1]))
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification (can be adjusted)

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Print model summary
    model.summary()

    # Example: Training the model (dummy labels for illustration)
    y = np.array([1, 1, 0])  # Example labels (binary classification)
    model.fit(X, y, epochs=5)
            ''')
        
        
    def hello10(self):
        print('''

    import nltk
    import networkx as nx
    from sklearn.feature_extraction.text import TfidfVectorizer
    from nltk.corpus import stopwords

    # Download necessary NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')

    # Sample document and query
    document = """
    Text summarization is the task of creating a shortened version of a text document that retains the most important information. 
    There are two primary types of summarization: extractive and abstractive. Extractive summarization selects key sentences from the document, 
    while abstractive summarization generates new sentences to summarize the content.
    """
    query = "summarization"

    # Tokenize the document into sentences
    sentences = nltk.sent_tokenize(document)

    # Vectorize sentences using TF-IDF
    vectorizer = TfidfVectorizer(stop_words=stopwords.words("english"))
    X = vectorizer.fit_transform(sentences)

    # Compute similarity matrix
    cosine_sim = (X * X.T).toarray()

    # Create a graph using the correct function
    graph = nx.from_numpy_array(cosine_sim)

    # Rank sentences using PageRank
    ranked_sentences = nx.pagerank(graph)

    # Sort sentences based on their rank
    sorted_sentences = sorted(ranked_sentences, key=ranked_sentences.get, reverse=True)

    # Select top 2 sentences for the summary
    summary = [sentences[i] for i in sorted_sentences[:2]]

    # Output the summary
    print("Summary:", " ".join(summary))
        
        ''')
        
        
    def tejas(self):
        print('''
            pro 1 


    import nltk
    from nltk.corpus import treebank
    from sklearn.metrics import confusion_matrix, accuracy_score

    # Download necessary resources
    nltk.download('treebank')
    nltk.download('universal_tagset')

    # Load the Penn Treebank dataset with universal tagset
    tagged_sentences = nltk.corpus.treebank.tagged_sents(tagset='universal')

    # Split the data into training and testing sets (e.g., 80/20 split)
    train_size = int(len(tagged_sentences) * 0.8)
    train_set = tagged_sentences[:train_size]
    test_set = tagged_sentences[train_size:]

    # Train an HMM using NLTK's HiddenMarkovModelTrainer
    from nltk.tag.hmm import HiddenMarkovModelTrainer

    trainer = HiddenMarkovModelTrainer()
    hmm_model = trainer.train(train_set)

    # Evaluate the model on the test set
    accuracy = hmm_model.evaluate(test_set)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Generate predictions for the test set to create confusion matrix
    true_tags = []
    predicted_tags = []

    for sentence in test_set:
        words = [word for word, _ in sentence]
        true_tags.extend([tag for _, tag in sentence])
        predicted_tags.extend(hmm_model.tag(words))

    # Flatten predicted_tags (removing words)
    predicted_tags_flat = [tag for _, tag in predicted_tags]

    # Calculate confusion matrix
    cm = confusion_matrix(true_tags, predicted_tags_flat, labels=hmm_model._states)
    print(f"Confusion Matrix:\n{cm}")

    # Optional: Normalize confusion matrix and print as a heatmap
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.heatmap(cm, annot=True, fmt='d', xticklabels=hmm_model._states, yticklabels=hmm_model._states, cmap='coolwarm')
    plt.xlabel('Predicted Tags')
    plt.ylabel('True Tags')
    plt.title('Confusion Matrix for PoS Tagging')
    plt.show()




    prog 2 


    import numpy as np
    from sklearn.datasets import fetch_20newsgroups
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import classification_report, accuracy_score
    from nltk.stem import PorterStemmer
    from nltk.corpus import stopwords
    import nltk

    # Download NLTK resources
    nltk.download('stopwords')

    # 1. Load Dataset
    categories = None  # Use all categories
    data = fetch_20newsgroups(subset='all', categories=categories, remove=('headers', 'footers', 'quotes'))

    # 2. Data Preprocessing
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    def preprocess(text):
        tokens = text.split()
        tokens = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
        return " ".join(tokens)

    # Preprocess all documents
    data_cleaned = [preprocess(doc) for doc in data.data]

    # 3. Split Dataset
    X_train, X_test, y_train, y_test = train_test_split(data_cleaned, data.target, test_size=0.2, random_state=42)

    # 4. Feature Extraction
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vect = vectorizer.fit_transform(X_train)
    X_test_vect = vectorizer.transform(X_test)

    # 5. Train Naive Bayes Classifier
    model = MultinomialNB()
    model.fit(X_train_vect, y_train)

    # 6. Evaluate the Model
    y_pred = model.predict(X_test_vect)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    report = classification_report(y_test, y_pred, target_names=data.target_names)
    print("Classification Report:\n", report)





    prog 3 


    import nltk
    from nltk import CFG
    from nltk.parse import ChartParser

    # 1. Define Grammar in Chomsky Normal Form (CNF)
    grammar = CFG.fromstring("""
        S -> NP VP
        VP -> V NP | V
        NP -> Det N | N
        Det -> 'the' | 'a'
        N -> 'cat' | 'dog' | 'mat'
        V -> 'chased' | 'sat'
    """)

    # 2. Create a Parser
    parser = ChartParser(grammar)

    # 3. Parse a Sentence
    def parse_sentence(sentence):
        """
        Parse a given sentence using NLTK's ChartParser.
        Args:
            sentence: Input sentence as a list of words.
        """
        print("Parsing Sentence:", " ".join(sentence))
        trees = list(parser.parse(sentence))  # Parse the sentence
        if trees:
            for tree in trees:
                print("Dependency Tree:")
                tree.pretty_print()  # Visualize the tree
        else:
            print("The sentence could not be parsed.")

    # Example Usage
    sentence = "the cat chased the dog".split()
    parse_sentence(sentence)



    prog 4 

    # 4

    # File: word2vec_embedding.py

    import gensim
    from gensim.models import Word2Vec
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import nltk

    # Download NLTK resources
    # nltk.download('punkt')
    # nltk.download('stopwords')

    # 1. Preprocess the Corpus
    def preprocess_corpus(corpus):
        """
        Preprocess the corpus by tokenizing, removing stopwords, and keeping only alphabetic words.
        Args:
            corpus: List of sentences (text data).
        Returns:
            List of tokenized and preprocessed sentences.
        """
        stop_words = set(stopwords.words('english'))
        processed_corpus = []
        for sentence in corpus:
            tokens = word_tokenize(sentence.lower())  # Tokenize and convert to lowercase
            filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
            processed_corpus.append(filtered_tokens)
        return processed_corpus

    # Example Corpus (Replace this with your dataset)
    corpus = [
        "The cat sat on the mat.",
        "The dog chased the cat.",
        "Dogs and cats are animals.",
        "The mat was sat on by the cat.",
    ]

    # Preprocess the corpus
    processed_corpus = preprocess_corpus(corpus)
    print("Processed Corpus:", processed_corpus)

    # 2. Train Word2Vec Model
    def train_word2vec(corpus, vector_size=100, window=5, min_count=1, epochs=10):
        """
        Train a Word2Vec model using Gensim.
        Args:
            corpus: Preprocessed corpus.
            vector_size: Dimensionality of word vectors.
            window: Context window size.
            min_count: Minimum frequency for a word to be included.
            epochs: Number of training epochs.
        Returns:
            Trained Word2Vec model.
        """
        model = Word2Vec(sentences=corpus, vector_size=vector_size, window=window, min_count=min_count, workers=4)
        model.train(corpus, total_examples=model.corpus_count, epochs=epochs)
        return model

    # Train the Word2Vec model
    model = train_word2vec(processed_corpus)

    # 3. Visualize Word Embeddings
    def visualize_embeddings(model, method="pca"):
        """
        Visualize word embeddings using PCA or t-SNE.
        Args:
            model: Trained Word2Vec model.
            method: Dimensionality reduction method ("pca" or "tsne").
        """
        words = list(model.wv.index_to_key)  # Get vocabulary
        vectors = model.wv[words]           # Get word vectors

        if method == "pca":
            reducer = PCA(n_components=2)
            reduced_vectors = reducer.fit_transform(vectors)
        elif method == "tsne":
            reducer = TSNE(n_components=2, random_state=42, perplexity=5)
            reduced_vectors = reducer.fit_transform(vectors)
        else:
            raise ValueError("Invalid method. Choose 'pca' or 'tsne'.")

        # Plot the reduced vectors
        plt.figure(figsize=(10, 10))
        plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], edgecolors='k', c='orange')
        for i, word in enumerate(words):
            plt.annotate(word, xy=(reduced_vectors[i, 0], reduced_vectors[i, 1]), fontsize=12)
        plt.title(f"Word Embeddings Visualization ({method.upper()})")
        plt.show()

    # Visualize embeddings using PCA
    visualize_embeddings(model, method="pca")

    # Visualize embeddings using t-SNE
    visualize_embeddings(model, method="tsne")



    prog 5 


    # 5
    # Required Libraries
    !pip install rouge-score

    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    import networkx as nx
    from rouge_score import rouge_scorer
    nltk.download('punkt')
    nltk.download('stopwords')

    # Text Preprocessing
    def preprocess_text(text):
        """
        Preprocess the input text: tokenize sentences and words, remove stopwords.
        Args:
            text (str): The input text.
        Returns:
            List of tokenized sentences and cleaned sentences.
        """
        stop_words = set(stopwords.words('english'))
        sentences = sent_tokenize(text)  # Sentence tokenization
        processed_sentences = []
        for sentence in sentences:
            words = word_tokenize(sentence.lower())  # Tokenize words
            words = [word for word in words if word.isalnum() and word not in stop_words]
            processed_sentences.append(words)
        return sentences, processed_sentences

    # Build Similarity Matrix
    def build_similarity_matrix(sentences):
        """
        Create a similarity matrix for the sentences using cosine similarity.
        Args:
            sentences (list): List of tokenized sentences.
        Returns:
            similarity_matrix (numpy.ndarray): Sentence similarity matrix.
        """
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        # Join words to recreate sentences
        joined_sentences = [' '.join(sentence) for sentence in sentences]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(joined_sentences)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        return similarity_matrix

    # TextRank Algorithm
    def textrank_summarization(text, top_n=3):
        """
        Summarize the text using the TextRank algorithm.
        Args:
            text (str): The input text.
            top_n (int): Number of sentences to include in the summary.
        Returns:
            summary (str): Extracted summary.
        """
        original_sentences, processed_sentences = preprocess_text(text)
        similarity_matrix = build_similarity_matrix(processed_sentences)

        # Create a graph from the similarity matrix
        graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(graph)

        # Rank sentences based on scores
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(original_sentences)), reverse=True)

        # Select top N sentences for the summary
        summary = " ".join([sentence for _, sentence in ranked_sentences[:top_n]])
        return summary

    # Example Text
    text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence
    concerned with the interactions between computers and human language, in particular how to program computers
    to process and analyze large amounts of natural language data. The result is a computer capable of
    "understanding" the contents of documents, including the contextual nuances of the language within them.
    The technology can then accurately extract information and insights contained in the documents as well as
    categorize and organize the documents themselves.
    """

    # Generate Summary
    summary = textrank_summarization(text, top_n=2)
    print("Summary:")
    print(summary)

    # Evaluate Summary using ROUGE
    def evaluate_summary(reference, generated):
        """
        Evaluate the generated summary using ROUGE metrics.
        Args:
            reference (str): Reference summary.
            generated (str): Generated summary.
        Returns:
            scores (dict): ROUGE scores.
        """
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference, generated)
        return scores

    # Reference Summary (Manually written)
    reference_summary = """
    NLP is a field of AI focused on programming computers to process and analyze natural language.
    It enables computers to understand documents' content, extract insights, and organize documents.
    """

    # Evaluate the generated summary
    rouge_scores = evaluate_summary(reference_summary, summary)
    print("\nROUGE Scores:")
    print(rouge_scores)


    prog 6 

    import unicodedata
    import nltk
    from nltk.corpus import conll2002
    from hmmlearn.hmm import MultinomialHMM
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    import numpy as np

    # Download NLTK data
    nltk.download('conll2002')

    # Normalize text to handle special characters
    def normalize_text(text):
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

    # Load and preprocess the dataset
    def preprocess_data(data):
        normalized_data = []
        for sent in data:
            normalized_sent = [(normalize_text(word), tag) for word, tag, _ in sent]
            normalized_data.append(normalized_sent)
        return normalized_data

    # Load train and test datasets
    train_data = preprocess_data(conll2002.iob_sents('esp.train'))
    test_data = preprocess_data(conll2002.iob_sents('esp.testb'))

    # Extract features (words) and labels (NER tags)
    def extract_features_and_labels(data):
        X = [[word for word, tag in sent] for sent in data]
        y = [[tag for word, tag in sent] for sent in data]
        return X, y

    X_train, y_train = extract_features_and_labels(train_data)
    X_test, y_test = extract_features_and_labels(test_data)

    # Flatten data for encoding
    flat_X_train = [word for sent in X_train for word in sent]
    flat_y_train = [tag for sent in y_train for tag in sent]
    flat_X_test = [word for sent in X_test for word in sent]
    flat_y_test = [tag for sent in y_test for tag in sent]

    # Encode words and tags
    word_encoder = LabelEncoder()
    tag_encoder = LabelEncoder()

    word_encoder.fit(flat_X_train + flat_X_test)
    tag_encoder.fit(flat_y_train + flat_y_test)

    X_train_encoded = [word_encoder.transform([word for word in sent]) for sent in X_train]
    X_test_encoded = [word_encoder.transform([word for word in sent]) for sent in X_test]

    y_train_encoded = [tag_encoder.transform([tag for tag in sent]) for sent in y_train]
    y_test_encoded = [tag_encoder.transform([tag for tag in sent]) for sent in y_test]

    # Prepare input for HMM (flatten sequences for hmmlearn)
    def prepare_hmm_data(X, y):
        lengths = [len(seq) for seq in X]
        X_flat = np.concatenate(X)
        y_flat = np.concatenate(y)
        return X_flat, y_flat, lengths

    X_train_hmm, y_train_hmm, train_lengths = prepare_hmm_data(X_train_encoded, y_train_encoded)
    X_test_hmm, y_test_hmm, test_lengths = prepare_hmm_data(X_test_encoded, y_test_encoded)

    # Train HMM
    hmm_model = MultinomialHMM(n_components=len(tag_encoder.classes_), random_state=42, n_iter=100)
    hmm_model.fit(X_train_hmm.reshape(-1, 1), train_lengths)

    # Predict using HMM
    y_pred_hmm = []
    start_idx = 0
    for length in test_lengths:
        end_idx = start_idx + length
        seq = X_test_hmm[start_idx:end_idx].reshape(-1, 1)
        predicted = hmm_model.predict(seq)
        y_pred_hmm.extend(predicted)
        start_idx = end_idx

    # Decode predictions and true labels
    y_pred_decoded = tag_encoder.inverse_transform(y_pred_hmm)
    y_true_decoded = tag_encoder.inverse_transform(y_test_hmm)

    # Evaluation
    accuracy = accuracy_score(y_true_decoded, y_pred_decoded)
    conf_matrix = confusion_matrix(y_true_decoded, y_pred_decoded, labels=tag_encoder.classes_)
    classification_report_str = classification_report(y_true_decoded, y_pred_decoded, labels=tag_encoder.classes_)

    print(f"Accuracy: {accuracy:.4f}")
    print("\nConfusion Matrix:")
    print(conf_matrix)
    print("\nClassification Report:")
    print(classification_report_str)


    prog 7 

    import nltk
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.svm import LinearSVC
    from sklearn.metrics import accuracy_score, f1_score, classification_report
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import pandas as pd
    import numpy as np

    # Download NLTK resources
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('movie_reviews')

    from nltk.corpus import movie_reviews

    # Load IMDB dataset from NLTK
    def load_imdb_data():
        """
        Load the IMDB dataset from the NLTK movie_reviews corpus.
        Returns:
            - data: List of text reviews.
            - labels: List of sentiment labels ('pos', 'neg').
        """
        data = []
        labels = []
        for fileid in movie_reviews.fileids():
            data.append(movie_reviews.raw(fileid))
            labels.append(movie_reviews.categories(fileid)[0])
        return data, labels

    # Preprocess the dataset
    def preprocess_text(text):
        """
        Preprocess text data by tokenizing, removing stopwords, and keeping only alphabetic tokens.
        Args:
            text: Raw text data.
        Returns:
            Preprocessed text as a string.
        """
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        return " ".join(filtered_tokens)

    # Load and preprocess the dataset
    data, labels = load_imdb_data()
    data = [preprocess_text(review) for review in data]

    # Encode labels as binary values
    label_map = {'pos': 1, 'neg': 0}
    labels = [label_map[label] for label in labels]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, random_state=42, stratify=labels)

    # Build a pipeline for training
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),  # Convert text to bag-of-words
        ('tfidf', TfidfTransformer()),     # Apply TF-IDF transformation
        ('classifier', LinearSVC())        # Linear Support Vector Classifier
    ])

    # Train the model
    pipeline.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))


    prog 8 

    import nltk
    from nltk.corpus import wordnet as wn
    from sklearn.metrics import mean_squared_error
    import numpy as np

    # Download NLTK resources
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('words')

    # WordSim-353 dataset (A small subset for demonstration)
    # Each pair contains two words and the similarity score (rated from 0 to 10 by human annotators)
    wordsim_353 = [
        ("car", "auto", 9.0),
        ("ship", "boat", 8.0),
        ("dog", "cat", 9.5),
        ("man", "woman", 10.0),
        ("tree", "bush", 7.5),
        ("apple", "banana", 8.5),
        ("love", "hate", 2.0),
        ("king", "queen", 9.5),
        ("school", "education", 8.0),
        ("dog", "wolf", 8.5),
    ]

    # Function to calculate similarity using Wu-Palmer similarity
    def calculate_similarity(word1, word2):
        """
        Calculate the semantic similarity between two words using Wu-Palmer similarity.
        Args:
            word1: First word.
            word2: Second word.
        Returns:
            Similarity score (float), or None if no synsets are found.
        """
        synsets1 = wn.synsets(word1)
        synsets2 = wn.synsets(word2)

        if not synsets1 or not synsets2:
            return 0.0  # Return 0 if no synsets found for either word

        # Take the first synset (most common sense)
        synset1 = synsets1[0]
        synset2 = synsets2[0]

        # Calculate similarity using Wu-Palmer similarity
        similarity = synset1.wup_similarity(synset2)
        return similarity if similarity is not None else 0.0

    # List to store predicted and true similarity scores
    predicted_scores = []
    true_scores = []

    # Calculate similarity for each word pair and store the results
    for word1, word2, true_score in wordsim_353:
        predicted_score = calculate_similarity(word1, word2)
        predicted_scores.append(predicted_score)
        true_scores.append(true_score)

    # Evaluate the results using Mean Squared Error (MSE)
    mse = mean_squared_error(true_scores, predicted_scores)
    print(f"Mean Squared Error between predicted and true similarity scores: {mse:.4f}")

    # Optionally, you could calculate the Pearson correlation for a better evaluation
    from scipy.stats import pearsonr
    corr, _ = pearsonr(predicted_scores, true_scores)
    print(f"Pearson correlation: {corr:.4f}")


    prog 9 



    import numpy as np
    import tensorflow as tf
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.datasets import imdb
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    from sklearn.manifold import TSNE

    # Step 1: Load the IMDB dataset
    # IMDB dataset comes preloaded with Keras
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

    # Step 2: Preprocess the data (pad sequences)
    max_sequence_length = 500  # Max length for each sentence
    x_train = pad_sequences(x_train, maxlen=max_sequence_length)
    x_test = pad_sequences(x_test, maxlen=max_sequence_length)

    # Step 3: Define a simple CNN model for sentence embeddings
    input_text = Input(shape=(max_sequence_length,))

    # Character-level embedding (the characters are tokens already in the IMDB dataset)
    embedding_layer = Embedding(input_dim=10000, output_dim=128, input_length=max_sequence_length)(input_text)

    # Apply Convolutional layers
    conv_layer = Conv1D(filters=128, kernel_size=3, activation='relu')(embedding_layer)
    pool_layer = GlobalMaxPooling1D()(conv_layer)

    # Dense layer
    dense_layer = Dense(128, activation='relu')(pool_layer)
    dropout_layer = Dropout(0.5)(dense_layer)
    output = Dense(1, activation='sigmoid')(dropout_layer)

    # Create the CNN model
    model = Model(inputs=input_text, outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Step 4: Train the model
    model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

    # Step 5: Get the sentence embeddings by taking the output from the CNN layers (before the final dense layer)
    embedding_model = Model(inputs=input_text, outputs=pool_layer)

    # Get sentence embeddings for the training data
    sentence_embeddings = embedding_model.predict(x_train)

    # Step 6: Visualize the sentence embeddings using PCA or t-SNE

    # First, reduce the dimensionality using PCA
    pca = PCA(n_components=2)
    reduced_embeddings_pca = pca.fit_transform(sentence_embeddings)

    # Plot the reduced embeddings using PCA
    plt.figure(figsize=(10, 8))
    plt.scatter(reduced_embeddings_pca[:, 0], reduced_embeddings_pca[:, 1], c=y_train, cmap='coolwarm', alpha=0.5)
    plt.title("Sentence Embeddings Visualization using PCA")
    plt.colorbar()
    plt.show()

    # Alternatively, reduce using t-SNE
    tsne = TSNE(n_components=2, random_state=42)
    reduced_embeddings_tsne = tsne.fit_transform(sentence_embeddings)

    # Plot the reduced embeddings using t-SNE
    plt.figure(figsize=(10, 8))
    plt.scatter(reduced_embeddings_tsne[:, 0], reduced_embeddings_tsne[:, 1], c=y_train, cmap='coolwarm', alpha=0.5)
    plt.title("Sentence Embeddings Visualization using t-SNE")
    plt.colorbar()
    plt.show()





    prog 10

    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    import networkx as nx
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from rouge_score import rouge_scorer
    import string
    import sklearn

    # Download necessary NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')

    # 1. Preprocess the text (tokenization, stopword removal)
    def preprocess_text(text):
        stop_words = set(stopwords.words('english'))
        sentences = sent_tokenize(text)  # Tokenize text into sentences
        clean_sentences = []

        for sentence in sentences:
            words = word_tokenize(sentence.lower())  # Tokenize into words and lowercase
            clean_words = [word for word in words if word.isalpha() and word not in stop_words]
            clean_sentences.append(' '.join(clean_words))

        return clean_sentences, sentences

    # 2. Create a similarity matrix based on cosine similarity
    def create_similarity_matrix(sentences):
        # Create the cosine similarity matrix
        vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        return similarity_matrix

    # 3. Implement Graph-Based Method (TextRank)
    def text_rank_summary(text, top_n=3):
        # Preprocess the text
        clean_sentences, original_sentences = preprocess_text(text)

        # Create a similarity matrix
        similarity_matrix = create_similarity_matrix(clean_sentences)

        # Build a graph based on the similarity matrix
        nx_graph = nx.from_numpy_array(similarity_matrix)

        # Apply PageRank (TextRank)
        scores = nx.pagerank(nx_graph)

        # Sort the sentences by their score
        ranked_sentences = [original_sentences[i] for i in sorted(scores, key=scores.get, reverse=True)]

        # Select top N sentences
        summary = ' '.join(ranked_sentences[:top_n])
        return summary

    # 4. Evaluate the summary using ROUGE metric
    def evaluate_summary(reference, summary):
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference, summary)
        return scores

    # Example text and query
    text = """
    Natural language processing (NLP) is a sub-field of artificial intelligence (AI) that is concerned with the interactions between computers and human (natural) languages. It deals with applications such as speech recognition, text analysis, sentiment analysis, machine translation, and much more. NLP is a highly interdisciplinary field, combining linguistics, computer science, and AI techniques to understand and generate human language in a way that is both meaningful and valuable.
    The ultimate goal of NLP is to develop systems that can perform tasks that require understanding and manipulating natural language, such as summarizing text, answering questions, and making recommendations. NLP has made significant progress over the past few years, with the development of powerful language models like GPT and BERT. These models have revolutionized the way machines understand and interact with human language, making NLP a crucial technology in today's world.
    """

    query = "NLP and its applications"

    # Generate summary based on the query (query-based summarization)
    summary = text_rank_summary(text, top_n=2)
    print("Generated Summary:", summary)

    # Evaluate using ROUGE (using the query as the reference summary)
    rouge_scores = evaluate_summary(query, summary)
    print("ROUGE Scores:", rouge_scores)
    

    
            ''')