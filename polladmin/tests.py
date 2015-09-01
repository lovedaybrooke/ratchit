from django.test import TestCase

from models import *


class ModelsTestCase(TestCase):
    fixtures = ['models.json']

    def test_unique_title_for_polls_of_same_event(self):
        """ Test that new event cannot use the same title as existing """

        event = Event.objects.get(pk=1)

        self.assertFalse(
            Poll.unique_title(event, "Drinks"),
            "Poll with the same name as existing can be created in one event")

    def test_unique_title_for_polls_of_different_events(self):
        """ Test that new event cannot use the same title as existing """

        event = Event(title="Totally different event")

        self.assertTrue(Poll.unique_title(event, "Drinks"),
            "Poll with the same name as other cannot be created in new event")

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

        self.assertFalse(
            Option.unique_title(poll, "Beer"), "Option with the same name "
            "as existing can be created in one poll")

    def test_unique_title_for_options_of_different_polls(self):
        """
        Test that new option for a new poll
        can use the same title as existing option for another poll
        """
        event = Event.objects.get(pk=1)
        poll = Poll(event=event, title="Seat choices")

        self.assertTrue(
            Option.unique_title(poll, "Water"), "Option with the same name "
            "as existing cannot be created in new poll")

    def test_block_create_categories(self):
        """ Test that new block_create function for categories works """

        poll = Poll(title="Swimwear")
        poll.event = Event.objects.get(pk=1)
        poll.save()

        # block = u'Speedos\r\nOne-piece\r\nBikini'
        block = u"Comfort\r\nPrice,1\r\nLook ,3 \r\n"

        Category.create_from_block(poll, block)

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

        self.assertFalse(
            Category.unique_title(poll, "Flavour"), "Category with the same "
            "name as existing can be created in one poll")

    def test_unique_title_for_categories_of_different_polls(self):
        """
        Test that new category for a new poll
        can use the same title as existing category for another poll
        """
        event = Event.objects.get(pk=1)
        poll = Poll(event=event, title="Seat choices")

        self.assertTrue(
            Category.unique_title(poll, "Flavour"), "Category with the same "
            "name as existing cannot be created in new poll")
