from fastapi import Query, HTTPException, status, APIRouter
from app.models import Vote, VotePublic, VoteRequest, Post
from app.api.deps import CurrentUser, SessionDep
from sqlmodel import select

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

# Create Vote
@router.post("/", response_model=VotePublic, status_code=status.HTTP_201_CREATED)
def vote(vote: VoteRequest, 
                session: SessionDep, 
                current_user : CurrentUser):
    
    post = session.exec(select(Post).where(Post.id == vote.post_id)).one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id :{vote.post_id} doesn't exists.")
    
    vote_query = session.exec(select(Vote).where((Vote.post_id == vote.post_id), (Vote.user_id == current_user.id)))
    found_vote = vote_query.one_or_none()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)   
        session.add(new_vote)
        session.commit()
        return {"message" : "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exists")
        
        session.delete(found_vote)
        session.commit()
        return {"message" : "successfully deleted vote"}