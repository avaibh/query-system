from graphene import ObjectType, ID, String, Int, List, Field, Schema
import uuid
import jwt

# Define a secret key for JWT token generation
SECRET_KEY = 'super-secret'

class Employee(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    age = Int()
    department = String()

class Enterprise(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    employees = List(Employee)

class Query(ObjectType):
    enterprise = Field(Enterprise, id=ID(required=True))

    def resolve_enterprise(self, info, id):
        # Replace this with actual logic to fetch the enterprise from a database or other data source
        return Enterprise(id=id, name="Test Enterprise", employees=[
            Employee(id=str(uuid.uuid4()), name="Alice", age=25, department="Sales"),
            Employee(id=str(uuid.uuid4()), name="Bob", age=30, department="Engineering")
        ])

def authenticate(username, password):
    # Replace this with actual authentication logic
    if username == 'admin' and password == 'password':
        return True
    else:
        return False

def generate_token(username):
    payload = {'username': username}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.exceptions.InvalidTokenError:
        return None

# Example usage of the authenticate, generate_token, and decode_token functions
username = 'admin'
password = 'password'
if authenticate(username, password):
    token = generate_token(username)
    print('Token:', token)
    payload = decode_token(token)
    print('Payload:', payload)
    schema = Schema(query=Query)
    result = schema.execute('''
        {
          enterprise(id: "123") {
            id
            name
            employees {
              id
              name
              age
              department
            }
          }
        }
    ''', context_value={"request": None})  # Set context_value to include the request object

    print(result.data)
else:
    print('Authentication failed')

wrong_password = "wrong_password"
if authenticate(username, wrong_password):
    token = generate_token(username)
    print('Token:', token)
    payload = decode_token(token)
    print('Payload:', payload)
    schema = Schema(query=Query)
    result = schema.execute('''
        {
          enterprise(id: "123") {
            id
            name
            employees {
              id
              name
              age
              department
            }
          }
        }
    ''', context_value={"request": None})  # Set context_value to include the request object

    print(result.data)
else:
    print('Authentication failed')
