from django.test import TestCase

from models import *


class ModelsTestCase(TestCase):
    fixtures = ['models.json']

    def test_unique_title_for_event(self):
        """ Test that new event cannot use the same title as existing """

        self.assertFalse(
            Event.unique_title("Monty Python at the Hollywood Bowl"),
            "Event with the same name as an existing event (and the same "
            "capitalisation) can be created")

        self.assertFalse(
            Event.unique_title("monty python at the hollywood bowl"),
            "Event with the same name as an existing event (but different "
            "capitalisation) can be created")

    def test_unique_title_for_polls_of_same_event(self):
        """ Test that new poll cannot use the same title as existing """

        event = Event.objects.get(pk=1)

        self.assertFalse(
            Poll.unique_title(event, "Drinks"),
            "Poll with the same name as existing poll (and the same "
            "capitalisation) can be created in one event")

        self.assertFalse(
            Poll.unique_title(event, "drinks"),
            "Poll with the same name as existing poll (but different "
            "capitalisation) can be created in one event")

    def test_unique_title_for_polls_of_different_events(self):
        """ Test that new poll cannot use the same title as existing """

        event = Event(title="Totally different event")

        self.assertTrue(Poll.unique_title(event, "Drinks"),
            "Poll with the same name as a poll from another event (and the "
            "same capitalisation) cannot be created in new event")

        self.assertTrue(Poll.unique_title(event, "drinks"),
            "Poll with the same name as a poll from another event (but "
            "different capitalisation) cannot be created in new event")

    def test_block_create_options(self):
        """ Test that new block_create for options function works """

        poll = Poll(title="Swimwear")
        poll.event = Event.objects.get(pk=1)
        poll.save()

        block = u"Speedos\r\nOne-piece\r\nBikini\r\n"

        Option.create_from_block(poll, block)

        speedos_option = Option.objects.filter(poll=poll).filter(
            title="Speedos")

        one_piece_option = Option.objects.filter(poll=poll).filter(
            title="One-piece")

        bikini_option = Option.objects.filter(poll=poll).filter(
            title="Bikini")

        number_of_options = len(Option.objects.filter(poll=poll))

        all_option_titles = ", ".join([option.title for option
            in Option.objects.filter(poll=poll)])

        self.assertTrue(speedos_option, "'Speedos' option was not created "
            "correctly by block create. The options created are: " +
            all_option_titles)

        self.assertTrue(one_piece_option, "'One-piece' option was not "
            "created correctly by block create. The options created are: " +
            all_option_titles)

        self.assertTrue(bikini_option, "'Bikini' option was not created "
            "correctly by block create. The options created are: " +
            all_option_titles)

        self.assertEqual(number_of_options, 3,
            "The block create function created the wrong number of options. "
            "There should be 3, but there are actually " +
            str(number_of_options))

    def test_unique_title_for_options_of_same_poll(self):
        """
        Test that new option for the a poll
        cannot use the same title as existing option for that poll
        """

        poll = Poll.objects.get(pk=1)

        self.assertFalse(Option.unique_title(poll, "Beer"),
            "Option with the same name as an existing option (and "
            "the same capitalisation) cannot be created in one poll")

        self.assertFalse(Option.unique_title(poll, "beer"),
            "Option with the same name as an existing option (but different "
            "capitalisation) cannot be created in one poll")

    def test_unique_title_for_options_of_different_polls(self):
        """
        Test that new option for a new poll
        can use the same title as existing option for another poll
        """
        event = Event.objects.get(pk=1)
        poll = Poll(event=event, title="Seat choices")

        self.assertTrue(Option.unique_title(poll, "Water"),
            "Option with the same name (and the same capitalisation) "
            "as an existing option from a different poll cannot be "
            "created in a new poll")

        self.assertTrue(Option.unique_title(poll, "water"),
            "Option with the same name (but different capitalisation) "
            "as an existing option from a different poll cannot be "
            "created in a new poll")

    def test_blocks_create_categories(self):
        """ 
        Test that blockS_create and block_create functions for
        categories works 
        """

        poll = Poll(title="Swimwear")
        poll.event = Event.objects.get(pk=1)
        poll.save()

        # block = u'Speedos\r\nOne-piece\r\nBikini'
        block_asc = u"Price\r\n"
        block_desc = "Comfort\r\nLook"

        Category.create_from_blocks(poll, block_desc, block_asc)

        comfort_category = Category.objects.filter(poll=poll).filter(
            title="Comfort")

        price_category = Category.objects.filter(poll=poll).filter(
            title="Price")

        look_category = Category.objects.filter(poll=poll).filter(
            title="Look")

        all_categories_titles = ', '.join([category.title for category
            in Category.objects.filter(poll=poll)])

        self.assertTrue(comfort_category, "'Comfort' category was not "
            "created correctly by block create. The categories created "
            "are: " + all_categories_titles)

        comfort_best_rating = comfort_category.get().best_possible_rating
        self.assertEqual(comfort_best_rating, 3,
            "'Comfort' category was not assigned the default "
            "best_possible_rating by block create. It should be 3 but is "
            "actually {rating}.".format(rating=comfort_best_rating))

        self.assertTrue(price_category, "'Price' category was not created "
            "correctly by block create. The categories created are: " +
            all_categories_titles)

        price_best_rating = price_category.get().best_possible_rating
        self.assertEqual(price_best_rating, 1,
            "'Price' category was not assigned the correct user-specified "
            "best_possible_rating by block create. It should be 1 but is "
            "actually {rating}.".format(rating=price_best_rating))

        self.assertTrue(look_category, "'Look' category was not created "
            "correctly by block create. The categories created are: " +
            all_categories_titles)
        look_best_rating = look_category.get().best_possible_rating
        self.assertEqual(look_best_rating, 3,
            "'Look' category was not assigned the correct user-specified "
            "best_possible_rating by block create. It should be 3 but is "
            "actually {rating}.".format(rating=look_best_rating))

    def test_unique_title_for_categories_of_same_poll(self):
        """
        Test that new category for a poll
        cannot use the same title as existing category for that poll
        """

        poll = Poll.objects.get(pk=1)

        self.assertFalse(Category.unique_title(poll, "Flavour"),
            "Category with the same name as an existing category (and "
            "the same capitalisation) cannot be created in one poll")

        self.assertFalse(Category.unique_title(poll, "flavour"),
            "Category with the same name as an existing category (but "
            "different capitalisation) cannot be created in one poll")

    def test_unique_title_for_categories_of_different_polls(self):
        """
        Test that new category for a new poll
        can use the same title as existing category for another poll
        """
        event = Event.objects.get(pk=1)
        poll = Poll(event=event, title="Seat choices")

        self.assertTrue(Category.unique_title(poll, "Flavour"),
            "Category with the same name (and the same capitalisation) "
            "as an existing category from a different poll cannot be "
            "created in a new poll")

        self.assertTrue(Category.unique_title(poll, "flavour"),
            "Category with the same name (but different capitalisation) "
            "as an existing category from a different poll cannot be "
            "created in a new poll")
