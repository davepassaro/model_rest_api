in terminal ---> [python main.py ]: to start

Requirements for non-user entities
For each entity a collection URL must be provided that is represented  by the collection name.
E.g.,  GET /boats represents the boats collection
If an entity is related to a user, then the collection URL must show only those entities in the collection which are related to the user corresponding to the valid JWT provided in the request
E.g., if each boat is owned by a user, then GET /boats should only show those entities that are owned by the user who is authenticated by the JWT supplied in the request
For an entity that is not related to users, the collection URL should show all the entities in the collection.
The collection URL for an entity must implement paging showing 5 entities at a time
At a minimum it must have a 'next' link on every page except the last
The collection must include a property that indicates how many total items are in the collection
Every representation of an entity must have a 'self' link pointing to the canonical representation of that entity
This must be a full URL, not relative path
Each entity must have at least 3 properties of its own.
id and self are not consider a property in this count.
Properties to model related entities are also not considered a property in this count.
E.g., a boat is not a property of a load in this count, and neither is the owner of a boat.
Properties that correspond to creation date and last modified date will be considered towards this count.
Every entity must support all 4 CRUD operations, i.e., create/add, read/get, update/edit and delete.
You must handle any "side effects" of these operations on an entity to other entities related to the entity.
E.g., Recall how you needed to update loads when deleting a boat.
Update for an entity should support both PUT and PATCH.
Every CRUD operation for an entity related to a user must be protected and require a valid JWT corresponding to the relevant user.
You must provide an endpoint to create a relationship and another to remove a relationship between the two non-user entities. It is your design choice to make these endpoints protected or unprotected.
E.g., In Assignment 4, you had provided an endpoint to put a load on a boat, and another endpoint to remove a load from a boat.
If an entity has a relationship with other entities, then this info must be displayed in the representation of the entity
E.g., if a load is on a boat, then
The representation of the boat must show the relationship with this load
The representation of this load must show the relationship with this boat
There is no requirement to provide dedicated endpoints to view just the relationship
E.g., Assignment 4 required an endpoint /boats/:boat_id/loads. Such an endpoint is not required in this project.
For endpoints that require a request body, you only need to support JSON representations in the request body.
Requests to some endpoints, e.g., GET don't have a body. This point doesn't apply to such endpoints.
 Any response bodies should be in JSON, including responses that contain an error message.
Responses from some endpoints, e.g., DELETE, don't have a body. This point doesn't apply to such endpoints.
Any request to an endpoint that will send back a response with a body must include 'application/json' in the accept header. If a request doesn't have such a header, it should be rejected.
User Details
You must have a User entity in your database.
You must support the ability for users of the application to create user accounts. There is no requirement to edit or delete users.
You may choose from the following methods of handling user accounts
You can handle all account creation and authentication yourself.
You can use a 3rd party authentication service.
You must provide a URL where a user can provide a username and password to login or create a user account.
Requests for the protected resources must use a JWT for authentication. So you must show the JWT to the user after the login. You must also show the user's unique ID after login.
The choice of what to use as the user's unique ID is up to you.
You can use the value of "sub" from the JWT as a user's unique ID. But this is not required.
You must provide an unprotected endpoint GET /users that returns all the users currently registered in the app, even if they don't currently have any relationship with a non-user entity. The response does not need to be paginated.
Minimally this endpoint should display the unique ID for a user. Beyond that it is your choice what else is displayed.
There is no requirement for an integration at the UI level between the login page and the REST API endpoints.
Status Codes
Your application should support at least the following status codes

200
201
204
401
403
405
406
