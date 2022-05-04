# RESTFS

Some people say that **object-oriented programming** doesn't have any style, but I 
think that it's **classy**.

### View the Demo on Heroku
* [Folders Root](https://restfs.herokuapp.com/folders/)
* [Topics Root](https://restfs.herokuapp.com/topics/)

Folders are accessible by PATH name.  I didn't document it extensively, but I
think the links included in the API output make it fairly intuitive to navigate.

Some of the API endpoints aren't directly accessible, so you might find the
[Postman](https://www.postman.com/) [collection](doc/RESTFS.postman_collection.json)
that I exported to the `doc/` directory handy for exploratory testing.

### Assumptions
I made a lot of assumptions here.  My implementation assumes that
reads will be the most common operation.  To support that efficiently,
I sacrificed the efficiency of some write operations.  For example, Folder
rename will be extremely expensive in a large system.

Retrieving the content of a single file is not supported.

### Design Diagrams
* [Models](https://cloud.smartdraw.com/share.aspx/?pubDocShare=FC8D6C4431063FB314E1BB92781FD728BF0)
* [Use Cases](https://cloud.smartdraw.com/share.aspx/?pubDocShare=F09E5C63519471BE4493FDE741802BE36C2)
* [List Folder Contents](https://cloud.smartdraw.com/share.aspx/?pubDocShare=07115C526A47DF72FBF2C970D88D146CD14)
* [Create or Update Folder or Document (PUT)](https://cloud.smartdraw.com/share.aspx/?pubDocShare=ACA57D5BBAC310025A3CBD3F825563F8E6D)
* [Delete Folder or Document](https://cloud.smartdraw.com/share.aspx/?pubDocShare=749469ABB55182A34B891535222D8F23820)
* [Create Topic](https://cloud.smartdraw.com/share.aspx/?pubDocShare=395BA4F28B17D2FA4E1A27C9D735B35D1E8)
* [Delete Topic](https://cloud.smartdraw.com/share.aspx/?pubDocShare=C1CB11AF4A61B0399B428E5AF67AE329057)

### API

| Path            | Method | Description                                                               |
|-----------------|--------|---------------------------------------------------------------------------|
|                 |        |                                                                           |
| /folders/{path} | GET    | Get information about a Folder or Document                                |
|                 | PUT    | Create or replace Folder or Document                                      |
|                 | DELETE | Delete Folder or Document.  Deletes recursively when deleting a a folder. |
|                 |        |                                                                           |
| /topics/        | GET    | Lists all topics.                                                         |
|                 | POST   | Creates a new topic.                                                      |
|                 |        |                                                                           |
| /topics/{name}  | DELETE | Deletes a topic, only if there are no iNodes with it attached.            |
