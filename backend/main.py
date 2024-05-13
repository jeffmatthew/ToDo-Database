from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Database setup
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model for ToDo item
class ToDoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    completed = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create ToDo item
@app.post("/todo/", response_model=ToDoItem)
def create_todo_item(text: str, db: Session = Depends(get_db)):
    db_todo = ToDoItem(text=text)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Get all ToDo items
@app.get("/todo/", response_model=list[ToDoItem])
def get_todo_items(db: Session = Depends(get_db)):
    return db.query(ToDoItem).all()

# Get single ToDo item by ID
@app.get("/todo/{item_id}", response_model=ToDoItem)
def get_todo_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(ToDoItem).filter(ToDoItem.id == item_id).first()

# Update ToDo item by ID
@app.put("/todo/{item_id}", response_model=ToDoItem)
def update_todo_item(item_id: int, text: str, completed: bool, db: Session = Depends(get_db)):
    db_todo = db.query(ToDoItem).filter(ToDoItem.id == item_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Item not found")
    db_todo.text = text
    db_todo.completed = completed
    db.commit()
    return db_todo

# Delete ToDo item by ID
@app.delete("/todo/{item_id}", response_model=ToDoItem)
def delete_todo_item(item_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(ToDoItem).filter(ToDoItem.id == item_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_todo)
    db.commit()
    return db_todo
