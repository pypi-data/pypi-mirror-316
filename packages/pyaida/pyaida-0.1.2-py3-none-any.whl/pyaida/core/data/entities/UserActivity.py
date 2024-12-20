from pyaida.core.data import AbstractEntityModel
import uuid

class CommentModel(AbstractEntityModel):
    """add comments to notes and drafts"""
    class Config:
        namespace :str = 'public'
        as_relationship: bool = True

class HighlightsModel(AbstractEntityModel):
    """extract highlights from resources"""
    class Config:
        namespace : str = 'public'
        as_relationship: bool = True
        
    resource_id: uuid.UUID
    
class UserPreferenceModel(AbstractEntityModel):
    """store user context"""
    class Config:
        namespace :str = 'public'
        