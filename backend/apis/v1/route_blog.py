from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.blog import CreateBlog, ReadBlog, UpdateBlog
from db.models.user import User
from apis.v1.route_login import get_current_user
from db.repository.blog import create_new_blog, delete_blog_by_id, retrieve_blog, list_blogs, update_blog_by_id

router = APIRouter()

@router.post("/", response_model=ReadBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    """
    Create a new blog post.
    
    - **title**: Title of the blog post
    - **slug**: URL-friendly version of the title (auto-generated if not provided)
    - **content**: Content of the blog post (optional)
    
    Returns the created blog post.
    """
    blog = create_new_blog(blog=blog, db=db, author_id=1)
    return blog

@router.get("/{id}", response_model=ReadBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a blog post by its ID.
    
    - **id**: ID of the blog post to retrieve
    
    Returns the blog post with the specified ID.
    """
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} does not exist"
        )
    return blog

@router.get("",response_model=List[ReadBlog])
def get_all_active_blogs(db: Session =Depends(get_db)):
    blogs = list_blogs(db=db)
    return blogs

@router.put("/{id}",response_model=ReadBlog)
def update_blog(id:int, blog:UpdateBlog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = update_blog_by_id(id=id, blog=blog, db=db, author_id= current_user.id)
    if isinstance(blog, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=blog.get("error")
        )
    
    return blog

@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message = delete_blog_by_id(id=id, db=db, author_id=current_user.id)
    if message.get("error"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message.get("error")
        )
    return {"msg": message.get("msg")}

