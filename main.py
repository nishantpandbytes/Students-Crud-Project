from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import models
import schemas
from database import engine, get_db

# Database tables create karna
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="EWB Internship Project - Student Database CRUD Application",
    version="1.0.0"
)

# 1. CREATE: Add new student
@app.post("/students", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# 2. READ: List all students (with optional filtering by name)
@app.get("/students", response_model=List[schemas.StudentResponse])
def get_students(name: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Student)
    if name:
        query = query.filter(models.Student.name.contains(name))
    return query.all()

# 3. READ: Retrieve single student by ID
@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with ID {student_id} not found"
        )
    return student

# 4. UPDATE: Update existing student details
@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, updated_data: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.id == student_id)
    student = student_query.first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with ID {student_id} not found"
        )
    
    update_dict = updated_data.dict(exclude_unset=True)
    student_query.update(update_dict, synchronize_session=False)
    db.commit()
    db.refresh(student)
    return student

# 5. DELETE: Remove student record
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with ID {student_id} not found"
        )
    
    db.delete(student)
    db.commit()
    return None