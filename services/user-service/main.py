from fastapi import FastAPI, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Base, User, Projects
from schemas import UserCreate, ProjectCreate
import database
from database import projects_collection  # import MongoDB collection
from datetime import datetime

app = FastAPI()

# Create tables (synchronous)
Base.metadata.create_all(bind=database.engine)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup endpoint
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store hashed password from frontend as-is
    db_user = User(
        name=user.name,
        age=user.age,
        occupation=user.occupation,
        organisation=user.organisation,
        interests=user.interests,
        email=user.email,
        password_hash=user.password  # already hashed on frontend
    )
    
    # Add to DB
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    
    
    return {"message": "User registered successfully", "user_id": db_user.id}

# Project creation endpoint
@app.post("/project-create")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    title_lower = project.title.lower()

    # Check if project exists (case-insensitive)
    existing_project = db.query(Projects).filter(Projects.title.ilike(title_lower)).first()
    if existing_project:
        raise HTTPException(status_code=400, detail="Project with this title already exists")

    # Insert new project
    new_project = Projects(
        title=title_lower,
        description=project.description,
        tech_stack=project.tech_stack
    )
    db.add(new_project)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Project with this title already exists")
    db.refresh(new_project)

    projects_collection.insert_one({
        "project_id": new_project.id,  # link to PostgreSQL ID
        "title": project.title,
        "description": project.description,
        "technologies": project.tech_stack,
        "created_at": datetime.utcnow(),
        "features": [],       # optional, can be added by user later
        "prerequisites": [],  # optional
        "extra_info": "",     # optional
        "attachments": []     # optional
    })

    return {"message": "Project created successfully", "project_id": new_project.id}
