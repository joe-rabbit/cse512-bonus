# Introduction
This is a working RAG (Retrieval-Augmented Generation) model built using Elasticsearch and OpenAI's GPT API. It indexes a Shakespearean dataset and provides explanations for prompts in Shakespearean English.
This project is created for CSE 512-extra credits requirements.Generative AI was used to creating the project.It only performs semantic searching on text. No other searching is performed.
#### Data used for this project can be found <a href="https://raw.githubusercontent.com/linuxacademy/content-elasticsearch-deep-dive/refs/heads/master/sample_data/shakespeare.json"> here </a>
The provided content represents a data format intended for ingestion into Elasticsearch, a distributed search engine and analytics platform. Each document corresponds to an entry (such as an act, scene, or line) from Shakespeare's play "Henry IV." Here's a detailed explanation of the structure
#### Key Elements:
Index Directive:
Example:
```bash
    {"index":{"_index":"shakespeare","_id":0}}
```
-  **_index**: Specifies the Elasticsearch index where the document will be stored (shakespeare in this case).
- **_id**: The unique identifier for the document within the index. Each document has its own ID, incrementing sequentially in this example.

#### Document Content:
Example:
```bash
        {"type":"act","line_id":1,"play_name":"Henry IV", "speech_number":"","line_number":"","speaker":"","text_entry":"ACT I"}
```
Represents the data for a specific entry. Key fields include:
- **type**: The category of the entry (e.g., act, scene, or line).
- **line_id**: A unique identifier for each line or entry in the play.
- **play_name**: The name of the play (Henry IV in this case).
- **speech_number**: Denotes a speech's sequence. It’s empty for entries like acts or scenes but populated for dialogue lines.
- **line_number**: The location of the line within the play, formatted as Act.Scene.Line.
- **speaker**: The character delivering the line (empty for acts or scenes).
- **text_entry**: The actual content of the entry (e.g., dialogue, act, or scene description).
Each **text_entry** is used for semantic searching

#### Prompt passed into the GPT API was
```bash
I have retrieved a line from a Shakespeare database based on a KNN search with the query '{QUERY}'.
Here is the closest result:
Score: {hit['_score']}
Text: {hit['_source']['text_entry']}
Please provide an analysis or interpretation of the retrieved line in the context of Shakespeare's works, focusing on themes and language style.
```

# Getting Started
- Create the elastic search account to access the cloud platform <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html"> here </a>
- Create the OpenAI API key <a href="https://platform.openai.com/settings/organization/api-keys"> here </a>
```bash
├── app.py
├── mp3_files
└── my-app
```
- **Front End** : The front end code is present is in the my-app dir , it consists of the chat-interface.tsx which is  a type script file consists of the chat UI as shown below.It provides an interface working with the model.
- **Back End** : The backend is code is present in app.py file.It consists of the openai api,and the main elastic search based indexing using semantic search as shown in the
<a href="https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/00-quick-start.ipynb"/>example</a>.

- **Front End**
```bash
cd my-app
```
and run to install all dependencies
```bash
npm install 
```
or use yarn to install all dependencies
```bash
yarn install
```
- **Back End**
```bash
pip install elasticsearch openai flask gtts
```
# Preview of the Working Application
![Preview of Application](https://github.com/user-attachments/assets/34977cdc-8334-47c2-a45c-94c94174ec88)
### Demonstration video
![View the demo here](https://drive.google.com/file/d/1MfC-Cd5ESQty5iOH7nSBsVgup6UmD_jE/view?usp=sharing)
- Note: the error in the video is due to the fact that there was no speaker built in on the system this project was designed on so I was unable to try out the mp3 file on the same system.However, there exists an mp3 file for demonstration purposes.
# Frameworks
- **Front End**: Built using Next.js (requires Node.js 18 or above installed on the system)
- **Back End**: Built using Flask

# To Run the Application
## Front End
```bash
cd my-app
npm run dev
```
## Back End
On a seperate terminal in the parent directory
```bash
python3 app.py
```
