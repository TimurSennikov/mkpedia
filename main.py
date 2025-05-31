import uvicorn
from mk import *

if __name__ == "__main__":
    uvicorn.run("mk:app", port=5000)
