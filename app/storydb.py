# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00: CircleStories

"""Story Database Handler

Handles everything related to story/block database management.
"""

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
    block_text          TEXT
);
"""


class StoryDB:
    """An instance of this class would be used to interface with the database.
    Only one should be created per app instance."""

    class Story:
        """This is a DAO (Data Access Object, i.e. a representation of data in the database).
        You can get these through `StoryDB.get_story(story_id)`"""

        def __init__(self, db_obj, keys, values):
            self.db_obj = db_obj
            self.keys = keys
            self.values = list(values)
            # Allow for access of columns through dot syntax:
            for k, v in zip(keys, values):
                setattr(self, k, v)

        def update_with(self, cur, values):
            """Used as update_cur.row_factory."""
            for k, v in zip(cur.description, values):
                k = k[0]
                setattr(self, k, v)
                self.values[self.keys.index(k)] = v

        @staticmethod
        def init_wrapper(db_obj):
            """Returns a function that creates a Story from a cursor and tuple of keys,
            but with `db_obj` already set to the given object. Used for story_cur.row_factory."""

            def factory(cur, values):
                return StoryDB.Story(
                    db_obj, tuple(t[0] for t in cur.description), values
                )

            return factory

        def full_text(self):
            """Retrieves the concatenated text of all blocks with this story_id, in order."""
            self.db_obj.block_cur.execute(
                "SELECT block_text FROM blocks WHERE story_id=? ORDER BY position",
                (self.story_id,),
            )
            return "\n\n".join(t[0] for t in self.db_obj.block_cur.fetchall())

        def add_block(self, author_id, block_text):
            self.db_obj.block_cur.execute(
                "INSERT INTO blocks(story_id, author_id, position, block_text) VALUES (?, ?, ?, ?)",
                (self.story_id, author_id, self.num_blocks, block_text),
            )
            self.num_blocks += 1
            self.db_obj.cur.execute(
                "SELECT block_id FROM blocks WHERE rowid=last_insert_rowid() LIMIT 1"
            )
            self.last_block_id = self.db_obj.cur.fetchone()[0]
            self.db_obj.update_cur.execute(
                "UPDATE stories SET num_blocks=?, last_block_id=? WHERE story_id=?",
                (self.num_blocks, self.last_block_id, self.story_id),
            )
            # self.update()

        def update(self):
            """Requests data from the database to update"""
            self.db_obj.update_cur.row_factory = self.update_with
            self.db_obj.update_cur.execute(
                "SELECT * FROM stories WHERE story_id=? LIMIT 1", (self.story_id,)
            )
            self.db_obj.update_cur.fetchone()

        def __repr__(self):
            return "Story(" + "|".join(map(repr, self.values)) + ")"

    def __init__(self, db_file):
        """Connects to the database and sets it up if necessary."""
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        self.block_cur = self.con.cursor()
        self.story_cur = self.con.cursor()
        self.update_cur = self.con.cursor()
        self.story_cur.row_factory = StoryDB.Story.init_wrapper(self)
        # self.cur.row_factory = sqlite3.Row
        self.setup()

    def setup(self):
        """Runs database setup commands (creating tables).
        Should not fail if the database was already set up."""
        self.story_cur.executescript(SETUP_COMMANDS)

    def add_story(self, creator_id, title):
        """Adds a story to the database and returns its story_id."""
        self.story_cur.execute(
            "INSERT INTO stories(creator_id, title) VALUES (?, ?)", (creator_id, title)
        )
        self.cur.execute(
            "SELECT story_id FROM stories WHERE rowid=last_insert_rowid() LIMIT 1"
        )
        return self.cur.fetchone()[0]

    def get_story(self, story_id):
        """Returns a Story DAO (Data access object) that
        represents a particular row of the stories table."""
        self.story_cur.execute(
            "SELECT * FROM stories WHERE story_id=? LIMIT 1", (story_id,)
        )
        return self.story_cur.fetchone()

    def close(self):
        """Commits to the database and closes the cursor properly."""
        print("StoryDB object closing...")
        self.con.commit()
        self.con.close()

    def __del__(self):
        """Ensures that the database is properly closed when
        this object is removed by the garbage collector."""
        self.close()
        print("StoryDB object deleted")


# FOR TESTING PURPOSES (not part of the actual app)
if __name__ == "__main__":
    print("Testing StoryDB functionality")
    db = StoryDB(":memory:")

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

    print()
    print(storyDAO)
    print(storyDAO.full_text())
    print()
    
    # print(db.get)