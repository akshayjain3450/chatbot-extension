import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from supabase import create_client
from bs4 import BeautifulSoup
import uuid

# Get the Supabase credentials from environment variables
supabase_url = ""
supabase_key = ""

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/home")
def read_root():
    return {"message": "Hello, Welcome to Chrome-Extension by Akshay Jain!"}


@app.get("/scrap")
async def scrap_webpage(request: Request):
    active_tab_url = request.query_params.get("tabUrl")
    text_content = extract_text_content(active_tab_url)
    write_to_supabase(text_content, active_tab_url)


@app.get("/search")
async def search_article(request: Request):
    keyword = request.query_params.get("keyword")
    url = request.query_params.get("tabUrl")
    result = query_from_supabase(keyword, url)
    return json.dumps(result)


@app.get("/download")
async def download(request: Request):
    # Get user-defined file name
    file_name = request.query_params.get("fileName")
    active_tab_url = request.query_params.get("tabUrl")
    # Save the text content as a downloadable file
    text_content = extract_text_content(active_tab_url)
    print("downloading file...")
    file_path = save_text_content(text_content, file_name)
    return FileResponse(file_path, filename=f"{file_name}.txt", media_type="text/plain")


def extract_text_content(url):
    # Send a GET request to the active page URL
    response = requests.get(url)
    response.raise_for_status()

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    main_content = soup.get_text()
    non_blank_lines = [line for line in main_content.splitlines() if line.strip()]
    final_content = '\n'.join(non_blank_lines)
    return final_content


def save_text_content(text_content, file_name):
    file_path = f"../webpage/{file_name}.txt"
    with open(file_path, "w") as file:
        file.write(text_content)
    return file_path


def write_to_supabase(text_content, url):
    client = connectSupabase()
    data, count = client.table("articles").select("url").eq("url", url).limit(1).execute()
    if len(data[1]) > 0:
        print("this article is already stored in database")
        return
    for line in text_content.splitlines():
        print(line)
        data, count = client.table('articles').insert(
            {
                "uuid": str(uuid.uuid4()),
                "url": str(url),
                "content": str(line)
            }
        ).execute()
    print("data written to database...")


def query_from_supabase(keyword, url):
    client = connectSupabase()
    data, count = client.table("articles") \
        .select("*") \
        .eq("url", url) \
        .text_search("content", keyword) \
        .execute()
    result = list()
    for row in data[1]:
        result.append(row['content'])
    return result


def connectSupabase():
    # Create a Supabase client
    return create_client(supabase_url, supabase_key)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
