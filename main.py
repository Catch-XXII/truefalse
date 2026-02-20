"""Main entry point for TrueFalse game."""

import time
from datetime import datetime

from config import DIFFICULTY_LEVELS
from const import DB_NAME
from db import create_sqlite_database, setup_database, close_connection
from db.operations import PlayerRepository, GameResultRepository
from game.engine import GameEngine
from models.game_result import GameResult
from models.player import Player
from ui.display import (
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_question,
    print_score,
    print_leaderboard,
    clear_screen,
)
from ui.prompts import (
    get_player_name,
    get_player_email,
    get_player_age,
    get_player_phone,
    get_true_false_answer,
    select_menu_option,
    confirm_action,
    select_difficulty,
)


class GameApp:
    """Main application class managing game flow."""

    def __init__(self) -> None:
        """Initialize the game application."""
        self.conn = create_sqlite_database(DB_NAME)
        setup_database(self.conn)
        self.player_repo = PlayerRepository(self.conn)
        self.result_repo = GameResultRepository(self.conn)
        self.current_player: Player | None = None

    def run(self) -> None:
        """Main game loop."""
        try:
            clear_screen()
            self._print_intro()

            while True:
                if not self.current_player:
                    self._player_selection()

                self._main_menu()
        except KeyboardInterrupt:
            print_warning("\nGame interrupted by user")
        except Exception as e:
            print_error(f"Unexpected error: {e}")
        finally:
            close_connection(self.conn)
            print_info("Thank you for playing!")

    def _print_intro(self) -> None:
        """Print game introduction."""
        intro_lines = [
            "          ::::::::::: :::::::::  :::    ::: ::::::::::          ::::::::  :::::::::          ::::::::::   :::     :::        ::::::::  ::::::::::",
            "             :+:     :+:    :+: :+:    :+: :+:                :+:    :+: :+:    :+:         :+:        :+: :+:   :+:       :+:    :+: :+:",
            "            +:+     +:+    +:+ +:+    +:+ +:+                +:+    +:+ +:+    +:+         +:+       +:+   +:+  +:+       +:+        +:+",
            "           +#+     +#++:++#:  +#+    +:+ +#++:++#           +#+    +:+ +#++:++#:          :#::+::# +#++:++#++: +#+       +#++:++#++ +#++:++#",
            "          +#+     +#+    +#+ +#+    +#+ +#+                +#+    +#+ +#+    +#+         +#+      +#+     +#+ +#+              +#+ +#+",
            "         #+#     #+#    #+# #+#    #+# #+#                #+#    #+# #+#    #+#         #+#      #+#     #+# #+#       #+#    #+# #+#",
            "        ###     ###    ###  ########  ##########          ########  ###    ###         ###      ###     ### ########## ########  ##########",
        ]

        for line in intro_lines:
            print(line)
            time.sleep(0.05)

        print("\n   A fun math true/false game to test your quick thinking!\n")
        time.sleep(1)

    def _player_selection(self) -> None:
        """Handle player selection - login or create new."""
        menu_options = ["New Player", "Returning Player", "Exit"]
        choice = select_menu_option(menu_options)

        if choice == 0:  # New Player
            self._create_new_player()
        elif choice == 1:  # Returning Player
            self._login_player()
        else:  # Exit
            exit(0)

    def _create_new_player(self) -> None:
        """Create a new player."""
        print_header("Create New Player Profile")

        name = get_player_name()
        email = get_player_email()

        # Check if email already exists
        existing = self.player_repo.find_player_by_email(email)
        if existing:
            print_error("Email already registered!")
            if confirm_action("Would you like to login instead?"):
                self._login_player()
            return

        age = get_player_age()
        phone = get_player_phone()

        try:
            # Insert player into database
            player_id = self.player_repo.insert_player(
                name=name,
                email=email,
                age=age,
                phone=phone,
                date=datetime.now(),
            )
            
            # Create Player object with database ID
            player = Player(name, email, age, phone, id=player_id)
            print_success(f"Welcome {name}! Profile created successfully.")
            self.current_player = player
        except ValueError as e:
            print_error(f"Invalid input: {e}")
            if confirm_action("Try again?"):
                self._create_new_player()
        except Exception as e:
            print_error(f"Error creating player: {e}")
            if confirm_action("Try again?"):
                self._create_new_player()

    def _login_player(self) -> None:
        """Login an existing player."""
        print_header("Player Login")

        email = get_player_email()
        player_data = self.player_repo.find_player_by_email(email)

        if not player_data:
            print_error("Player not found!")
            if confirm_action("Create new player instead?"):
                self._create_new_player()
            return

        player = Player(
            name=player_data["name"],
            email=player_data["email"],
            age=player_data["age"],
            phone=player_data["phone"],
            date=player_data["date"],
            id=player_data["id"],
        )
        print_success(f"Welcome back, {player.name}!")
        self.current_player = player

    def _main_menu(self) -> None:
        """Display main menu and handle selection."""
        if not self.current_player:
            return

        while True:
            print_header(f"Main Menu - {self.current_player.name}")

            menu_options = ["Play Game", "View Leaderboard", "View Your Stats", "View Rules", "Change Player", "Exit"]
            choice = select_menu_option(menu_options)

            if choice == 0:  # Play Game
                self._play_game()
            elif choice == 1:  # View Leaderboard
                self._view_leaderboard()
            elif choice == 2:  # View Your Stats
                self._view_player_stats()
            elif choice == 3:  # View Rules
                self._view_rules()
            elif choice == 4:  # Change Player
                self.current_player = None
                return
            else:  # Exit
                self.current_player = None
                return

    def _play_game(self) -> None:
        """Run a game session."""
        if not self.current_player:
            return

        difficulty_name = select_difficulty()
        difficulty = DIFFICULTY_LEVELS[difficulty_name]

        print_header(f"Starting {difficulty.name} Game")
        print_info(f"Questions: {difficulty.num_questions}")
        print_info(f"Points per correct: {difficulty.score_per_correct}")
        print_info(f"Penalty per wrong: {difficulty.score_penalty}")
        print("\nPress Enter to start...")
        input()

        engine = GameEngine(self.current_player, difficulty)
        start_time = time.time()

        try:
            while not engine.is_game_finished():
                current, total = engine.get_progress()
                engine.prepare_round()  # Generate question for this round
                question_str = engine.get_current_question()  # Get the prepared question
                print_question(question_str, current + 1, total)

                try:
                    answer = get_true_false_answer()
                    is_correct = engine.play_round(str(answer))

                    if is_correct:
                        print_success("Correct!")
                    else:
                        print_error("Wrong!")

                    print_score(engine.get_score())

                except ValueError as e:
                    print_error(str(e))
                    continue

        except KeyboardInterrupt:
            if confirm_action("Quit game?"):
                print_warning("Game cancelled")
                return

        end_time = time.time()
        duration = end_time - start_time

        # Save game result
        max_score = engine.get_max_possible_score()
        final_score = engine.get_score()

        result = GameResult(
            player_id=self.current_player.id,
            difficulty=difficulty_name,
            score=final_score,
            max_score=max_score,
            duration=duration,
            created_at=datetime.now(),
        )
        
        # Insert result into database
        try:
            self.result_repo.insert_game_result(result)
        except Exception as e:
            print_warning(f"Failed to save game result: {e}")

        self._show_game_summary(result, duration)

    def _show_game_summary(self, result: GameResult, duration: float) -> None:
        """Display game summary."""
        print_header("Game Summary")

        accuracy = result.accuracy
        time_str = f"{int(duration // 60)}m {int(duration % 60)}s"

        print(f"Difficulty: {result.difficulty.capitalize()}")
        print(f"Score: {result.score}/{result.max_score}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Time: {time_str}")

        if accuracy == 100:
            print_success("Perfect score! Outstanding!")
        elif accuracy >= 80:
            print_success("Great job!")
        elif accuracy >= 60:
            print_info("Good effort!")
        else:
            print_warning("Keep practicing!")

    def _view_leaderboard(self) -> None:
        """Display the leaderboard."""
        print_header("Top 20 Players")

        try:
            leaderboard = self.result_repo.get_leaderboard(limit=20)
            if not leaderboard:
                print_info("No games played yet!")
            else:
                print_leaderboard(leaderboard)
        except Exception as e:
            print_error(f"Error loading leaderboard: {e}")

        input("Press Enter to continue...")

    def _view_player_stats(self) -> None:
        """Display player's personal statistics."""
        if not self.current_player:
            return

        print_header(f"Stats for {self.current_player.name}")

        try:
            history = self.result_repo.get_player_game_history(
                player_id=0, limit=10  # Will use real player ID when implemented
            )

            if not history:
                print_info("No games played yet!")
            else:
                print(f"Recent Games ({min(len(history), 10)}):\n")
                print(f"{'#':<4} {'Difficulty':<12} {'Score':<15} {'Accuracy':<12} {'Time':<10}")
                print("-" * 55)

                for i, game in enumerate(history, 1):
                    max_score = game["max_score"]
                    score = game["score"]
                    accuracy = (score / max_score * 100) if max_score > 0 else 0
                    time_str = f"{game['duration']:.1f}s"

                    print(
                        f"{i:<4} {game['difficulty']:<12} {score}/{max_score:<12} "
                        f"{accuracy:>5.1f}%       {time_str:<10}"
                    )

        except Exception as e:
            print_error(f"Error loading stats: {e}")

        input("\nPress Enter to continue...")

    def _view_rules(self) -> None:
        """Display game rules."""
        print_header("Game Rules")

        rules = """
1. You will be presented with math equations using <, =, or > operators
   Example: "45 < 67" (is 45 less than 67?)

2. For each equation, answer TRUE (T) or FALSE (F)

3. Scoring:
   - Correct answer: +5 points (Easy), +3 (Medium), +2 (Hard)
   - Wrong answer: -5 points (Easy), -2 (Medium)
   - Minimum score: 0 (never goes negative)

4. Complete all questions to finish the game

5. Different difficulty levels:
   - Easy: 5 questions, more forgiving scoring
   - Medium: 9 questions, moderate challenge
   - Hard: 15 questions, expert level

6. Your best scores are saved to the leaderboard

7. Good luck and have fun!
        """

        print(rules)
        input("Press Enter to continue...")

    def shutdown(self) -> None:
        """Shutdown the application gracefully."""
        close_connection(self.conn)


def main() -> None:
    """Entry point for the application."""
    app = GameApp()
    app.run()


if __name__ == "__main__":
    main()
