import uvicorn
from src.main import app_socket
if __name__ == "__main__":
    uvicorn.run(app_socket, host="0.0.0.0", port=8000)
