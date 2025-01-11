from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# インメモリのユーザーデータベース
users = []

# ユーザーモデルの定義
class User(BaseModel):
    username: str
    email: str
    password: str

# Create: ユーザー作成
@app.post("/users/")
def create_user(user: User):
    # ユーザー名の重複チェック
    if any(u['username'] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")
    # ユーザー情報の保存
    users.append(user.dict())
    return {"message": "User registered successfully"}

# Read: 全ユーザー取得
@app.get("/users/")
def read_users():
    return {"Users": users}

# Read: 特定のユーザー取得
@app.get("/users/{username}")
def read_user(username: str):
    # ユーザーが存在するかのチェック
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

