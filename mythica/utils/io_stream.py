from pydantic import BaseModel,PrivateAttr

class EcosystemIO(BaseModel):
    _log:list[str] = PrivateAttr(default_factory=list[str])

    def log(self,message:str) -> None:
        self._log.append(message)

    def get_log(self) -> list[str]:
        return self._log.copy()
    
    def clear_log(self) -> None:
        self._log.clear()