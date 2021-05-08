import threading

from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText, UniqueConstraint

from userbot.modules.sql_helper import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return "<User {} ({})>".format(self.username, self.user_id)


class Chats(BASE):
    __tablename__ = "chats"
    chat_id = Column(String(14), primary_key=True)
    chat_name = Column(UnicodeText, nullable=False)

    def __init__(self, chat_id, chat_name):
        self.chat_id = str(chat_id)
        self.chat_name = chat_name

    def __repr__(self):
        return "<Chat {} ({})>".format(self.chat_name, self.chat_id)


class ChatMembers(BASE):
    __tablename__ = "chat_members"
    priv_chat_id = Column(Integer, primary_key=True)
    # NOTE: Use dual primary key instead of private primary key?
    chat = Column(String(14),
                  ForeignKey("chats.chat_id",
                             onupdate="CASCADE",
                             ondelete="CASCADE"),
                  nullable=False)
    user = Column(Integer,
                  ForeignKey("users.user_id",
                             onupdate="CASCADE",
                             ondelete="CASCADE"),
                  nullable=False)
    __table_args__ = (
        UniqueConstraint(
            'chat',
            'user',
            name='_chat_members_uc'),
    )

    def __init__(self, chat, user):
        self.chat = chat
        self.user = user

    def __repr__(self):
        return "<Chat user {} ({}) in chat {} ({})>".format(
            self.user.username, self.user.user_id, self.chat.chat_name, self.chat.chat_id)


Users.__table__.create(checkfirst=True)
Chats.__table__.create(checkfirst=True)
ChatMembers.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def get_all_chats():
    try:
        return SESSION.query(Chats).all()
    finally:
        SESSION.close()
