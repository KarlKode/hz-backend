# Web Dashboard for the PosAidOn project @ HackZurich 2016.


##Screenshots
Heatmap View for getting an overview of critical areas

![image](heatmap.png)

Map detail view with basic needs (medic,food,water,shelter)

![image](needs.png)

Live feed view of incoming requests

![image](livefeed.png)

## SocketIO Events
### Client -> Server
#### ```reports add```
Add a new report

#### ```reports list```
Get a list with all reports

#### ```reports accept```
Accept a report

#### ```reports done```
Mark a previously accepted report as fulfilled

#### ```reports reset```
Reset the whole database to a state with only dummy data

### Server -> Client

#### ```reports new```
Notification that a new report has been added to the database

#### ```reports status change```
Notification that the status of a report has changed

#### ```reports change help```
Notification that help is request

## Schema
### reports
```
{
  id: 123, // Can also be null
  name: "Max Muster",
  source: "ios|phone|sms",
  number: "+41791231234", // can also be null
  status: "ok|injured|heavily_injured",
  location: {
    lat: 12.000,
    lng: 13.000
  },
  needs: ["medic", "shelter", "food", "water"],
  needs_status: "open|processing|done",
  skills: ["medic", "food", "water"],
  photos: ["base64 of first photo", "base64 of second photo"]
}
```
