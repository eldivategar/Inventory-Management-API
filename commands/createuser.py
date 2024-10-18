from app.models.user import User

def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    try:
        user = User.create(username, password)
        print("User created successfully")
    except ValueError as e:
        print(f"Error: {e}")
