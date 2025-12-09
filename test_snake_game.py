import pytest
import snake_game

# Define constants for testing, assuming they match or are derived from snake_game.py's internal constants
# These are typical values for a simple snake game grid.
TEST_SCREEN_WIDTH = 600
TEST_SCREEN_HEIGHT = 400
TEST_TILE_SIZE = 20
TEST_GRID_WIDTH = TEST_SCREEN_WIDTH // TEST_TILE_SIZE  # 30
TEST_GRID_HEIGHT = TEST_SCREEN_HEIGHT // TEST_TILE_SIZE # 20

# Directions as tuples (dx, dy)
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

# --- Pytest Fixtures ---
@pytest.fixture
def initial_snake():
    """Provides a default initial snake segment list for tests."""
    # Head at (5, 5), body segments at (4, 5) and (3, 5), typically moving right.
    return [(5, 5), (4, 5), (3, 5)]

# --- Test Snake Movement (move_snake) ---
def test_move_snake_right(initial_snake):
    """Tests if the snake moves one step to the right and its tail is removed."""
    snake_copy = list(initial_snake) # Work on a copy of the fixture
    # The `move_snake` function is assumed to modify the snake list in-place.
    snake_game.move_snake(snake_copy, RIGHT)
    # New head is (6, 5), old head (5, 5) becomes second segment, old tail (3, 5) is removed.
    assert snake_copy == [(6, 5), (5, 5), (4, 5)]

def test_move_snake_up(initial_snake):
    """Tests if the snake moves one step up and its tail is removed."""
    snake_copy = list(initial_snake)
    snake_game.move_snake(snake_copy, UP)
    # Head (5, 5) moves to (5, 4). Tail (3, 5) removed.
    assert snake_copy == [(5, 4), (5, 5), (4, 5)]

def test_move_snake_single_segment():
    """Tests movement for a single-segment snake."""
    snake_copy = [(10, 10)]
    snake_game.move_snake(snake_copy, LEFT)
    assert snake_copy == [(9, 10)] # Head moves, tail is removed (which is itself)

# --- Test Collision Detection (check_collision_with_walls, check_collision_with_self) ---
def test_collision_with_right_wall():
    """Tests collision when the head is at or beyond the right wall boundary."""
    head = (TEST_GRID_WIDTH, 10) # X-coordinate is outside (0 to GRID_WIDTH-1)
    assert snake_game.check_collision_with_walls(head, TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT, TEST_TILE_SIZE) is True

def test_collision_with_left_wall():
    """Tests collision when the head is at or beyond the left wall boundary."""
    head = (-1, 10)
    assert snake_game.check_collision_with_walls(head, TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT, TEST_TILE_SIZE) is True

def test_collision_with_top_wall():
    """Tests collision when the head is at or beyond the top wall boundary."""
    head = (10, -1)
    assert snake_game.check_collision_with_walls(head, TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT, TEST_TILE_SIZE) is True

def test_collision_with_bottom_wall():
    """Tests collision when the head is at or beyond the bottom wall boundary."""
    head = (10, TEST_GRID_HEIGHT) # Y-coordinate is outside (0 to GRID_HEIGHT-1)
    assert snake_game.check_collision_with_walls(head, TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT, TEST_TILE_SIZE) is True

def test_no_collision_with_walls():
    """Tests no collision when the head is safely within the game boundaries."""
    head = (TEST_GRID_WIDTH // 2, TEST_GRID_HEIGHT // 2) # Center of the grid
    assert snake_game.check_collision_with_walls(head, TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT, TEST_TILE_SIZE) is False

def test_collision_with_self():
    """Tests collision when the snake's head occupies the same cell as a body segment."""
    # Example of a snake whose head has collided with its own body.
    colliding_snake_example = [(5, 5), (6, 5), (6, 6), (5, 6), (5,5)] # Head (5,5) crashes into last segment (5,5)
    assert snake_game.check_collision_with_self(colliding_snake_example) is True

def test_no_collision_with_self(initial_snake):
    """Tests no self-collision for a normally moving snake."""
    assert snake_game.check_collision_with_self(initial_snake) is False

def test_no_collision_with_self_short_snake():
    """Tests no self-collision for a very short snake (which cannot self-collide)."""
    assert snake_game.check_collision_with_self([(5, 5)]) is False # Single segment
    assert snake_game.check_collision_with_self([(5, 5), (4, 5)]) is False # Two segments

# --- Test Food Generation (generate_food) ---
def test_generate_food_not_on_snake(initial_snake):
    """Tests that generated food is not on any snake segment and is within bounds."""
    # `generate_food` is assumed to retry until a valid spot is found.
    # We test multiple calls to ensure robustness.
    for _ in range(5):
        food_pos = snake_game.generate_food(initial_snake, TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT, TEST_TILE_SIZE)
        assert food_pos not in initial_snake
        assert 0 <= food_pos[0] < TEST_GRID_WIDTH
        assert 0 <= food_pos[1] < TEST_GRID_HEIGHT

# --- Test Eating Food and Growing Snake (check_food_eaten, grow_snake) ---
def test_check_food_eaten_true():
    """Tests when the snake's head is on the food position."""
    snake_head = (10, 10)
    food_position = (10, 10)
    assert snake_game.check_food_eaten(snake_head, food_position) is True

def test_check_food_eaten_false():
    """Tests when the snake's head is not on the food position."""
    snake_head = (10, 10)
    food_position = (11, 10) # Food is one tile away
    assert snake_game.check_food_eaten(snake_head, food_position) is False

def test_grow_snake(initial_snake):
    """Tests that the snake grows by adding a new head without removing the tail."""
    snake_copy = list(initial_snake) # [(5, 5), (4, 5), (3, 5)]
    new_head_after_eating = (6, 5) # Simulate the new head after moving to food
    snake_game.grow_snake(snake_copy, new_head_after_eating)
    # The new head is added, and no tail segment is removed.
    assert snake_copy == [(6, 5), (5, 5), (4, 5), (3, 5)]
    assert len(snake_copy) == len(initial_snake) + 1

# --- Test Direction Change Logic (change_direction) ---
def test_change_direction_valid():
    """Tests valid changes in snake direction (e.g., Right to Down)."""
    assert snake_game.change_direction(RIGHT, DOWN) == DOWN
    assert snake_game.change_direction(UP, RIGHT) == RIGHT
    assert snake_game.change_direction(LEFT, UP) == UP
    assert snake_game.change_direction(DOWN, LEFT) == LEFT

def test_change_direction_invalid_opposite():
    """Tests invalid changes in snake direction (180-degree turns)."""
    assert snake_game.change_direction(RIGHT, LEFT) == RIGHT # Cannot turn 180 degrees
    assert snake_game.change_direction(LEFT, RIGHT) == LEFT
    assert snake_game.change_direction(UP, DOWN) == UP
    assert snake_game.change_direction(DOWN, UP) == DOWN

def test_change_direction_same():
    """Tests changing direction to the current direction (should result in no change)."""
    assert snake_game.change_direction(RIGHT, RIGHT) == RIGHT
    assert snake_game.change_direction(UP, UP) == UP
