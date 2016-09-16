# HackZurich Catastrophe

## SocketIO Events
### ```reports-add```
Add a new report

### ```reports-list```
Get a list with all reports

### ```reports-accept```
Accept a report

### ```reports-done```
Mark a previously accepted report as fulfilled


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
  needs: [
    {
      type: "medic",
      status: "open|processing|done"
    },
    {
      type: "food",
      status: "open|processing|done"
    },
    {
      type: "water",
      status: "open|processing|done"
    },
  ],
  skills: ["medic", "food", "water"],
  photos: ["base64 of first photo", "base64 of second photo"]
}
```

