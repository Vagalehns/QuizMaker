import sqlite3
import os

class GameDB:
    def __init__(self, db_path):




        self.db_path = db_path
        


        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()

    
        self.initiate_DB()

    def initiate_DB(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    def clear_DB(self):
        self.cursor.execute("DROP TABLE IF EXISTS players;")
        self.cursor.execute("DROP TABLE IF EXISTS teams;")
        self.conn.commit()
        

    def add_team(self, name):
        try:
            self.cursor.execute("INSERT INTO teams (name) VALUES (?);", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Team '{name}' already exists.")
    
    def list_teams(self):
        self.cursor.execute("SELECT id, name FROM teams")
        result=self.cursor.fetchall()

        return result

    def add_player(self, name, team_name):
        self.cursor.execute("SELECT id FROM teams WHERE name = ?;", (team_name,))
        result = self.cursor.fetchone()

        if result:

            team_id = result[0]

            self.cursor.execute(
                "INSERT INTO players (name, team_id) VALUES (?, ?);",
                (name, team_id)
            )

            self.conn.commit()

        else:

            raise ValueError(f"Team '{team_name}' does not exist. Add the team first.")



    def __del__(self):
        self.conn.close()



def TEST_main():
    print("Run test 1")
    DB=GameDB("./test2.sqlite")

    DB.add_team("Zebras")
    DB.add_team("Pandas")
    DB.add_team("Delfīni")

if __name__ == "__main__":
    TEST_main()