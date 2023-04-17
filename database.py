# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.ext.declarative import declarative_base
# from contextlib import contextmanager
# from flask_sqlalchemy import SQLAlchemy
#
# Base = declarative_base()
# db = SQLAlchemy()
#
# def init_db(app):
#     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#     Base.metadata.create_all(bind=engine)
#     session_factory = sessionmaker(bind=engine)
#
#     @contextmanager
#     def create_session():
#         session = scoped_session(session_factory)()
#         try:
#             yield session
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             session.close()
#     return create_session
#
# @contextmanager
# def session_scope():
#     with init_db().scope_session() as session:
#         try:
#             yield session
#             session.commit()
#         except:
#             session.rollback()
#             raise
#########################################################################
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy()

def init_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

@contextmanager
def session_scope(app):
    engine, Session = init_db(app)
    session = scoped_session(Session)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
