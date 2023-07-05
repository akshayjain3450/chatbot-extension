# chatbot-extension
This project is simple chatbot chrome extension which scraps data of the current active tab and let user ask chatbot to return snippets from the article with a certain keyword. This is built using VueJS and FastAPI

## Steps to run the project:

### Frontend:
Tech Stack: Node 18.16.0, NPM 9.5.1, VueJS
#### Install node packages
1. (Current location of terminal should be frontend) `npm install`

### Backend:
Tech Stack: Python 3.10
#### Create a virtual environment and activate
1. `make virtual`
#### Install the dependencies/libraries
2. `make setup-backend`
#### Place the creds
3. Put the supabase url and key in backend.py
#### Run the backend server
3. (Run this from backend folder location) `uvicorn backend:app --reload`


### How to use the extension:
1. Load the extension in Chrome:
2. Open Chrome and navigate to chrome://extensions. 
3. Enable the "Developer mode" toggle on the top right of the page. 
4. Click on the "Load unpacked" button and select the folder containing your extension.
