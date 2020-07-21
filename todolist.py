from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

EXIT = "0"

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class TodoList:
    def __init__(self, session):
        self.session = session

    def print_tasks_for_day(self, date=datetime.today()):
        tasks = self.session.query(Task).filter(Task.deadline == date.date()).all()
        if not tasks:
            print("Nothing to do!")
        else:
            i = 1
            for task in tasks:
                print(f"{i}. {task}")
        print()

    def print_today_tasks(self):
        today = datetime.today()
        print(f"Today {today.strftime('%d %b').lstrip('0')}:")
        self.print_tasks_for_day(today)

    def print_week_tasks(self):
        for n in range(7):
            date = datetime.today() + timedelta(days=n)
            print(f"{date.strftime('%A')} {date.strftime('%d %b').lstrip('0')}:")
            self.print_tasks_for_day(date)

    def print_all_tasks(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        print("All tasks:")
        i = 1
        for task in tasks:
            print(f"{i}. {task}. {task.deadline.strftime('%d %b').lstrip('0')}")
        print()

    def add_task(self):
        task_description = input("Enter task\n")
        task_deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
        task = Task(task=task_description, deadline=task_deadline)
        self.session.add(task)
        self.session.commit()
        print("The task has been added!\n")

    def missed_tasks(self, date=datetime.today()):
        tasks = self.session.query(Task).filter(Task.deadline < date.date()).order_by(Task.deadline).all()
        if not tasks:
            print("Nothing is missed!")
        else:
            i = 1
            for task in tasks:
                print(f"{i}. {task}")
        print()

    def delete_task(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        print("Choose the number of the task you want to delete:")
        i = 1
        for task in tasks:
            print(f"{i}. {task}. {task.deadline.strftime('%d %b').lstrip('0')}")
        print()
        number = int(input())
        session.delete(tasks[number])
        session.commit()





Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
todolist = TodoList(session)

while True:
    choice = input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n""")
    print()
    if choice == EXIT:
        session.close()
        break
    elif choice == '1':
        todolist.print_today_tasks()
    elif choice == '2':
        todolist.print_week_tasks()
    elif choice == '3':
        todolist.print_all_tasks()
    elif choice == '4':
        todolist.missed_tasks()
    elif choice == '5':
        todolist.add_task()
    elif choice == '6':
        todolist.delete_task()



print("Bye!")