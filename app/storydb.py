# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00: CircleStories

"""Story Database Handler

Handles everything related to story/block database management.
"""

from contextlib import contextmanager
import sqlite3

SETUP_COMMANDS = """
CREATE TABLE IF NOT EXISTS stories (
    story_id            TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    creation_timestamp  DATE DEFAULT CURRENT_TIMESTAMP,
    creator_id          INTEGER,
    num_blocks          INTEGER DEFAULT 0,
    last_block_id       INTEGER,
    title               TEXT
);

CREATE TABLE IF NOT EXISTS blocks (
    block_id            TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    creation_timestamp  DATE DEFAULT CURRENT_TIMESTAMP,
    story_id            INTEGER,
    author_id           INTEGER,
    position            INTEGER,
    block_text          TEXT,
    block_img           TEXT
);
"""


class StoryDB:
    """An instance of this class would be used to interface with the database.
    Only one should be created per app instance."""

    class Story:
        """This is a DAO (Data Access Object, i.e. a representation of data in
        the database). You can get these through `StoryDB.get_story(story_id)`"""

        def __init__(self, db_obj, keys, values):
            self.db_obj = db_obj
            self.keys = keys
            self.values = list(values)
            # Allow for access of columns through dot syntax:
            for k, v in zip(keys, values):
                setattr(self, k, v)

        def update_with(self, cur, values):
            """Used as cur.row_factory."""

            for k, v in zip(cur.description, values):
                k = k[0]
                setattr(self, k, v)
                self.values[self.keys.index(k)] = v

        @staticmethod
        def init_wrapper(db_obj):
            """Returns a function that creates a Story from a cursor and tuple
            of keys, but with `db_obj` already set to the given object. Used
            for cur.row_factory."""

            def factory(cur, values):
                return StoryDB.Story(
                    db_obj, tuple(t[0] for t in cur.description), values
                )

            return factory

        def get_blocks(self):
            """Retrieves the concatenated text of all blocks with this
            story_id, in order."""

            with self.db_obj.connect() as cur:
                cur.execute(
                    "SELECT block_text FROM blocks WHERE story_id=? ORDER BY position",
                    (self.story_id,),
                )
                return [block[0] for block in cur.fetchall()]
        
        def get_blocks_images(self):
            """Retrieves the concatenated images of all blocks with this
            story_id, in order."""

            with self.db_obj.connect() as cur:
                cur.execute(
                    "SELECT block_img FROM blocks WHERE story_id=? ORDER BY position",
                    (self.story_id,),
                )
                return [block[0] for block in cur.fetchall()]

        def add_block(self, author_id, block_text, block_img):
            """Adds a new block to this Story with the provided author_id and
            block_text."""
            with self.db_obj.connect() as cur:
                cur.execute(
                    """INSERT INTO blocks(story_id, author_id, position, block_text, block_img)
                    VALUES (?, ?, ?, ?, ?)""",
                    (self.story_id, author_id, self.num_blocks, block_text, block_img),
                )
                self.num_blocks += 1
                cur.execute(
                    "SELECT block_id FROM blocks WHERE rowid=last_insert_rowid() LIMIT 1"
                )
                # last_block_id will be added with setattr
                self.last_block_id = cur.fetchone()[0]  # pylint: disable=W0201
                cur.execute(
                    "UPDATE stories SET num_blocks=?, last_block_id=? WHERE story_id=?",
                    (self.num_blocks, self.last_block_id, self.story_id),
                )
                # self.update()

        def last_block(self):
            """Returns the text of the last block"""
            with self.db_obj.connect() as cur:
                cur.execute(
                    "SELECT block_text FROM blocks WHERE story_id=? AND position=? LIMIT 1",
                    (self.story_id, self.num_blocks - 1),
                )
                return cur.fetchone()[0]
        
        def last_block_image(self):
            """Returns the image of the last block"""
            with self.db_obj.connect() as cur:
                cur.execute(
                    "SELECT block_img FROM blocks WHERE story_id=? AND position=? LIMIT 1",
                    (self.story_id, self.num_blocks - 1),
                )
                return cur.fetchone()[0]

        def update(self):
            """Requests data from the database to update this object"""
            with self.db_obj.connect() as cur:
                cur.row_factory = self.update_with
                cur.execute(
                    "SELECT * FROM stories WHERE story_id=? LIMIT 1", (self.story_id,)
                ).fetchone()

        def __repr__(self):
            return "Story(" + "|".join(map(repr, self.values)) + ")"

    def __init__(self, db_file):
        """Connects to the database and sets it up if necessary."""
        self.db_file = db_file
        self.story_factory = StoryDB.Story.init_wrapper(self)
        # self.cur = self.con.cursor()
        # self.block_cur = self.con.cursor()
        # self.story_cur = self.con.cursor()
        # self.update_cur = self.con.cursor()
        # self.story_cur.row_factory = self.story_factory
        self.setup()

    @contextmanager
    def connect(self):
        """Context manager for a connection & cursor simultaneously"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            yield cur

    def setup(self):
        """Runs database setup commands (creating tables).
        Should not fail if the database was already set up."""
        with self.connect() as cur:
            cur.executescript(SETUP_COMMANDS)

    def add_story(self, creator_id, title):
        """Adds a story to the database and returns its story_id."""
        with self.connect() as cur:
            cur.execute(
                "INSERT INTO stories(creator_id, title) VALUES (?, ?)",
                (creator_id, title),
            )
            cur.execute(
                "SELECT story_id FROM stories WHERE rowid=last_insert_rowid() LIMIT 1"
            )
            return cur.fetchone()[0]

    def get_story(self, story_id):
        """Returns a Story DAO (Data access object) that
        represents a particular row of the stories table."""
        with self.connect() as cur:
            cur.row_factory = self.story_factory
            cur.execute("SELECT * FROM stories WHERE story_id=? LIMIT 1", (story_id,))
            return cur.fetchone()

    def is_contributor(self, user_id, story_id):
        """Returns whether this user contributed to this story.
        The creator counts as a contributor."""
        with self.connect() as cur:
            cur.execute(
                "SELECT TRUE FROM blocks WHERE author_id=? AND story_id=? LIMIT 1",
                (user_id, story_id),
            )
            return bool(cur.fetchone())

    def is_creator(self, user_id, story_id):
        """Returns whether this user contributed to this story."""
        with self.connect() as cur:
            cur.execute(
                "SELECT TRUE FROM stories WHERE creator_id=? AND story_id=? LIMIT 1",
                (user_id, story_id),
            )
            return bool(cur.fetchone())

    def get_created_stories(self, user_id):
        """Returns list of story ids created by this user."""
        with self.connect() as cur:
            cur.execute(
                "SELECT story_id FROM stories WHERE user_id=? ORDER BY creation_timestamp",
                (user_id,),
            )
            return [s[0] for s in cur.fetchall()]

    def get_contributed_stories(self, user_id):
        """Returns list of story ids contributed to by this user.
        The stories created by this user are included."""
        with self.connect() as cur:
            cur.execute(
                """SELECT DISTINCT story_id FROM blocks WHERE author_id=?
                ORDER BY creation_timestamp""",
                (user_id,),
            )
            return [s[0] for s in cur.fetchall()]

    def get_not_contributed_stories(self, user_id):
        """Returns list of story ids not contributed to by this user."""
        with self.connect() as cur:
            cur.execute(
                "SELECT DISTINCT story_id FROM blocks ORDER BY creation_timestamp"
            )
            return [
                s[0] for s in cur.fetchall() if not self.is_contributor(user_id, s[0])
            ]


# FOR TESTING PURPOSES (not part of the actual app)
if __name__ == "__main__":
    print("Testing StoryDB functionality")
    db = StoryDB("TEMP_DB.db")

    insertedStory = db.add_story(26_21_19_21_06, "How I was Two Periods Late to School")
    print(insertedStory)
    storyDAO = db.get_story(insertedStory)
    print(type(storyDAO))

    print(storyDAO)
    print(storyDAO.full_text())

    storyDAO.add_block(
        26_21_19_21_06,
        """I woke up about 30 minutes late (~6:30 AM), as usual for that week.
Then I took a long time to get ready for school, so I left ~40 minutes late.
I stood on the crowded S79, which is usually a 30 minute ride.
This time it was about an hour long, due to heavy traffic and a different route.
By the time I arrived at school, there was only 10 minutes left in 2nd period.""",
    )
    storyDAO.update()
    print()
    print(storyDAO)
    print(storyDAO.full_text())
    print()

    storyDAO.add_block(
        26_21_19_21_06,
        """I didn't think to go to my 2nd period class, Weighttraining, since I
wouldn't be able to change. But I realized later that I should have gone to
tell him what had happened. Instead I stayed near the 2nd floor atrium and
chatted with a friend until 3rd period. We got cool new dry-erase whiteboard
desks in that class. This story is going off topic. But they are pretty cool
desks.""",
    )
    storyDAO.update()

    print()
    print(storyDAO)
    print(storyDAO.full_text())
    print()

    print(storyDAO.last_block())

    print(db.get_story("not a real id"))

    import os

    os.remove("TEMP_DB.db")
