MOVIE_DETAILS = {
    "Home Alone": {
        "genre": "Comedy, Family",
        "synopsis": "An eight-year-old troublemaker must protect his house from a pair of burglars when he is accidentally left home alone by his family during Christmas vacation.",
        "rating": "7.7/10",
    },
    "Back to the future": {
        "genre": "Science Fiction, Adventure",
        "synopsis": "Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the eccentric scientist Doc Brown.",
        "rating": "8.5/10",
    },
    "insidious": {
        "genre": "Horror",
        "synopsis": "Fifteen years after murdering his sister on Halloween night 1963, Michael Myers escapes from a mental hospital and returns to the small town of Haddonfield, Illinois to kill again.",
        "rating": "7.7/10",
    },
    "Coda": {
        "genre": "Drama, Musical",
        "synopsis": "As a CODA (Child of Deaf Adults), Ruby is the only hearing person in her deaf family. When the family's fishing business is threatened, Ruby finds herself torn between pursuing her passion at Berklee College of Music and her fear of abandoning her parents.",
        "rating": "8.0/10",
    },
    "The Greatest Showman": {
        "genre": "Drama, Musical",
        "synopsis": "Celebrates the birth of show business and tells of a visionary who rose from nothing to create a spectacle that became a worldwide sensation.",
        "rating": "7.5/10",
    },
    "Tetris": {
        "genre": "Drama, Biography",
        "synopsis": "The story of how one of the world's most popular video games found its way to players around the globe. Businessman Henk Rogers and Tetris inventor Alexey Pajitnov join forces in the USSR, risking it all to bring Tetris to the masses.",
        "rating": "7.4/10",
    },
    "500 Days of Summer": {
        "genre": "Romance, Drama",  # Removed "Horror" as it seems incorrect for this movie
        "synopsis": "An offbeat romantic comedy about a woman who doesn't believe true love exists, and the young man who falls for her.",
        "rating": "7.7/10",
    },
    "My Neighbour Totoro": {
        "genre": "Animation, Fantasy",
        "synopsis": "When two girls move to the country to be near their ailing mother, they have adventures with the wondrous forest spirits who live nearby.",
        "rating": "8.1/10",
    },
    "Koe no Katachi": {
        "genre": "Animation, Drama",
        "synopsis": "A young man is ostracized by his classmates after he bullies a deaf girl to the point where she moves away. Years later, he sets off on a path for redemption.",
        "rating": "8.2/10",
    },
    "Forrest Gump": {
        "genre": "Drama, Romance",
        "synopsis": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.",
        "rating": "8.8/10",
    },
    "Weathering with You": {
        "genre": "Animation, Fantasy",
        "synopsis": "A high school boy who has run away to Tokyo befriends a girl who appears to be able to manipulate the weather.",
        "rating": "7.5/10",
    },
    "spiderman": {
        "genre": "Action, Adventure",
        "synopsis": "After being bitten by a genetically-modified spider, a shy teenager gains spider-like abilities that he uses to fight injustice as a masked superhero and face a vengeful enemy.",
        "rating": "7.3/10",
    },
    "josee": {
        "genre": "Animation, Romance",
        "synopsis": "A youth romantic drama between a young man who has a fateful encounter with Josee, a girl who has difficulty walking and rarely goes out, spending most of her time reading.",
        "rating": "7.5/10",
    },
    "suzume": {
        "genre": "Animation, Fantasy",
        "synopsis": "A modern action adventure road story where a 17-year-old girl named Suzume helps a mysterious young man close doors from the other side that are releasing disasters all over Japan.",
        "rating": "7.7/10",
    },
    "maquia": {
        "genre": "Animation, Fantasy",
        "synopsis": "An immortal girl and a normal boy meet and become friends, sharing a bond that lasts throughout the years.",
        "rating": "7.4/10",
    },
    "clouds": {
        "genre": "Drama, Romance",
        "synopsis": "A teenager is diagnosed with a rare form of bone cancer and finds a way to inspire others with the little time he has left.",
        "rating": "7.1/10",
    },
}


def get_movie_details(title):
    """Returns genre, synopsis, and rating for a given movie title."""
    return MOVIE_DETAILS.get(
        title, {"genre": "N/A", "synopsis": "Synopsis not available.", "rating": "N/A"}
    )
