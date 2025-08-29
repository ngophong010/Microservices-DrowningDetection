from app.models.alert import Alert

class CRUDAlert:
    async def create(self, camera_id: str, confidence: float) -> Alert:
        alert = Alert(camera_id=camera_id, confidence=confidence)
        await alert.insert()
        return alert

alert = CRUDAlert()