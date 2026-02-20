"""Database operations - data access layer."""

import sqlite3
from datetime import datetime
from typing import Optional

from models.game_result import GameResult


class PlayerRepository:
    """Repository for player data access."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Initialize repository with database connection.

        Args:
            conn: SQLite database connection
        """
        self.conn = conn

    def insert_player(
        self, name: str, email: str, age: int, phone: str, date: datetime
    ) -> int:
        """Insert a new player into the database.

        Args:
            name: Player's name
            email: Player's email (unique)
            age: Player's age
            phone: Player's phone (unique)
            date: Registration date

        Returns:
            The ID of the inserted player

        Raises:
            sqlite3.IntegrityError: If email or phone already exists
            sqlite3.Error: On database error
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO player (name, email, age, phone, score, duration, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (name, email, age, phone, 0, 0.0, date),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as error:
            self.conn.rollback()
            raise sqlite3.IntegrityError(
                f"Player with this email or phone already exists: {error}"
            ) from error
        except sqlite3.Error as error:
            self.conn.rollback()
            raise sqlite3.Error(f"Error inserting player: {error}") from error
        finally:
            cursor.close()

    def find_player_by_email(self, email: str) -> Optional[dict]:
        """Find player by email.

        Args:
            email: Player's email

        Returns:
            Player dict with keys: id, name, email, age, phone, score, duration, date
            None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM player WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3],
                    "phone": row[4],
                    "score": row[5],
                    "duration": row[6],
                    "date": row[7],
                }
            return None
        except sqlite3.Error as error:
            raise sqlite3.Error(f"Error querying player: {error}") from error
        finally:
            cursor.close()

    def find_player_by_id(self, player_id: int) -> Optional[dict]:
        """Find player by ID.

        Args:
            player_id: Player's ID

        Returns:
            Player dict or None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM player WHERE id = ?", (player_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3],
                    "phone": row[4],
                    "score": row[5],
                    "duration": row[6],
                    "date": row[7],
                }
            return None
        except sqlite3.Error as error:
            raise sqlite3.Error(f"Error querying player: {error}") from error
        finally:
            cursor.close()


class GameResultRepository:
    """Repository for game result data access."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Initialize repository with database connection.

        Args:
            conn: SQLite database connection
        """
        self.conn = conn

    def insert_game_result(self, result: GameResult) -> int:
        """Insert a game result into the database.

        Args:
            result: GameResult instance

        Returns:
            The ID of the inserted result

        Raises:
            sqlite3.Error: On database error
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO game_session
                (player_id, difficulty, score, max_score, duration, created_at)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    result.player_id,
                    result.difficulty,
                    result.score,
                    result.max_score,
                    result.duration,
                    result.created_at,
                ),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as error:
            self.conn.rollback()
            raise sqlite3.Error(f"Error inserting game result: {error}") from error
        finally:
            cursor.close()

    def get_leaderboard(self, limit: int = 20) -> list[dict]:
        """Get the top players by score.

        Args:
            limit: Maximum number of results (default 20)

        Returns:
            List of dicts with player info and their best game
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """SELECT p.id, p.name, p.email, MAX(gs.score) as best_score,
                   AVG(gs.score) as avg_score, COUNT(gs.id) as games_played
                FROM player p
                LEFT JOIN game_session gs ON p.id = gs.player_id
                GROUP BY p.id
                ORDER BY best_score DESC
                LIMIT ?""",
                (limit,),
            )
            rows = cursor.fetchall()
            results = []
            for i, row in enumerate(rows, 1):
                results.append(
                    {
                        "rank": i,
                        "player_id": row[0],
                        "name": row[1],
                        "email": row[2],
                        "best_score": row[3],
                        "avg_score": row[4],
                        "games_played": row[5],
                    }
                )
            return results
        except sqlite3.Error as error:
            raise sqlite3.Error(f"Error fetching leaderboard: {error}") from error
        finally:
            cursor.close()

    def get_player_game_history(self, player_id: int, limit: int = 10) -> list[dict]:
        """Get player's game history.

        Args:
            player_id: Player's ID
            limit: Maximum number of results (default 10)

        Returns:
            List of dicts with game results, newest first
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """SELECT id, difficulty, score, max_score, duration, created_at
                FROM game_session
                WHERE player_id = ?
                ORDER BY created_at DESC
                LIMIT ?""",
                (player_id, limit),
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(
                    {
                        "id": row[0],
                        "difficulty": row[1],
                        "score": row[2],
                        "max_score": row[3],
                        "duration": row[4],
                        "created_at": row[5],
                    }
                )
            return results
        except sqlite3.Error as error:
            raise sqlite3.Error(
                f"Error fetching player game history: {error}"
            ) from error
        finally:
            cursor.close()
