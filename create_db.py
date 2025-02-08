import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from datetime import date

#Engine to connect to database
engine = sqlalchemy.create_engine('sqlite:///Company2.db')

base = declarative_base()

#Create Table classes
class Employees(base):
    __tablename__ = 'Employees'
    ID = Column(Integer, primary_key = True)
    Name = Column(String)
    Department = Column(String)
    Salary = Column(Integer)
    Hire_Date = Column(Date)

    parent = relationship("Departments",back_populates="child")
    
class Departments(base):
    __tablename__ = 'Departments'
    ID = Column(Integer, primary_key = True)
    Name = Column(String)
    Manager_ID = Column(Integer, ForeignKey("Employees.ID"))

    child = relationship("Employees",back_populates="parent")

#Create tables in the database
base.metadata.create_all(engine)

#Create session to add entries to the table
Session = sessionmaker(bind = engine)
sess = Session()

#Add sample data to the database
employee_data = [
    Employees(ID = 1, Name = "Alice", Department = "Sales", Salary = 50000, Hire_Date = date(2021, 1, 15)),
    Employees(ID = 2, Name = "Bob", Department = "Engineering", Salary = 70000, Hire_Date = date(2020, 6, 10)),
    Employees(ID = 3, Name = "Charlie", Department = "Marketing", Salary = 60000, Hire_Date = date(2022, 3, 20))
]

Department_data = [
    Departments(ID = 1, Name = "Sales", Manager_ID = 1),
    Departments(ID = 2, Name = "Engineering", Manager_ID = 2)
]

#Commit the changes
sess.add_all(employee_data)
sess.add_all(Department_data)
sess.commit()

#close the session
sess.close()