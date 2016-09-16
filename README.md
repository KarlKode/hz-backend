# HackZurich Catastrophe

## API

## Schema
### reports
```
{
  name: "Max Muster",
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

