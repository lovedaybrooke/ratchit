from models import Option, Category, Poll
from ratings.models import Rating


def calculate_scores_for_single_option(poll, option):
    categories = Category.get_ordered_queryset(poll)
    score_list = []
    final_score = 0
    for category in categories:
        ratings = Rating.objects.filter(poll=poll).filter(
            option=option).filter(category=category)
        category_rating = 0
        for rating in ratings:
            category_rating += rating.rating
        score_list.append(category_rating)
        final_score += category_rating
    return [score_list, final_score]


def calculate_scores_for_all_options(event, poll):
    options = Option.objects.filter(poll=poll)
    return_dict = {"poll": poll, "event": event}
    if Rating.objects.filter(poll=poll):
        return_dict["raters"] = Rating.number_of_raters(poll)
        return_dict["categories"] = Category.objects.filter(poll=poll)
        return_dict["options"] = []
        for option in options:
            scores = calculate_scores_for_single_option(poll, option)
            return_dict["options"].append({"title": option.title,
                "scores": scores[0], "final_score": scores[1]})
    else:
        return_dict["no_ratings"] = True
    return return_dict
