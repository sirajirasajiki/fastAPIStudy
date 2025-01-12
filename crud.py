from sqlalchemy.orm import Session
from models import User

# ユーザー作成
def create_user(db: Session, username: str, email: str) -> User:
    new_user = User(username=username, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 特定のユーザーを取得
def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# 全ユーザーを取得
def get_users(db: Session):
    return db.query(User).all()

# ユーザー情報更新
def update_user(db: Session, user_id: int, username: str = None, email: str = None) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None  # ユーザーが見つからない場合はNoneを返す
    if username:
        user.username = username
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    return user

# ユーザー情報削除
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False  # ユーザーが見つからない場合はFalseを返す
    db.delete(user)
    db.commit()
    return True