# File Sharing API In FastAPI.

## Summary
It is the minimalistic file sharing api built on fastapi.Where registred users can upload files and 
share them with others who have registered on the app and also files can be downloaded with appropriate access.Implementd JWT authentication access control and restricting the endpoint.


**Key Features**
- `/reigster`    : Endpoint for registering the to the servie.
- `/login`       : Endpoint to log in to service after resgister login returns a JWT token for authentication which should be  used in th client side.the token get expired after certain amount time 
after expiration a user has to log in again for authentication
- `/file_upload` : Endpoint for uploading files. To Upload user must be logged in.
- `/sharefile`   : Endpoint for sharing files with others it rquires the file_name and email of the user whom to share the file.Only the user who has uploaded the file has rigth to share the file 
- `/getfiles`    : Endpoint for retriving files owned by th currently logged in user
- `/getSharedFiles` : Endpoint for retriving files shared to the currently logged in user
- `/download/{id}`  : Endpoint for downloading files only file owner or the file has been shared to someone can download. This endpoint requires the id of file that is to be downloaded  


## Language And Tools Used 

1. `Pyhton` With `FastAPI` For API Creating.
2. `Postgres` As Database. 
3. `SqlAlchemy` For ORM. 
4. `Pytest` For Unit Testing

## Contrubution And Recomendations
Any Kind Contribution And Recomendation That Enriches The Service Are Welcomed.












