import enum
from sqlalchemy.dialects.mysql import JSON
from app.support.db import db

# ENUM TYPES


class StateType(enum.Enum):
    DONE = "DONE"
    INPROGRESS = "INPROGRESS"


class MoveType(enum.Enum):
    MOVE = "MOVE"
    QUIT = "QUIT"

# MODELS


class GamesModel(db.Model):
    """
    This class represents the Games table.
    """
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))
    columns = db.Column(db.Integer)
    rows = db.Column(db.Integer)
    board = db.Column(JSON)
    state = db.Column(db.Enum(StateType))
    winner_id = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, game_id, model):
        game = self.query.filter_by(id=game_id).first()
        game.state = model['state']
        game.board = model['board']
        game.board = model['winner_id']
        db.session.commit()


class PlayersModel(db.Model):
    """
    This class represents the Players table.
    """
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()


class GamesToPlayersModel(db.Model):
    """
     This class represents the Games to Players table.
     """
    __tablename__ = 'games_to_players'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()


class MovesModel(db.Model):
    """
     This class represents the Moves table.
     """
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    type = db.Column(db.Enum(MoveType))
    board_column = db.Column(db.Integer)
    board_row = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
