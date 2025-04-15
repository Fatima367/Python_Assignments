def main():
    adjective = input("Enter an adjective: ")
    type_of_food = input("Enter any food: ")
    liquid = input("Enter any drink or liquid foods: ")
    plural_noun = input("Enter plural nouns: ")
    ingredient = input("Enter any food ingredient: ")
    currency = input("Enter any currency: ")
    verb = input("Enter any verb(2nd Form): ")
    something_really_weird = input("Enter something really weird: ")
    verb_with_ing = input("Enter any verb with 'ing': ")


    story = f"""
    "The Strange Sandwich"

    Today, I made the most {adjective} sandwich. First, I took two slices
    of {type_of_food} and spread them with {liquid}. Then I added some {plural_noun},
    a spoonful of {ingredient}, and topped it off with a {currency}.

    I took a bite and instantly {verb}. It tasted like {something_really_weird}!

    I’ll never eat that again... unless I’m {verb_with_ing} with aliens.
    """

    print(story)

if __name__ == "__main__":
    main()