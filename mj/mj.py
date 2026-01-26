from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Optional
import random

class SuitType(str, Enum):
    """Suit types for numbered tiles"""
    WAN = 'w'  # Characters
    TONG = 't'  # Circles
    TIAO = 's'  # Bamboos

class HonorType(str, Enum):
    """Honor and flower tile types"""
    # Honor tiles
    HONGZHONG = 'h'  # Red Dragon
    FACAI = 'f'  # Green Dragon
    BAIBAN = 'b'  # White Dragon
    
    # Flower tiles
    CHUN = 'c1'  # Spring
    XIA = 'c2'  # Summer
    QIU = 'c3'  # Autumn
    DONG = 'c4'  # Winter
    MEI = 'f1'  # Plum Blossom
    LAN = 'f2'  # Orchid
    ZHU = 'f3'  # Bamboo
    JU = 'f4'  # Chrysanthemum

class MahjongTile(BaseModel):
    """Mahjong tile"""
    # Numbered tile properties
    number: Optional[int] = Field(None, description="Number for suit tiles")
    suit: Optional[SuitType] = Field(None, description="Suit for numbered tiles")
    
    # Honor/Flower tile properties
    honor: Optional[HonorType] = Field(None, description="Honor type for honor/flower tiles")
    
    # Common properties
    tile_type: str = Field(..., description="Tile type: 'suit' or 'honor'")

    @model_validator(mode='after')
    def validate_model(self):
        # Validate tile_type
        if self.tile_type not in ['suit', 'honor']:
            raise ValueError('tile_type must be either "suit" or "honor"')
        
        # Validate suit tiles
        if self.tile_type == 'suit':
            if self.number is None:
                raise ValueError('suit tiles must have a number')
            if self.suit is None:
                raise ValueError('suit tiles must have a suit')
            if self.honor is not None:
                raise ValueError('suit tiles should not have an honor type')
            if not 1 <= self.number <= 9:
                raise ValueError('number must be between 1 and 9')
        
        # Validate honor/flower tiles
        else:  # self.tile_type == 'honor'
            if self.number is not None:
                raise ValueError('honor tiles should not have a number')
            if self.suit is not None:
                raise ValueError('honor tiles should not have a suit')
            if self.honor is None:
                raise ValueError('honor tiles must have an honor type')
        
        return self
    
    @property
    def full_name(self) -> str:
        """Get the full name of the tile"""
        if self.tile_type == 'suit':
            suit_names = {
                SuitType.WAN: 'Characters',
                SuitType.TONG: 'Circles',
                SuitType.TIAO: 'Bamboos'
            }
            return f"{self.number} {suit_names[self.suit]}"
        else:
            honor_names = {
                HonorType.HONGZHONG: 'Red Dragon',
                HonorType.FACAI: 'Green Dragon',
                HonorType.BAIBAN: 'White Dragon',
                HonorType.CHUN: 'Spring',
                HonorType.XIA: 'Summer',
                HonorType.QIU: 'Autumn',
                HonorType.DONG: 'Winter',
                HonorType.MEI: 'Plum Blossom',
                HonorType.LAN: 'Orchid',
                HonorType.ZHU: 'Bamboo',
                HonorType.JU: 'Chrysanthemum'
            }
            return honor_names[self.honor]

class MahjongDeck:
    def __init__(self):
        self.tiles = self._initialize_deck()
    
    def _initialize_deck(self):
        """Initialize a mahjong deck"""
        tiles = []
        
        # Numbered tiles: 4 of each number per suit
        for suit in [SuitType.WAN, SuitType.TONG, SuitType.TIAO]:
            for number in range(1, 10):
                for _ in range(4):
                    tiles.append(MahjongTile(
                        number=number,
                        suit=suit,
                        honor=None,
                        tile_type='suit'
                    ))
        
        # Honor tiles: 4 of each
        for honor in [HonorType.HONGZHONG, HonorType.FACAI, HonorType.BAIBAN]:
            for _ in range(4):
                tiles.append(MahjongTile(
                    number=None,
                    suit=None,
                    honor=honor,
                    tile_type='honor'
                ))
        
        # Flower tiles: 1 of each (8 total)
        for honor in [HonorType.CHUN, HonorType.XIA, HonorType.QIU, HonorType.DONG,
                      HonorType.MEI, HonorType.LAN, HonorType.ZHU, HonorType.JU]:
            tiles.append(MahjongTile(
                number=None,
                suit=None,
                honor=honor,
                tile_type='honor'
            ))
        
        return tiles
    
    def reset(self):
        """Reset the deck"""
        self.tiles = self._initialize_deck()
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.tiles)
    
    def draw(self) -> MahjongTile:
        """Draw a tile from the end of the deck"""
        if not self.tiles:
            raise ValueError('No tiles left in the deck')
        return self.tiles.pop()
    
    def draw_from_front(self) -> MahjongTile:
        """Draw a tile from the front of the deck"""
        if not self.tiles:
            raise ValueError('No tiles left in the deck')
        return self.tiles.pop(0)
    
    def remaining(self) -> int:
        """Get the number of remaining tiles"""
        return len(self.tiles)
    
    def __len__(self) -> int:
        return len(self.tiles)
    
    def __iter__(self):
        return iter(self.tiles)
    
    def __repr__(self) -> str:
        return f"MahjongDeck(remaining={self.remaining()})"

