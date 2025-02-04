from .config import tape, TweepyTestCase, username
from tweepy import Cursor


class TweepyCursorTests(TweepyTestCase):
    @tape.use_cassette('testidcursoritems.json')
    def testidcursoritems(self):
        items = list(Cursor(self.api.user_timeline).items(2))
        self.assertEqual(len(items), 2)

    @tape.use_cassette('testidcursorpages.json')
    def testidcursorpages(self):
        pages = list(Cursor(self.api.user_timeline, count=1).pages(2))
        self.assertEqual(len(pages), 2)

    @tape.use_cassette('testcursorcursoritems.yaml', serializer='yaml')
    def testcursorcursoritems(self):
        items = list(Cursor(self.api.friends_ids).items(2))
        self.assertEqual(len(items), 2)

        items = list(Cursor(self.api.followers_ids, screen_name=username).items(1))
        self.assertEqual(len(items), 1)

    @tape.use_cassette('testcursorcursorpages.yaml', serializer='yaml')
    def testcursorcursorpages(self):
        pages = list(Cursor(self.api.friends_ids).pages(1))
        self.assertTrue(len(pages) == 1)

        pages = list(Cursor(self.api.followers_ids, screen_name=username).pages(1))
        self.assertTrue(len(pages) == 1)

    @tape.use_cassette('testcursorsetstartcursor.json')
    def testcursorsetstartcursor(self):
        c = Cursor(self.api.friends_ids, cursor=123456)
        self.assertEqual(c.iterator.next_cursor, 123456)
        self.assertFalse('cursor' in c.iterator.kwargs)

    @tape.use_cassette('testcursornext.yaml', serializer='yaml')
    def testcursornext(self):
        """
        Test next(cursor) behavior, screen name being passed correctly.
        Regression test for issue #518
        """
        cursor = Cursor(self.api.user_timeline, screen_name='Twitter').items(5)
        status = next(cursor)

        self.assertEqual(status.user.screen_name, 'Twitter')
