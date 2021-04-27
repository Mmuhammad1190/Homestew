"""Parameters for headers in search queries for recipes"""


CUISINES = [(None, '-- Choose a cuisine --'), ("african", 'African'),
            ("american", 'American'), ("british", 'British'),
            ("cajun", 'Cajun'),
            ("caribbean", 'Caribbean'), ("chinese", 'Chinese'),
            ("eastern european", 'Eastern European'),
            ("european", 'European'), ("french", 'French'),
            ("german", 'German'),
            ("greek", 'Greek'), ("indian", 'Indian'), ("irish", 'Irish'),
            ("italian", 'Italian'), ("japanese", 'Japanese'),
            ("jewish", 'Jewish'),
            ("korean", 'Korean'), ("latin american", 'Latin American'),
            ("mediterranean", 'Mediterranean'),
            ("mexican", 'Mexican'), ("middle eastern", 'Middle Eastern'),
            ("nordic", 'Nordic'), ("southern", 'Southern'),
            ("spanish", 'Spanish'), ("thai", 'Thai')]

EXCLUDED_CUISINES = [(None, '-- Exclude a cuisine --'), ("african", 'African'),
                     ("american", 'American'), ("british", 'British'),
                     ("cajun", 'Cajun'),
                     ("caribbean", 'Caribbean'), ("chinese", 'Chinese'),
                     ("eastern european", 'Eastern European'),
                     ("european", 'European'), ("french", 'French'),
                     ("german", 'German'),
                     ("greek", 'Greek'), ("indian", 'Indian'), ("irish", 'Irish'),
                     ("italian", 'Italian'), ("japanese", 'Japanese'),
                     ("jewish", 'Jewish'),
                     ("korean", 'Korean'), ("latin american", 'Latin American'),
                     ("mediterranean", 'Mediterranean'),
                     ("mexican", 'Mexican'), ("middle eastern", 'Middle Eastern'),
                     ("nordic", 'Nordic'), ("southern", 'Southern'),
                     ("spanish", 'Spanish'), ("thai", 'Thai')]

DIETS = [(None, '-- Choose a diet --'), ("gluten free", 'Gluten Free'),
         ("ketogenic", 'Ketogenic'),
         ("vegetarian", 'Vegetarian'),
         ("lacto-vegetarian", 'Lacto-Vegetarian'),
         ("ovo-vegetarian", 'Ovo-Vegetarian'), ("vegan", 'Vegan'),
         ("pescetarian", 'Pescetarian'), ("paleo", 'Paleo'),
         ("primal", 'Primal'), ("whole30", 'Whole30')]

INTOLERANCES = [(None, '-- Any allergies? --'), ("dairy", 'Dairy'), ("egg", 'Egg'), ("gluten", 'Gluten'),
                ("grain", 'Grain'), ("peanut", 'Peanut'), ("seafood", 'Seafood'),
                ("sesame", 'Sesame'), ("shellfish", 'Shellfish'), ("soy", 'Soy'),
                ("sulfite", 'Sulfite'), ("tree nut", 'Tree Nut'),
                ("wheat", 'Wheat')]

TYPES = [(None, '-- Choose a meal type --'), ("main course", 'main course'), ("side dish", 'side dish'),
         ("dessert", 'dessert'), ("appetizer", 'appetizer'),
         ("salad", 'salad'), ("bread", 'bread'),
         ("breakfast", 'breakfast'), ("soup", 'soup'),
         ("beverage", 'beverage'), ("sauce", 'sauce'),
         ("marinade", 'marinade'), ("fingerfood", 'fingerfood'),
         ("snack", 'snack'), ("drink", 'drink')]

SORT = [(None, '-- Sort by --'), ("popularity", 'popularity'), ("healthiness", 'healthiness'),
        ("time", 'time'), ("calories", 'calories'), ("random", 'random')]
