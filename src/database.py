from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import logging

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    group_link = Column(String, unique=True)
    instance_name = Column(String)
    joined_date = Column(DateTime)
    message_sent = Column(Boolean, default=False)
    last_action_date = Column(DateTime)

class Database:
    def __init__(self):
        database_url = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/telegram_db')
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_group(self, group_link: str):
        session = self.Session()
        try:
            group = Group(
                group_link=group_link,
                last_action_date=datetime.utcnow()
            )
            session.add(group)
            session.commit()
            logging.info(f"Added group to database: {group_link}")
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding group {group_link} to database: {e}")
            raise e
        finally:
            session.close()

    def get_unprocessed_groups(self, limit: int = 25):
        session = self.Session()
        try:
            groups = session.query(Group)\
                .filter(Group.message_sent == False)\
                .limit(limit)\
                .all()
            logging.info(f"Retrieved {len(groups)} unprocessed groups.")
            return groups
        except Exception as e:
            logging.error(f"Error retrieving unprocessed groups: {e}")
            return []
        finally:
            session.close()

    def mark_group_processed(self, group_link: str, instance_name: str):
        session = self.Session()
        try:
            group = session.query(Group)\
                .filter(Group.group_link == group_link)\
                .first()
            if group:
                group.message_sent = True
                group.instance_name = instance_name
                group.last_action_date = datetime.utcnow()
                session.commit()
                logging.info(f"Marked group as processed: {group_link} by {instance_name}")
        except Exception as e:
            session.rollback()
            logging.error(f"Error marking group {group_link} as processed: {e}")
            raise e
        finally:
            session.close()