# HackZurich Catastrophe

## SocketIO Events
### ```reports add```
Add a new report

### ```reports list```
Get a list with all reports

### ```reports accept```
Accept a report

### ```reports done```
Mark a previously accepted report as fulfilled

### ```reports status change```
Notification that the status of a report has changed

### ```reports change help```
Notification that help is request

## Schema
### reports
```
{
  id: 123, // Can also be null
  name: "Max Muster",
  source: "ios|phone",
  number: "+41791231234", // can also be null
  status: "ok|injured|heavily_injured",
  location: {
    lat: 12.000,
    lng: 13.000
  },
  needs: ["medic", "food", "water"],
  needs_status: "open|processing|done",
  skills: ["medic", "food", "water"],
  photos: ["base64 of first photo", "base64 of second photo"]
}
```
