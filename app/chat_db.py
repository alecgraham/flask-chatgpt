import psycopg2 as pg
import os
from datetime import datetime

create_schema = "create schema chatgpt;"
users_ddl = '''CREATE TABLE chatgpt.users (
    username  varchar(50) NOT NULL UNIQUE,
    password  varchar(255),
    active BOOLEAN,
    insert_instant  timestamp
    )
    '''
conversations_ddl = '''
    CREATE TABLE chatgpt.conversations (
    id  SERIAL PRIMARY KEY,
    username   varchar(50),
    summary   VARCHAR(500),
    summarized_yn BOOLEAN,
    insert_instant  timestamp
    )
    '''

# message id comes from front end and represents order in message array
messages_ddl = '''
    CREATE TABLE chatgpt.messages (
    conversation_id   INTEGER,
    line    INTEGER,
    role    VARCHAR(50),
    message_text    VARCHAR(2000),
    insert_instant  timestamp
    )
    '''

insert_user = '''
    insert into chatgpt.users (username, password, active, insert_instant) values (%s,%s,%s, CURRENT_TIMESTAMP);
'''


def connect_db():
  db_string = os.environ.get('DATABASE_URL')
  conn = pg.connect(db_string)
  return conn


def build_db():
  conn = connect_db()
  cur = conn.cursor()
  cur.execute(create_schema)
  #cur = conn.cursor()
  cur.execute(users_ddl)
  cur.execute(conversations_ddl)
  cur.execute(messages_ddl)
  conn.commit()
  cur.close()
  conn.close()

def check_db_exists():
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("select schema_name from information_schema.schemata where schema_name = 'chatgpt'")
  schema = cur.fetchall()
  if schema:
    return True
  else:
    return False

def get_conversation_messages(id):
  conn = connect_db()
  cur = conn.cursor()
  cur.execute('select line, role, message_text from chatgpt.messages where conversation_id = %s order by line asc',(id,))
  results = cur.fetchall()
  return results

def insert_message(id,line,role,content):
  insert_statement = '''
    insert into chatgpt.messages(conversation_id,line,role, message_text, insert_instant) values (%s,%s,%s,%s, CURRENT_TIMESTAMP);
'''
  conn = connect_db()
  cur = conn.cursor()
  cur.execute(insert_statement,(id,line,role,content))
  conn.commit()
  cur.close()
  conn.close()
  return True

def insert_conversation(username):
  ts = datetime.now()
  insert_statement = '''
    insert into chatgpt.conversations(username,insert_instant) values (%s, %s);
'''
  conn = connect_db()
  cur = conn.cursor()
  cur.execute(insert_statement,(username,ts))
  conn.commit()
  select_statement = 'select id from chatgpt.conversations where username = %s and insert_instant = %s'
  cur.execute(select_statement,(username,ts))
  id = cur.fetchone()[0]
  cur.close()
  conn.close()
  return id

def select_conversations(username):
  select_statement = '''
    select c.id
      ,coalesce(c.summary,m.message_text,'blank') as text
    from chatgpt.conversations c
    left join chatgpt.messages m on m.conversation_id = c.id
      and m.line = 1
    where c.username = %s
    order by c.id desc
  '''
  conn = connect_db()
  cur = conn.cursor()
  cur.execute(select_statement,(username,))
  results = cur.fetchall()
  return results