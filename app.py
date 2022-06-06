from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.utils import load_plugins, start_download, PluginHandler
from core.assets import Base, plugin_dir, models
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
def search(keywords: models.Keywords):
    try:
        results = []
        for plug in Base.plugins:
            search_results = plug().search(keywords.keywords)
            results.append({
                "plugin": plug.__name__,
                "results": search_results
            })
        response["response"] = results
    except:
        response["response"] = []
    
    return response

@app.post("/download/novel")
def download(keywords: models.Keywords):
    try:
        start_download(keywords.keywords)
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
def settings(arg: models.Settings):
    response["response"] = arg
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
    response["response"] = [plug.__module__ for plug in Base.plugins if not plug.__module__.startswith("default.")]
    return response

@app.get("/plugins/default")
def default_plugins():
    response["response"] = [plug.__module__ for plug in Base.plugins if plug.__module__.startswith("default.")]
    return response

@app.get("/plugins/local")
def local_plugins():
    response["response"] = [plug.__module__ for plug in Base.plugins]
    return response

@app.post("/download/plugin")
def download_plugin(plugin: models.Plugin):
    try:
        plug_handle.download_plugin(plugin.plugin_name)
        response["response"] = "success"
    except:
        response["response"] = "failed"

    return response

@app.post("/delete/plugin")
def delete_plugin(plugin: models.Plugin):
    try:
        plug_handle.delete_plugin(plugin.plugin_name)
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