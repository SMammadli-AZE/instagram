def add_user(username, password, db_path="database.txt"):
    with open(db_path, "a") as f:
        f.write(f"{username}:{password}\n")
    print(f"Saved -> {username}:{password}")