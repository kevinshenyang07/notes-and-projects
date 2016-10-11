## Yet Another Language Detection Model

### Problem Description:
European Parliament Proceedings Parallel Corpus is a text dataset used for evaluating language detection engines. The extracted 5.7GB corpus includes 21 languages spoken in EU.

The taks is to create a machine learning model trained on this dataset to predict the language of a similar document.

It's nice that the documents are structured and formal texts, which saves much time on text cleaning. While the challenge is to train the model with the huge amout of data and to detect the language in very short time when used in web application.

### Approach:
1. Sample the corpus and transform both training and test data into cleaned language - text pair.
2. Use TFIDF model or Word2Vec to transform text into sentence vector.
3. Use Logistic Regression with LBFGS or Random Forest as the models to be trained.
4. Experiment with the parameters by cross-validation to decide which model to be used in the end. 
5. Use grid paramters to get the optimal model on test data.

### Why using Python to process the text files?
Since there are so many text files for each language, it would be less efficient for spark to handle all the file I/O while using local Python has less overhead. Compared to Map-Reduce framework, file streaming would be much faster when loading the whole corpus.

### Why Spark?
Simply because it's scalable. It can be easily scaled to 100 languages and larger dataset, even the model trained in local is decent, we have the option to push it higher.

### Why TFIDF over Word2Vec and Logistic Regression over Random Forest?
TFIDF is still little bit faster than Word2Vec and requires less memory. Both of them are good enough as a input layer. Logistic Regression is better in this case because it takes less time training and works better dealing with numerical features.

### The result and possible improvement?
Best model accuracy: 99.47%,  f-score: 0.9947.
Model stored in model/ directory.

More features can be used in TFIDF model (currenly limited by local memory).