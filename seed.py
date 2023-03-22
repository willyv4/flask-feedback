from app import db
from models import User, Feedback

# Clear out any existing data
db.drop_all()
db.create_all()

# Create some test users
u1 = User.register('user1', 'password', 'user1@example.com', 'John', 'Doe')
u2 = User.register('user2', 'password', 'user2@example.com', 'Jane', 'Doe')
u3 = User.register('user3', 'password', 'user3@example.com', 'Bob', 'Smith')
u4 = User.register('user4', 'password', 'user4@example.com', 'Alice', 'Smith')

# Add users to session
db.session.add_all([u1, u2, u3, u4])
db.session.commit()

# Create some feedback
f1 = Feedback(title='First Feedback',
              content='This is the first piece of feedback from user1', username='user1')
f2 = Feedback(title='Second Feedback',
              content='This is the second piece of feedback from user1', username='user4')
f3 = Feedback(title='First Feedback',
              content='This is the first piece of feedback from user2', username='user1')
f4 = Feedback(title='Second Feedback',
              content='This is the second piece of feedback from user2', username='user2')
f5 = Feedback(title='First Feedback',
              content='This is the first piece of feedback from user3', username='user3')

db.session.add_all([f1, f2, f3, f4, f5])
db.session.commit()
