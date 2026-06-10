from enum import Enum
import uuid
from fastapi import APIRouter, HTTPException, status
from core.schemas import IssueOut, IssueCreate, IssueUpdate, IssueStatus
from core.json_storage import load_data, save_data

router = APIRouter(
    prefix='/issues',
    tags=["Issues"],               # Groups in docs
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=list[IssueOut], summary="Get issues data from json file")
async def get_issues():
    """ Retrieve all issues data from json file """
    return load_data()

@router.get("/{issue_id}", response_model=IssueOut, summary="Get an issue by ID from json file")
async def get_issue_by_id(issue_id: str) -> IssueOut:
    """ Helper function to get an issue by ID """
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return IssueOut.model_validate(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
@router.post("/", 
             response_model=IssueOut, 
             status_code=status.HTTP_201_CREATED,
             summary="Create an issue and save to json file")
async def create_issue(issue: IssueCreate):
    """ Create an issue and save to json file """
    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": issue.title,
        "description": issue.description,
        "priority": issue.priority,
        "status": IssueStatus.OPEN
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue
    
@router.put("/{issue_id}", response_model=IssueOut, summary="Update an existing issue in json file")
async def update_issue(issue_id: str, issue_update: IssueUpdate):
    """ Update an existing issue in json file """
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            # if issue_update.title is not None:
            #     issue["title"] = issue_update.title
            # if issue_update.description is not None:
            #     issue["description"] = issue_update.description
            # if issue_update.priority is not None:
            #     issue["priority"] = issue_update.priority
            # if issue_update.status is not None:
            #     issue["status"] = issue_update.status

            # Update fields if provided
            update_data = issue_update.model_dump(exclude_unset=True)
            issue.update(update_data)

            save_data(issues)
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")


@router.put("/upd_model/{model_issue_id}", response_model=IssueOut, summary="Update an existing issue in json file using model conversion (Pydantic objects)")
async def update_issue_model(issue_id: str, issue_update: IssueUpdate):
    """ Update an existing issue in json file """
    raw_issues = load_data()
    issues = [IssueOut.model_validate(item) for item in raw_issues]

    for issue in issues:
        if issue.id == issue_id:
            if issue_update.title is not None:
                issue.title = issue_update.title
            if issue_update.description is not None:
                issue.description = issue_update.description
            if issue_update.priority is not None:
                issue.priority = issue_update.priority
            if issue_update.status is not None:
                issue.status = issue_update.status

            # # Update fields if provided
            # update_data = issue_update.model_dump(exclude_unset=True)
            # issue.update(update_data)
            # save_data(issues)
            # return issue

             # Convertimos la lista de objetos de vuelta a diccionarios para guardar el JSON
            raw_data_to_save = [item.model_dump() for item in issues]
            save_data(raw_data_to_save)
            return issue
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an issue from json file")
async def delete_issue(issue_id: str):
    """ Delete an issue from json file """
    issues = load_data()
    print("Issues loaded:", issues)
    for i, issue in enumerate(issues):
        print(issue["id"], issue_id)
        if issue["id"] == issue_id:
            del issues[i]
            save_data(issues)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")