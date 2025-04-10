import requests

BASE_URL = "http://127.0.0.1:8000"

auth_token = None
post_id = None

def register():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    data = {"username": username, "email": email, "password": password}
    res = requests.post(f"{BASE_URL}/register", json=data)
    print("Registered:", res.json())

def login():
    global auth_token
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    # OAuth2 expects username and password form data
    data = {"username": email, "password": password}
    
    res = requests.post(
        f"{BASE_URL}/login",
        data=data,  # sends as application/x-www-form-urlencoded
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if res.status_code == 200:
        auth_token = res.json()["access_token"]
        print("✅ Login Successful. Token stored.")
    else:
        print("❌ Login failed:", res.json())

def create_post():
    global post_id
    if not auth_token:
        print("You must login first.")
        return
    
    title = input("Post Title: ")
    content = input("Post content: ")
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"title": title, "content": content}
    res = requests.post(f"{BASE_URL}/posts", json=data, headers=headers)
    post_id = res.json().get("id")
    print("Created Post:", res.json())

def get_posts():
    res = requests.get(f"{BASE_URL}/posts")
    print("Posts:", res.json())

def comment_on_post():
    if not auth_token:
        print("You must login first.")
        return
    
    post = input("Post ID to comment on: ")
    content = input("Comment content: ")
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"content": content}
    res = requests.post(f"{BASE_URL}/posts/{post}/comments", json=data, headers=headers)
    print("Commented:", res.json())

def delete_post():
    if not auth_token:
        print("You must login first.")
        return
    
    post = input("Post ID to delete: ")
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.delete(f"{BASE_URL}/posts/{post}", headers=headers)
    print("Deleted:", res.json())

def get_commnets_on_a_post():
    post = input("Post ID to view comments: ")
    res = requests.get(f"{BASE_URL}/posts/{post}/comments")
    print("Posts:", res.json())

def delete_comment():
    if not auth_token:
        print("You must login first.")
        return
    
    comment = input("Comment ID to delete: ")
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.delete(f"{BASE_URL}/comments/{comment}", headers=headers)
    print("Deleted:", res.json())

def show_menu():
    print("\n=== BLOG CLI ===")
    print("1. Register")
    print("2. Login")
    print("3. Create a post")
    print("4. View all post")
    print("5. Comment on a post")
    print("6. Delete a post")
    print("7. View comments on a post")
    print("8. Delete a comment")
    print("9. Exit")

def main():
    print("=== Welcome to Blog CLI ===")
    prompt = input('Enter "blog" to begin: ')
    if prompt.lower() != "blog":
        print("Exiting.")
        return
    
    while True:
        show_menu()
        choice = input("=> ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            create_post()
        elif choice == "4":
            get_posts()
        elif choice == "5":
            comment_on_post()
        elif choice == "6":
            delete_post()
        elif choice == "7":
            get_commnets_on_a_post()
        elif choice == "8":
            delete_comment()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()