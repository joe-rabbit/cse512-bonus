# Introduction
This is a working RAG (Retrieval-Augmented Generation) model built using Elasticsearch and OpenAI's GPT API. It indexes a Shakespearean dataset and provides explanations for prompts in Shakespearean English.
This project is created for CSE 512-extra credits requirements.Generative AI was used to creating the project.It only performs semantic searching on text. No other searching is performed
# Explaination of the Structure
```bash
├── app.py
├── mp3_files
└── my-app
```
- **Front End** : The front end code is present is in the my-app dir , it consists of the chat-interface.tsx which is  a type script file consists of the chat UI as shown below.It provides an interface working with the model.
- **Back End** : The backend is code is present in app.py file.It consists of the openai api,and the main elastic search based indexing using semantic search as shown in the
<a href="https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/00-quick-start.ipynb"/>example</a>.
# Pre-requirements
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
![View the demo here](https://github.com/joe-rabbit/cse512-bonus/blob/main/Bonus_Submission.mp4)
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
