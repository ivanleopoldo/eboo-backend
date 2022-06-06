from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.utils import load_plugins
from core.utils import PluginHandler
from core.utils import start_download
from core.assets import Base
from core.assets import plugin_dir
from pathlib import Path
import uvicorn
import os

# init
app = FastAPI()
plug_handle = PluginHandler(plugin_dir, "plugins.db.json")

# cors
origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

# middleware
@app.middleware("http")
async def middleware(request, call_next):
    Base.plugins = []
    load_plugins()

    res = await call_next(request)
    return res

# global var
response = dict({
        "response": ""
    })

# main routes
@app.get("/")
def index():
    response["response"] = "connected"
    return response

@app.post("/search")
def search(keywords: str):
    try:
        results = []
        for plug in Base.plugins:
            search_results = plug().search(keywords)
            results.append({
                "plugin": plug.__name__,
                "results": search_results
            })
        response["response"] = results
    except:
        response["response"] = []
    
    return response

@app.post("/download/novel")
def download(keywords: str):
    try:
        start_download(keywords)
        response["response"] = "success"
    except:
        response["response"] = "failed"
    
    return response

@app.post("/email/novel")
def email_novel():
    pass

@app.get("/settings")
def settings():
    response["response"] = "success"
    return response

@app.post("/settings")
def settings(string: str):
    response["response"] = string
    return response

# plugin manager routes
@app.get("/plugins/downloadable")
def downloadable_plugins():
    try:
        response["response"] = [plug for plug in plug_handle.get_plugin_list() if plug not in [plug.__module__ for plug in Base.plugins]]
    except:
        response["response"] = []

    return response

@app.get("/plugins/downloaded")
def downloaded_plugins():
    pass

@app.get("/plugins/default")
def default_plugins():
    pass

@app.get("/plugins/local")
def local_plugins():
    return {"plugins": [plug for plug in Base.plugins]}

@app.post("/download/plugin")
def download_plugin(plugin: str):
    try:
        plug_handle.download_plugin(plugin)
        response["response"] = "success"
    except:
        response["response"] = "failed"

    return response

@app.post("/delete/plugin")
def delete_plugin(plugin: str):
    try:
        plug_handle.delete_plugin(plugin)
        response["response"] = "success"
    except:
        response["response"] = "failed"
        
    return response

# dev routes
@app.get("/path")
def path():
    return {
        "path": os.getcwd(),
        "dir": os.path.dirname(__file__),
        "abs": str(Path(__file__))
    }

@app.get("/github/plugins")
def available_plugins():
    try:
        response["response"] = plug_handle.get_plugin_list()
    except:
        response["response"] = []

    return response

# functions
def serve():
    # uvicorn.run(app, port=81)
    uvicorn.run("app:app", port=81, reload=True)

# main
if __name__ == "__main__":
    serve()