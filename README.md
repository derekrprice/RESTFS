# RESTFS

View the [Demo](https://restfs.herokuapp.com/) on Heroku

### Assumptions
I made a lot of assumptions here.  My implementation assumes that
reads will be the most common operation and to support that efficiently,
I made some choices that will still support content changes for Documents
and Topic changes for both Documents and Folders efficiently but which
will make some write operations, like Folder rename, extremely
expensive in a large system.

### Design Diagrams
* [Models](https://cloud.smartdraw.com/share.aspx/?pubDocShare=FC8D6C4431063FB314E1BB92781FD728BF0)
* [Use Cases](https://cloud.smartdraw.com/share.aspx/?pubDocShare=F09E5C63519471BE4493FDE741802BE36C2)
* [List Folder Contents Flow](https://cloud.smartdraw.com/share.aspx/?pubDocShare=07115C526A47DF72FBF2C970D88D146CD14)

### API
