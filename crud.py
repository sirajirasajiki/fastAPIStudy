from sqlalchemy.orm import Session
from .models import User

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
